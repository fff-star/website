---
title: Getting Started with Your Own Digital Garden
date: 2025-06-01
tags: [tutorial, how-to]
description: A step-by-step guide to setting up your own Obsidian-powered digital garden with Astro
---

A **digital garden** is a personal space on the web where you cultivate ideas over time — unlike a traditional blog where posts are chronologically ordered and "finished," a digital garden is always growing, always evolving.

## Why a Digital Garden?

- **Learn in public**: Writing helps you think more clearly
- **Connect ideas**: Wiki-links create a web of knowledge
- **Evergreen content**: Update and improve notes over time
- **Own your data**: Your notes, your domain, your rules

## The Stack

This site uses:

1. **Obsidian** — Write notes locally with a great editor
2. **Astro** — Build a fast, static site
3. **Markdown plugins** — `[[wiki-links]]`, LaTeX, callouts
4. **Knowledge Graph** — Visualize connections between notes

## Getting Started

### 1. Set up Obsidian

Download [Obsidian](https://obsidian.md/) and create a vault. Write some notes with `[[wiki-links]]` and LaTeX.

### 2. Clone this site

```bash
git clone https://github.com/fff/website
cd website
npm install
```

### 3. Add your notes

Copy your Obsidian markdown files into `src/content/notes/`. Make sure each file has proper frontmatter:

```yaml
---
title: Your Note Title
date: 2025-01-01
tags: [tag1, tag2]
---
```

### 4. Build and deploy

```bash
npm run build
```

The static site is generated in `dist/`. Deploy to **Vercel**, **Netlify**, **Cloudflare Pages**, or any static host.

## What's Next?

In future posts, I'll cover:
- Customizing the theme
- Adding graph analytics with graphology
- Setting up search with Pagefind
