/**
 * Tests for site configuration.
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { getSiteConfig, SITE } from '../src/i18n/site.ts';
import type { Locale } from '../src/types.ts';

describe('getSiteConfig', () => {
  it('returns English config', () => {
    const config = getSiteConfig('en' as Locale);
    assert.equal(config.title, 'fff-star');
    assert.equal(config.author, 'fff');
    assert.ok(config.description.includes('fff-star'), 'description should mention fff-star');
    assert.ok(config.description.includes('**'), 'description should contain **bold** markers');
  });

  it('returns Chinese config', () => {
    const config = getSiteConfig('zh' as Locale);
    assert.equal(config.title, 'fff-star');
    assert.equal(config.author, 'fff');
    assert.ok(config.description.includes('你好'), 'zh description should contain Chinese greeting');
    assert.ok(config.description.includes('**'), 'zh description should contain **bold** markers');
  });

  it('returns same author for both locales', () => {
    assert.equal(
      getSiteConfig('en' as Locale).author,
      getSiteConfig('zh' as Locale).author,
    );
  });

  it('returns same title for both locales', () => {
    assert.equal(
      getSiteConfig('en' as Locale).title,
      getSiteConfig('zh' as Locale).title,
    );
  });
});

describe('SITE', () => {
  it('has a URL', () => {
    assert.ok(SITE.url.startsWith('https://'), 'SITE.url should be a valid URL');
  });

  it('has GitHub and Codeberg social links', () => {
    assert.ok(SITE.social.github.includes('github.com'), 'should have GitHub URL');
    assert.ok(SITE.social.codeberg.includes('codeberg.org'), 'should have Codeberg URL');
  });
});
