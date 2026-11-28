import { collectSkill, computeBundleHash, validatePublishedReport } from '../../../scripts/skill-review.js';

/**
 * @typedef {import('../../../scripts/skill-review.js').ReviewReport} ReviewReport
 * @typedef {{ id: string, name: string, source?: Record<string, string>, files: { path: string, content: string }[] }} ReviewSkill
 * @typedef {{ status: 'not-reviewed' | 'invalid' | 'stale' | ReviewReport['status'], report: ReviewReport | null, message: string }} ReviewState
 */

/**
 * @param {unknown} input
 * @param {ReviewSkill} skill
 * @returns {ReviewState}
 */
export function getSecurityReview(input, skill) {
  if (input === undefined) {
    return {
      status: 'not-reviewed',
      report: null,
      message: 'No published AI review is available. Inspect the skill files yourself before installing.',
    };
  }

  try {
    const report = validatePublishedReport(input);
    if (report.skillId !== skill.id || report.fixture !== null || !report.revision) {
      throw new Error('Report identity does not match this catalog skill');
    }
    if (report.contentHash !== computeBundleHash(skill)) {
      return {
        status: 'stale',
        report,
        message: 'This skill has changed since the review. Review the current files before installing; any findings below describe an older version.',
      };
    }
    validatePublishedReport(report, collectSkill(skill, { revision: report.revision }));
    const messages = {
      'complete-with-findings': 'Assess the concerns below before installing this skill.',
      'complete-no-findings': 'No concerns were reported in the reviewed catalog files. This is not a safety guarantee.',
      incomplete: 'The reviewer did not complete the review. Check the review details and any coverage gaps before installing.',
      error: 'The review failed. Inspect the skill files yourself; no safety conclusion is available.',
    };
    return { status: report.status, report, message: messages[report.status] };
  } catch (error) {
    console.warn(`[security-review] ${skill.id}: ${error instanceof Error ? error.message : String(error)}`);
    return {
      status: 'invalid',
      report: null,
      message: 'The published review could not be validated. Inspect the skill files yourself before installing.',
    };
  }
}

/**
 * Presentation is derived only from validated review state, never legacy scan flags.
 * @param {ReviewState} review
 */
export function summarizeSecurityReview(review) {
  const labels = {
    'not-reviewed': 'Not reviewed',
    invalid: 'Report unavailable',
    stale: 'Out of date',
    'complete-with-findings': 'Findings to assess',
    'complete-no-findings': 'No findings observed',
    incomplete: 'Incomplete review',
    error: 'Review failed',
  };
  const coverage = review.report?.coverage;
  const reviewed = coverage?.reviewedFiles.length ?? 0;
  const missing = (coverage?.omittedFiles.length ?? 0) + (coverage?.unreviewedFiles.length ?? 0);
  return {
    label: labels[review.status],
    coverage: coverage ? `${reviewed} of ${reviewed + missing} catalog files reviewed` : 'Coverage unavailable',
    gaps: missing,
  };
}
