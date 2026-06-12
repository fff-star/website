// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwindcss from '@tailwindcss/vite';
import remarkWikiLink from './src/lib/remark-wiki-link.mjs';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeCallouts from 'rehype-callouts';
import rehypeSlug from 'rehype-slug';

// https://astro.build/config
export default defineConfig({
  site: 'https://fff.sh',
  integrations: [react()],
  markdown: {
    syntaxHighlight: 'shiki',
    shikiConfig: {
      // Always use dark themes — PaperMod always renders code blocks on dark bg
      themes: {
        light: 'github-dark',
        dark: 'github-dark',
      },
    },
    remarkPlugins: [
      remarkWikiLink,
      remarkMath,
    ],
    rehypePlugins: [
      rehypeCallouts,
      [rehypeKatex, { throwOnError: false }],
      rehypeSlug,
    ],
  },
  vite: {
    plugins: [tailwindcss()],
    ssr: {
      noExternal: [], // Let Astro handle all SSR
    },
    // Prevent SSR from trying to evaluate browser-only packages
    resolve: {
      alias: {
        'react-force-graph-2d': 'react-force-graph-2d',
        'force-graph': 'force-graph',
      },
    },
  },
});
