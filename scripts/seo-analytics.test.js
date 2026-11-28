import test from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import { getAnalyticsConfig, getAnalyticsScript } from '../site/src/components/analytics-config.js';

// Synthetic IDs are used only in isolated tests, never in deployed configuration.
const measurementId = `G-${'A'.repeat(10)}`;

test('analytics and verification default off, including blank configuration', () => {
  assert.deepEqual(getAnalyticsConfig(), {
    measurementId: '', googleVerification: '', bingVerification: '',
  });
  assert.equal(getAnalyticsConfig({ PUBLIC_GA_MEASUREMENT_ID: ' \n ' }).measurementId, '');
  assert.equal(getAnalyticsScript('', 'https://skillshub.space/'), '');
});

test('valid verification tokens work independently of analytics', () => {
  assert.deepEqual(getAnalyticsConfig({
    PUBLIC_GOOGLE_SITE_VERIFICATION: ' google_token-1 ',
    PUBLIC_BING_SITE_VERIFICATION: 'aB'.repeat(16),
  }), {
    measurementId: '',
    googleVerification: 'google_token-1',
    bingVerification: 'aB'.repeat(16),
  });
  assert.equal(getAnalyticsConfig({ PUBLIC_GA_MEASUREMENT_ID: ` ${measurementId} ` }).measurementId, measurementId);
});

test('invalid IDs and pasted verification tags fail with actionable variable names', () => {
  for (const value of ['UA-123456-1', 'G-short', 'G-abcdefghij', `${measurementId}"><script>`, 'placeholder']) {
    assert.throws(() => getAnalyticsConfig({ PUBLIC_GA_MEASUREMENT_ID: value }), /PUBLIC_GA_MEASUREMENT_ID.*unset/);
  }
  for (const name of ['PUBLIC_GOOGLE_SITE_VERIFICATION', 'PUBLIC_BING_SITE_VERIFICATION']) {
    assert.throws(() => getAnalyticsConfig({ [name]: '<meta content="token">' }), new RegExp(`${name}.*content token`));
  }
});

test('initialization queues one standard pageview config without custom events or query data', () => {
  const context = {
    document: { referrer: 'https://example.com/path?private=secret#fragment' },
    location: { href: 'https://skillshub.space/skills/?q=private#fragment' },
    URL,
  };
  context.window = context;
  vm.runInNewContext(getAnalyticsScript(measurementId, 'https://skillshub.space/skills/?q=private#fragment'), context);
  const calls = context.dataLayer.map(args => Array.from(args));
  assert.equal(calls.length, 2);
  assert.equal(calls[0][0], 'js');
  assert.equal(calls[1][0], 'config');
  assert.equal(calls[1][1], measurementId);
  assert.deepEqual(JSON.parse(JSON.stringify(calls[1][2])), {
    page_location: 'https://skillshub.space/skills/',
    page_referrer: 'https://example.com/path',
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
  });
});

test('empty referrer is supported and inline location data cannot close the script', () => {
  const context = {
    document: { referrer: '' },
    location: { href: 'https://skillshub.space/' },
    URL,
  };
  context.window = context;
  const script = getAnalyticsScript(measurementId, 'https://skillshub.space/</script>');
  assert(!script.includes('</script>'));
  vm.runInNewContext(script, context);
  assert.equal(context.dataLayer[1][2].page_referrer, '');
});

test('runtime campaign attribution preserves only the six allowlisted UTM parameters', () => {
  const context = {
    document: { referrer: '' },
    location: {
      href: 'https://skillshub.space/?utm_source=newsletter&utm_medium=email&utm_campaign=autumn+launch&utm_id=launch-1&utm_term=agent+skills&utm_content=header&utm_extra=secret&q=private&token=private#private',
    },
    URL,
  };
  context.window = context;
  vm.runInNewContext(getAnalyticsScript(measurementId, 'https://skillshub.space/'), context);
  assert.equal(context.dataLayer.length, 2);
  assert.deepEqual(JSON.parse(JSON.stringify(context.dataLayer[1][2])), {
    page_location: 'https://skillshub.space/',
    page_referrer: '',
    allow_google_signals: false,
    allow_ad_personalization_signals: false,
    campaign_source: 'newsletter',
    campaign_medium: 'email',
    campaign_name: 'autumn launch',
    campaign_id: 'launch-1',
    campaign_term: 'agent skills',
    campaign_content: 'header',
  });
});

test('blank campaign parameters do not override default acquisition attribution', () => {
  const context = {
    document: { referrer: '' },
    location: { href: 'https://skillshub.space/?utm_source=&utm_campaign=' },
    URL,
  };
  context.window = context;
  vm.runInNewContext(getAnalyticsScript(measurementId, 'https://skillshub.space/'), context);
  assert(!Object.keys(context.dataLayer[1][2]).some(key => key.startsWith('campaign_')));
});
