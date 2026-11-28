function optionalValue(env, name, pattern, expected) {
  const value = env[name]?.trim() || '';
  if (value && !pattern.test(value)) {
    throw new Error(`${name} must be ${expected}, or unset to disable it.`);
  }
  return value;
}

export function getAnalyticsConfig(env = {}) {
  return {
    measurementId: optionalValue(env, 'PUBLIC_GA_MEASUREMENT_ID', /^G-[A-Z0-9]{10}$/, 'a GA4 measurement ID (G- followed by 10 uppercase letters or digits)'),
    googleVerification: optionalValue(env, 'PUBLIC_GOOGLE_SITE_VERIFICATION', /^[A-Za-z0-9_-]+={0,2}$/, 'the Google verification content token, not an HTML tag'),
    bingVerification: optionalValue(env, 'PUBLIC_BING_SITE_VERIFICATION', /^[A-Fa-f0-9]{32}$/, 'the 32-character hexadecimal Bing verification content token, not an HTML tag'),
  };
}

export function getAnalyticsScript(measurementId, pageUrl) {
  const config = getAnalyticsConfig({ PUBLIC_GA_MEASUREMENT_ID: measurementId });
  if (!config.measurementId) return '';

  const location = new URL(pageUrl);
  location.search = '';
  location.hash = '';
  // Inline script data must not be able to close its containing HTML element.
  const literal = value => JSON.stringify(value).replace(/</g, '\\u003c');
  return `
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
let pageReferrer = '';
if (document.referrer) {
  const referrer = new URL(document.referrer);
  pageReferrer = referrer.origin + referrer.pathname;
}
const campaign = {};
const query = new URL(window.location.href).searchParams;
for (const [utm, parameter] of [
  ['utm_source', 'campaign_source'],
  ['utm_medium', 'campaign_medium'],
  ['utm_campaign', 'campaign_name'],
  ['utm_id', 'campaign_id'],
  ['utm_term', 'campaign_term'],
  ['utm_content', 'campaign_content']
]) {
  const value = query.get(utm);
  if (value) campaign[parameter] = value;
}
gtag('config', ${literal(config.measurementId)}, {
  page_location: ${literal(location.href)},
  page_referrer: pageReferrer,
  allow_google_signals: false,
  allow_ad_personalization_signals: false,
  ...campaign
});
`;
}
