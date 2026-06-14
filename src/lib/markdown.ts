/**
 * Minimal markdown utilities — only what the site actually needs.
 * No dependency, no parser, just targeted regex transforms.
 */

const BOLD_RE = /\*\*(.+?)\*\*/g;

/** Escape HTML entities so captured text doesn't break markup. */
function escapeHtml(text: string): string {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

/** Remove **bold** markers (for meta tags, plain text). */
export function stripBold(text: string): string {
  return text.replace(BOLD_RE, (_, content) => content);
}

/** Convert **bold** to <strong> (for inline HTML). */
export function boldToHtml(text: string): string {
  return text.replace(BOLD_RE, (_, content) => `<strong>${escapeHtml(content)}</strong>`);
}
