#!/usr/bin/env node
/**
 * Report-only review boundary. Never executes skill content or fetches its URLs.
 *
 * collect --skill <catalog-id> --output <input.json>
 * collect --fixture <case-id> --output <input.json> [--skill <matching-fixture-skill-id>]
 * validate --input <input.json> --response <response.json> --output <report.json> [--model <name>]
 * evaluate --fixture <case-id> --report <report.json> --output <evaluation.json>
 *
 * Validation always writes <output>.summary.md; invalid/missing output exits 1.
 * Quotes must match the entire inclusive line range, split on LF (preserving CR).
 * Completeness covers only files present in the canonical catalog, not upstream.
 * Fixture labels are used only by evaluate, never included in collected inputs.
 */
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';

/**
 * @typedef {'prompt-injection'|'credential-exposure'|'data-exfiltration'|'destructive-operation'|'unsafe-execution'|'supply-chain'|'other'} ReviewCategory
 * @typedef {'low'|'medium'|'high'|'critical'} ReviewSeverity
 * @typedef {'complete-with-findings'|'complete-no-findings'|'incomplete'|'error'} ReviewStatus
 * @typedef {'invalid-path'|'duplicate-path'|'unavailable-content'|'unsupported-content'|'file-too-large'|'file-limit'|'bundle-limit'|'missing-skill-markdown'} OmissionReason
 * @typedef {Object} ReviewFinding
 * @property {ReviewCategory} category
 * @property {ReviewSeverity} severity
 * @property {string} path
 * @property {number} startLine One-based inclusive line number.
 * @property {number} endLine One-based inclusive line number.
 * @property {string} quote Exact complete source lines; render as text, never markup.
 * @property {string} explanation Untrusted model text, even after evidence validation.
 *
 * @typedef {Object} OmittedReviewFile
 * @property {string} path May be an unsafe original path, recorded as data only.
 * @property {OmissionReason} reason
 *
 * @typedef {Object} ReviewCoverage
 * @property {'catalog-files-only'} scope
 * @property {string[]} reviewedFiles
 * @property {OmittedReviewFile[]} omittedFiles
 * @property {string[]} unreviewedFiles
 *
 * @typedef {Object} ReviewReport
 * @property {1} schemaVersion
 * @property {string|null} skillId Null only for errors without a valid input.
 * @property {string|null} revision Canonical checkout commit; null without valid input.
 * @property {string|null} bundleHash Revision-bound bounded manifest hash.
 * @property {string|null} contentHash Full original catalog source hash, independent of revision.
 * @property {string} reviewedAt ISO 8601 UTC timestamp.
 * @property {string} model Trusted caller-supplied model identifier, or "unspecified".
 * @property {'1.0.0'} rubricVersion
 * @property {string|null} fixture Case ID, or null for canonical catalog reviews.
 * @property {ReviewStatus} status
 * @property {ReviewCoverage} coverage
 * @property {ReviewFinding[]} findings
 * @property {string[]} errors
 */

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const CATALOG = 'site/src/data/skills.json';
export const SCHEMA_VERSION = 1;
export const RUBRIC_VERSION = '1.0.0';
export const LIMITS = Object.freeze({
  files: 32, fileBytes: 64 * 1024, inputBytes: 256 * 1024,
  responseBytes: 1024 * 1024, findings: 64, quoteChars: 8192,
  explanationChars: 2048, pathChars: 1024, summaryBytes: 32 * 1024,
});
export const CATEGORIES = Object.freeze([
  'prompt-injection', 'credential-exposure', 'data-exfiltration',
  'destructive-operation', 'unsafe-execution', 'supply-chain', 'other',
]);
export const SEVERITIES = Object.freeze(['low', 'medium', 'high', 'critical']);
const HASH = /^[a-f0-9]{64}$/;
const REVISION = /^[a-f0-9]{40,64}$/;
const ID = /^[a-z0-9]+(?:[._-][a-z0-9]+)*$/;
const TEXT_EXTENSIONS = new Set((
  '.md .mdx .txt .rst .adoc .json .jsonc .jsonl .yaml .yml .toml .ini .cfg .conf ' +
  '.js .mjs .cjs .jsx .ts .tsx .py .sh .bash .zsh .ps1 .psm1 .psd1 .bat .cmd ' +
  '.go .rs .rb .php .java .kt .kts .c .h .cpp .hpp .cs .fs .swift .scala ' +
  '.css .scss .html .htm .xml .sql .graphql .gql .vue .svelte .r .lua .pl ' +
  '.dockerfile .makefile .gitignore .editorconfig .env .csv .tsv .ipynb'
).split(/\s+/));
const REASONS = new Set([
  'invalid-path', 'duplicate-path', 'unavailable-content', 'unsupported-content',
  'file-too-large', 'file-limit', 'bundle-limit', 'missing-skill-markdown',
]);

