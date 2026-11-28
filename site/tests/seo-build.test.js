import assert from 'node:assert/strict';
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join, relative, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import config from '../astro.config.mjs';

const dist = fileURLToPath(new URL('../dist/', import.meta.url));
const origin = new URL(config.site);

function findPages(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = join(directory, entry.name);
    return entry.isDirectory() ? findPages(path) : entry.name.endsWith('.html') ? [path] : [];
  });
}

const pages = findPages(dist).map((path) => ({
  path,
  url: new URL(relative(dist, path).split(sep).join('/').replace(/index\.html$/, ''), origin).href,
  html: readFileSync(path, 'utf8'),
}));

function attributes(tag) {
  return Object.fromEntries(
    [...tag.matchAll(/([\w:-]+)="([^"]*)"/g)].map(([, name, value]) => [name, value]),
  );
}

function metadata(html) {
  return Object.fromEntries(
    [...html.matchAll(/<meta\b(?:[^"'>]|"[^"]*"|'[^']*')*>/g)]
      .map(([tag]) => attributes(tag))
      .filter((attrs) => attrs.property || attrs.name)
      .map((attrs) => [attrs.property || attrs.name, attrs.content]),
  );
}

test('the sitemap lists every generated HTML page exactly once', () => {
  const sitemap = readFileSync(join(dist, 'sitemap.xml'), 'utf8');
  assert.match(sitemap, /xmlns="http:\/\/www\.sitemaps\.org\/schemas\/sitemap\/0\.9"/);
  const locations = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/gs)].map(([, url]) =>
    url.replaceAll('&amp;', '&').replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&quot;', '"').replaceAll('&apos;', "'"),
  );
  assert.ok(pages.length > 0);
  assert.equal(locations.length, new Set(locations).size, 'duplicate sitemap URLs');
  assert.deepEqual(locations.sort(), pages.map(({ url }) => url).sort());
});

test('all pages have consistent canonical and share metadata', () => {
  for (const { url, html } of pages) {
    const canonical = [...html.matchAll(/<link\b[^>]*>/g)]
      .map(([tag]) => attributes(tag))
      .filter((attrs) => attrs.rel === 'canonical');
    assert.equal(canonical.length, 1, url);
    assert.equal(canonical[0].href, url);
    const meta = metadata(html);
    assert.ok(meta.description?.trim(), `${url}: missing description`);
    assert.ok(meta['og:title']?.trim(), `${url}: missing Open Graph title`);
    assert.equal(meta['og:url'], url);
    assert.equal(meta['og:description'], meta.description);
    assert.ok(meta['twitter:card'], `${url}: missing Twitter card`);
    assert.ok(meta['twitter:title']?.trim(), `${url}: missing Twitter title`);
    const image = new URL(meta['og:image']);
    assert.equal(image.origin, origin.origin);
    assert.match(image.pathname, /\.(png|jpe?g|webp)$/);
    assert.ok(existsSync(join(dist, ...image.pathname.split('/').filter(Boolean))), image.href);
    for (const [, json] of html.matchAll(/<script\b[^>]*type="application\/ld\+json"[^>]*>(.*?)<\/script>/gs)) {
      assert.doesNotThrow(() => JSON.parse(json), `${url}: invalid JSON-LD`);
    }
  }
  assert.match(pages.find(({ url }) => url === origin.href).html, /type="application\/ld\+json"/);
});

test('crawler and LLM discovery files are available at the public root', () => {
  const robots = readFileSync(join(dist, 'robots.txt'), 'utf8');
  assert.match(robots, /^User-agent:\s*\*/m);
  assert.ok(robots.includes(`Sitemap: ${new URL('sitemap.xml', origin).href}`));
  assert.doesNotMatch(robots, /^Disallow:\s*\/\s*$/m);
  for (const name of ['llms.txt', 'llms-full.txt']) {
    const text = readFileSync(join(dist, name), 'utf8');
    assert.match(text, /^# /);
    assert.ok(text.includes(new URL('skills/', origin).href), `${name}: missing catalog URL`);
    assert.doesNotMatch(text, /\]\(<?https?:\/\/(?:localhost|127\.0\.0\.1)(?::\d+)?[/>]/, `${name}: contains development links`);
  }
});

test('analytics and verification match the build configuration', () => {
  const measurementId = process.env.PUBLIC_GA_MEASUREMENT_ID?.trim();
  for (const { url, html } of pages) {
    if (measurementId) {
      const tags = [...html.matchAll(/<script\b[^>]*src="https:\/\/www\.googletagmanager\.com\/gtag\/js\?id=([^"]+)"[^>]*>/g)];
      assert.equal(tags.length, 1, `${url}: expected one analytics loader`);
      assert.equal(tags[0][1], measurementId);
      assert.ok(html.includes(`gtag('config', "${measurementId}"`), `${url}: missing analytics configuration`);
    } else {
      assert.doesNotMatch(html, /https:\/\/www\.googletagmanager\.com\/gtag\/js/, url);
    }
    const meta = metadata(html);
    for (const [variable, name] of [
      ['PUBLIC_GOOGLE_SITE_VERIFICATION', 'google-site-verification'],
      ['PUBLIC_BING_SITE_VERIFICATION', 'msvalidate.01'],
    ]) {
      assert.equal(meta[name], process.env[variable]?.trim() || undefined, `${url}: ${name}`);
    }
  }
});
