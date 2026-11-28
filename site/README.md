# Skills Hub website

Static Astro site published at **https://skillshub.space** by `.github/workflows/deploy.yml`.
The production origin is configured in `astro.config.mjs`. Keep it aligned with the
GitHub Pages custom domain when moving the site.

## Development and validation

Run from the repository root (Node.js 20 or newer):

```sh
npm ci --prefix site
npm run dev --prefix site
npm run build --prefix site
npm run preview --prefix site
npm --prefix site test
node --test scripts/seo-analytics.test.js
npm test
```

The site build uses the catalog already present in `src/data/`. The root
`npm run build` additionally aggregates, scans, and validates catalog/plugin data;
it is not required for website-only changes. The output is `site/dist/`.
`npm --prefix site test` builds the site and checks the generated SEO artifacts;
deployment runs this same command before uploading the site. The root `npm test`
runs the repository's Node.js test suite, including focused analytics tests.

## Optional traffic measurement

Traffic measurement is **off by default**: an unset or blank measurement ID renders
no Google scripts and makes no analytics requests. To opt in, create a GA4 property
and web data stream for `https://skillshub.space`, then copy its actual measurement
ID. No account or ID is created by this repository.

| Build-time variable | Value |
| --- | --- |
| `PUBLIC_GA_MEASUREMENT_ID` | Your GA4 measurement ID: `G-` followed by 10 uppercase letters/digits |
| `PUBLIC_GOOGLE_SITE_VERIFICATION` | Only the `content` token of Google's verification meta tag |
| `PUBLIC_BING_SITE_VERIFICATION` | Only the 32-character hexadecimal `content` token of Bing's verification meta tag |

For local configuration, copy `site/.env.example` to `site/.env`, fill only the
values you need, and restart/rebuild Astro. Do not commit `.env`. For production,
set **repository variables** under **Settings → Secrets and variables → Actions →
Variables** with the exact names above. The deploy workflow passes them to the
Astro build, not the deploy job. These are public identifiers embedded in generated
HTML, not secrets. Invalid nonblank values fail the build with the variable name.
Verification is independent of analytics and never enables tracking.

After changing or removing variables, run **Deploy to GitHub Pages** via
`workflow_dispatch` (or push to `main`). GitHub Pages serves static files: changing
a variable alone does not change the deployed site. Clear the measurement variable
and redeploy to disable tracking.

`src/components/Analytics.astro` belongs once in the shared layout's `<head>`.
It loads Google's tag only when configured and requests the standard pageview on
each full page load. It adds no click, copy, search, or other custom events and no
user IDs. Page locations and referrers omit queries/fragments. To preserve campaign
acquisition attribution, the tag reads only `utm_source`, `utm_medium`,
`utm_campaign`, `utm_id`, `utm_term`, and `utm_content` from the visitor's current
URL and passes nonempty values as GA4's standard `campaign_source`,
`campaign_medium`, `campaign_name`, `campaign_id`, `campaign_term`, and
`campaign_content` parameters. Other query parameters and fragments are not
included in this configuration. Never put personal or sensitive data in campaign
tags; use campaign labels intended for analytics.
Google signals and ad-personalization signals are disabled.
In the GA4 web stream settings, **disable
Enhanced measurement** to avoid Google's optional automatic click, scroll, search,
download, video, or history-based events. GA4 may still collect its standard
session/engagement and device data; this is not anonymous or cookieless analytics.

This is a **site-owner opt-in**, not a visitor consent manager. Before enabling,
review applicable privacy/consent requirements, configure retention and internal
traffic filters, and publish the appropriate notice. If prior visitor consent is
required, leave it disabled until a consent solution gates loading the tag.
Do not use real production IDs for routine local tests.

After deployment, inspect page source for the configured tag and use GA4 Realtime
or Tag Assistant to confirm pageviews. An actual account and unblocked browser are
required; blockers and consent choices mean analytics is not a complete visitor count.
Use GA4 acquisition reports for measured visits/referrals and Search Console/Bing
reports for search impressions/clicks; these measure different things.

## Search verification and discovery

1. Add `https://skillshub.space/` as a URL-prefix property in
   [Google Search Console](https://search.google.com/search-console). Choose HTML
   tag verification, set `PUBLIC_GOOGLE_SITE_VERIFICATION` to its content token,
   rebuild/deploy, inspect the homepage `<head>`, then verify. A Google **Domain**
   property instead requires DNS verification and does not use this meta tag.
2. Add the site in [Bing Webmaster Tools](https://www.bing.com/webmasters/).
   Choose meta-tag verification and set `PUBLIC_BING_SITE_VERIFICATION`, or import
   the verified Search Console property. Deploy before clicking Verify. Keep
   verification tokens deployed while ownership verification is needed.
3. In both services, submit **https://skillshub.space/sitemap.xml**. Check sitemap
   processing and indexing reports after deployment. Google's URL Inspection and
   Bing's URL Inspection can diagnose representative homepage, category, and skill
   URLs; sitemap submission requests discovery but does not guarantee indexing.
4. Check `/robots.txt`, canonical URLs, sitemap URLs, titles/descriptions, and social
   preview metadata whenever the domain or routing changes. Crawl permission does
   not imply indexing, ranking, or crawler compliance.

`/llms.txt` and `/llms-full.txt` provide machine-readable catalog context.
**llms.txt is an emerging convention**, not a universally supported standard,
crawler authorization mechanism, SEO ranking signal, or traffic guarantee.
Measure actual referrals rather than assuming AI systems read or cite these files.
