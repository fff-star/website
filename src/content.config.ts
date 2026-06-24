import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Shared schemas — content is organized in locale subdirectories (en/ zh/)
// so a single collection per content type serves all languages.

const blogSchema = z.object({
  title: z.string(),
  date: z.coerce.date(),
  updated: z.coerce.date().optional(),
  description: z.string(),
  draft: z.boolean().default(false),
  cover: z.string().optional(),
});

const docsSchema = z.object({
  title: z.string(),
  date: z.coerce.date(),
  updated: z.coerce.date().optional(),
  description: z.string(),
  draft: z.boolean().default(false),
  cover: z.string().optional(),
});

const notesSchema = z.object({
  title: z.string().default('Untitled'),
  date: z.coerce.date().optional(),
  updated: z.coerce.date().optional(),
  tags: z.array(z.coerce.string()).default([]),
  publish: z.boolean().default(true),
  aliases: z.array(z.coerce.string()).default([]),
  description: z.string().default(''),
  draft: z.boolean().default(false),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: blogSchema,
});

const docs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/docs' }),
  schema: docsSchema,
});

const notes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/notes' }),
  schema: notesSchema,
});

export const collections = { blog, docs, notes };

// --- Locale helpers (canonical definition in src/types.ts) ---
export { type Locale, locales, defaultLocale } from './types.ts';
