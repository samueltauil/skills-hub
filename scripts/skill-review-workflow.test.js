import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
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

test('compiled review tools read stdin, return pages and persist exactly one response', () => {
  const lock = matter(`---\n${fs.readFileSync(
    new URL('../.github/workflows/skill-security-review.lock.yml', import.meta.url), 'utf8',
  )}\n---`).data;
  const setup = lock.jobs.agent.steps.find(step => step.name === 'Setup Safe Inputs Tool Files').run;
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-review-tools-'));
  try {
    fs.mkdirSync(path.join(root, '.review-data'));
    const text = JSON.stringify({ content: 'line\r\n'.repeat(1800) });
    const inputPath = path.join(root, '.review-data', 'input.json');
    fs.writeFileSync(inputPath, text);
    for (const name of ['read_review_bundle', 'submit_review']) {
      const match = setup.match(new RegExp(`${name}\\.py << '([^']+)'\\n([\\s\\S]*?)\\n\\1`));
      assert.ok(match, `compiled ${name} subprocess handler`);
      fs.writeFileSync(path.join(root, `${name}.py`), match[2]);
    }
    const invoke = (name, inputs) => spawnSync(
      process.platform === 'win32' ? 'python' : 'python3',
      [path.join(root, `${name}.py`)],
      {
        input: JSON.stringify(inputs), encoding: 'utf8', timeout: 10000,
        env: { ...process.env, GITHUB_WORKSPACE: root, PYTHONIOENCODING: 'utf-8' },
      },
    );
    let offset = 0;
    let reconstructed = '';
    do {
      const result = invoke('read_review_bundle', { offset });
      assert.equal(result.status, 0, result.stderr || result.error?.message);
      const page = JSON.parse(result.stdout);
      assert.equal(page.offset, offset);
      assert.equal(page.totalChars, text.length);
      reconstructed += page.text;
      offset = page.nextOffset;
    } while (offset !== null);
    assert.equal(reconstructed, text);
    for (const offset of [-1, 0.5, true, text.length]) {
      assert.notEqual(invoke('read_review_bundle', { offset }).status, 0);
    }
    fs.writeFileSync(inputPath, 'x'.repeat(262145));
    assert.notEqual(invoke('read_review_bundle', { offset: 0 }).status, 0);
    for (const response of ['{', JSON.stringify('x'.repeat(1048576))]) {
      assert.notEqual(invoke('submit_review', { response }).status, 0);
      assert.equal(fs.existsSync(path.join(root, '.review-data', 'response.json')), false);
    }
    const response = JSON.stringify({ bundleHash: manifest.bundleHash, findings: [] });
    const submitted = invoke('submit_review', { response });
    assert.equal(submitted.status, 0, submitted.stderr);
    assert.match(JSON.parse(submitted.stdout), /Recorded for validation/);
    assert.notEqual(invoke('submit_review', { response: '{}' }).status, 0);
    assert.equal(fs.readFileSync(path.join(root, '.review-data', 'response.json'), 'utf8'), response);
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('review artifact uploads explicitly include the hidden review files', () => {
  const transport = workflow['post-steps'].find(step => step.with?.name === 'skill-review-transport');
  const report = workflow.jobs.report.steps.find(step => step.with?.name === 'skill-security-review');
  for (const step of [transport, report]) assert.equal(step.with['include-hidden-files'], true);
  assert.deepEqual(transport.with.path.trim().split('\n'), [
    '.review-data/input.json', '.review-data/response.json',
  ]);
});

test('independent skills do not share workflow or engine concurrency groups', () => {
  const lock = matter(`---\n${fs.readFileSync(
    new URL('../.github/workflows/skill-security-review.lock.yml', import.meta.url), 'utf8',
  )}\n---`).data;
  for (const config of [lock.concurrency, lock.jobs.agent.concurrency]) {
    assert.match(config.group, /\$\{\{ inputs\.skill \|\| inputs\.fixture \}\}/);
    assert.equal(config['cancel-in-progress'] ?? false, false);
  }
  assert.notEqual(lock.concurrency.group, lock.jobs.agent.concurrency.group);
});
