import { getBlogPosts, getDocsPosts } from '../lib/content';

const SITE = 'https://fff-star.pages.dev';

async function urls(locale, posts, pathPrefix) {
  return posts
    .map((p) => {
      const slug = p.id.replace(new RegExp(`^${locale}/`), '').replace(/\.md$/, '');
      return `  <url><loc>${SITE}/${locale}/${pathPrefix}/${slug}/</loc><lastmod>${p.data.updated?.toISOString() ?? p.data.date.toISOString()}</lastmod></url>`;
    })
    .join('\n');
}

export async function GET() {
  const enBlog = await getBlogPosts('en');
  const zhBlog = await getBlogPosts('zh');
  const enDocs = await getDocsPosts('en');
  const zhDocs = await getDocsPosts('zh');

  const staticPages = [
    '/en/', '/zh/',
    '/en/blog/', '/zh/blog/',
    '/en/docs/', '/zh/docs/',
    '/en/notes/', '/zh/notes/',
    '/en/search/', '/zh/search/',
  ];

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${staticPages.map((p) => `  <url><loc>${SITE}${p}</loc></url>`).join('\n')}
${await urls('en', enBlog, 'blog')}
${await urls('zh', zhBlog, 'blog')}
${await urls('en', enDocs, 'docs')}
${await urls('zh', zhDocs, 'docs')}
</urlset>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml; charset=utf-8' },
  });
}
