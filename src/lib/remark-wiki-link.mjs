/**
 * Custom remark plugin for Obsidian-style [[wiki-links]].
 *
 * Builds per-locale title→path maps from the filesystem so
 * [[Note Name]] resolves to the correct URL within the same locale.
 * Locale is inferred from the file path (content/notes/<locale>/...).
 */

import { visit } from 'unist-util-visit';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const NOTES_DIR = path.resolve(__dirname, '../content/notes');

// Per-locale cache: locale → (slugified title → relative path within locale)
const localeMap = new Map();

function buildLocaleMap(locale) {
  if (localeMap.has(locale)) return localeMap.get(locale);
  const map = new Map();
  const localeDir = path.join(NOTES_DIR, locale);
  if (!fs.existsSync(localeDir)) {
    localeMap.set(locale, map);
    return map;
  }

  function walk(dir) {
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const e of entries) {
      const full = path.join(dir, e.name);
      if (e.isDirectory() && e.name !== '.obsidian' && e.name !== '.trash') {
        walk(full);
      } else if (e.name.endsWith('.md')) {
        const relPath = path.relative(localeDir, full).replace(/\\/g, '/');
        const id = relPath.replace(/\.md$/, '');
        const filename = id.split('/').pop();

        try {
          const raw = fs.readFileSync(full, 'utf-8');
          const fmMatch = raw.match(/^---\r?\n([\s\S]*?)\n---/);
          if (fmMatch) {
            const fm = fmMatch[1];
            const titleMatch = fm.match(/^title:\s*(.+)$/m);
            const aliasesMatch = fm.match(/^aliases:\s*\[(.+)\]$/m);
            // Also handle multi-line YAML alias lists
            const aliasesBlockMatch = fm.match(/^aliases:\s*\n((?:\s+-\s+.+\n?)+)/m);

            if (titleMatch) {
              const title = titleMatch[1].trim().replace(/['"]/g, '');
              const slug = title.replace(/\s+/g, '-').toLowerCase();
              map.set(slug, id);
            }

            // Inline array: aliases: [a, b]
            if (aliasesMatch) {
              const aliases = aliasesMatch[1].split(',').map((a) => a.trim().replace(/['"]/g, ''));
              for (const alias of aliases) {
                const slug = alias.replace(/\s+/g, '-').toLowerCase();
                map.set(slug, id);
              }
            }

            // Multi-line list: aliases:\n  - a\n  - b
            if (aliasesBlockMatch) {
              const items = aliasesBlockMatch[1].match(/-\s+(.+)/g);
              if (items) {
                for (const item of items) {
                  const alias = item.replace(/^-\s+/, '').trim().replace(/['"]/g, '');
                  const slug = alias.replace(/\s+/g, '-').toLowerCase();
                  map.set(slug, id);
                }
              }
            }
          }
        } catch {
          // Skip files that can't be read
        }

        if (filename) map.set(filename, id);
      }
    }
  }

  walk(localeDir);
  localeMap.set(locale, map);
  return map;
}

/** Determine locale from the file's path on disk */
function getLocaleFromFile(file) {
  const filePath = file.history?.[0] ?? file.path ?? '';
  // Path like .../content/notes/en/folder/note.md or .../content/blog/en/post.md
  const match = filePath.match(/content\/(?:notes|blog)\/(en|zh)\//);
  return match ? match[1] : 'en';
}

export default function remarkWikiLink() {
  return (tree, file) => {
    const locale = getLocaleFromFile(file);
    const map = buildLocaleMap(locale);

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
        const slugKey = targetPart.toLowerCase().replace(/['"]/g, '').replace(/\s+/g, '-');
        const resolvedId = map.get(slugKey);

        const href = resolvedId
          ? `/${locale}/notes/${resolvedId}/`
          : `/${locale}/notes/${slugKey}/`;
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
