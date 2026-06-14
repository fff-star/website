/**
 * Remark plugin that converts ==text== syntax to <mark>text</mark>.
 *
 * Compatible with Typora, Obsidian (with Highlightr plugin),
 * Logseq, and other tools that use this convention.
 */

import { visit } from 'unist-util-visit';

const MARK_REGEX = /==([^=\n]+)==/g;

export default function remarkMark() {
  return (tree) => {
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
          value: `<mark>${m.inner}</mark>`,
        });

        lastEnd = m.end;
      }

      if (lastEnd < node.value.length) {
        newNodes.push({ type: 'text', value: node.value.slice(lastEnd) });
      }

      parent.children.splice(index, 1, ...newNodes);
    });
  };
}
