#!/usr/bin/env node
/**
 * enrich-skills.js
 *
 * Uses @github/copilot-sdk to AI-enrich skill metadata in
 * site/src/data/skills.json.  Adds / improves:
 *   - shortDescription  (one tight sentence)
 *   - tags              (up to 5 relevant keywords)
 *   - complexity        (beginner | intermediate | advanced)
 *   - platforms         (windows | macos | linux subset)
 *
 * The script is incremental: skills already enriched (enrichedAt field is
 * set) are skipped unless --force is passed.
 *
 * Usage:
 *   node scripts/enrich-skills.js [--force] [--limit N] [--dry-run]
 *
 * Environment variables:
 *   GITHUB_TOKEN  Required – used for Copilot SDK authentication.
 *
 * The script exits gracefully (exit 0) when the Copilot CLI is unavailable,
 * so it can be used in environments where it is not installed without
 * breaking the CI pipeline.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { parseArgs } from 'util';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

// ── CLI args ──────────────────────────────────────────────────────────────────
const { values: args } = parseArgs({
  options: {
    force: { type: 'boolean', default: false },
    limit: { type: 'string', default: '0' },
    'dry-run': { type: 'boolean', default: false },
  },
  strict: false,
});

const LIMIT = parseInt(args.limit, 10) || 0;
const DRY_RUN = args['dry-run'];
const FORCE = args.force;

// ── Helpers ───────────────────────────────────────────────────────────────────
function truncate(str, max = 300) {
  return str && str.length > max ? str.slice(0, max) + '…' : str;
}

/**
 * Build a prompt asking Copilot to return structured JSON enrichment for a
 * skill entry.
 */
function buildPrompt(skill) {
  const content = truncate(skill.skillMdContent || skill.description || '', 800);
  return `You are enriching a metadata record for a GitHub Copilot skill.

Skill name: ${skill.name}
Current description: ${skill.description}
Category: ${skill.category}
Author: ${skill.author}

Skill content (first 800 chars):
${content}

Return ONLY a JSON object with these fields – no prose, no markdown fences:
{
  "shortDescription": "<one concise sentence, max 120 chars>",
  "tags": ["<tag1>", "<tag2>", "<tag3>"],
  "complexity": "<beginner|intermediate|advanced>",
  "platforms": ["<windows|macos|linux> (include all that apply)"]
}`;
}

/**
 * Parse the JSON that Copilot returns.  Copilot sometimes wraps the JSON in
 * a markdown code fence; strip that before parsing.
 */
function parseEnrichmentResponse(text) {
  const cleaned = text.replace(/```json\s*/g, '').replace(/```\s*/g, '').trim();
  const start = cleaned.indexOf('{');
  const end = cleaned.lastIndexOf('}');
  if (start === -1 || end === -1) throw new Error('No JSON object found in response');
  return JSON.parse(cleaned.slice(start, end + 1));
}

// ── Copilot SDK integration ───────────────────────────────────────────────────
async function enrichWithCopilot(skill, client) {
  const prompt = buildPrompt(skill);
  const session = await client.createSession({ model: 'gpt-4o' });

  let fullText = '';
  const done = new Promise((resolve, reject) => {
    session.on('assistant.message', event => {
      fullText += event.data.content ?? '';
    });
    session.on('session.idle', resolve);
    session.on('session.error', reject);
  });

  await session.send({ prompt });
  await done;
  await session.disconnect();

  return parseEnrichmentResponse(fullText);
}

// ── Apply enrichment to a skill ───────────────────────────────────────────────
function applyEnrichment(skill, enrichment, now) {
  if (enrichment.shortDescription && typeof enrichment.shortDescription === 'string') {
    skill.shortDescription = enrichment.shortDescription.slice(0, 140);
  }
  if (Array.isArray(enrichment.tags) && enrichment.tags.length > 0) {
    skill.tags = enrichment.tags.slice(0, 5).map(t => String(t).toLowerCase().replace(/[^a-z0-9-]/g, '-'));
  }
  if (['beginner', 'intermediate', 'advanced'].includes(enrichment.complexity)) {
    skill.complexity = enrichment.complexity;
  }
  if (Array.isArray(enrichment.platforms) && enrichment.platforms.length > 0) {
    const validPlatforms = ['windows', 'macos', 'linux'];
    const normalizedPlatforms = enrichment.platforms
      .map(p => String(p).toLowerCase().trim())
      .filter(Boolean);
    skill.platforms = normalizedPlatforms.filter(p => validPlatforms.includes(p));
  }
  skill.enrichedAt = now;
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const token = process.env.GITHUB_TOKEN;
  if (!token) {
    console.warn('⚠️  GITHUB_TOKEN not set – skipping enrichment.');
    process.exit(0);
  }

  // Attempt to import the Copilot SDK
  let CopilotClient;
  try {
    const sdk = await import('@github/copilot-sdk');
    CopilotClient = sdk.CopilotClient;
  } catch (err) {
    console.warn('⚠️  @github/copilot-sdk not available:', err.message);
    console.warn('   Skipping enrichment.');
    process.exit(0);
  }

  const skillsPath = path.join(ROOT, 'site', 'src', 'data', 'skills.json');
  const skillsData = JSON.parse(fs.readFileSync(skillsPath, 'utf-8'));
  const skills = skillsData.skills;

  // Filter skills that need enrichment
  const toEnrich = skills.filter(s => FORCE || !s.enrichedAt);
  const batch = LIMIT > 0 ? toEnrich.slice(0, LIMIT) : toEnrich;

  console.log(`📦 Skills total: ${skills.length}`);
  console.log(`🔄 Skills to enrich: ${batch.length}${LIMIT > 0 ? ` (limited to ${LIMIT})` : ''}`);

  if (batch.length === 0) {
    console.log('✅ All skills already enriched. Use --force to re-enrich.');
    process.exit(0);
  }

  if (DRY_RUN) {
    console.log('🧪 Dry-run mode: no changes will be written.');
  }

  // Start Copilot client
  let client;
  try {
    client = new CopilotClient({ githubToken: token });
    await client.start();
  } catch (err) {
    console.warn('⚠️  Could not start Copilot client:', err.message);
    console.warn('   Is the Copilot CLI installed and accessible?');
    console.warn('   Skipping enrichment.');
    process.exit(0);
  }

  const now = new Date().toISOString();
  let enriched = 0;
  let failed = 0;

  try {
    for (const skill of batch) {
      process.stdout.write(`  Enriching ${skill.id}… `);
      try {
        const enrichment = await enrichWithCopilot(skill, client);
        if (!DRY_RUN) applyEnrichment(skill, enrichment, now);
        enriched++;
        console.log('✅');
      } catch (err) {
        failed++;
        console.log(`❌ (${err.message})`);
      }
    }
  } finally {
    await client.stop().catch(() => {});
  }

  if (!DRY_RUN && enriched > 0) {
    skillsData.lastUpdated = now;
    fs.writeFileSync(skillsPath, JSON.stringify(skillsData, null, 2));
    console.log(`\n✅ Wrote enrichment for ${enriched} skill(s) to skills.json`);
  }

  if (failed > 0) {
    console.warn(`\n⚠️  ${failed} skill(s) failed to enrich.`);
  }

  console.log('\n✅ Enrichment complete.');
}

main().catch(err => {
  console.error('❌ Fatal error:', err);
  process.exit(1);
});