function requireThat(condition, message) {
  if (!condition) throw new Error(message);
}
function object(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}
function keys(value, allowed, where) {
  requireThat(object(value), `${where} must be an object`);
  requireThat(Object.keys(value).length === allowed.length &&
    allowed.every(key => Object.hasOwn(value, key)), `${where} has missing or unexpected fields`);
}
function string(value, max, where, allowEmpty = false) {
  requireThat(typeof value === 'string' && (allowEmpty || value.length > 0) &&
    value.length <= max, `${where} must be a bounded string`);
}
function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  if (object(value)) return `{${Object.keys(value).sort().map(key =>
    `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
  return JSON.stringify(value);
}
export function sha256(content) {
  return createHash('sha256').update(content, 'utf8').digest('hex');
}
function bytes(value) {
  return Buffer.byteLength(JSON.stringify(value), 'utf8') + 1;
}
export function computeManifestHash(manifest) {
  const { bundleHash: ignored, ...payload } = manifest;
  return sha256(canonical(payload));
}
// Full canonical catalog source, including omitted/oversized/unsupported files.
// It excludes checkout revision so a report-only commit does not stale itself.
export function computeBundleHash(skill) {
  if (Object.hasOwn(skill, 'schemaVersion')) return computeManifestHash(skill);
  requireThat(Array.isArray(skill.files), 'Catalog files must be an array');
  return sha256(canonical({
    id: skill.id, name: skill.name ?? skill.id, source: skill.source ?? {},
    files: skill.files.map(file => ({ path: file.path, content: file.content ?? null }))
      .sort((a, b) => canonical(a) < canonical(b) ? -1 : canonical(a) > canonical(b) ? 1 : 0),
  }));
}
export function computeContentHash(manifest) {
  return manifest.skill.contentHash;
}
export function isSafeReviewPath(value) {
  return typeof value === 'string' && value.length > 0 && value.length <= LIMITS.pathChars &&
    !/[\\:\u0000-\u001f\u007f]/.test(value) && !value.startsWith('/') &&
    value.split('/').every(part => part && part !== '.' && part !== '..' &&
      !/[. ]$/.test(part) && !/[<>|"*?]/.test(part) &&
      !/^(?:con|prn|aux|nul|com[1-9]|lpt[1-9])(?:\.|$)/i.test(part));
}
function supportedText(file) {
  const extension = path.posix.extname(file.path).toLowerCase();
  const basename = path.posix.basename(file.path).toLowerCase();
  return (TEXT_EXTENSIONS.has(extension) ||
    /^(?:license|licence|notice|copying|dockerfile|makefile|gemfile|rakefile)$/.test(basename)) &&
    !/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f\ufffd]/u.test(file.content) &&
    Buffer.from(file.content, 'utf8').toString('utf8') === file.content;
}
function skillMetadata(skill, fixture) {
  requireThat(object(skill) && typeof skill.id === 'string' && ID.test(skill.id) &&
    skill.id.length <= 128, 'Invalid catalog skill id');
  string(skill.name ?? skill.id, 256, 'skill.name');
  const source = {};
  if (skill.source !== undefined) {
    requireThat(object(skill.source), 'skill.source must be an object');
    for (const key of ['repo', 'repoName', 'path', 'branch']) {
      if (skill.source[key] !== undefined) {
        string(skill.source[key], 2048, `skill.source.${key}`);
        source[key] = skill.source[key];
      }
    }
  }
  return { id: skill.id, name: skill.name ?? skill.id, source, fixture };
}

