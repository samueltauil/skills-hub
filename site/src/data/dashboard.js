import { getSecurityReview } from './security-reviews.js';

/**
 * @typedef {import('./security-reviews.js').ReviewSkill & {
 * category?: string, license?: string, complexity?: string
 * }} DashboardSkill
 */

/** @param {number} count @param {number} total */
export function percentage(count, total) {
  return total === 0 ? 0 : count / total * 100;
}

/**
 * Counts catalog entries, not upstream repository contents. Source groups match
 * the browse page's repoName filter; unknown metadata remains visible.
 * @param {DashboardSkill[]} skills
 * @param {Record<string, unknown>} [reports] Published JSON keyed by skill ID.
 */
export function aggregateDashboard(skills, reports = {}) {
  const groups = { categories: new Map(), sources: new Map(), licenses: new Map(), complexities: new Map() };
  const reviews = {
    'complete-no-findings': 0,
    'complete-with-findings': 0,
    incomplete: 0,
    stale: 0,
    error: 0,
    invalid: 0,
    'not-reviewed': 0,
  };
  let fileCount = 0;
  for (const skill of skills) {
    for (const [group, key] of [
      [groups.categories, skill.category || 'general'],
      [groups.sources, skill.source?.repoName || 'unknown'],
      [groups.licenses, skill.license || 'Not specified'],
      [groups.complexities, skill.complexity || 'Not specified'],
    ]) {
      group.set(key, (group.get(key) || 0) + 1);
    }
    fileCount += skill.files?.length || 0;
    const input = Object.hasOwn(reports, skill.id) ? reports[skill.id] : undefined;
    reviews[getSecurityReview(input, skill).status]++;
  }
  const distribution = (group) => [...group]
    .map(([id, count]) => ({ id, count, percentage: percentage(count, skills.length) }))
    .sort((a, b) => b.count - a.count || a.id.localeCompare(b.id, 'en'));
  const completeCount = reviews['complete-no-findings'] + reviews['complete-with-findings'];
  return {
    skillCount: skills.length,
    categoryCount: groups.categories.size,
    sourceCount: [...groups.sources.keys()].filter(id => id !== 'unknown').length,
    unknownSourceCount: groups.sources.get('unknown') || 0,
    fileCount,
    categories: distribution(groups.categories),
    sources: distribution(groups.sources),
    licenses: distribution(groups.licenses),
    complexities: distribution(groups.complexities),
    reviews,
    completeCount,
    completePercentage: percentage(completeCount, skills.length),
  };
}
