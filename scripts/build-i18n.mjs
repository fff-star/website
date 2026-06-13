/**
 * Post-build script: generate /en/ locale pages by duplicating
 * the zh output and patching locale-dependent attributes and links.
 */
import fs from 'node:fs';
import path from 'node:path';

const DIST = 'dist';
const EN_DIR = path.join(DIST, 'en');

// Remove old en dir
fs.rmSync(EN_DIR, { recursive: true, force: true });

// Walk dist and mirror all HTML files to /en/
function walk(dir) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const e of entries) {
    const src = path.join(dir, e.name);
    if (e.isDirectory() && e.name !== '_astro' && e.name !== 'en' && e.name !== 'pagefind') {
      walk(src);
    } else if (e.name.endsWith('.html')) {
      const rel = path.relative(DIST, src);
      const dest = path.join(EN_DIR, rel);
      fs.mkdirSync(path.dirname(dest), { recursive: true });

      let html = fs.readFileSync(src, 'utf-8');

      // Switch lang attribute
      html = html.replace(/lang="zh"/g, 'lang="en"');

      // Fix nav/homepage links to point to /en/ versions
      html = html.replace(/href="\/notes\//g, 'href="/en/notes/');
      html = html.replace(/href="\/blog\//g, 'href="/en/blog/');
      html = html.replace(/href="\/tags\//g, 'href="/en/tags/');
      html = html.replace(/href="\/search\//g, 'href="/en/search/');
      html = html.replace(/href="\/rss.xml"/g, 'href="/en/rss.xml"');

      // Fix locale switch: "EN" → "中文", and its href /en/... → /...
      html = html.replace(
        /<a href="\/en(\/[^"]*)" class="locale-switch"[^>]*>EN</g,
        '<a href="$1" class="locale-switch" aria-label="Switch to zh">中文<'
      );

      // Fix canonicals
      html = html.replace(
        /<link rel="canonical" href="https:\/\/fff-star\.pages\.dev(\/[^"]*)"/g,
        '<link rel="canonical" href="https://fff-star.pages.dev/en$1"'
      );

      // Fix og:url
      html = html.replace(
        /<meta property="og:url" content="https:\/\/fff-star\.pages\.dev(\/[^"]*)"/g,
        '<meta property="og:url" content="https://fff-star.pages.dev/en$1"'
      );

      fs.writeFileSync(dest, html);
    }
  }
}

walk(DIST);

// Copy root-level assets to /en/
const rootFiles = ['favicon.ico', 'favicon.svg', 'rss.xml'];
for (const f of rootFiles) {
  const src = path.join(DIST, f);
  if (fs.existsSync(src)) {
    fs.copyFileSync(src, path.join(EN_DIR, f));
  }
}

console.log('✓ Generated /en/ locale pages');
