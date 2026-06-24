/**
 * Tests for markdown utility functions.
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { stripBold, boldToHtml } from '../src/lib/markdown.ts';

describe('stripBold', () => {
  it('removes ** markers from text', () => {
    assert.equal(stripBold('Hello **world**!'), 'Hello world!');
  });

  it('returns unchanged text when no bold markers', () => {
    assert.equal(stripBold('Hello world.'), 'Hello world.');
  });

  it('handles multiple bold spans', () => {
    assert.equal(stripBold('**foo** and **bar**'), 'foo and bar');
  });

  it('handles empty string', () => {
    assert.equal(stripBold(''), '');
  });

  it('handles adjacent bold spans', () => {
    assert.equal(stripBold('**hello****world**'), 'helloworld');
  });

  it('does NOT match single asterisks (only **)', () => {
    assert.equal(stripBold('*not bold*'), '*not bold*');
  });

  it('handles bold with HTML entities in content', () => {
    assert.equal(stripBold('**use &amp; here**'), 'use &amp; here');
  });
});

describe('boldToHtml', () => {
  it('converts **bold** to <strong>bold</strong>', () => {
    assert.equal(boldToHtml('Hello **world**!'), 'Hello <strong>world</strong>!');
  });

  it('returns unchanged text when no bold markers', () => {
    assert.equal(boldToHtml('Hello world.'), 'Hello world.');
  });

  it('handles multiple bold spans', () => {
    assert.equal(
      boldToHtml('**foo** and **bar**'),
      '<strong>foo</strong> and <strong>bar</strong>',
    );
  });

  it('escapes HTML in bold content', () => {
    // Content with < and & must be escaped inside <strong>
    assert.equal(
      boldToHtml('**a < b & c**'),
      '<strong>a &lt; b &amp; c</strong>',
    );
  });

  it('escapes double quotes in bold content', () => {
    assert.equal(
      boldToHtml('**say "hello"**'),
      '<strong>say &quot;hello&quot;</strong>',
    );
  });

  it('handles empty string', () => {
    assert.equal(boldToHtml(''), '');
  });

  it('does NOT match single asterisks', () => {
    assert.equal(boldToHtml('*not bold*'), '*not bold*');
  });
});
