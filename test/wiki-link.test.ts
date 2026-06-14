/**
 * Tests for the wiki-link remark plugin.
 *
 * Creates real .md files on disk (temporary) then runs the plugin through a
 * remark→rehype pipeline, so every assertion exercises the actual filesystem
 * walk, frontmatter parsing, and AST transformation — no mocks, no stubs.
 */

import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';
import remarkWikiLink, { slugify } from '../src/lib/remark-wiki-link.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// Fixtures go inside content/notes so the plugin's hardcoded NOTES_DIR can find them.
// .gitignore covers __wiki_test__/ in case of SIGKILL during before().
const NOTES_EN = path.resolve(__dirname, '../src/content/notes/en/__wiki_test__');

const NOTES = {
  'cryptography-basics.md': `---
title: "Cryptography Basics"
date: 2026-01-01
tags: [crypto]
---

# Cryptography Basics

Intro content.
`,
  'coding-theory.md': `---
title: Coding Theory
aliases: [Error-Correcting Codes, ECC]
date: 2026-02-01
---

# Coding Theory

A deep dive.
`,
  // Multi-line aliases
  'multi-alias.md': `---
title: Multi Alias Note
aliases:
  - First Alias
  - Second Alias
date: 2026-03-01
---

# Multi
`,
  // No title — filename fallback only
  'no-title.md': `---
date: 2026-04-01
---

# No Title Note
`,
};

describe('remark-wiki-link', () => {
  before(() => {
    fs.mkdirSync(NOTES_EN, { recursive: true });
    for (const [filename, content] of Object.entries(NOTES)) {
      fs.writeFileSync(path.join(NOTES_EN, filename), content);
    }
  });

  after(() => {
    fs.rmSync(NOTES_EN, { recursive: true, force: true });
  });

  async function transform(md: string) {
    const result = await unified()
      .use(remarkParse)
      .use(remarkWikiLink)
      .use(remarkRehype)
      .use(rehypeStringify)
      .process({ value: md, path: path.join(NOTES_EN, 'test-note.md') });
    return String(result);
  }

  it('resolves [[WikiLink]] by note title', async () => {
    const out = await transform('See [[Cryptography Basics]] for more.');
    const expected = `/en/notes/__wiki_test__/${slugify('Cryptography Basics')}/`;
    assert.ok(out.includes(`href="${expected}"`), `Missing href "${expected}" in:\n${out}`);
    assert.ok(out.includes('class="wiki-link"'), `Missing wiki-link class in:\n${out}`);
    // Closing-quote boundary: must NOT match wiki-link-new
    assert.ok(!out.includes('class="wiki-link-new"'), `Unexpected wiki-link-new in:\n${out}`);
    assert.ok(out.includes('>Cryptography Basics<'), `Missing link text in:\n${out}`);
  });

  it('marks non-existent notes with wiki-link-new class', async () => {
    const out = await transform('See [[AbsolutelyFakePage]].');
    assert.ok(out.includes('class="wiki-link-new"'), `Missing wiki-link-new class in:\n${out}`);
    assert.ok(!out.includes('class="wiki-link"'), `Unexpected wiki-link class in:\n${out}`);
  });

  it('supports [[Target|Display Text]] pipe alias', async () => {
    const out = await transform('Read [[Cryptography Basics|the crypto intro]].');
    assert.ok(out.includes('>the crypto intro<'), `Expected link text "the crypto intro" in:\n${out}`);
    const expected = `/en/notes/__wiki_test__/${slugify('Cryptography Basics')}/`;
    assert.ok(out.includes(`href="${expected}"`), `Missing correct href in:\n${out}`);
  });

  it('resolves via frontmatter aliases (inline array)', async () => {
    const out = await transform('See [[Error-Correcting Codes]].');
    assert.ok(out.includes('class="wiki-link"'), `Expected wiki-link class in:\n${out}`);
    assert.ok(
      out.includes(`href="/en/notes/__wiki_test__/${slugify('Coding Theory')}/"`),
      `Expected href to point to coding-theory in:\n${out}`,
    );
  });

  it('resolves via frontmatter aliases (multi-line list)', async () => {
    const out = await transform('Check [[First Alias]] and [[Second Alias]].');
    const resolved = [...out.matchAll(/class="wiki-link"/g)];
    assert.equal(resolved.length, 2, `Expected 2 resolved links, got ${resolved.length} in:\n${out}`);
    // Also verify no new-class links leaked in
    const unresolved = [...out.matchAll(/class="wiki-link-new"/g)];
    assert.equal(unresolved.length, 0, `Expected 0 unresolved links, got ${unresolved.length} in:\n${out}`);
  });

  it('falls back to filename when note has no title', async () => {
    const out = await transform('See [[no-title]].');
    assert.ok(out.includes('class="wiki-link"'), `Expected wiki-link class for filename fallback in:\n${out}`);
  });

  it('resolves case-insensitively', async () => {
    const out = await transform('See [[coding theory]].');
    const expected = `/en/notes/__wiki_test__/${slugify('Coding Theory')}/`;
    assert.ok(out.includes(`href="${expected}"`), `Expected case-insensitive match in:\n${out}`);
  });
});
