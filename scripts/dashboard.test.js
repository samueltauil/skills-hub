import test from 'node:test';
import assert from 'node:assert/strict';
import { aggregateDashboard } from '../site/src/data/dashboard.js';
import { collectSkill, errorReport, validateResponse } from './skill-review.js';

function skill(id, metadata = {}) {
  return { id, name: id, files: [{ path: 'SKILL.md', content: 'Inspect permissions.' }], ...metadata };
}

function report(entry, response = {}) {
  const manifest = collectSkill(entry, { revision: 'a'.repeat(40) });
  return validateResponse(manifest, {
    bundleHash: manifest.bundleHash, status: 'complete',
    reviewedFiles: ['SKILL.md'], findings: [], ...response,
  });
}

test('counts actual skills and bundled files with deterministic distributions and browse-compatible fallbacks', () => {
  const skills = [
    skill('alpha', { category: 'testing', source: { repoName: 'org/repo' }, license: 'MIT', complexity: 'beginner' }),
    skill('beta', { category: 'testing', source: { repoName: 'org/repo' }, license: 'MIT', files: [] }),
    skill('gamma', { category: 'security', source: { repoName: 'other/repo' }, files: [{ path: 'a.md', content: '' }, { path: 'b.md', content: '' }] }),
    { id: 'delta', name: 'delta' },
  ];
  const before = structuredClone(skills);
  const data = aggregateDashboard(skills);
  assert.equal(data.skillCount, 4);
  assert.equal(data.fileCount, 3);
  assert.equal(data.categoryCount, 3);
  assert.equal(data.sourceCount, 2);
  assert.equal(data.unknownSourceCount, 1);
  assert.deepEqual(data.categories, [
    { id: 'testing', count: 2, percentage: 50 },
    { id: 'general', count: 1, percentage: 25 },
    { id: 'security', count: 1, percentage: 25 },
  ]);
  assert.deepEqual(data.sources.map(row => [row.id, row.count]), [['org/repo', 2], ['other/repo', 1], ['unknown', 1]]);
  assert.deepEqual(data.licenses.map(row => [row.id, row.count]), [['MIT', 2], ['Not specified', 2]]);
  assert.deepEqual(data.complexities.map(row => [row.id, row.count]), [['Not specified', 3], ['beginner', 1]]);
  for (const key of ['categories', 'sources', 'licenses', 'complexities']) {
    assert.equal(data[key].reduce((sum, row) => sum + row.count, 0), 4);
    assert.equal(data[key].reduce((sum, row) => sum + row.percentage, 0), 100);
  }
  assert.deepEqual(skills, before);
});

test('validates all report states and counts only complete, current reviews toward completion', t => {
  t.mock.method(console, 'warn', () => {});
  const skills = ['clean', 'findings', 'partial', 'stale', 'error', 'invalid', 'missing'].map(id => skill(id));
  const [clean, findings, partial, stale, failed, invalid] = skills;
  const reports = {
    clean: report(clean),
    findings: report(findings, { findings: [{
      category: 'unsafe-execution', severity: 'low', path: 'SKILL.md', startLine: 1, endLine: 1,
      quote: 'Inspect permissions.', explanation: 'Review permissions before continuing.',
    }] }),
    partial: report(partial, { status: 'incomplete', reviewedFiles: [] }),
    stale: report({ ...stale, files: [{ path: 'SKILL.md', content: 'Previous content.' }] }),
    error: errorReport(new Error('Model timed out'), collectSkill(failed, { revision: 'a'.repeat(40) })),
    invalid: { ...report(invalid), skillId: 'other' },
    orphan: report(skill('orphan')),
  };
  const before = structuredClone(reports);
  const data = aggregateDashboard(skills, reports);
  assert.deepEqual(data.reviews, {
    'complete-no-findings': 1, 'complete-with-findings': 1,
    incomplete: 1, stale: 1, error: 1, invalid: 1, 'not-reviewed': 1,
  });
  assert.equal(data.completeCount, 2);
  assert.equal(data.completePercentage, 2 / 7 * 100);
  assert.equal(Object.values(data.reviews).reduce((a, b) => a + b, 0), 7);
  assert.deepEqual(reports, before);
});

test('report validation catches forged evidence and unfinished file coverage', t => {
  t.mock.method(console, 'warn', () => {});
  const forgedSkill = skill('forged');
  const partial = skill('partial', { files: [
    { path: 'SKILL.md', content: 'Inspect permissions.' }, { path: 'notes.md', content: 'More instructions.' },
  ] });
  const forged = { ...report(forgedSkill), status: 'complete-with-findings', findings: [{
    category: 'unsafe-execution', severity: 'high', path: 'SKILL.md', startLine: 1, endLine: 1,
    quote: 'Fabricated evidence.', explanation: 'Not in the current catalog.',
  }] };
  const data = aggregateDashboard([forgedSkill, partial], { forged, partial: report(partial) });
  assert.equal(data.reviews.invalid, 1);
  assert.equal(data.reviews.incomplete, 1);
  assert.equal(data.completeCount, 0);
});

test('empty catalogs and missing reports yield finite zero coverage, never inferred reviews', () => {
  const empty = aggregateDashboard([]);
  for (const key of ['skillCount', 'categoryCount', 'sourceCount', 'fileCount', 'completeCount', 'completePercentage']) {
    assert.equal(empty[key], 0);
  }
  assert.deepEqual(empty.categories, []);
  assert.deepEqual(empty.sources, []);
  const legacy = skill('legacy', { verified: true, securityScan: { verified: true, issueCount: 0 } });
  const data = aggregateDashboard([legacy]);
  assert.equal(data.reviews['not-reviewed'], 1);
  assert.equal(data.completeCount, 0);
  assert.equal(data.sources[0].percentage, 100);
});