export function collectSkill(skill, { revision, fixture = null } = {}) {
  requireThat(typeof revision === 'string' && REVISION.test(revision), 'Invalid catalog revision');
  requireThat(fixture === null || (typeof fixture === 'string' && ID.test(fixture) &&
    fixture.length <= 128), 'Invalid fixture id');
  const manifest = {
    schemaVersion: SCHEMA_VERSION, revision, bundleHash: '0'.repeat(64),
    skill: { ...skillMetadata(skill, fixture), contentHash: computeBundleHash(skill) }, files: [], omittedFiles: [],
  };
  requireThat(Array.isArray(skill.files), 'Catalog files must be an array');
  requireThat(skill.files.length <= 4096, 'Too many catalog entries to enumerate within the input budget');
  const candidates = [];
  const counts = new Map();
  for (const file of skill.files) {
    requireThat(object(file), 'Malformed catalog file entry');
    string(file.path, LIMITS.pathChars, 'catalog file path');
    counts.set(file.path.toLowerCase(), (counts.get(file.path.toLowerCase()) ?? 0) + 1);
  }
  for (const file of [...skill.files].sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0)) {
    let reason;
    if (!isSafeReviewPath(file.path)) reason = 'invalid-path';
    else if (counts.get(file.path.toLowerCase()) > 1) reason = 'duplicate-path';
    else if (typeof file.content !== 'string') reason = 'unavailable-content';
    else if (Buffer.byteLength(file.content, 'utf8') > LIMITS.fileBytes) reason = 'file-too-large';
    else if (!supportedText(file)) reason = 'unsupported-content';
    if (reason) manifest.omittedFiles.push({ path: file.path, reason });
    else candidates.push(file);
  }
  if (!skill.files.some(file => file.path === 'SKILL.md')) {
    manifest.omittedFiles.push({ path: 'SKILL.md', reason: 'missing-skill-markdown' });
  }
  // Reserve every gap up front: adding content can never silently drop an omission.
  const pending = candidates.map(file => ({ path: file.path, reason: 'bundle-limit' }));
  manifest.omittedFiles.push(...pending);
  requireThat(bytes(manifest) <= LIMITS.inputBytes, 'Omission metadata exceeds the total input budget');
  for (let index = 0; index < candidates.length; index++) {
    const file = candidates[index];
    const omission = pending[index];
    if (manifest.files.length >= LIMITS.files) {
      omission.reason = 'file-limit';
      continue;
    }
    manifest.omittedFiles.splice(manifest.omittedFiles.indexOf(omission), 1);
    manifest.files.push({ path: file.path, sha256: sha256(file.content), content: file.content });
    if (bytes(manifest) > LIMITS.inputBytes) {
      manifest.files.pop();
      manifest.omittedFiles.push(omission);
    }
  }
  manifest.omittedFiles.sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);
  manifest.bundleHash = computeBundleHash(manifest);
  validateManifest(manifest);
  return manifest;
}

