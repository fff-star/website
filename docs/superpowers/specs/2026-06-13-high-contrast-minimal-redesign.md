# High-Contrast Minimal Redesign

**Date:** 2026-06-13
**Scope:** Full-site visual redesign + CSS architecture cleanup

## Summary

Redesign fff.sh from "Arctic Frost" (cold slate-blue palette, Fraunces italic + Atkinson Hyperlegible, decorative elements) to a high-contrast minimal aesthetic: pure grayscale palette, Fraunces upright headings + Inter body, no borders, geometric spacing, steel blue accent retained.

## Design Decisions

| Dimension | Before | After |
|---|---|---|
| Palette | Icy whites + slate blues | Pure grayscale (`#fafafa`/`#fff`/`#111`/`#e5e5e5`) |
| Accent | `#0f6ea0` | `#0f6ea0` (unchanged) |
| Heading font | Fraunces italic, variable weight | Fraunces upright, tighter weight scale |
| Body font | Atkinson Hyperlegible 18px | Inter 15-16px |
| Cards | Left thick border + full border | No border, background-only differentiation |
| Decoration | Drop cap, gradient dividers, hero italic | All removed |
| Dark mode | Blue-gray darks | Pure black-gray darks (`#0a0a0a`/`#1a1a1a`) |
| Code font | JetBrains Mono | JetBrains Mono (unchanged) |
| Inline styles | Heavy use of `style=""` across components | Migrate to CSS classes |

## What Stays the Same

- Card structure (post-entry, archive-entry)
- Notes folder page behavior (shows index.md, lists folder names only)
- Layout widths (`--main-width: 720px`, `--nav-width: 1024px`)
- Header/footer structure
- Knowledge graph, backlinks, TOC, search (Pagefind)
- Wiki-link styling pattern (dotted underline)
- Tag display patterns

## Color System

### Light Theme
```
--theme:      #fafafa   (page background)
--entry:      #ffffff   (card/surface background)
--primary:    #111111   (heading text)
--secondary:  #666666   (muted text)
--tertiary:   #f5f5f5   (subtle surface, code bg)
--content:    #333333   (body text)
--accent:     #0f6ea0   (links, highlights)
--accent-hover: #0a5580
--accent-dim: #e8f2f8   (accent background, mark bg)
--code-block-bg: #f0f0f0
--code-bg:    #f5f5f5
--border:     #e5e5e5   (only for tables, code blocks, TOC — NOT cards)
```

### Dark Theme
```
--theme:      #0a0a0a
--entry:      #1a1a1a
--primary:    #e5e5e5
--secondary:  #999999
--tertiary:   #262626
--content:    #cccccc
--accent:     #4db8e8
--accent-hover: #80d4f7
--accent-dim: #0d2a3a
--code-block-bg: #1a1a1a
--code-bg:    #1a1a1a
--border:     #2a2a2a
```

## Typography Scale

### Headings (Fraunces, upright, no italic)
```
h1: 32px, weight 500 (was 38px, 380 italic)
h2: 22px, weight 500 (was 24px, 470)
h3: 18px, weight 550 (was 20px, 450)
h4: 16px, weight 600 (was 18px, 500)
.post-title: 32px, weight 500 (was 42px, 400 italic)
```

### Body (Inter)
```
body: 16px, line-height 1.6 (was 18px, 1.65)
.entry-content: 14px (was 15px)
.post-content: 16px, line-height 1.7 (was 18px, 1.75)
.entry-footer: 12px (was 13px)
```

## What Gets Removed

1. Drop cap on `.post-content > p:first-of-type::first-letter`
2. `.section-divider` gradient rule
3. `.first-entry .entry-header h1` italic style
4. `.post-entry` left border (`border-left: 4px solid`)
5. `.post-entry` border (`border: 1px solid var(--border)`)
6. Hero italic Fraunces
7. All decorative gradient elements

## What Gets Added

1. **Font import**: Inter from Google Fonts (replace Atkinson Hyperlegible)
2. **`.page-header h1`** CSS rule (was missing, defined only in @media)

## Inline Style Migration

Move inline `style=""` attributes to CSS classes in `global.css`:
- **Header.astro**: nav, logo, menu, active link styles → `.header`, `.header-nav`, `.logo`, `.menu`, `.menu-active`
- **index.astro**: blog post list styles → `.home-post-list`, `.home-post-item`
- **notes/index.astro**: folder listing → `.folder-list`, `.folder-item`
- **tags/index.astro**: tag listing → `.tag-list`, `.tag-item`
- **tags/[tag].astro**: post listing → `.tag-post-list`
- **NoteCard.astro**: already uses CSS classes
- **TagList.astro**: already uses CSS classes
- **ThemeToggle.astro**: keep inline styles (dynamic display toggle requires it)

## Implementation Order

1. `global.css` — color system, typography, remove decoration, add missing styles
2. `BaseLayout.astro` — update font import link
3. `Header.astro` — migrate inline styles to classes
4. `index.astro` (homepage) — migrate inline styles
5. `notes/index.astro` — migrate inline styles
6. `tags/index.astro`, `tags/[tag].astro` — migrate inline styles
7. Verify all pages render correctly

## Non-Goals

- Changing layout widths or page structure
- Adding new features (prev/next nav, new components)
- Changing content rendering (wiki-links, code blocks, callouts, KaTeX)
- Modifying the graph visualization
- Search page redesign (Pagefind handles its own UI)
