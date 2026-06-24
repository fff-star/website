/**
 * Remark plugin that converts ==text== syntax to <mark>text</mark>.
 *
 * Compatible with Typora, Obsidian (with Highlightr plugin),
 * Logseq, and other tools that use this convention.
 */

import { visit } from 'unist-util-visit';

/** Escape HTML special chars to prevent XSS when building raw HTML nodes. */
function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export default function remarkMark() {
  // (?<![=])==(?![=]) — opening: exactly two equals, no third = on either side
  // ([^\n]+?)           — inner content (lazy, allows = inside, no newlines)
  // (?<![=])==(?![=]) — closing: exactly two equals, no third = on either side
  const MARK_REGEX = /(?<![=])==(?![=])([^\n]+?)(?<![=])==(?![=])/g;

  return (tree) => {
    /** @type {Array<{node: object, index: number, parent: object}>} */
    const pending = [];

    // First pass: collect text nodes that need modification.
    visit(tree, 'text', (node, index, parent) => {
      if (!parent) return;

      MARK_REGEX.lastIndex = 0;
      const matches = [];
      let match;

      while ((match = MARK_REGEX.exec(node.value)) !== null) {
        matches.push({
          start: match.index,
          end: match.index + match[0].length,
          inner: match[1],
        });
      }

      if (matches.length === 0) return;

      const newNodes = [];
      let lastEnd = 0;

      for (const m of matches) {
        if (m.start > lastEnd) {
          newNodes.push({ type: 'text', value: node.value.slice(lastEnd, m.start) });
        }

        newNodes.push({
          type: 'html',
          value: `<mark>${escapeHtml(m.inner)}</mark>`,
        });

        lastEnd = m.end;
      }

      if (lastEnd < node.value.length) {
        newNodes.push({ type: 'text', value: node.value.slice(lastEnd) });
      }

      pending.push({ parent, index, newNodes });
    });

    // Second pass: apply replacements in reverse index order so earlier
    // indices remain valid when later mutations shift the array.
    // Sort by parent identity then descending index.
    pending.sort((a, b) => {
      if (a.parent !== b.parent) return 0; // different parents, order doesn't matter
      return b.index - a.index;
    });

    for (const { parent, index, newNodes } of pending) {
      parent.children.splice(index, 1, ...newNodes);
    }
  };
}
