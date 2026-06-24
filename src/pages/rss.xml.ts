import rss from '@astrojs/rss';
import { getBlogPosts } from '../lib/content';
import { getSiteConfig } from '../i18n/site';
import type { Locale } from '../types.ts';

export async function GET() {
  const site = 'https://fff-star.pages.dev';
  const enPosts = await getBlogPosts('en');
  const enConfig = getSiteConfig('en');

  return rss({
    title: enConfig.title,
    description: enConfig.description,
    site,
    items: enPosts.map((post) => ({
      title: post.data.title,
      description: post.data.description ?? '',
      pubDate: post.data.date,
      link: `/en/blog/${post.id.replace(/^en\//, '').replace(/\.md$/, '')}/`,
    })),
    customData: `<language>en</language>`,
  });
}
