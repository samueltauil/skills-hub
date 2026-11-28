/**
 * @typedef {{ id: string, name: string, description: string, shortDescription?: string,
 * category?: string, author?: string, license?: string, tags?: string[],
 * complexity?: string, platforms?: string[],
 * source?: { repo: string, repoName?: string, branch?: string, path?: string } }} CatalogSkill
 * @typedef {Record<string, { name: string, description: string }>} CategoryMetadata
 */

/** @param {URL | undefined} site */
function siteUrl(site) {
  if (!site || !['https:', 'http:'].includes(site.protocol)) {
    throw new Error('SEO discovery requires an absolute HTTP(S) Astro.site URL.');
  }
  const base = new URL(site);
  base.search = '';
  base.hash = '';
  if (!base.pathname.endsWith('/')) base.pathname += '/';
  return base;
}

/** @param {string} value */
function xml(value) {
  return value.replace(/[&<>"']/g, char => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;',
  })[char]);
}

/** @param {string} value */
function markdown(value) {
  return value.replace(/\s+/g, ' ').trim()
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/[\\[\]*_`#]/g, '\\$&');
}

/** @param {string} name @param {string} url */
function link(name, url) {
  return `[${markdown(name)}](<${url}>)`;
}

/** @param {CatalogSkill[]} skills */
function categoryIds(skills) {
  // Match categories/[id].astro, including its fallback for uncategorized skills.
  return [...new Set(skills.map(skill => skill.category || 'general'))].sort();
}

/** @param {CatalogSkill[]} skills */
function sortedSkills(skills) {
  return [...skills].sort((a, b) => a.id < b.id ? -1 : a.id > b.id ? 1 : 0);
}

/** @param {URL | undefined} site @param {CatalogSkill[]} skills */
export function discoveryUrls(site, skills) {
  const base = siteUrl(site);
  const paths = [
    '', 'skills/', 'categories/', 'dashboard/',
    ...categoryIds(skills).map(id => `categories/${encodeURIComponent(id)}/`),
    ...sortedSkills(skills).map(skill => `skills/${encodeURIComponent(skill.id)}/`),
  ];
  return [...new Set(paths)].map(path => new URL(path, base).href);
}

/** @param {URL | undefined} site */
export function renderRobots(site) {
  return `User-agent: *\nAllow: /\n\nSitemap: ${new URL('sitemap.xml', siteUrl(site)).href}\n`;
}

/** @param {URL | undefined} site @param {CatalogSkill[]} skills */
export function renderSitemap(site, skills) {
  const entries = discoveryUrls(site, skills)
    .map(url => `  <url><loc>${xml(url)}</loc></url>`).join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries}\n</urlset>\n`;
}

/**
 * @param {URL | undefined} site
 * @param {CatalogSkill[]} skills
 * @param {CategoryMetadata} categories
 * @param {boolean} [full]
 */
export function renderLlms(site, skills, categories, full = false) {
  const base = siteUrl(site);
  const url = (/** @type {string} */ path) => new URL(path, base).href;
  const lines = [
    '# Skills Hub',
    '',
    '> A catalog of reusable skills for GitHub Copilot and AI coding agents.',
    '',
    `This catalog contains ${skills.length} skills in ${categoryIds(skills).length} categories.`,
    full
      ? 'Full catalog metadata follows. Skill instructions and bundled files are available on the linked skill pages and upstream sources.'
      : 'Browse skills by category or follow a skill link for instructions, bundled files, and upstream sources.',
    '',
    '## Site',
    '',
    `- ${link('Home', url(''))}`,
    `- ${link('All skills', url('skills/'))}`,
    `- ${link('All categories', url('categories/'))}`,
    `- ${link('Skills dashboard', url('dashboard/'))}`,
    `- ${link('Sitemap', url('sitemap.xml'))}`,
    `- ${link(full ? 'Catalog index for language models' : 'Full catalog metadata', url(full ? 'llms.txt' : 'llms-full.txt'))}`,
    '',
    '## Categories',
    '',
    ...categoryIds(skills).map(id => {
      const category = categories[id] || { name: id, description: `Skills in the ${id} category` };
      return `- ${link(category.name, url(`categories/${encodeURIComponent(id)}/`))}: ${markdown(category.description)}`;
    }),
    '',
    '## Skills',
    '',
  ];

  for (const skill of sortedSkills(skills)) {
    const skillLink = link(skill.name, url(`skills/${encodeURIComponent(skill.id)}/`));
    if (!full) {
      lines.push(`- ${skillLink}: ${markdown(skill.shortDescription || skill.description)}`);
      continue;
    }
    const categoryId = skill.category || 'general';
    lines.push(
      `### ${skillLink}`,
      '',
      markdown(skill.description),
      '',
      `- ID: ${markdown(skill.id)}`,
      `- Category: ${link(categories[categoryId]?.name || categoryId, url(`categories/${encodeURIComponent(categoryId)}/`))}`,
    );
    for (const [label, value] of [
      ['Author', skill.author], ['License', skill.license], ['Complexity', skill.complexity],
      ['Platforms', skill.platforms?.join(', ')], ['Tags', skill.tags?.join(', ')],
    ]) {
      if (value) lines.push(`- ${label}: ${markdown(value)}`);
    }
    if (skill.source?.repo) {
      const source = skill.source;
      const repo = new URL(source.repo);
      if (['http:', 'https:'].includes(repo.protocol)) {
        lines.push(`- Repository: ${link(source.repoName || source.repo, repo.href)}`);
        if (source.path) {
          const sourceUrl = new URL(repo);
          sourceUrl.pathname = `${sourceUrl.pathname.replace(/\/$/, '')}/tree/${encodeURIComponent(source.branch || 'main')}/${source.path.split('/').map(encodeURIComponent).join('/')}`;
          sourceUrl.search = '';
          sourceUrl.hash = '';
          lines.push(`- Source: ${link(source.path, sourceUrl.href)}`);
        }
      }
    }
    lines.push('');
  }
  return `${lines.join('\n').trimEnd()}\n`;
}
