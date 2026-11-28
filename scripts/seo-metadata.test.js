import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {
  canonicalUrl,
  createMetadata,
  DEFAULT_DESCRIPTION,
  metadataDescription,
  serializeJsonLd,
} from '../site/src/data/seo.js';

const site = new URL('https://skillshub.space');

test('canonicals use the configured origin, strip query/hash, and normalize trailing slashes', () => {
  const cases = [
    ['http://localhost:4321/', 'https://skillshub.space/'],
    ['http://localhost:4321/skills?q=testing#results', 'https://skillshub.space/skills/'],
    ['/categories/testing///?sort=count', 'https://skillshub.space/categories/testing/'],
    ['/skills/a%20b/?q=x', 'https://skillshub.space/skills/a%20b/'],
    ['//untrusted.example/skills/example', 'https://skillshub.space/skills/example/'],
  ];
  for (const [input, expected] of cases) assert.equal(canonicalUrl(site, input), expected);
  assert.equal(
    canonicalUrl(new URL('https://preview.example/catalog/'), '/catalog/skills/?q=x'),
    'https://preview.example/catalog/skills/',
  );
  assert.throws(() => canonicalUrl(undefined, '/skills/'), /site must be configured/);
});

test('descriptions are compact plain text with a meaningful fallback', () => {
  assert.equal(metadataDescription('  Browse\n skills\tby category. '), 'Browse skills by category.');
  assert.equal(metadataDescription('  \n '), DEFAULT_DESCRIPTION);
  const longDescription = 'Read source files and install skills. '.repeat(12);
  const description = metadataDescription(longDescription);
  assert(description.length <= 200);
  assert(description.endsWith('…'));
  assert(longDescription.startsWith(description.slice(0, -1)));
});

test('collection metadata connects the canonical page, website and visible breadcrumb trail', () => {
  const metadata = createMetadata({
    site,
    pageUrl: 'http://localhost:4321/categories/testing/?q=ignored',
    title: 'Testing Skills',
    description: 'Skills for writing and managing tests.',
    pageType: 'CollectionPage',
    breadcrumbs: [
      { name: 'Home', path: '/' },
      { name: 'Categories', path: '/categories/' },
      { name: 'Testing', path: '/categories/testing/' },
    ],
  });
  assert.equal(metadata.canonical, 'https://skillshub.space/categories/testing/');
  assert.equal(metadata.image, 'https://skillshub.space/images/social-preview.png');
  const [website, page, breadcrumb] = metadata.jsonLd['@graph'];
  assert.equal(website['@type'], 'WebSite');
  assert.equal(page['@type'], 'CollectionPage');
  assert.equal(page.isPartOf['@id'], website['@id']);
  assert.equal(page.breadcrumb['@id'], breadcrumb['@id']);
  assert.equal(page.name, metadata.title);
  assert.equal(page.description, metadata.description);
  assert.equal(page.url, metadata.canonical);
  assert.deepEqual(breadcrumb.itemListElement.map(item => [item.position, item.name, item.item]), [
    [1, 'Home', 'https://skillshub.space/'],
    [2, 'Categories', 'https://skillshub.space/categories/'],
    [3, 'Testing', metadata.canonical],
  ]);
});

test('skill schema describes the actual instruction bundle without invented rich-result claims', () => {
  const skill = {
    name: 'Example Skill',
    description: 'Instructions for testing an example application.',
    sourceUrl: 'https://github.com/example/skills/tree/main/example',
  };
  const metadata = createMetadata({ site, pageUrl: '/skills/example/', title: skill.name, description: skill.description, skill });
  const [, page, work] = metadata.jsonLd['@graph'];
  assert.equal(work['@type'], 'CreativeWork');
  assert.equal(work.name, skill.name);
  assert.equal(work.description, skill.description);
  assert.equal(work.isBasedOn, skill.sourceUrl);
  assert.equal(work.url, metadata.canonical);
  assert.equal(work.mainEntityOfPage['@id'], page['@id']);
  assert.equal(page.mainEntity['@id'], work['@id']);
  for (const unsupported of ['aggregateRating', 'review', 'offers', 'SearchAction', 'datePublished', 'dateModified']) {
    assert(!JSON.stringify(metadata.jsonLd).includes(`"${unsupported}"`));
  }
  const withoutSource = createMetadata({
    site, pageUrl: '/skills/example/', title: skill.name, skill: { ...skill, sourceUrl: 'javascript:alert(1)' },
  });
  assert(!('isBasedOn' in withoutSource.jsonLd['@graph'][2]));
});

test('site and preview URLs honor alternative origins and deployment base paths', () => {
  const metadata = createMetadata({
    site: new URL('https://preview.example'),
    baseUrl: '/catalog/',
    pageUrl: 'http://localhost:4321/catalog/',
    title: 'Agent Skills',
  });
  assert.equal(metadata.canonical, 'https://preview.example/catalog/');
  assert.equal(metadata.image, 'https://preview.example/catalog/images/social-preview.png');
  assert.equal(metadata.jsonLd['@graph'][0].url, metadata.canonical);
  assert.equal(metadata.jsonLd['@graph'][1]['@type'], 'WebPage');
  assert.equal(metadata.jsonLd['@graph'].length, 2);
});

test('JSON-LD cannot terminate its script element and preserves original catalog text', () => {
  const malicious = '</script><script>alert("x")</script><!-- & >\u2028\u2029';
  const metadata = createMetadata({
    site, pageUrl: '/skills/example/', title: malicious, description: malicious,
    skill: { name: malicious, description: malicious },
  });
  const serialized = serializeJsonLd(metadata.jsonLd);
  assert(!/[<>&\u2028\u2029]/.test(serialized));
  assert.deepEqual(JSON.parse(serialized), metadata.jsonLd);
});

test('social preview is a real 1200 by 630 PNG rather than an SVG renamed for crawlers', () => {
  const image = fs.readFileSync(new URL('../site/public/images/social-preview.png', import.meta.url));
  assert.deepEqual(image.subarray(0, 8), Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]));
  assert.equal(image.toString('ascii', 12, 16), 'IHDR');
  assert.equal(image.readUInt32BE(16), 1200);
  assert.equal(image.readUInt32BE(20), 630);
});
