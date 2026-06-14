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
  site: 'https://fff-star.pages.dev',
  integrations: [react()],
  markdown: {
    allowDangerousHtml: true,
    syntaxHighlight: 'shiki',
    shikiConfig: {
      themes: { light: 'github-dark', dark: 'github-dark' },
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
    ssr: { noExternal: [] },
    resolve: {
      alias: {
        'react-force-graph-2d': 'react-force-graph-2d',
        'force-graph': 'force-graph',
      },
    },
  },
});
