import { visit } from 'unist-util-visit';
import { imageSize } from 'image-size';
import { resolve } from 'path';
import { readFileSync, existsSync } from 'fs';
import type { Element } from 'hast';
import type { VFile } from 'vfile';

/**
 * Rehype plugin that:
 * 1. Adds loading="lazy" and decoding="async" to all <img> elements
 * 2. Reads local image dimensions at build time and adds width/height attributes
 *    to prevent Cumulative Layout Shift (CLS)
 *
 * Remote images (http://, https://) are skipped for dimension detection
 * but still get loading="lazy".
 */
export default function rehypeImgAttrs() {
  return (tree: any, file: VFile) => {
    const fileDir = file.dirname;

    visit(tree, 'element', (node: Element) => {
      if (node.tagName !== 'img') return;

      const src = node.properties.src as string | undefined;
      if (!src) return;

      // Always add lazy loading and async decoding
      node.properties.loading = 'lazy';
      node.properties.decoding = 'async';

      // Skip remote images for dimension detection
      if (src.startsWith('http://') || src.startsWith('https://')) return;

      // Resolve local image relative to the markdown file
      if (!fileDir) return;

      const imgPath = resolve(fileDir, src);
      if (!existsSync(imgPath)) return;

      try {
        const buf = readFileSync(imgPath);
        const dims = imageSize(buf);
        if (dims.width && dims.height) {
          node.properties.width = String(dims.width);
          node.properties.height = String(dims.height);
        }
      } catch {
        // Skip silently — not all file types are supported
      }
    });
  };
}
