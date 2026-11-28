export const SITE_NAME = 'Copilot Skills Hub';
export const DEFAULT_DESCRIPTION = 'Discover curated Agent Skills for GitHub Copilot. Browse by category, explore source files, and install skills as Agent Plugins.';

/** Resolve page URLs against the configured deployment origin, never the request host. */
export function canonicalUrl(site, pageUrl) {
  if (!site) throw new Error('Astro site must be configured to generate canonical URLs.');
  const origin = new URL(site).origin;
  const url = new URL(origin);
  const pathname = new URL(pageUrl, `${origin}/`).pathname;
  url.pathname = `${pathname.replace(/\/+$/, '')}/`;
  return url.href;
}

export function metadataDescription(description) {
  const text = String(description || '').replace(/\s+/g, ' ').trim() || DEFAULT_DESCRIPTION;
  if (text.length <= 200) return text;
  const excerpt = text.slice(0, 197).replace(/\s+\S*$/, '').trimEnd();
  return `${excerpt}…`;
}

export function serializeJsonLd(value) {
  // JSON in a script element is raw HTML text; neutralize closing tags and separators.
  return JSON.stringify(value).replace(/[<>&\u2028\u2029]/g, character => ({
    '<': '\\u003c',
    '>': '\\u003e',
    '&': '\\u0026',
    '\u2028': '\\u2028',
    '\u2029': '\\u2029',
  })[character]);
}

export function createMetadata({
  site,
  pageUrl,
  baseUrl = '/',
  title,
  description,
  pageType = 'WebPage',
  breadcrumbs = [],
  skill,
}) {
  const canonical = canonicalUrl(site, pageUrl);
  const home = canonicalUrl(site, baseUrl);
  const fullTitle = `${title} | ${SITE_NAME}`;
  const summary = metadataDescription(description);
  const image = new URL('images/social-preview.png', home).href;
  const website = {
    '@type': 'WebSite',
    '@id': `${home}#website`,
    url: home,
    name: SITE_NAME,
    description: DEFAULT_DESCRIPTION,
    inLanguage: 'en',
  };
  const page = {
    '@type': pageType,
    '@id': `${canonical}#webpage`,
    url: canonical,
    name: fullTitle,
    description: summary,
    inLanguage: 'en',
    isPartOf: { '@id': website['@id'] },
  };
  const graph = [website, page];

  if (breadcrumbs.length) {
    const breadcrumb = {
      '@type': 'BreadcrumbList',
      '@id': `${canonical}#breadcrumb`,
      itemListElement: breadcrumbs.map((item, index) => ({
        '@type': 'ListItem',
        position: index + 1,
        name: item.name,
        item: canonicalUrl(site, item.path),
      })),
    };
    page.breadcrumb = { '@id': breadcrumb['@id'] };
    graph.push(breadcrumb);
  }

  if (skill) {
    const work = {
      '@type': 'CreativeWork',
      '@id': `${canonical}#skill`,
      name: skill.name,
      description: skill.description,
      url: canonical,
      mainEntityOfPage: { '@id': page['@id'] },
    };
    if (skill.sourceUrl && /^https?:\/\//i.test(skill.sourceUrl)) {
      work.isBasedOn = skill.sourceUrl;
    }
    page.mainEntity = { '@id': work['@id'] };
    graph.push(work);
  }

  return {
    canonical,
    title: fullTitle,
    description: summary,
    image,
    jsonLd: { '@context': 'https://schema.org', '@graph': graph },
  };
}
