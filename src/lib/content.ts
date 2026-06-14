import { getCollection } from 'astro:content';
import type { Locale } from '../content.config';

/** Get published blog posts for a given locale, sorted by date descending. */
export async function getBlogPosts(locale: Locale) {
  const posts = await getCollection('blog', ({ data, id }) =>
    !data.draft && id.startsWith(`${locale}/`),
  );
  return [...posts].sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

/** Get published docs posts for a given locale, sorted by date descending. */
export async function getDocsPosts(locale: Locale) {
  const posts = await getCollection('docs', ({ data, id }) =>
    !data.draft && id.startsWith(`${locale}/`),
  );
  return [...posts].sort((a, b) => b.data.date.getTime() - a.data.date.getTime());
}

/** Get published notes for a given locale. */
export async function getNotes(locale: Locale) {
  return getCollection('notes', ({ data, id }) =>
    data.publish && !data.draft && id.startsWith(`${locale}/`),
  );
}
