#!/usr/bin/env node
/**
 * scan-skills.js
 *
 * Scans every skill in site/src/data/skills.json for potentially dangerous
 * code patterns defined in skills/security-rules.yml.
 *
 * Usage:
 *   node scripts/scan-skills.js [--output report.json] [--update-skills]
 *
 * Options:
 *   --output <file>    Write a JSON report to this path (default: scan-report.json)
 *   --update-skills    Write scan results back into skills.json (adds securityScan field)
 *   --fail-on-high     Exit with code 1 if any high-severity issues are found
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { parseArgs } from 'util';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

// ── Parse CLI args ────────────────────────────────────────────────────────────
const { values: args } = parseArgs({
  options: {
    output: { type: 'string', default: 'scan-report.json' },
    'update-skills': { type: 'boolean', default: false },
    'fail-on-high': { type: 'boolean', default: false },
  },
  strict: false,
});

// ── Load rules ────────────────────────────────────────────────────────────────
async function loadRules() {
  // js-yaml is present as a transitive dependency (via gray-matter); prefer it
  // over the manual fallback parser so we handle the full YAML spec correctly.
  const rulesPath = path.join(ROOT, 'skills', 'security-rules.yml');
  const raw = fs.readFileSync(rulesPath, 'utf-8');

  // Use js-yaml when available (direct or transitive); fall back to the minimal
  // hand-rolled parser for controlled schema if the import fails.
  let yaml;
  try {
    const { default: jsYaml } = await import('js-yaml');
    yaml = jsYaml;
  } catch {
    return parseSimpleRulesYaml(raw);
  }
  return yaml.load(raw).rules;
}

/**
 * Minimal YAML parser for security-rules.yml.
 * Supports the exact structure used in that file only.
 */
