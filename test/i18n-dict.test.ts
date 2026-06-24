/**
 * Tests for i18n dictionary structure.
 *
 * Validates that both locales have the same keys, no missing/empty values,
 * and consistent variable placeholders.
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { dict } from '../src/i18n/dict.ts';

const ZH_KEYS = Object.keys(dict.zh);
const EN_KEYS = Object.keys(dict.en);

describe('i18n dict', () => {
  it('has the same number of keys in both locales', () => {
    assert.equal(ZH_KEYS.length, EN_KEYS.length, 'Key counts differ between zh and en');
  });

  it('has no keys in zh that are missing from en', () => {
    const missingInEn = ZH_KEYS.filter((k) => !(k in dict.en));
    assert.deepEqual(missingInEn, [], `zh keys missing from en: ${missingInEn.join(', ')}`);
  });

  it('has no keys in en that are missing from zh', () => {
    const missingInZh = EN_KEYS.filter((k) => !(k in dict.zh));
    assert.deepEqual(missingInZh, [], `en keys missing from zh: ${missingInZh.join(', ')}`);
  });

  it('has no empty string values in zh', () => {
    const empty = ZH_KEYS.filter((k) => dict.zh[k as keyof typeof dict.zh] === '');
    assert.deepEqual(empty, [], `zh keys with empty values: ${empty.join(', ')}`);
  });

  it('has no empty string values in en', () => {
    const empty = EN_KEYS.filter((k) => dict.en[k as keyof typeof dict.en] === '');
    assert.deepEqual(empty, [], `en keys with empty values: ${empty.join(', ')}`);
  });

  it('has consistent {variable} placeholders between locales', () => {
    // Extract variable names from each key's value
    const varRe = /\{(\w+)\}/g;
    const mismatches: string[] = [];

    for (const key of ZH_KEYS) {
      const zhVars = new Set([...dict.zh[key as keyof typeof dict.zh].matchAll(varRe)].map((m) => m[1]));
      const enVars = new Set([...dict.en[key as keyof typeof dict.en].matchAll(varRe)].map((m) => m[1]));

      const zhOnly = [...zhVars].filter((v) => !enVars.has(v));
      const enOnly = [...enVars].filter((v) => !zhVars.has(v));

      if (zhOnly.length || enOnly.length) {
        mismatches.push(`${key}: zh=[${zhOnly}], en=[${enOnly}]`);
      }
    }

    assert.deepEqual(mismatches, [], `Variable placeholder mismatches:\n${mismatches.join('\n')}`);
  });
});
