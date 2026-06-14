// @ts-check
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import remarkWikiLink from './src/lib/remark-wiki-link.mjs';
import remarkMark from './src/lib/remark-mark.mjs';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import rehypeCallouts from 'rehype-callouts';
import rehypeSlug from 'rehype-slug';
import rehypeImgAttrs from './src/lib/rehype-img-attrs.ts';

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
      remarkMark,
      remarkMath,
    ],
    rehypePlugins: [
      rehypeCallouts,
      [rehypeKatex, { throwOnError: false }],
      rehypeSlug,
      rehypeImgAttrs,
    ],
  },
  vite: {
    ssr: { noExternal: [] },
    resolve: {
      alias: {
        'react-force-graph-2d': 'react-force-graph-2d',
        'force-graph': 'force-graph',
      },
    },
  },
});
