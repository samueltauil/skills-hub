import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { discoveryUrls, renderLlms, renderRobots, renderSitemap } from '../site/src/data/seo-discovery.js';

const site = new URL('https://catalog.example/');
const skills = [
  {
    id: 'zeta', name: 'Zeta', description: 'Full Zeta description.', shortDescription: 'Short Zeta.',
    category: 'testing', author: 'Example', license: 'MIT', complexity: 'advanced',
    platforms: ['linux'], tags: ['test'],
    source: { repo: 'https://github.com/example/skills', repoName: 'example/skills', branch: 'release/v1', path: 'skills/zeta' },
  },
  { id: 'alpha', name: 'Alpha', description: 'Alpha description.', category: '' },
];
const categories = {
  testing: { name: 'Testing', description: 'Testing skills.' },
  unused: { name: 'Unused', description: 'Must not be published.' },
};

test('discovery follows real page routes and category fallback without mutating the catalog', () => {
  assert.deepEqual(discoveryUrls(site, skills), [
    'https://catalog.example/',
    'https://catalog.example/skills/',
    'https://catalog.example/categories/',
    'https://catalog.example/categories/general/',
    'https://catalog.example/categories/testing/',
    'https://catalog.example/skills/alpha/',
    'https://catalog.example/skills/zeta/',
  ]);
  assert.equal(skills[0].id, 'zeta');
  assert.deepEqual(discoveryUrls(site, []), [
    'https://catalog.example/', 'https://catalog.example/skills/', 'https://catalog.example/categories/',
  ]);
});

test('robots and sitemap honor Astro.site and omit unsupported freshness or ratings', () => {
  const configuredSite = new URL('https://preview.example/catalog');
  assert.equal(renderRobots(configuredSite), 'User-agent: *\nAllow: /\n\nSitemap: https://preview.example/catalog/sitemap.xml\n');
  const sitemap = renderSitemap(configuredSite, skills);
  assert.match(sitemap, /^<\?xml version="1.0" encoding="UTF-8"\?>/);
  assert.match(sitemap, /xmlns="http:\/\/www.sitemaps.org\/schemas\/sitemap\/0.9"/);
  assert.equal((sitemap.match(/<loc>/g) || []).length, 7);
  assert.ok(sitemap.includes('<loc>https://preview.example/catalog/skills/zeta/</loc>'));
  assert.doesNotMatch(sitemap, /lastmod|changefreq|priority|rating|skillshub\.space/);
  assert.throws(() => renderRobots(undefined), /Astro.site/);
});

test('sitemap encodes route segments and escapes XML', () => {
  const special = [{ id: "a&b'<x>", name: 'Special', category: 'a/b' }];
  const sitemap = renderSitemap(site, special);
  assert.ok(sitemap.includes('/skills/a%26b&apos;%3Cx%3E/'));
  assert.ok(sitemap.includes('/categories/a%2Fb/'));
  assert.equal((renderSitemap(site, [...skills, skills[0]]).match(/<loc>/g) || []).length, 7);
});

test('LLM index and full catalog use real descriptions, categories and upstream metadata', () => {
  const index = renderLlms(site, skills, categories);
  const full = renderLlms(site, skills, categories, true);
  assert.ok(index.includes('2 skills in 2 categories'));
  assert.ok(index.includes('[Zeta](<https://catalog.example/skills/zeta/>): Short Zeta.'));
  assert.ok(index.includes('[general](<https://catalog.example/categories/general/>)'));
  assert.ok(index.includes('https://catalog.example/llms-full.txt'));
  assert.doesNotMatch(index, /Unused|Full Zeta description/);
  assert.ok(full.includes('Full Zeta description.'));
  assert.ok(full.includes('- Author: Example\n- License: MIT\n- Complexity: advanced\n- Platforms: linux\n- Tags: test'));
  assert.ok(full.includes('https://github.com/example/skills/tree/release%2Fv1/skills/zeta'));
  assert.ok(full.includes('https://catalog.example/llms.txt'));
  assert.doesNotMatch(full, /rating|lastmod|Short Zeta/);
});

test('LLM Markdown keeps catalog text from creating links or markup', () => {
  const output = renderLlms(site, [{
    id: 'example', name: '[Example](bad)', description: '<script>\n*unexpected* & text',
  }], {});
  assert.ok(output.includes('\\[Example\\](bad)'));
  assert.ok(output.includes('&lt;script&gt; \\*unexpected\\* &amp; text'));
  assert.doesNotMatch(output, /<script>/);
});

test('every canonical catalog skill and used category is discoverable', () => {
  const catalog = JSON.parse(fs.readFileSync(new URL('../site/src/data/skills.json', import.meta.url), 'utf8'));
  const urls = discoveryUrls(site, catalog.skills);
  const usedCategories = new Set(catalog.skills.map(skill => skill.category || 'general'));
  assert.equal(urls.length, 3 + usedCategories.size + catalog.skills.length);
  const index = renderLlms(site, catalog.skills, {});
  const full = renderLlms(site, catalog.skills, {}, true);
  for (const skill of catalog.skills) {
    const url = new URL(`skills/${encodeURIComponent(skill.id)}/`, site).href;
    assert.ok(urls.includes(url), skill.id);
    assert.ok(index.includes(`<${url}>`), skill.id);
    assert.ok(full.includes(`<${url}>`), skill.id);
  }
});

