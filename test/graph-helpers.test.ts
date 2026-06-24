/**
 * Tests for graph helper functions (extractWikilinks, getFolder, getFilename).
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { extractWikilinks, getFolder, getFilename } from '../src/lib/graph-helpers.ts';

describe('extractWikilinks', () => {
  it('extracts a simple [[wikilink]]', () => {
    assert.deepEqual(extractWikilinks('See [[Cryptography Basics]] for more.'), [
      'cryptography-basics',
    ]);
  });

  it('extracts link with pipe alias [[Target|Display]]', () => {
    assert.deepEqual(extractWikilinks('Read [[Cryptography|the intro]].'), [
      'cryptography',
    ]);
  });

  it('extracts link with heading anchor [[Page#heading]]', () => {
    assert.deepEqual(extractWikilinks('Jump to [[Page#section-1]].'), ['page']);
  });

  it('extracts link with both alias and heading', () => {
    assert.deepEqual(extractWikilinks('See [[Target|Display#heading]].'), ['target']);
  });

  it('extracts multiple links from one string', () => {
    assert.deepEqual(extractWikilinks('[[a]] and [[b]] and [[c]]'), ['a', 'b', 'c']);
  });

  it('deduplicates identical links', () => {
    assert.deepEqual(extractWikilinks('[[same]] [[same]] [[same]]'), ['same']);
  });

  it('trims whitespace inside brackets', () => {
    assert.deepEqual(extractWikilinks('[[  hello world  ]]'), ['hello-world']);
  });

  it('lowercases and replaces spaces with dashes', () => {
    assert.deepEqual(extractWikilinks('[[Hello World]]'), ['hello-world']);
  });

  it('returns empty array when no links present', () => {
    assert.deepEqual(extractWikilinks('Just plain text with no links.'), []);
  });

  it('returns empty array for empty string', () => {
    assert.deepEqual(extractWikilinks(''), []);
  });

  it('does NOT match single bracket [text]', () => {
    assert.deepEqual(extractWikilinks('[not a link]'), []);
  });

  it('handles unicode characters in link text', () => {
    assert.deepEqual(extractWikilinks('[[密码学]]'), ['密码学']);
  });
});

describe('getFolder', () => {
  it('extracts folder from a three-part id', () => {
    assert.equal(getFolder('en/demos/hello-world'), 'demos');
  });

  it('extracts folder from zh locale', () => {
    assert.equal(getFolder('zh/crypto/test-note'), 'crypto');
  });

  it('returns empty string for two-part id (no folder)', () => {
    assert.equal(getFolder('en/notes'), '');
  });

  it('returns empty string for single segment', () => {
    assert.equal(getFolder('en'), '');
  });

  it('only extracts the second segment', () => {
    assert.equal(getFolder('en/folder/sub/deep'), 'folder');
  });
});

describe('getFilename', () => {
  it('extracts filename from a full id path', () => {
    assert.equal(getFilename('en/demos/hello-world'), 'hello-world');
  });

  it('returns the string unchanged when no slashes', () => {
    assert.equal(getFilename('hello-world'), 'hello-world');
  });

  it('preserves file extension', () => {
    assert.equal(getFilename('en/folder/note.md'), 'note.md');
  });

  it('handles deeply nested paths', () => {
    assert.equal(getFilename('a/b/c/d/e'), 'e');
  });

  it('handles trailing slash by returning empty', () => {
    assert.equal(getFilename('en/folder/'), '');
  });
});
