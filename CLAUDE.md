# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

| Command | Description |
|---|---|
| `npm run dev` | Start dev server at `localhost:4321` |
| `npm run build` | Build to `dist/` + run Pagefind search index |
| `npm run preview` | Preview the production build locally |
| `npm run astro -- --help` | Astro CLI passthrough |
| `npm test` | Run all tests (85 tests, 0 fail) |

## Architecture

This is an Astro 6 personal website with three content collections — **blog** (`src/content/blog/`), **docs** (`src/content/docs/`), and **notes** (`src/content/notes/`). Notes are an Obsidian-style vault where folders act as knowledge domains. Content is authored in Markdown with YAML frontmatter (see `src/content.config.ts` for schemas).

### Key architectural decisions

**Dual rendering path for the knowledge graph.** The graph component has two implementations: a React version (`KnowledgeGraph.jsx`) for the initial icon/loading state, and a browser-only loader (`graph-loader.js`) that loads `force-graph` from CDN to avoid the SSR crash (`force-graph` references `window` at import time). The Astro island (`GraphIsland.astro`) serializes graph data as a `data-graph` JSON attribute on a container div so the browser script can hydrate it without an extra fetch.

**[[wiki-link]] resolution happens at build time** via a custom remark plugin (`src/lib/remark-wiki-link.mjs`). It walks `src/content/notes/` on first use, builds a slugified title→path map from frontmatter titles and aliases, then transforms `[[Target]]` AST nodes into `<a>` tags with resolved URLs. Unresolved links get class `wiki-link-new` (wavy underline) instead of `wiki-link` (dotted underline). Tests in `test/wiki-link.test.ts` cover title resolution, aliases (inline + multi-line), filename fallback, and case insensitivity.

**`==highlight==` syntax** is supported via `src/lib/remark-mark.mjs`, which converts `==text==` into `<mark>` elements. This is compatible with Typora, Obsidian, and Logseq. Standard Markdown `~~strikethrough~~` renders as `<del>`. The plugin uses a two-pass approach: first collect all text nodes, then apply replacements in reverse index order to avoid corrupting the tree walk. Inner text is HTML-escaped to prevent XSS.

**Table of Contents** is a reusable Astro component (`src/components/ui/TableOfContents.astro`) that accepts `headings` from Astro's `render()`, filters by `minDepth`/`maxDepth`, and renders a collapsible `<details>` tree with indented links. It replaced inline regex-based ToC generation in blog, docs, and notes pages.

**Bilingual (zh/en) via `[lang]` routing.** The default locale is `en`. All content routes live under `src/pages/[lang]/` with `[lang]` as the top-level path parameter. `getStaticPaths()` generates both `{ lang: 'en' }` and `{ lang: 'zh' }` for each route. Content collections use locale subdirectories (`content/<type>/en/`, `content/<type>/zh/`) with locale filtering via `id.startsWith('${locale}/')`. The i18n dictionary (`src/i18n/dict.ts`) holds all UI strings; `useTranslations(locale)` returns a `t(key, vars?)` function. Site config per locale is in `src/i18n/site.ts`.

**Graph is folder-scoped.** `src/lib/graph.ts` provides three generators: `buildFolderGraph(folder)` for a single knowledge domain, `buildGraph()` for all-folders overview, and `buildLocalGraph(slug)` for a note's neighborhood. Pure string helpers (`extractWikilinks`, `getFolder`, `getFilename`) are extracted to `src/lib/graph-helpers.ts` so they can be tested without pulling in `astro:content`. Wiki-links only connect notes within the same folder — cross-folder edges don't exist in this model.

### Type system

The `Locale` type (`'en' | 'zh'`) is defined once in `src/types.ts` along with `locales` and `defaultLocale`, and re-exported by both `src/content.config.ts` and `src/i18n/dict.ts`. Import it from `src/types.ts` when possible (avoids pulling in `astro:content`). Markdown utilities live in `src/lib/markdown.ts` (`stripBold`, `boldToHtml`).

### Tests

All tests use `node --experimental-strip-types --test test/*.ts` (also `npm test`). No test framework — just `node:test` + `node:assert/strict`. Pure function tests import directly; remark plugin tests run through a `unified().use(remarkParse).use(plugin).use(remarkRehype).use(rehypeStringify)` pipeline.

| Test file | Covers |
|---|---|
| `test/remark-mark.test.ts` (13) | `==highlight==` → `<mark>`, XSS escaping, regex edge cases |
| `test/wiki-link.test.ts` (7) | `[[wikilink]]` resolution, aliases, case insensitivity, fallback |
| `test/markdown.test.ts` (14) | `stripBold`, `boldToHtml` — HTML escaping, edge cases |
| `test/i18n-utils.test.ts` (17) | `localePath`, `otherLocale`, `useTranslations` — interpolation, fallback |
| `test/i18n-dict.test.ts` (6) | Structural: key parity, empty values, variable placeholder consistency |
| `test/site-config.test.ts` (6) | `getSiteConfig` per locale, `SITE` constants |
| `test/graph-helpers.test.ts` (22) | `extractWikilinks`, `getFolder`, `getFilename` — pure helpers |

### Route map

| Route | File | Notes |
|---|---|---|
| `/` | `pages/index.astro` | Redirects to `/en/` |
| `/[lang]/` | `pages/[lang]/index.astro` | Hero + recent blog posts |
| `/[lang]/blog/` | `pages/[lang]/blog/index.astro` | Year/month archive |
| `/[lang]/blog/[...slug]/` | `pages/[lang]/blog/[...slug].astro` | Single post with ToC |
| `/[lang]/docs/` | `pages/[lang]/docs/index.astro` | Docs listing |
| `/[lang]/docs/[...slug]/` | `pages/[lang]/docs/[...slug].astro` | Single doc with ToC |
| `/[lang]/notes/` | `pages/[lang]/notes/index.astro` | Folder listing |
| `/[lang]/notes/[folder]/` | `pages/[lang]/notes/[folder].astro` | Folder index page (renders `index.md`) |
| `/[lang]/notes/[...slug]/` | `pages/[lang]/notes/[...slug].astro` | Single note with ToC |
| `/[lang]/notes/graph/` | `pages/[lang]/notes/graph.astro` | Knowledge graph with folder selector |
| `/[lang]/search/` | `pages/[lang]/search.astro` | Pagefind search UI |

### Design system

Single `src/styles/global.css` file (~1700 lines) with CSS custom properties for theming. No CSS framework — all styles are hand-authored against design tokens (`--primary`, `--secondary`, `--accent`, `--gap`, `--radius`, etc.). Two themes: `:root` (light, `#fafaf7` background) and `[data-theme='dark']` (`#0a0a0a` background). The theme toggle in `BaseLayout.astro` runs an inline `<script>` before CSS loads to prevent flash. Persisted to `localStorage('pref-theme')`. Typography: Fraunces for headings, Inter for body, JetBrains Mono for code. Accent color is a warm rust (`#c2643a` light / `#e8956a` dark).

**Language-specific typography** is handled via `:lang(en)` and `:lang(zh)` selectors. English uses `line-height: 1.7` with `hyphens: auto`, while Chinese uses `line-height: 1.8` with `hyphens: none` and `text-spacing: normal` for auto CJK-Latin spacing. Post content headings use a proximity-based margin scheme (top margin > bottom margin so headings sit closer to their content). Body text is 18px with `line-height: 1.65`.