function parseSimpleRulesYaml(raw) {
  const rules = [];
  let current = null;
  let inPatterns = false;
  let inLanguages = false;

  for (const line of raw.split('\n')) {
    const trimmed = line.trim();

    if (trimmed.startsWith('- id:')) {
      if (current) rules.push(current);
      current = { id: trimmed.slice(5).trim(), name: '', description: '', severity: 'medium', flags: '', patterns: [], languages: [] };
      inPatterns = false;
      inLanguages = false;
    } else if (current && trimmed.startsWith('name:')) {
      current.name = trimmed.slice(5).trim();
    } else if (current && trimmed.startsWith('description:')) {
      // multi-line (>) is joined later; take single-line value if present
      const val = trimmed.slice(12).trim();
      if (val && val !== '>') current.description = val;
    } else if (current && trimmed.startsWith('severity:')) {
      current.severity = trimmed.slice(9).trim();
    } else if (current && trimmed.startsWith('flags:')) {
      current.flags = trimmed.slice(6).trim().replace(/^['"]|['"]$/g, '');
    } else if (current && trimmed === 'patterns:') {
      inPatterns = true;
      inLanguages = false;
    } else if (current && trimmed.startsWith('languages:')) {
      inPatterns = false;
      inLanguages = true;
      const inline = trimmed.slice(10).trim();
      if (inline && inline !== '[]') {
        current.languages = inline.replace(/[\[\]]/g, '').split(',').map(s => s.trim()).filter(Boolean);
        inLanguages = false;
      } else if (inline === '[]') {
        inLanguages = false;
      }
    } else if (current && inPatterns && trimmed.startsWith('- ')) {
      const pat = trimmed.slice(2).replace(/^['"]|['"]$/g, '');
      current.patterns.push(pat);
    } else if (current && inLanguages && trimmed.startsWith('- ')) {
      current.languages.push(trimmed.slice(2).replace(/^['"]|['"]$/g, ''));
    }
  }

  if (current) rules.push(current);
  return rules;
}

// ── Code block extraction ─────────────────────────────────────────────────────
/**
 * Extract fenced code blocks from Markdown content.
 * Returns an array of { lang, code } objects.
 */
function extractCodeBlocks(markdown) {
  const blocks = [];
  const fence = /^```(\w*)\n([\s\S]*?)^```/gm;
  let match;
  while ((match = fence.exec(markdown)) !== null) {
    blocks.push({ lang: (match[1] || '').toLowerCase(), code: match[2] });
  }
  return blocks;
}

// ── Rule matching ─────────────────────────────────────────────────────────────
/**
 * Test a single code block against all rules.
 * Returns an array of issue objects.
 */
function scanBlock(block, rules) {
  const issues = [];
  for (const rule of rules) {
    // Check language filter
    if (rule.languages.length > 0 && !rule.languages.includes(block.lang)) {
      continue;
    }

    for (const pattern of rule.patterns) {
      let re;
      try {
        // Merge the default 'gm' flags with any per-rule extra flags (e.g. 'i')
        // defined in the YAML `flags` field, avoiding duplicate flag characters.
        const extraFlags = (rule.flags || '').replace(/[gm]/g, '');
        re = new RegExp(pattern, 'gm' + extraFlags);
      } catch {
        continue; // skip malformed patterns
      }

      const matches = [...block.code.matchAll(re)];
      if (matches.length > 0) {
        issues.push({
          ruleId: rule.id,
          ruleName: rule.name,
          severity: rule.severity,
          pattern,
          matchCount: matches.length,
          snippet: block.code.slice(0, 120).replace(/\n/g, '↵'),
          language: block.lang,
        });
        break; // one issue per rule per block is enough
      }
    }
  }
  return issues;
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  console.log('🔍 Loading security rules…');
  const rules = await loadRules();
  console.log(`   Loaded ${rules.length} rules`);

  const skillsPath = path.join(ROOT, 'site', 'src', 'data', 'skills.json');
  const skillsData = JSON.parse(fs.readFileSync(skillsPath, 'utf-8'));
  const skills = skillsData.skills;

  console.log(`🔍 Scanning ${skills.length} skills…`);

  const report = {
    generatedAt: new Date().toISOString(),
    totalSkills: skills.length,
    rulesApplied: rules.length,
    summary: { high: 0, medium: 0, low: 0, verified: 0 },
    findings: [],
  };

  let highCount = 0;

  for (const skill of skills) {
    const content = skill.skillMdContent || '';
    const blocks = extractCodeBlocks(content);

    const skillIssues = [];
    for (const block of blocks) {
      const issues = scanBlock(block, rules);
      skillIssues.push(...issues);
    }

    const highIssues = skillIssues.filter(i => i.severity === 'high');
    const mediumIssues = skillIssues.filter(i => i.severity === 'medium');
    const lowIssues = skillIssues.filter(i => i.severity === 'low');

    const verified = skillIssues.length === 0;

    // Update summary
    report.summary.high += highIssues.length;
    report.summary.medium += mediumIssues.length;
    report.summary.low += lowIssues.length;
    if (verified) report.summary.verified++;

    if (skillIssues.length > 0) {
      highCount += highIssues.length;
      report.findings.push({
        skillId: skill.id,
        skillName: skill.name,
        issueCount: skillIssues.length,
        issues: skillIssues,
      });
    }

    // Attach scan summary to skill in-memory (for optional write-back).
    // Only summary fields are persisted; detailed issues live in the external
    // JSON report artifact to keep skills.json small and diff-friendly.
    skill.securityScan = {
      scannedAt: report.generatedAt,
      verified,
      issueCount: skillIssues.length,
      highCount: highIssues.length,
    };
    // Top-level convenience flag for badge display
    skill.verified = verified;
  }

  // Write JSON report
  const reportPath = path.resolve(args.output);
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
  console.log(`\n📋 Report written to ${reportPath}`);

  // Print summary
  console.log('\n📊 Summary:');
  console.log(`   ✅ Verified (no issues): ${report.summary.verified} / ${skills.length}`);
  console.log(`   🔴 High severity issues: ${report.summary.high}`);
  console.log(`   🟡 Medium severity issues: ${report.summary.medium}`);
  console.log(`   🟢 Low severity issues: ${report.summary.low}`);
  console.log(`   ⚠️  Skills with findings: ${report.findings.length}`);

  if (report.findings.length > 0) {
    console.log('\n⚠️  Findings (top 10):');
    for (const finding of report.findings.slice(0, 10)) {
      const severities = finding.issues.map(i => i.severity).join(', ');
      console.log(`   - ${finding.skillId}: ${finding.issueCount} issue(s) [${severities}]`);
    }
  }

  // Optional write-back to skills.json
  if (args['update-skills']) {
    fs.writeFileSync(skillsPath, JSON.stringify(skillsData, null, 2));
    console.log('\n✅ skills.json updated with security scan results');
  }

  if (args['fail-on-high'] && highCount > 0) {
    console.error(`\n❌ ${highCount} high-severity issue(s) found. Failing.`);
    process.exit(1);
  }

  console.log('\n✅ Security scan complete.');
}

main().catch(err => {
  console.error('❌ Fatal error:', err);
  process.exit(1);
});
