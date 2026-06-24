/**
 * Pure string helpers for the knowledge graph.
 * Extracted to avoid pulling astro:content into tests.
 */

/** Extract [[wiki-links]] from markdown content */
export function extractWikilinks(content: string): string[] {
  const regex = /\[\[([^\]|#]+?)(?:\|[^\]]+)?(?:#[^\]]+)?\]\]/g;
  const links: string[] = [];
  let match;
  while ((match = regex.exec(content)) !== null) {
    links.push(match[1].trim().toLowerCase().replace(/\s+/g, '-'));
  }
  return [...new Set(links)];
}

/** Get the folder path for a note id (e.g. "en/demos/hello-world" → "demos") */
export function getFolder(id: string): string {
  const parts = id.split('/');
  return parts.length >= 3 ? parts[1] : '';
}

/** Get just the filename from an id (e.g. "en/demos/hello-world" → "hello-world") */
export function getFilename(id: string): string {
  const idx = id.lastIndexOf('/');
  return idx === -1 ? id : id.slice(idx + 1);
}
