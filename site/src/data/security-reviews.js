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
      message: 'No published AI instruction review is available for this skill.',
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
        message: 'This skill has changed since the review. The findings below describe an older version.',
      };
    }
    validatePublishedReport(report, collectSkill(skill, { revision: report.revision }));
    const messages = {
      'complete-with-findings': 'The reviewer reported concerns for human assessment, with evidence below.',
      'complete-no-findings': 'No concerns were reported in the reviewed catalog files. This is not a safety guarantee.',
      incomplete: 'The review did not cover the entire catalog bundle. Check the coverage gaps below.',
      error: 'The review could not be completed. This is not a clean result.',
    };
    return { status: report.status, report, message: messages[report.status] };
  } catch (error) {
    console.warn(`[security-review] ${skill.id}: ${error instanceof Error ? error.message : String(error)}`);
    return {
      status: 'invalid',
      report: null,
      message: 'The published review could not be validated and is not displayed.',
    };
  }
}