export function validateManifest(manifest) {
  keys(manifest, ['schemaVersion', 'revision', 'bundleHash', 'skill', 'files', 'omittedFiles'], 'input');
  requireThat(bytes(manifest) <= LIMITS.inputBytes, 'Input exceeds total byte limit');
  requireThat(manifest.schemaVersion === SCHEMA_VERSION, 'Unsupported input schemaVersion');
  requireThat(typeof manifest.revision === 'string' && REVISION.test(manifest.revision), 'Invalid input revision');
  keys(manifest.skill, ['id', 'name', 'source', 'fixture', 'contentHash'], 'input.skill');
  const { contentHash, ...metadata } = manifest.skill;
  requireThat(typeof contentHash === 'string' && HASH.test(contentHash), 'Invalid original content hash');
  requireThat(canonical(skillMetadata(manifest.skill, manifest.skill.fixture)) === canonical(metadata),
    'Invalid input skill metadata');
  requireThat(manifest.skill.fixture === null || (typeof manifest.skill.fixture === 'string' &&
    ID.test(manifest.skill.fixture) && manifest.skill.fixture.length <= 128), 'Invalid input fixture');
  requireThat(Array.isArray(manifest.files) && manifest.files.length <= LIMITS.files, 'Invalid input files limit');
  requireThat(Array.isArray(manifest.omittedFiles) && manifest.omittedFiles.length <= 4097, 'Invalid omittedFiles');
  const paths = new Set();
  for (const file of manifest.files) {
    keys(file, ['path', 'sha256', 'content'], 'input file');
    requireThat(isSafeReviewPath(file.path), 'Unsafe input file path');
    requireThat(!paths.has(file.path.toLowerCase()), 'Duplicate input file path');
    paths.add(file.path.toLowerCase());
    requireThat(typeof file.content === 'string' &&
      Buffer.byteLength(file.content, 'utf8') <= LIMITS.fileBytes && supportedText(file), 'Unsupported input file content');
    requireThat(typeof file.sha256 === 'string' && HASH.test(file.sha256) &&
      file.sha256 === sha256(file.content), 'Input file hash mismatch');
  }
  for (const omitted of manifest.omittedFiles) {
    keys(omitted, ['path', 'reason'], 'omitted file');
    string(omitted.path, LIMITS.pathChars, 'omitted file path');
    requireThat(REASONS.has(omitted.reason), 'Unknown omission reason');
    requireThat(!paths.has(omitted.path.toLowerCase()), 'Omitted file also appears in input files');
  }
  requireThat(manifest.files.some(file => file.path === 'SKILL.md') ||
    manifest.omittedFiles.some(file => file.path === 'SKILL.md'), 'Missing SKILL.md coverage gap');
  requireThat(typeof manifest.bundleHash === 'string' && HASH.test(manifest.bundleHash) &&
    manifest.bundleHash === computeBundleHash(manifest), 'Input bundle hash mismatch');
  return manifest;
}

/** @returns {ReviewReport} */
export function validateResponse(manifest, response, { model = 'unspecified', reviewedAt = new Date().toISOString() } = {}) {
  validateManifest(manifest);
  string(model, 128, 'model');
  requireThat(typeof reviewedAt === 'string' && !Number.isNaN(Date.parse(reviewedAt)) &&
    new Date(reviewedAt).toISOString() === reviewedAt, 'Invalid reviewedAt timestamp');
  keys(response, ['bundleHash', 'status', 'reviewedFiles', 'findings'], 'response');
  requireThat(bytes(response) <= LIMITS.responseBytes, 'Response exceeds byte limit');
  requireThat(response.bundleHash === manifest.bundleHash, 'Response bundle hash mismatch');
  requireThat(['complete', 'incomplete'].includes(response.status), 'Invalid response status');
  requireThat(Array.isArray(response.reviewedFiles) && response.reviewedFiles.length <= LIMITS.files,
    'Invalid reviewedFiles limit');
  const files = new Map(manifest.files.map(file => [file.path, file]));
  const reviewed = new Set();
  for (const file of response.reviewedFiles) {
    requireThat(typeof file === 'string' && files.has(file), 'Unknown reviewed file path');
    requireThat(!reviewed.has(file), 'Duplicate reviewed file path');
    reviewed.add(file);
  }
  requireThat(Array.isArray(response.findings) && response.findings.length <= LIMITS.findings, 'Invalid findings limit');
  const findingKeys = new Set();
  for (const finding of response.findings) {
    keys(finding, ['category', 'severity', 'path', 'startLine', 'endLine', 'quote', 'explanation'], 'finding');
    requireThat(CATEGORIES.includes(finding.category), 'Invalid finding category');
    requireThat(SEVERITIES.includes(finding.severity), 'Invalid finding severity');
    requireThat(typeof finding.path === 'string' && reviewed.has(finding.path), 'Finding path was not reviewed');
    const lines = files.get(finding.path).content.split('\n');
    requireThat(Number.isSafeInteger(finding.startLine) && Number.isSafeInteger(finding.endLine) &&
      finding.startLine >= 1 && finding.endLine >= finding.startLine && finding.endLine <= lines.length,
    'Invalid finding line range');
    string(finding.quote, LIMITS.quoteChars, 'finding.quote');
    string(finding.explanation, LIMITS.explanationChars, 'finding.explanation');
    requireThat(finding.quote.trim().length > 0, 'Finding quote must contain evidence');
    requireThat(finding.quote === lines.slice(finding.startLine - 1, finding.endLine).join('\n'),
      'Finding evidence does not exactly match the cited lines');
    const key = canonical(finding);
    requireThat(!findingKeys.has(key), 'Duplicate finding');
    findingKeys.add(key);
  }
  const unreviewedFiles = manifest.files.filter(file => !reviewed.has(file.path)).map(file => file.path);
  const incomplete = response.status === 'incomplete' || manifest.omittedFiles.length > 0 ||
    unreviewedFiles.length > 0 || manifest.files.length === 0;
  return {
    schemaVersion: SCHEMA_VERSION, skillId: manifest.skill.id,
    revision: manifest.revision, bundleHash: manifest.bundleHash, contentHash: computeContentHash(manifest),
    reviewedAt, model, rubricVersion: RUBRIC_VERSION, fixture: manifest.skill.fixture,
    status: incomplete ? 'incomplete' : response.findings.length ? 'complete-with-findings' : 'complete-no-findings',
    coverage: {
      scope: 'catalog-files-only', reviewedFiles: [...reviewed].sort(),
      omittedFiles: manifest.omittedFiles, unreviewedFiles,
    },
    findings: response.findings, errors: [],
  };
}

