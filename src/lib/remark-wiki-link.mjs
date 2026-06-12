/**
 * Custom remark plugin for Obsidian-style [[wiki-links]].
 *
 * Builds a global title→path map from the filesystem so
 * [[Note Name]] resolves to the correct folder-scoped URL.
 */

import { visit } from 'unist-util-visit';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const NOTES_DIR = path.resolve(__dirname, '../content/notes');

// Global cache: slugified title → relative path (folder/file)
let titleMap = null;

function buildTitleMap() {
  if (titleMap) return titleMap;
  titleMap = new Map();

  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const e of entries) {
      const full = path.join(dir, e.name);
      if (e.isDirectory() && e.name !== '.obsidian' && e.name !== '.trash') {
        walk(full);
      } else if (e.name.endsWith('.md')) {
        const relPath = path.relative(NOTES_DIR, full).replace(/\\/g, '/');
        const id = relPath.replace(/\.md$/, '');
        const filename = id.split('/').pop();

        // Read frontmatter
        try {
          const raw = fs.readFileSync(full, 'utf-8');
          const fmMatch = raw.match(/^---\n([\s\S]*?)\n---/);
          if (fmMatch) {
            const fm = fmMatch[1];
            const titleMatch = fm.match(/^title:\s*(.+)$/m);
            const aliasesMatch = fm.match(/^aliases:\s*\[(.+)\]$/m);

            if (titleMatch) {
              const title = titleMatch[1].trim().replace(/['"]/g, '');
              const slug = title.replace(/\s+/g, '-').toLowerCase();
              titleMap.set(slug, id);
            }

            if (aliasesMatch) {
              const aliases = aliasesMatch[1].split(',').map((a) => a.trim().replace(/['"]/g, ''));
              for (const alias of aliases) {
                const slug = alias.replace(/\s+/g, '-').toLowerCase();
                titleMap.set(slug, id);
              }
            }
          }
        } catch {
          // Skip files that can't be read
        }

        // Also map by filename (without extension)
        if (filename) titleMap.set(filename, id);
      }
    }
  }

  walk(NOTES_DIR);
  return titleMap;
}

export default function remarkWikiLink() {
  return (tree) => {
    const map = buildTitleMap();

    visit(tree, 'text', (node, index, parent) => {
      if (!parent) return;

      const regex = /\[\[([^\]]+)\]\]/g;
      const matches = [];
      let match;

      while ((match = regex.exec(node.value)) !== null) {
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

        // [[Target]] or [[Target|Alias]] or [[Target#heading]]
        const parts = m.inner.split('|');
        const targetPart = parts[0].split('#')[0].trim();
        const displayName = parts[1]?.trim() ?? parts[0].split('#')[0].trim();
        const slugKey = targetPart.toLowerCase().replace(/\s+/g, '-');
        const resolvedId = map.get(slugKey);

        const href = resolvedId ? `/notes/${resolvedId}/` : `/notes/${slugKey}/`;
        const className = resolvedId ? 'wiki-link' : 'wiki-link-new';

        newNodes.push({
          type: 'link',
          url: href,
          data: {
            hName: 'a',
            hProperties: { href, class: className },
          },
          children: [{ type: 'text', value: displayName }],
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
