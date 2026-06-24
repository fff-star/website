import { getCollection } from 'astro:content';
import type { Locale } from '../content.config';
import { extractWikilinks, getFolder, getFilename } from './graph-helpers.ts';

interface GraphNode {
  id: string;
  name: string;
  val: number;
  backlinks: number;
  color?: string;
  url: string;
}

interface GraphLink {
  source: string;
  target: string;
  weight: number;
}

export interface GraphData {
  nodes: GraphNode[];
  links: GraphLink[];
  folder?: string;
}

const TAG_COLORS = [
  '#4a90d9', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6',
  '#1abc9c', '#e67e22', '#3498db', '#c0392b', '#27ae60',
];

// extractWikilinks, getFolder, getFilename — imported from ./graph-helpers.ts

/** List all unique folders in the vault for a given locale */
export async function getFolders(locale: Locale): Promise<string[]> {
  const notes = await getCollection('notes', ({ data, id }) =>
    data.publish && !data.draft && id.startsWith(`${locale}/`),
  );
  const folders = new Set<string>();
  for (const note of notes) {
    const id = note.id.replace(/\.md$/, '');
    const folder = getFolder(id);
    if (folder) folders.add(folder);
  }
  return [...folders].sort();
}

/**
 * Build graph scoped to a single folder within a locale.
 * Wiki-links only connect notes within the same folder.
 * Accepts optional pre-fetched notes to avoid repeated getCollection calls.
 */
export async function buildFolderGraph(
  folder: string,
  locale: Locale,
  preFetchedNotes?: Awaited<ReturnType<typeof getCollection<'notes'>>>,
): Promise<GraphData> {
  const allNotes = preFetchedNotes ?? await getCollection('notes', ({ data, id }) =>
    data.publish && !data.draft && id.startsWith(`${locale}/`),
  );

  // Filter to this folder
  const prefix = `${locale}/${folder}/`;
  const notes = allNotes.filter((n) => {
    const id = n.id.replace(/\.md$/, '');
    return id.startsWith(prefix);
  });

  // Build map of filename → full id for link resolution
  const nameToId = new Map<string, string>();
  for (const n of notes) {
    const id = n.id.replace(/\.md$/, '');
    // Slugify filename to match extractWikilinks output
    const slugged = getFilename(id).toLowerCase().replace(/\s+/g, '-');
    nameToId.set(slugged, id);
  }

  const linkSet = new Map<string, number>();
  const backlinksMap = new Map<string, number>();

  for (const note of notes) {
    const sourceId = note.id.replace(/\.md$/, '');
    const content = note.body ?? '';
    const targets = extractWikilinks(content);

    backlinksMap.set(sourceId, backlinksMap.get(sourceId) ?? 0);

    for (const target of targets) {
      // Resolve target within the same folder
      const resolved = nameToId.get(target) ?? target;
      // Only add edge if target is in this folder
      if (!nameToId.has(target) && resolved === target) continue;

      const key = `${sourceId}:${resolved}`;
      linkSet.set(key, (linkSet.get(key) ?? 0) + 1);
      backlinksMap.set(resolved, (backlinksMap.get(resolved) ?? 0) + 1);
    }
  }

  const nodes: GraphNode[] = [];
  const seenIds = new Set<string>();

  for (const note of notes) {
    const id = note.id.replace(/\.md$/, '');
    if (seenIds.has(id)) continue;
    seenIds.add(id);

    const backlinks = backlinksMap.get(id) ?? 0;
    const val = Math.max(1, Math.log2(backlinks + 1) * 2);

    const firstTag = note.data.tags?.[0];
    const colorIdx = firstTag
      ? [...firstTag].reduce((acc, c) => acc + c.charCodeAt(0), 0) % TAG_COLORS.length
      : 0;

    nodes.push({
      id,
      name: note.data.title,
      val,
      backlinks,
      color: TAG_COLORS[colorIdx],
      url: `/${locale}/notes/${id.split('/').slice(1).join('/')}/`,
    });
  }

  const links: GraphLink[] = [];
  for (const [key, weight] of linkSet) {
    const [source, target] = key.split(':');
    if (seenIds.has(source) && seenIds.has(target)) {
      links.push({ source, target, weight });
    }
  }

  return { nodes, links, folder };
}

/**
 * Build graph for ALL folders combined (overview) for a given locale.
 * Edges only connect notes within the same folder.
 */
export async function buildGraph(locale: Locale): Promise<GraphData> {
  const folders = await getFolders(locale);
  // Fetch notes once, share across all folder graphs
  const allNotes = await getCollection('notes', ({ data, id }) =>
    data.publish && !data.draft && id.startsWith(`${locale}/`),
  );
  const allNodes: GraphNode[] = [];
  const allLinks: GraphLink[] = [];

  for (const folder of folders) {
    const data = await buildFolderGraph(folder, locale, allNotes);
    allNodes.push(...data.nodes);
    allLinks.push(...data.links);
  }

  return { nodes: allNodes, links: allLinks };
}

/**
 * Local graph: current note + its neighbors, all within the same folder and locale.
 */
export async function buildLocalGraph(currentSlug: string, locale: Locale): Promise<GraphData> {
  // currentSlug may or may not have locale prefix already
  const id = currentSlug.replace(/\.md$/, '');
  const folder = getFolder(id.startsWith(`${locale}/`) ? id : `${locale}/${id}`);
  const folderGraph = await buildFolderGraph(folder, locale);

  const currentId = id.startsWith(`${locale}/`) ? id : `${locale}/${id}`;

  const neighborIds = new Set<string>();
  neighborIds.add(currentId);

  for (const link of folderGraph.links) {
    if (link.source === currentId) neighborIds.add(link.target);
    if (link.target === currentId) neighborIds.add(link.source);
  }

  return {
    nodes: folderGraph.nodes.filter((n) => neighborIds.has(n.id)),
    links: folderGraph.links.filter(
      (l) => neighborIds.has(l.source) || neighborIds.has(l.target),
    ),
    folder: folderGraph.folder,
  };
}