/** @returns {ReviewReport} */
export function errorReport(error, manifest = null) {
  // Only carry identity from an already validated input, never from model output.
  let valid = null;
  try { valid = validateManifest(manifest); } catch { /* Invalid input has no trusted identity. */ }
  return {
    schemaVersion: SCHEMA_VERSION, skillId: valid?.skill.id ?? null,
    revision: valid?.revision ?? null, bundleHash: valid?.bundleHash ?? null,
    contentHash: valid ? computeContentHash(valid) : null,
    reviewedAt: new Date().toISOString(), model: 'unspecified', rubricVersion: RUBRIC_VERSION,
    fixture: valid?.skill.fixture ?? null, status: 'error',
    coverage: {
      scope: 'catalog-files-only', reviewedFiles: [], omittedFiles: valid?.omittedFiles ?? [],
      unreviewedFiles: valid?.files.map(file => file.path) ?? [],
    },
    findings: [], errors: [String(error.message ?? error).slice(0, 2048)],
  };
}

/**
 * Structural guard for a persisted report. Throws on invalid data; returns report.
 * For importing/publishing an artifact, pass its trusted collected manifest too:
 * this verifies all evidence, hashes and coverage, not just the JSON structure.
 * @param {unknown} report
 * @param {ReturnType<typeof collectSkill>} [manifest]
 * @returns {ReviewReport}
 */
