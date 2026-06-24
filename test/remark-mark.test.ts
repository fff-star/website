/**
 * Tests for the remark-mark plugin (==highlight== → <mark>).
 *
 * Runs through a remark→rehype pipeline so every assertion exercises
 * the real AST transformation — no mocks, no stubs.
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';
import remarkMark from '../src/lib/remark-mark.mjs';

async function transform(md: string) {
  const result = await unified()
    .use(remarkParse)
    .use(remarkMark)
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeStringify, { allowDangerousHtml: true })
    .process(md);
  return String(result);
}

describe('remark-mark', () => {
  it('converts ==text== to <mark>text</mark>', async () => {
    const out = await transform('Hello ==world==!');
    assert.ok(out.includes('<mark>world</mark>'), `Expected <mark> in:\n${out}`);
  });

  it('leaves plain text unchanged', async () => {
    const out = await transform('Hello world.');
    assert.ok(!out.includes('<mark>'), `Unexpected <mark> in:\n${out}`);
  });

  it('handles multiple highlights in one paragraph', async () => {
    const out = await transform('==foo== and ==bar==.');
    const count = [...out.matchAll(/<mark>/g)].length;
    assert.equal(count, 2, `Expected 2 <mark> tags, got ${count} in:\n${out}`);
    assert.ok(out.includes('<mark>foo</mark>'), `Missing foo mark in:\n${out}`);
    assert.ok(out.includes('<mark>bar</mark>'), `Missing bar mark in:\n${out}`);
  });

  it('escapes HTML special chars to prevent XSS', async () => {
    // < followed by space stays as text per CommonMark spec (not inline HTML)
    const out = await transform('==a < b==');
    assert.ok(out.includes('<mark>a &lt; b</mark>'), `Expected escaped < in:\n${out}`);
  });

  it('escapes & and " characters', async () => {
    const out = await transform('=="a & b"==');
    assert.ok(out.includes('<mark>&quot;a &amp; b&quot;</mark>'), `Missing escaped entities in:\n${out}`);
  });

  it('allows = inside highlight', async () => {
    const out = await transform('==a=b==');
    assert.ok(out.includes('<mark>a=b</mark>'), `Expected a=b inside mark in:\n${out}`);
  });

  it('does NOT match === (three equals)', async () => {
    const out = await transform('===not a highlight===');
    assert.ok(!out.includes('<mark>'), `Unexpected <mark> from === in:\n${out}`);
  });

  it('does NOT match ==text== across newlines', async () => {
    const out = await transform('==line one\nline two==');
    assert.ok(!out.includes('<mark>'), `Unexpected <mark> across newline in:\n${out}`);
  });

  it('handles consecutive highlights separated by space', async () => {
    const out = await transform('==hello== ==world==');
    const count = [...out.matchAll(/<mark>/g)].length;
    assert.equal(count, 2, `Expected 2 <mark> tags, got ${count} in:\n${out}`);
  });

  it('does not highlight == with no inner content', async () => {
    const out = await transform('====');
    assert.ok(!out.includes('<mark>'), `Unexpected <mark> from ==== in:\n${out}`);
  });

  it('highlights text containing HTML entities correctly', async () => {
    // Markdown parser decodes &amp; → & in the AST text node.
    // escapeHtml then re-encodes & → &amp; for safe HTML output.
    const out = await transform('==use &amp; in code==');
    assert.ok(
      out.includes('<mark>use &amp; in code</mark>'),
      `Missing correctly escaped entities in:\n${out}`,
    );
  });

  it('handles highlight at start of paragraph', async () => {
    const out = await transform('==start== then text.');
    assert.ok(out.includes('<mark>start</mark>'), `Expected mark at start in:\n${out}`);
    assert.ok(out.includes(' then text.'), `Expected trailing text in:\n${out}`);
  });

  it('handles highlight at end of paragraph', async () => {
    const out = await transform('Text then ==end==');
    assert.ok(out.includes('<mark>end</mark>'), `Expected mark at end in:\n${out}`);
    assert.ok(out.includes('Text then '), `Expected leading text in:\n${out}`);
  });
});
