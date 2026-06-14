let handlerAttached = false;

/**
 * Create copy buttons on all code blocks and set up delegated click handling.
 * Safe to call multiple times — subsequent calls are no-ops.
 */
export function initCopyButtons(): void {
  // Attach delegated click handler once
  if (!handlerAttached) {
    document.addEventListener('click', async (e) => {
      const btn = (e.target as HTMLElement).closest('.copy-code');
      if (!btn || !(btn instanceof HTMLButtonElement)) return;

      e.preventDefault();
      const pre = btn.closest('pre');
      const code = pre?.querySelector('code');
      const text = code?.textContent ?? '';

      try {
        await navigator.clipboard.writeText(text);
      } catch {
        // Fallback for older browsers / insecure contexts
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        textarea.remove();
      }

      btn.textContent = 'Copied!';
      setTimeout(() => {
        btn.textContent = 'Copy';
      }, 1500);
    });
    handlerAttached = true;
  }

  // Create buttons on code blocks (skip blocks that already have one)
  document.querySelectorAll('pre.astro-code').forEach((pre) => {
    if (pre.querySelector('.copy-code')) return;

    const btn = document.createElement('button');
    btn.className = 'copy-code';
    btn.textContent = 'Copy';
    btn.setAttribute('aria-label', 'Copy code to clipboard');
    pre.appendChild(btn);
  });
}
