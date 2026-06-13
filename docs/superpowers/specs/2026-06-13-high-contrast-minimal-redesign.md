# High-Contrast Minimal Redesign

**Date:** 2026-06-13 (updated 2026-06-13)
**Scope:** Full-site visual redesign + CSS architecture cleanup + bug fixes

## Summary

Redesign fff.sh to a high-contrast minimal aesthetic: pure grayscale palette, Fraunces upright headings + Inter body, no decorative borders on cards, geometric spacing, steel blue accent. Fixes critical CSS scoping bug that made theme toggle icons invisible.

## Bugs Fixed

1. **Theme toggle icons invisible** — Astro CSS scoping rewrote `[data-theme='dark'] .sun` as `[data-astro-cid][data-theme=dark] .sun[data-astro-cid]`, which could never match because `data-theme` is on `<html>`, not the scoped component. Fixed by using `<style is:global>` in ThemeToggle.astro.
2. **Wiki-link 404s** — Folder renamed from `network wiki` (space) to `network-wiki` (hyphen) to match Astro's content collection slug normalization. Wiki links now resolve to URLs that match generated page paths.

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
--code-block-bg: #1e1e1e   (dark — shiki uses dark themes for both modes)
--code-bg:    #f5f5f5
--border:     #e5e5e5
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

Chosen to balance readability (technical Chinese content with formulas/tables/code) with personality. The 720px content column and dense Chinese characters informed sizing decisions.

### Headings (Fraunces, upright, weight 500)
```
h1: 36px   (page titles — substantial without dominating)
h2: 26px   (section headings — clear hierarchy jump)
h3: 20px   (sub-sections, weight 550)
h4: 18px   (minor headings, weight 600)
.post-title: 36px
.page-header h1: 36px
.post-content h1: 30px (slightly smaller than page title)
.post-content h2: 26px
.post-content h3: 20px
.post-content h4: 18px
```

### Body (Inter, weight 450)
```
body: 18px, line-height 1.6
.post-content: 18px, line-height 1.7
.entry-content (card previews): 15px
.entry-footer: 14px
.post-meta, .breadcrumbs: 15px
.footer: 14px
```

### Card / List Titles (Fraunces)
```
.entry-header h2: 24px
.blog-item-title: 22px
.archive-entry-title a: 22px
.folder-item a: 22px
.tag-item a: 22px
```

## Layout (unchanged)
```
--gap: 24px
--content-gap: 16px
--nav-width: 1024px
--main-width: 720px
--header-height: 60px
--footer-height: 56px
--radius: 6px
```

## What Was Removed
- Drop cap on `.post-content > p:first-of-type::first-letter`
- All decorative gradient elements
- Left-border card indicators
- Atkinson Hyperlegible font (replaced with Inter)

## What Was Added
- `.page-header h1` CSS rule
- `.graph-folder-chip` CSS for graph page folder selector
- `.skip-link` CSS class for accessibility
- `.empty-message` utility class for empty states
- `.graph-folder-nav`, `.graph-folder-info`, `.graph-folder-label` for graph page

## Inline Style Migration
Moved ~18 inline `style=""` attributes to CSS classes in `global.css`:
- BaseLayout: skip-link, main content area
- Graph page: folder nav, chips, stats, fallback
- Notes/Blog pages: TOC spacing, post-meta
- Components: NoteCard tags, PostEntry cover, Backlinks desc, TagList empty state

## Non-Goals
- Changing layout widths or page structure
- Adding new features
- Changing content rendering (wiki-links, code blocks, callouts, KaTeX)
- Modifying the graph visualization
- Search page redesign (Pagefind handles its own UI)
