import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import { transform as compileAstro } from '@astrojs/compiler';
import { transform as compileTypeScript } from 'esbuild';
import { experimental_AstroContainer as AstroContainer } from 'astro/container';
import { collectSkill, errorReport, validateResponse } from '../../scripts/skill-review.js';

const componentUrl = new URL('../src/components/SecurityReview.astro', import.meta.url);
const source = await fs.readFile(componentUrl, 'utf8');
// Replace Vite's build-time file discovery with fixture reports; render the actual component.
const compiled = await compileAstro(source.replace(
  "import.meta.glob('../data/security-reviews/*.json', { eager: true, import: 'default' })",
  'Astro.props.reports',
).replace(
  "'../data/security-reviews.js'",
  JSON.stringify(new URL('../src/data/security-reviews.js', import.meta.url).href),
), {
  filename: componentUrl.pathname,
  internalURL: import.meta.resolve('astro/compiler-runtime'),
  resultScopedSlot: true,
  renderScript: true,
});
// CSS imports and legacy compiler metadata are handled by Vite, not the HTML-only container.
const { code } = await compileTypeScript(compiled.code.replace(
  /^import\s+["'][^"']+\?astro&type=style[^"']+["'];?\s*$/gm, '',
).replace(
  /export const \$\$metadata = [^\n]+\n/g, '',
).replace(
  /,\s*createMetadata as \$\$createMetadata/, '',
), { loader: 'ts', format: 'esm' });
const { default: SecurityReview } = await import(`data:text/javascript;base64,${Buffer.from(code).toString('base64')}`);
const container = await AstroContainer.create();
const skill = { id: 'example', name: 'example', source: {}, files: [{ path: 'SKILL.md', content: '# Example\nInspect permissions.' }] };
const manifest = collectSkill(skill, { revision: 'a'.repeat(40) });
const complete = validateResponse(manifest, {
  bundleHash: manifest.bundleHash, status: 'complete', reviewedFiles: ['SKILL.md'], findings: [],
});

async function render(report, currentSkill = skill) {
  return container.renderToString(SecurityReview, { props: {
    skill: currentSkill,
    reports: report === undefined ? {} : { '../data/security-reviews/example.json': report },
  } });
}

test('renders distinct statuses without clean claims for missing, stale, partial, failed or invalid reviews', async t => {
  t.mock.method(console, 'warn', () => {});
  const incomplete = validateResponse(manifest, {
    bundleHash: manifest.bundleHash, status: 'incomplete', reviewedFiles: ['SKILL.md'], findings: [],
  });
  const cases = [
    [undefined, skill, 'Not reviewed', 'not-reviewed'],
    [complete, { ...skill, files: [{ path: 'SKILL.md', content: 'Changed' }] }, 'Out of date', 'stale'],
    [incomplete, skill, 'Incomplete review', 'incomplete'],
    [errorReport(new Error('Model timed out'), manifest), skill, 'Review failed', 'error'],
    [{ ...complete, skillId: 'other' }, skill, 'Report unavailable', 'invalid'],
  ];
  for (const [report, currentSkill, label, status] of cases) {
    const html = await render(report, currentSkill);
    assert(html.includes(label));
    assert(html.includes(`data-review-status="${status}"`));
    assert(!html.includes('No findings observed'));
    assert(!html.includes('Pattern checks passed'));
    assert.match(html, /<section[^>]+aria-labelledby="security-review-example"/);
    assert.match(html, /<h2[^>]+id="security-review-example"/);
  }
});

test('complete review shows concise coverage/date and collapses technical metadata', async () => {
  const html = await render(complete);
  assert(html.includes('No findings observed'));
  assert(html.includes('1 of 1 catalog files reviewed'));
  assert(html.includes('not a safety guarantee'));
  assert.match(html, /<time datetime=/);
  assert.match(html, /<details[^>]*class="review-details(?: [^"]*)?"[^>]*>\s*<summary[^>]*>Review details/);
  assert(!/<details[^>]*\bopen\b/.test(html));
  assert(html.indexOf('Catalog commit') > html.indexOf('Review details'));
  assert(html.includes('GitHub Agentic Workflows'));
});

test('findings show explanations and actions while cited markup stays escaped inside disclosure', async () => {
  const quote = '<img src=x onerror=alert(1)>';
  const bundle = { ...skill, files: [{ path: 'SKILL.md', content: quote }] };
  const collected = collectSkill(bundle, { revision: manifest.revision });
  const report = validateResponse(collected, {
    bundleHash: collected.bundleHash, status: 'complete', reviewedFiles: ['SKILL.md'],
    findings: [{
      category: 'unsafe-execution', severity: 'high', path: 'SKILL.md',
      startLine: 1, endLine: 1, quote, explanation: `Inspect this content: ${quote}`,
    }],
  });
  const html = await render(report, bundle);
  assert(html.includes('Findings to assess'));
  assert(html.includes('not confirmed vulnerabilities'));
  assert(html.indexOf('Inspect this content:') < html.indexOf('View cited evidence'));
  assert(html.indexOf('Before installing:') < html.indexOf('View cited evidence'));
  assert(html.includes('lines 1–1'));
  assert(!html.includes('<img'));
  assert(html.includes('&lt;img'));
  assert.match(html, /<details[^>]*class="finding-details(?: [^"]*)?"[^>]*>\s*<summary[^>]*>View cited evidence/);
});

test('incomplete review exposes omitted and unreviewed paths without a no-findings verdict', async () => {
  const bundle = { ...skill, files: [
    ...skill.files,
    { path: 'notes.md', content: 'Check permissions.' },
    { path: 'image.png', content: '' },
  ] };
  const collected = collectSkill(bundle, { revision: manifest.revision });
  const report = validateResponse(collected, {
    bundleHash: collected.bundleHash, status: 'complete', reviewedFiles: ['SKILL.md'], findings: [],
  });
  const html = await render(report, bundle);
  assert(html.includes('Incomplete review'));
  assert(html.includes('1 of 3 catalog files reviewed'));
  assert(html.includes('2 not reviewed'));
  assert(html.includes('Review details and coverage gaps'));
  assert(html.includes('notes.md'));
  assert(html.includes('image.png'));
  assert(!html.includes('No findings observed'));
});

test('catalog and detail pages no longer consume legacy scan flags or badges', async () => {
  const paths = [
    'components/SkillCard.astro', 'pages/index.astro', 'pages/categories/[id].astro',
    'pages/skills/index.astro', 'pages/skills/[id].astro',
  ];
  for (const path of paths) {
    const content = await fs.readFile(new URL(`../src/${path}`, import.meta.url), 'utf8');
    assert.doesNotMatch(content, /securityScan|\bverified\b|badge-scanned|Security Scan/, path);
  }
  const detail = await fs.readFile(new URL('../src/pages/skills/[id].astro', import.meta.url), 'utf8');
  assert.equal(detail.match(/<SecurityReview\b/g)?.length, 1);
  assert(detail.indexOf('<SecurityReview') < detail.indexOf('<!-- Installation Section -->'));
  assert(detail.indexOf('<SecurityReview') < detail.indexOf('<aside'));
});
