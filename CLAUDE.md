# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

| Command | Description |
|---|---|
| `npm run dev` | Start dev server at `localhost:4321` |
| `npm run build` | Build to `dist/` + run Pagefind search index |
| `npm run preview` | Preview the production build locally |
| `npm run astro -- --help` | Astro CLI passthrough |

## Architecture

This is an Astro 6 personal website with two content collections — **blog** (`src/content/blog/`) and **notes** (`src/content/notes/`). Notes are an Obsidian-style vault where folders act as knowledge domains. Content is authored in Markdown with YAML frontmatter (see `src/content.config.ts` for schemas).

### Key architectural decisions

**Dual rendering path for the knowledge graph.** The graph component has two implementations: a React version (`KnowledgeGraph.jsx`) for the initial icon/loading state, and a browser-only loader (`graph-loader.js`) that loads `force-graph` from CDN to avoid the SSR crash (`force-graph` references `window` at import time). The Astro island (`GraphIsland.astro`) serializes graph data as a `data-graph` JSON attribute on a container div so the browser script can hydrate it without an extra fetch.

**[[wiki-link]] resolution happens at build time** via a custom remark plugin (`src/lib/remark-wiki-link.mjs`). It walks `src/content/notes/` on first use, builds a slugified title→path map from frontmatter titles and aliases, then transforms `[[Target]]` AST nodes into `<a>` tags with resolved URLs. Unresolved links get class `wiki-link-new` (wavy underline) instead of `wiki-link` (dotted underline).

**Bilingual (zh/en) via post-build mirroring** (`scripts/build-i18n.mjs`). Default locale is `zh`. The build script walks `dist/`, copies all HTML files to `dist/en/`, patches `lang` attributes, rewrites nav/og/canonical URLs to prefix `/en/`, and flips the locale switcher link. The `_redirects` file (`/en/* /:splat 200`) makes Cloudflare Pages serve the mirrored files. The i18n dictionary (`src/i18n/dict.ts`) holds all UI strings; `useTranslations(locale)` returns a `t(key, vars?)` function.

**Graph is folder-scoped.** `src/lib/graph.ts` provides three generators: `buildFolderGraph(folder)` for a single knowledge domain, `buildGraph()` for all-folders overview, and `buildLocalGraph(slug)` for a note's neighborhood. Wiki-links only connect notes within the same folder — cross-folder edges don't exist in this model.

### Route map

| Route | File | Notes |
|---|---|---|
| `/` | `pages/index.astro` | Hero + recent blog + note vaults |
| `/blog/` | `pages/blog/index.astro` | Year/month archive |
| `/blog/[...slug]/` | `pages/blog/[...slug].astro` | Single post with ToC |
| `/notes/` | `pages/notes/index.astro` | Folder listing |
| `/notes/[folder]/` | `pages/notes/[folder].astro` | Folder index page (renders `index.md`) |
| `/notes/[...slug]/` | `pages/notes/[...slug].astro` | Single note with ToC |
| `/notes/graph/` | `pages/notes/graph.astro` | Knowledge graph with folder selector |
| `/tags/` | `pages/tags/index.astro` | Tag cloud |
| `/tags/[tag]/` | `pages/tags/[tag].astro` | Posts by tag |
| `/search/` | `pages/search.astro` | Pagefind search UI |
| `/rss.xml` | `pages/rss.xml.js` | RSS feed (blog posts only) |

### Design system

Single `src/styles/global.css` file (~1700 lines) with CSS custom properties for theming. Two themes: `:root` (light, `#fafaf7` background) and `[data-theme='dark']` (`#0a0a0a` background). The theme toggle in `BaseLayout.astro` runs an inline `<script>` before CSS loads to prevent flash. Persisted to `localStorage('pref-theme')`. Typography: Fraunces for headings, Inter for body, JetBrains Mono for code. Accent color is a warm rust (`#c2643a` light / `#e8956a` dark).
