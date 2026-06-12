import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const notes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/notes' }),
  schema: z.object({
    title: z.string().default('Untitled'),
    date: z.coerce.date().optional(),
    updated: z.coerce.date().optional(),
    tags: z.array(z.coerce.string()).default([]),
    publish: z.boolean().default(true),
    aliases: z.array(z.coerce.string()).default([]),
    description: z.string().default(''),
    draft: z.boolean().default(false),
  }),
});

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    tags: z.array(z.coerce.string()).default([]),
    description: z.string(),
    draft: z.boolean().default(false),
    cover: z.string().optional(),
  }),
});

export const collections = { notes, blog };
