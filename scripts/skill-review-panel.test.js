import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { collectSkill, errorReport, validatePublishedReport, validateResponse } from './skill-review.js';
import { getSecurityReview, summarizeSecurityReview } from '../site/src/data/security-reviews.js';

const skill = {
  id: 'example',
  name: 'example',
  files: [{ path: 'SKILL.md', content: '# Example\nExplain the supplied source code.' }],
};
const manifest = collectSkill(skill, { revision: 'a'.repeat(40) });
const report = validateResponse(manifest, {
  bundleHash: manifest.bundleHash,
  status: 'complete',
  reviewedFiles: ['SKILL.md'],
  findings: [],
});

test('missing review remains distinct from a complete review with no findings', () => {
  assert.equal(getSecurityReview(undefined, skill).status, 'not-reviewed');
  assert.equal(getSecurityReview(report, skill).status, 'complete-no-findings');
});

test('changed source content makes an otherwise valid review stale', () => {
  const changed = { ...skill, files: [{ path: 'SKILL.md', content: '# Different instructions' }] };
  const state = getSecurityReview(report, changed);
  assert.equal(state.status, 'stale');
  assert.equal(state.report, report);
});

test('current reports must match evidence and coverage, not only their stored hash', t => {
  t.mock.method(console, 'warn', () => {});
  const forged = {
    ...report,
    status: 'complete-with-findings',
    findings: [{
      category: 'prompt-injection', severity: 'high', path: 'SKILL.md',
      startLine: 2, endLine: 2, quote: 'This is not in the source', explanation: 'Forged evidence',
    }],
  };
  assert.equal(getSecurityReview(forged, skill).status, 'invalid');
  assert.equal(getSecurityReview({ ...report, skillId: 'other' }, skill).status, 'invalid');
  assert.equal(getSecurityReview({ ...report, fixture: 'case-001' }, skill).status, 'invalid');
  assert.equal(console.warn.mock.callCount(), 3);
});

test('incomplete and failed reviews never become clean results', () => {
  const incomplete = validateResponse(manifest, {
    bundleHash: manifest.bundleHash, status: 'incomplete', reviewedFiles: [], findings: [],
  });
  assert.equal(getSecurityReview(incomplete, skill).status, 'incomplete');
  assert.equal(getSecurityReview(errorReport(new Error('Model timed out'), manifest), skill).status, 'error');
});

test('coverage summary counts both omitted and unreviewed files', () => {
  const bundle = {
    ...skill,
    files: [...skill.files, { path: 'notes.md', content: 'Check permissions.' }, { path: 'image.png', content: '' }],
  };
  const collected = collectSkill(bundle, { revision: manifest.revision });
  const partial = validateResponse(collected, {
    bundleHash: collected.bundleHash, status: 'complete', reviewedFiles: ['SKILL.md'], findings: [],
  });
  const review = getSecurityReview(partial, bundle);
  const summary = summarizeSecurityReview(review);
  assert.equal(review.status, 'incomplete');
  assert.equal(summary.coverage, '1 of 3 catalog files reviewed');
  assert.equal(summary.gaps, 2);
  assert.notEqual(summary.label, 'No findings observed');
});

test('legacy scan flags cannot influence review status or coverage', () => {
  const legacy = { ...skill, verified: true, securityScan: { verified: true, issueCount: 0 } };
  const unreviewed = summarizeSecurityReview(getSecurityReview(undefined, legacy));
  assert.equal(unreviewed.label, 'Not reviewed');
  assert.equal(unreviewed.coverage, 'Coverage unavailable');
  const changed = { ...legacy, files: [{ path: 'SKILL.md', content: 'Changed.' }] };
  assert.equal(summarizeSecurityReview(getSecurityReview(report, changed)).label, 'Out of date');
});

test('published review files belong to catalog skills and pass panel validation', () => {
  const directory = fileURLToPath(new URL('../site/src/data/security-reviews/', import.meta.url));
  const catalog = JSON.parse(fs.readFileSync(new URL('../site/src/data/skills.json', import.meta.url), 'utf8'));
  const skills = new Map(catalog.skills.map(entry => [entry.id, entry]));
  const reportsByRevision = new Map();
  for (const filename of fs.readdirSync(directory).filter(name => name.endsWith('.json'))) {
    const file = path.join(directory, filename);
    assert(fs.lstatSync(file).isFile(), `Report must be a regular file: ${filename}`);
    assert(fs.statSync(file).size <= 2 * 1024 * 1024, `Report exceeds size limit: ${filename}`);
    const id = filename.slice(0, -5);
    assert(skills.has(id), `Report does not belong to a catalog skill: ${filename}`);
    const report = validatePublishedReport(JSON.parse(fs.readFileSync(file, 'utf8')));
    const review = getSecurityReview(report, skills.get(id));
    assert.notEqual(review.status, 'invalid', `Invalid published report: ${filename}`);
    if (!reportsByRevision.has(report.revision)) reportsByRevision.set(report.revision, []);
    reportsByRevision.get(report.revision).push(report);
  }
  for (const [revision, reports] of reportsByRevision) {
    const original = JSON.parse(execFileSync('git', ['show', `${revision}:site/src/data/skills.json`], {
      cwd: fileURLToPath(new URL('../', import.meta.url)), encoding: 'utf8', maxBuffer: 256 * 1024 * 1024,
    }));
    const originals = new Map(original.skills.map(entry => [entry.id, entry]));
    for (const report of reports) {
      assert(originals.has(report.skillId), `Skill absent from reviewed revision: ${report.skillId}`);
      validatePublishedReport(report, collectSkill(originals.get(report.skillId), { revision }));
    }
  }
});