export function validatePublishedReport(report, manifest) {
  keys(report, ['schemaVersion', 'skillId', 'revision', 'bundleHash', 'contentHash',
    'reviewedAt', 'model', 'rubricVersion', 'fixture', 'status', 'coverage', 'findings', 'errors'], 'report');
  requireThat(bytes(report) <= 2 * LIMITS.responseBytes, 'Report exceeds byte limit');
  requireThat(report.schemaVersion === SCHEMA_VERSION && report.rubricVersion === RUBRIC_VERSION,
    'Unsupported report version');
  requireThat(['complete-with-findings', 'complete-no-findings', 'incomplete', 'error'].includes(report.status),
    'Invalid report status');
  const isError = report.status === 'error';
  requireThat((isError && report.skillId === null) ||
    (typeof report.skillId === 'string' && ID.test(report.skillId) && report.skillId.length <= 128), 'Invalid report skillId');
  for (const key of ['bundleHash', 'contentHash']) {
    requireThat((isError && report[key] === null) || (typeof report[key] === 'string' && HASH.test(report[key])),
      `Invalid report ${key}`);
  }
  requireThat((isError && report.revision === null) ||
    (typeof report.revision === 'string' && REVISION.test(report.revision)), 'Invalid report revision');
  const identities = [report.skillId, report.revision, report.bundleHash, report.contentHash];
  requireThat(identities.every(value => value === null) || identities.every(value => value !== null),
    'Partial report identity');
  requireThat(report.fixture === null || (typeof report.fixture === 'string' &&
    ID.test(report.fixture) && report.fixture.length <= 128), 'Invalid report fixture');
  string(report.model, 128, 'report.model');
  requireThat(typeof report.reviewedAt === 'string' && !Number.isNaN(Date.parse(report.reviewedAt)) &&
    new Date(report.reviewedAt).toISOString() === report.reviewedAt, 'Invalid report reviewedAt');
  keys(report.coverage, ['scope', 'reviewedFiles', 'omittedFiles', 'unreviewedFiles'], 'report.coverage');
  requireThat(report.coverage.scope === 'catalog-files-only', 'Invalid report scope');
  const paths = new Set();
  for (const key of ['reviewedFiles', 'unreviewedFiles']) {
    requireThat(Array.isArray(report.coverage[key]) && report.coverage[key].length <= LIMITS.files,
      `Invalid report ${key}`);
    for (const file of report.coverage[key]) {
      requireThat(isSafeReviewPath(file) && !paths.has(file.toLowerCase()), 'Invalid report coverage path');
      paths.add(file.toLowerCase());
    }
  }
  requireThat(paths.size <= LIMITS.files, 'Too many report file paths');
  requireThat(Array.isArray(report.coverage.omittedFiles) && report.coverage.omittedFiles.length <= 4097,
    'Invalid report omissions');
  for (const omitted of report.coverage.omittedFiles) {
    keys(omitted, ['path', 'reason'], 'report omitted file');
    string(omitted.path, LIMITS.pathChars, 'report omitted path');
    requireThat(REASONS.has(omitted.reason) && !paths.has(omitted.path.toLowerCase()), 'Invalid report omission');
  }
  requireThat(Array.isArray(report.findings) && report.findings.length <= LIMITS.findings, 'Invalid report findings');
  const findings = new Set();
  for (const finding of report.findings) {
    keys(finding, ['category', 'severity', 'path', 'startLine', 'endLine', 'quote', 'explanation'], 'report finding');
    requireThat(CATEGORIES.includes(finding.category) && SEVERITIES.includes(finding.severity), 'Invalid report finding enum');
    requireThat(report.coverage.reviewedFiles.includes(finding.path), 'Report finding path was not reviewed');
    requireThat(Number.isSafeInteger(finding.startLine) && finding.startLine > 0 &&
      Number.isSafeInteger(finding.endLine) && finding.endLine >= finding.startLine &&
      finding.endLine <= LIMITS.fileBytes + 1, 'Invalid report finding lines');
    string(finding.quote, LIMITS.quoteChars, 'report finding quote');
    string(finding.explanation, LIMITS.explanationChars, 'report finding explanation');
    requireThat(finding.quote.trim().length > 0 && !findings.has(canonical(finding)), 'Invalid or duplicate report evidence');
    findings.add(canonical(finding));
  }
  requireThat(Array.isArray(report.errors) && report.errors.length <= 16, 'Invalid report errors');
  for (const error of report.errors) string(error, 2048, 'report error');
  requireThat(isError ? report.errors.length > 0 && report.findings.length === 0 &&
    report.coverage.reviewedFiles.length === 0 : report.errors.length === 0, 'Inconsistent report error status');
  if (report.status.startsWith('complete-')) {
    requireThat(report.coverage.reviewedFiles.length > 0 && report.coverage.omittedFiles.length === 0 &&
      report.coverage.unreviewedFiles.length === 0, 'Complete report contains coverage gaps');
    requireThat((report.status === 'complete-with-findings') === (report.findings.length > 0),
      'Complete report status disagrees with findings');
  }
  if (manifest !== undefined) {
    validateManifest(manifest);
    requireThat(report.skillId === manifest.skill.id && report.bundleHash === manifest.bundleHash &&
      report.contentHash === manifest.skill.contentHash && report.revision === manifest.revision &&
      report.fixture === manifest.skill.fixture, 'Report does not match trusted input');
    if (isError) {
      requireThat(canonical(report.coverage) === canonical(errorReport(new Error('error'), manifest).coverage),
        'Error report coverage does not match trusted input');
    } else {
      const validated = validateResponse(manifest, {
        bundleHash: report.bundleHash, status: report.status === 'incomplete' ? 'incomplete' : 'complete',
        reviewedFiles: report.coverage.reviewedFiles, findings: report.findings,
      }, { model: report.model, reviewedAt: report.reviewedAt });
      requireThat(canonical(validated) === canonical(report), 'Report coverage or findings do not match trusted input');
    }
  }
  return report;
}

