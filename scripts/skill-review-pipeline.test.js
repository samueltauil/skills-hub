import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';

const root = new URL('../', import.meta.url);
const read = file => fs.readFileSync(new URL(file, root), 'utf8');
const workflow = file => matter(`---\n${read(`.github/workflows/${file}`)}\n---`).data;

test('normal build and refresh paths never invoke the legacy scanner', () => {
  const { scripts } = JSON.parse(read('package.json'));
  assert.equal(scripts.scan, undefined);
  assert.equal(scripts['scan:ai'], undefined);
  assert.match(scripts.build, /npm run aggregate/);
  assert.match(scripts.build, /npm run validate:plugins/);
  assert.doesNotMatch(JSON.stringify(scripts), /scan-skills|npm run scan|--update-skills/);
  for (const file of fs.readdirSync(new URL('.github/workflows/', root))) {
    assert.doesNotMatch(read(`.github/workflows/${file}`), /node\s+scripts\/scan-skills\.js|npm run scan|--update-skills/, file);
  }
  assert.doesNotMatch(read('scripts/aggregate-skills.js'), /scan-skills|securityScan|\.verified\s*=/);
});

test('enrichment remains manual and independent of security scanning', () => {
  const enrich = workflow('enrich-skills.yml');
  assert.deepEqual(Object.keys(enrich.on), ['workflow_dispatch']);
  assert.deepEqual(Object.keys(enrich.jobs), ['enrich']);
  assert.equal(enrich.jobs.enrich.needs, undefined);
  const steps = enrich.jobs.enrich.steps.map(step => step.run ?? '').join('\n');
  assert.match(steps, /scripts\/enrich-skills\.js/);
  assert.match(steps, /scripts\/validate-plugins\.js/);
  const sync = workflow('sync-skills.yml');
  assert.ok(sync.on.schedule);
  assert.ok(sync.jobs['sync-skills'].steps.some(step => step.run?.includes('scripts/aggregate-skills.js')));
});

test('legacy write-back is rejected before scanning and leaves catalog bytes intact', () => {
  const catalog = new URL('site/src/data/skills.json', root);
  const before = fs.readFileSync(catalog);
  for (const flags of [['--update-skills'], ['--update-skills', '--ai-scan']]) {
    const result = spawnSync(process.execPath, [
      fileURLToPath(new URL('scripts/scan-skills.js', root)),
      ...flags,
    ], { cwd: root, encoding: 'utf8', timeout: 10_000 });
    assert.equal(result.status, 1, result.stderr);
    assert.match(result.stderr, /--update-skills is retired/);
    assert.doesNotMatch(result.stdout, /Loading security rules|Scanning/);
    assert.deepEqual(fs.readFileSync(catalog), before);
  }
});

test('changed ordinary workflows retain LF line endings', () => {
  for (const file of ['enrich-skills.yml', 'sync-skills.yml', 'validate-skill-reviews.yml']) {
    assert.ok(!read(`.github/workflows/${file}`).includes('\r'), file);
  }
});

test('review CI runs rendered UI tests after building and covers pipeline and UI changes', () => {
  const ci = workflow('validate-skill-reviews.yml');
  const runs = ci.jobs.validate.steps.map(step => step.run);
  const buildIndex = runs.indexOf('npm --prefix site run build');
  assert.ok(buildIndex >= 0);
  assert.ok(runs.indexOf('node --test site/tests/*.test.js') > buildIndex);
  assert.ok(runs.includes('node --test scripts/skill-review*.test.js'));
  assert.ok(runs.includes('node --test scripts/dashboard.test.js scripts/seo-*.test.js'));
  const requiredPaths = [
    'scripts/skill-review*', 'scripts/aggregate-skills.js', 'scripts/scan-skills.js',
    'scripts/enrich-skills.js', 'scripts/build-plugins.js', '.github/plugin/marketplace.json',
    'site/src/data/security-reviews*', 'site/src/data/security-reviews/**',
    'site/src/data/skills.json', 'site/src/components/SecurityReview.astro',
    'site/src/components/SkillCard.astro', 'site/src/pages/index.astro',
    'site/src/pages/categories/**', 'site/src/pages/skills/**', 'site/tests/**',
    'scripts/dashboard.test.js', 'scripts/seo-*.test.js', 'site/src/data/dashboard.js',
    'site/src/data/seo*.js', 'site/src/layouts/**',
    'site/src/components/DashboardDistribution.astro', 'site/src/pages/dashboard.astro',
    '.github/workflows/skill-security-review*', '.github/workflows/validate-skill-reviews.yml',
    '.github/workflows/enrich-skills.yml', '.github/workflows/sync-skills.yml',
    'package*.json', 'site/package*.json',
  ];
  for (const event of ['push', 'pull_request']) {
    for (const file of requiredPaths) assert.ok(ci.on[event].paths.includes(file), `${event}: ${file}`);
  }
});

test('marketplace description makes no blanket security coverage claim', () => {
  const { description } = JSON.parse(read('.github/plugin/marketplace.json')).metadata;
  assert.match(description, /See each skill page for security review coverage/);
  assert.doesNotMatch(description, /Every skill is security scanned/);
  assert.ok(read('scripts/build-plugins.js').includes(description));
});
