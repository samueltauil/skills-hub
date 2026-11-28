import test from 'node:test';
import assert from 'node:assert/strict';
import { readdirSync, readFileSync } from 'node:fs';
import { aggregateDashboard } from '../src/data/dashboard.js';
import config from '../astro.config.mjs';

const read = path => readFileSync(new URL(path, import.meta.url), 'utf8');
const skills = JSON.parse(read('../src/data/skills.json')).skills;
const reports = Object.fromEntries(
  readdirSync(new URL('../src/data/security-reviews/', import.meta.url))
    .filter(name => name.endsWith('.json'))
    .map(name => [name.slice(0, -5), JSON.parse(read(`../src/data/security-reviews/${name}`))]),
);
const data = aggregateDashboard(skills, reports);
const html = read('../dist/dashboard/index.html');
const base = config.base || '/';
const number = new Intl.NumberFormat('en-US');
const percent = new Intl.NumberFormat('en-US', { maximumFractionDigits: 1 });

test('generated dashboard reflects canonical catalog totals and all validated review buckets', () => {
  for (const [metric, count] of [
    ['skills', data.skillCount], ['categories', data.categoryCount], ['sources', data.sourceCount],
    ['files', data.fileCount], ['complete-reviews', data.completeCount],
  ]) {
    assert.ok(html.includes(`data-metric="${metric}" data-count="${count}"`), metric);
  }
  for (const [status, count] of Object.entries(data.reviews)) {
    assert.ok(html.includes(`data-review-status="${status}" data-count="${count}"`), status);
    const row = html.match(new RegExp(`<li data-review-status="${status}"[^>]*>(.*?)</li>`, 's'))?.[1];
    assert.ok(row, status);
    assert.ok(row.includes(`${number.format(count)} <span`), `${status}: visible count`);
    assert.ok(row.includes(`· ${percent.format(data.skillCount ? count / data.skillCount * 100 : 0)}%`), `${status}: visible percentage`);
  }
  assert.ok(html.includes(`${number.format(data.completeCount)} of ${number.format(data.skillCount)} skills`));
  assert.match(html, /not security certifications/);
  assert.match(html, /not live activity/);
  assert.doesNotMatch(html, /NaN|Infinity|securityScan|badge-scanned/);
  assert.match(html, /<section[^>]+aria-labelledby="review-heading"/);
  assert.match(html, /class="coverage-bar" aria-hidden="true"/);
});

test('every distribution has accurate counts and working category or source drilldowns', () => {
  for (const row of data.categories) {
    assert.ok(html.includes(`data-category="${row.id}" data-count="${row.count}"`), row.id);
    assert.ok(html.includes(`href="${base}categories/${encodeURIComponent(row.id)}/"`), row.id);
  }
  for (const row of data.sources) {
    assert.ok(html.includes(`data-distribution-id="${row.id}" data-count="${row.count}"`), row.id);
    assert.ok(html.includes(`href="${base}skills/?${new URLSearchParams({ source: row.id })}"`), row.id);
  }
  assert.equal((html.match(/data-category-logo=/g) || []).length, data.categories.length);
  if (data.sources.length > 8) assert.match(html, /<details[^>]*class="more-sources/);
});

test('dashboard is linked in shared navigation and SEO discovery with its own metadata', () => {
  const canonical = new URL('dashboard/', config.site).href;
  assert.ok(html.includes(`<link rel="canonical" href="${canonical}"`));
  assert.match(html, /<title>Skills Dashboard/);
  assert.match(html, /"@type":"CollectionPage"/);
  assert.ok(html.includes(`href="${base}dashboard/" aria-current="page"`));
  for (const page of ['index.html', 'skills/index.html', 'categories/index.html']) {
    assert.ok(read(`../dist/${page}`).includes(`href="${base}dashboard/"`), page);
  }
  assert.ok(read('../dist/sitemap.xml').includes(`<loc>${canonical}</loc>`));
  for (const path of ['llms.txt', 'llms-full.txt']) {
    assert.ok(read(`../dist/${path}`).includes(`[Skills dashboard](<${canonical}>)`), path);
  }
});