function escapeMarkdown(value) {
  // Encode every nonalphanumeric ASCII character (and all non-ASCII), preventing
  // markdown, HTML, autolinks, mentions, controls, and bidi tricks in review text.
  return [...String(value)].map(char => /[a-zA-Z0-9 ]/.test(char) ? char :
    `&#${char.codePointAt(0)};`).join('');
}
/** @param {ReviewReport} report */
export function renderSummary(report) {
  let output = '# Skill review report\n\n';
  output += `Status: ${escapeMarkdown(report.status)}\n\n`;
  output += 'Report only. No safety certification. Scope: catalog files only; upstream files may be absent.\n\n';
  output += `Reviewed files: ${report.coverage.reviewedFiles.length}; omitted files: ${report.coverage.omittedFiles.length}; unreviewed files: ${report.coverage.unreviewedFiles.length}.\n\n`;
  const sections = [
    ...report.errors.map(error => `Error: ${escapeMarkdown(error)}\n\n`),
    ...report.coverage.omittedFiles.map(file => `Omitted: ${escapeMarkdown(file.path)} (${escapeMarkdown(file.reason)})\n\n`),
    ...report.coverage.unreviewedFiles.map(file => `Unreviewed: ${escapeMarkdown(file)}\n\n`),
    ...report.findings.map(finding =>
      `## ${escapeMarkdown(finding.severity)}: ${escapeMarkdown(finding.category)}\n\n` +
      `File: ${escapeMarkdown(finding.path)}; lines ${finding.startLine}-${finding.endLine}.\n\n` +
      `Evidence: ${escapeMarkdown(finding.quote)}\n\nExplanation: ${escapeMarkdown(finding.explanation)}\n\n`),
  ];
  const notice = 'Summary display limit reached. See the JSON artifact for the complete validated report.\n';
  for (const section of sections) {
    if (Buffer.byteLength(output + section + notice, 'utf8') > LIMITS.summaryBytes) return output + notice;
    output += section;
  }
  return output;
}

function readJson(file, limit, label) {
  const descriptor = fs.openSync(file, 'r');
  try {
    const stat = fs.fstatSync(descriptor);
    requireThat(stat.isFile() && stat.size <= limit, `${label} is not a regular file within its byte limit`);
    const buffer = Buffer.alloc(limit + 1);
    let length = 0;
    while (length < buffer.length) {
      const count = fs.readSync(descriptor, buffer, length, buffer.length - length, null);
      if (!count) break;
      length += count;
    }
    requireThat(length <= limit, `${label} exceeds its byte limit`);
    const content = new TextDecoder('utf-8', { fatal: true }).decode(buffer.subarray(0, length));
    try { return JSON.parse(content); } catch { throw new Error(`${label} is malformed JSON`); }
  } finally { fs.closeSync(descriptor); }
}
function fixtureData(caseId, root = ROOT) {
  requireThat(typeof caseId === 'string' && ID.test(caseId) && caseId.length <= 128, 'Invalid fixture id');
  return readJson(path.join(root, 'scripts', 'fixtures', 'skill-review', `${caseId}.json`),
    LIMITS.responseBytes, 'Fixture');
}
export function collectFromHead(skillId, { root = ROOT, fixture = null } = {}) {
  const data = fixture !== null ? fixtureData(fixture, root) : null;
  if (data && skillId === undefined) skillId = data.skill?.id;
  requireThat(typeof skillId === 'string' && ID.test(skillId) && skillId.length <= 128, 'Invalid skill id');
  const revision = execFileSync('git', ['rev-parse', '--verify', 'HEAD'], { cwd: root, encoding: 'utf8' }).trim();
  if (data) {
    requireThat(data.skill?.id === skillId, 'Fixture skill id does not match --skill');
    return collectSkill(data.skill, { revision, fixture });
  }
  // Fixed object path at the pinned revision, not a mutable worktree or user path.
  const catalog = JSON.parse(execFileSync('git', ['show', `${revision}:${CATALOG}`],
    { cwd: root, encoding: 'utf8', maxBuffer: 128 * 1024 * 1024 }));
  requireThat(Array.isArray(catalog.skills), 'Malformed canonical catalog');
  const matches = catalog.skills.filter(skill => skill.id === skillId);
  requireThat(matches.length === 1, 'Catalog skill id must identify exactly one skill');
  return collectSkill(matches[0], { revision });
}

