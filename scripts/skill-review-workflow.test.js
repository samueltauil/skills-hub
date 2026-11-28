import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import matter from 'gray-matter';
import { collectSkill, errorReport, validateResponse } from './skill-review.js';

const workflow = matter(fs.readFileSync(
  new URL('../.github/workflows/skill-security-review.md', import.meta.url), 'utf8',
)).data;
const manifest = collectSkill({
  id: 'example', name: 'example',
  files: [{ path: 'SKILL.md', content: 'Example instruction.' }],
}, { revision: 'a'.repeat(40) });

function canPublish(report, { publish = true, fixture = '', ref = 'refs/heads/main', agentResult = 'success', reportResult = 'success' } = {}) {
  // Evaluate the trusted workflow's simple boolean condition with realistic job outputs.
  const condition = new Function('github', 'inputs', 'needs', `return (${workflow.jobs.publish.if});`);
  return condition({ ref }, { publish, fixture }, {
    agent: { result: agentResult },
    report: { result: reportResult, outputs: { status: report.status, skill_id: report.skillId ?? '' } },
  });
}

test('opt-in publishing accepts actual complete and incomplete validator statuses', () => {
  const response = { bundleHash: manifest.bundleHash, status: 'complete', reviewedFiles: ['SKILL.md'], findings: [] };
  const noFindings = validateResponse(manifest, response);
  const withFindings = validateResponse(manifest, {
    ...response,
    findings: [{
      category: 'other', severity: 'low', path: 'SKILL.md', startLine: 1, endLine: 1,
      quote: 'Example instruction.', explanation: 'An evaluation example requiring human assessment.',
    }],
  });
  const incomplete = validateResponse(manifest, { ...response, status: 'incomplete', reviewedFiles: [] });
  for (const report of [noFindings, withFindings, incomplete]) assert.equal(canPublish(report), true, report.status);
});

test('publishing excludes fixtures, errors, unrequested writes and failed or off-main runs', () => {
  const report = validateResponse(manifest, {
    bundleHash: manifest.bundleHash, status: 'complete', reviewedFiles: ['SKILL.md'], findings: [],
  });
  for (const options of [
    { publish: false }, { fixture: 'case-001' }, { ref: 'refs/heads/untrusted' },
    { agentResult: 'failure' }, { reportResult: 'failure' },
  ]) assert.equal(canPublish(report, options), false);
  assert.equal(canPublish(errorReport(new Error('No response'), manifest)), false);
  assert.equal(canPublish({ ...report, skillId: null }), false);
});