export function evaluateFixture(fixture, report) {
  requireThat(object(fixture) && object(fixture.expected) && ['benign', 'malicious'].includes(fixture.expected.label),
    'Invalid fixture expected label');
  const checked = validatePublishedReport(report);
  const manifest = collectSkill(fixture.skill, { revision: checked.revision, fixture: fixture.caseId });
  validatePublishedReport(checked, manifest);
  const conclusive = checked.status.startsWith('complete-');
  const detected = checked.findings.length > 0;
  const malicious = fixture.expected.label === 'malicious';
  return {
    caseId: fixture.caseId, expected: fixture.expected.label, status: checked.status,
    conclusive, falsePositive: conclusive && !malicious && detected,
    falseNegative: conclusive && malicious && !detected,
    truePositive: conclusive && malicious && detected, trueNegative: conclusive && !malicious && !detected,
    abstention: !conclusive,
    limitation: 'Case-level detection comparison only; not a measure of safety or finding correctness.',
  };
}

function writeJson(output, value) {
  fs.mkdirSync(path.dirname(path.resolve(output)), { recursive: true });
  fs.writeFileSync(output, JSON.stringify(value, null, 2) + '\n', { encoding: 'utf8', flag: 'w' });
}
export function runCli(argv) {
  let output;
  let input;
  let canWriteError = true;
  try {
    const { values, positionals } = parseArgs({
      args: argv, allowPositionals: true, strict: true,
      options: Object.fromEntries(['skill', 'fixture', 'input', 'response', 'output', 'model', 'report']
        .map(key => [key, { type: 'string' }])),
    });
    output = values.output;
    requireThat(typeof output === 'string' && output.length > 0, '--output is required');
    requireThat(positionals.length === 1, 'Exactly one command is required');
    const command = positionals[0];
    const allowed = {
      collect: ['skill', 'fixture', 'output'], validate: ['input', 'response', 'output', 'model'],
      evaluate: ['fixture', 'report', 'output'],
    }[command];
    requireThat(allowed && Object.keys(values).every(key => allowed.includes(key)), 'Unknown command or unsupported option');
    for (const key of ['input', 'response', 'report']) {
      if (values[key] && (path.resolve(values[key]) === path.resolve(output) ||
        path.resolve(values[key]) === path.resolve(`${output}.summary.md`))) {
        canWriteError = false;
        throw new Error('Output must not overwrite an input');
      }
    }
    if (command === 'collect') {
      const collected = collectFromHead(values.skill, { fixture: values.fixture ?? null });
      fs.mkdirSync(path.dirname(path.resolve(output)), { recursive: true });
      fs.writeFileSync(output, JSON.stringify(collected) + '\n', 'utf8');
    } else if (command === 'validate') {
      requireThat(values.input && values.response, '--input and --response are required');
      input = readJson(values.input, LIMITS.inputBytes, 'Input');
      validateManifest(input);
      const report = validateResponse(input, readJson(values.response, LIMITS.responseBytes, 'Response'),
        { model: values.model ?? 'unspecified' });
      writeJson(output, report);
      fs.writeFileSync(`${output}.summary.md`, renderSummary(report), 'utf8');
    } else {
      requireThat(values.fixture && values.report, '--fixture and --report are required');
      writeJson(output, evaluateFixture(fixtureData(values.fixture),
        readJson(values.report, 2 * LIMITS.responseBytes, 'Report')));
    }
    return 0;
  } catch (error) {
    const report = errorReport(error, input);
    if (output && canWriteError) {
      try {
        writeJson(output, report);
        fs.writeFileSync(`${output}.summary.md`, renderSummary(report), 'utf8');
      } catch { process.stderr.write('Unable to write error report artifacts.\n'); }
    }
    process.stderr.write(`Skill review error: ${report.errors[0].replace(/[\r\n\u001b]/g, ' ')}\n`);
    return 1;
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = runCli(process.argv.slice(2));
}
