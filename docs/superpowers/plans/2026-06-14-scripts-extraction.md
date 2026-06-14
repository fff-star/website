# Scripts Extraction Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extract scattered inline JS from Astro components into shareable `src/scripts/` modules with consistent conventions, while keeping performance-critical inline scripts in place.

**Architecture:** Five focused TypeScript modules under `src/scripts/`, each with a single `init*()` or `watch*()` export. Astro components import and call them in processed `<script>` tags. The anti-flash theme script, Pagefind search, and graph loader stay inline (they have hard runtime ordering / page-specific constraints). Event handlers switch from per-element `addEventListener` to document-level delegation where practical.

**Tech Stack:** TypeScript (compiled by Vite via Astro), vanilla DOM APIs, no runtime dependencies.

---

## File Map

```
src/scripts/
  motion.ts         — prefersReducedMotion() utility (zero deps)
  theme.ts          — getTheme(), setTheme(), toggleTheme(), watchSystemTheme()
  copy-code.ts      — initCopyButtons() with delegated click handler
  scroll-top.ts     — initScrollTop() with motion-aware smooth scroll
  locale-switch.ts  — initLocaleSwitch() with HEAD precheck

Modified:
  src/components/ui/ThemeToggle.astro      — import theme.ts, remove inline JS
  src/components/layout/Footer.astro       — import scroll-top.ts, remove inline JS
  src/components/layout/Header.astro       — import locale-switch.ts, remove inline JS
  src/components/layout/BaseLayout.astro   — import copy-code.ts + theme.ts, remove inline JS
```

### What stays inline (and why)

| Script | Location | Reason |
|--------|----------|--------|
| Theme anti-flash | `BaseLayout.astro` `is:inline` | Must run before first CSS paint |
| Pagefind search | `search.astro` | Page-specific, depends on `define:vars` for i18n strings |
| Copyright year | `Footer.astro` | One-liner `<time>` update, not worth a module |
| Graph loader | `graph-loader.js` | Already a separate file, CDN-dependent |

---

### Task 1: Create `src/scripts/motion.ts`

**Files:**
- Create: `src/scripts/motion.ts`
- Verify: `npm run build`

- [ ] **Step 1: Create the file**

```typescript
// src/scripts/motion.ts
/**
 * Returns true if the user has requested reduced motion.
 * Use this before any JS-driven animation or smooth scroll.
 */
export function prefersReducedMotion(): boolean {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}
```

- [ ] **Step 2: Verify it builds**

```bash
npm run build
```

Expected: build succeeds, no errors referencing the new file.

- [ ] **Step 3: Commit**

```bash
git add src/scripts/motion.ts
git commit -m "feat: add prefersReducedMotion utility

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 2: Create `src/scripts/theme.ts`

**Files:**
- Create: `src/scripts/theme.ts`

The theme logic is currently duplicated between:
- `BaseLayout.astro:41-53` (anti-flash: reads localStorage + system preference, sets `data-theme`)
- `ThemeToggle.astro:66-75` (toggle: flips the current theme)

This module centralizes get/set/toggle. The anti-flash script keeps its own minimal inline copy (it can't import modules — runs before Vite loads).

- [ ] **Step 1: Create the file**

```typescript
// src/scripts/theme.ts
type Theme = 'light' | 'dark';

const STORAGE_KEY = 'pref-theme';

/**
 * Resolve current theme: stored preference > system preference > light.
 */
export function getTheme(): Theme {
  if (typeof localStorage === 'undefined') return 'light';
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored === 'dark' || stored === 'light') return stored;
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

/**
 * Persist theme to DOM and localStorage.
 */
export function setTheme(theme: Theme): void {
  document.documentElement.dataset.theme = theme;
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    // localStorage may be unavailable (private browsing, storage full)
  }
}

/**
 * Toggle between light and dark, persist, return the new theme.
 */
export function toggleTheme(): Theme {
  const next: Theme = document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
  setTheme(next);
  return next;
}

/**
 * Watch for system theme changes. Only fires when no user preference is stored.
 * Returns an unsubscribe function.
 */
export function watchSystemTheme(onChange: (theme: Theme) => void): () => void {
  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  const handler = () => {
    if (!localStorage.getItem(STORAGE_KEY)) {
      onChange(mq.matches ? 'dark' : 'light');
    }
  };
  mq.addEventListener('change', handler);
  return () => mq.removeEventListener('change', handler);
}
```

- [ ] **Step 2: Verify it builds**

```bash
npm run build
```

Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
git add src/scripts/theme.ts
git commit -m "feat: add theme utility module (get, set, toggle, watch)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 3: Update ThemeToggle.astro to use theme.ts

**Files:**
- Modify: `src/components/ui/ThemeToggle.astro`

Replace the inline `document.getElementById('theme-toggle')?.addEventListener(...)` with an import from `theme.ts`.

- [ ] **Step 1: Replace the inline script**

Remove lines 66-75 from `src/components/ui/ThemeToggle.astro`:

```diff
- <script>
-   document.getElementById('theme-toggle')?.addEventListener('click', () => {
-     const html = document.documentElement;
-     if (html.dataset.theme === 'dark') {
-       html.dataset.theme = 'light';
-       localStorage.setItem('pref-theme', 'light');
-     } else {
-       html.dataset.theme = 'dark';
-       localStorage.setItem('pref-theme', 'dark');
-     }
-   });
- </script>
```

Add after the closing `</button>` tag (before `</script>` that was removed):

```astro
<script>
  import { toggleTheme } from '../../scripts/theme';
  document.getElementById('theme-toggle')?.addEventListener('click', toggleTheme);
</script>
```

- [ ] **Step 2: Verify the build and test manually**

```bash
npm run build && npm run preview
```

Manual check: open the site, click the theme toggle — it should switch light ↔ dark and persist across page reloads.

- [ ] **Step 3: Commit**

```bash
git add src/components/ui/ThemeToggle.astro
git commit -m "refactor: use theme module in ThemeToggle

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 4: Create `src/scripts/copy-code.ts`

**Files:**
- Create: `src/scripts/copy-code.ts`

The current copy-button code in `BaseLayout.astro:95-109` uses `querySelectorAll` + per-element `addEventListener`. This module uses event delegation (one listener on `document`) and is idempotent (safe to call multiple times — useful with Astro view transitions).

- [ ] **Step 1: Create the file**

```typescript
// src/scripts/copy-code.ts
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
```

- [ ] **Step 2: Verify it builds**

```bash
npm run build
```

Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
git add src/scripts/copy-code.ts
git commit -m "feat: add copy-code module with delegated event handling

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 5: Update BaseLayout.astro to use theme.ts + copy-code.ts

**Files:**
- Modify: `src/components/layout/BaseLayout.astro`

The BaseLayout currently has two inline `<script>` blocks:
1. Lines 41-53: anti-flash theme detection (`is:inline`) — **keep this, it must run before CSS**
2. Lines 95-109: copy button creation — **replace with import**

- [ ] **Step 1: Add system theme watching to the anti-flash script**

The anti-flash script currently sets theme once but doesn't react to system preference changes. Add a listener so theme stays in sync when no user preference is set:

In `BaseLayout.astro`, after the anti-flash script block (after line 53), add:

```astro
<script>
  // React to system theme changes when no explicit preference is stored
  import { setTheme } from '../scripts/theme';

  const mq = window.matchMedia('(prefers-color-scheme: dark)');
  mq.addEventListener('change', () => {
    if (!localStorage.getItem('pref-theme')) {
      setTheme(mq.matches ? 'dark' : 'light');
    }
  });
</script>
```

- [ ] **Step 2: Replace the copy-button inline script**

Remove lines 95-109 (the `document.querySelectorAll('pre.astro-code').forEach(...)` block):

```diff
-     <!-- Copy button for code blocks -->
-     <script is:inline>
-       document.querySelectorAll('pre.astro-code').forEach((pre) => {
-         const btn = document.createElement('button');
-         btn.className = 'copy-code';
-         btn.textContent = 'Copy';
-         btn.addEventListener('click', async () => {
-           const code = pre.querySelector('code');
-           const text = code?.textContent ?? '';
-           await navigator.clipboard.writeText(text);
-           btn.textContent = 'Copied!';
-           setTimeout(() => (btn.textContent = 'Copy'), 1500);
-         });
-         pre.appendChild(btn);
-       });
-     </script>
```

Replace with:

```astro
    <!-- Initialize copy buttons on code blocks -->
    <script>
      import { initCopyButtons } from '../scripts/copy-code';
      initCopyButtons();
    </script>
```

- [ ] **Step 3: Verify build and manual test**

```bash
npm run build && npm run preview
```

Manual checks:
- Theme toggle works, persists across pages
- System theme change is picked up when no user preference is set
- Code copy buttons appear on code blocks, click copies text

- [ ] **Step 4: Commit**

```bash
git add src/components/layout/BaseLayout.astro
git commit -m "refactor: use theme + copy-code modules in BaseLayout

Add system theme change listener. Replace inline copy-button
script with initCopyButtons() import.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 6: Create `src/scripts/scroll-top.ts`

**Files:**
- Create: `src/scripts/scroll-top.ts`

Extracts the scroll-to-top button logic (visibility toggle + click handler) from `Footer.astro:52-83`. Uses `motion.ts` for the reduced-motion check.

- [ ] **Step 1: Create the file**

```typescript
// src/scripts/scroll-top.ts
import { prefersReducedMotion } from './motion';

/**
 * Initialize the scroll-to-top button.
 * - Shows button when scrolled past 400px
 * - Smooth scrolls to top on click (respects prefers-reduced-motion)
 */
export function initScrollTop(): void {
  const btn = document.getElementById('top-link');
  if (!btn) return;

  const updateVisibility = () => {
    btn.classList.toggle('hidden', window.scrollY <= 400);
  };

  // Check initial state (handles deep-link / browser restore)
  updateVisibility();

  // Throttled scroll listener
  let ticking = false;
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(() => {
        updateVisibility();
        ticking = false;
      });
      ticking = true;
    }
  });

  btn.addEventListener('click', () => {
    window.scrollTo({
      top: 0,
      behavior: prefersReducedMotion() ? 'auto' : 'smooth',
    });
  });
}
```

- [ ] **Step 2: Verify it builds**

```bash
npm run build
```

Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
git add src/scripts/scroll-top.ts
git commit -m "feat: add scroll-top module with motion-aware behavior

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 7: Update Footer.astro to use scroll-top.ts

**Files:**
- Modify: `src/components/layout/Footer.astro`

Replace the inline scroll-to-top script (lines 52-83) with an import. Keep the copyright-year one-liner inline (it's just 2 lines of DOM update).

- [ ] **Step 1: Replace the scroll-to-top script**

Remove lines 52-83 from `src/components/layout/Footer.astro`:

```diff
- <script>
-   // Keep copyright year current
-   const yearEl = document.getElementById('copyright-year');
-   if (yearEl) yearEl.textContent = new Date().getFullYear();
- 
-   const topLink = document.getElementById('top-link');
-   if (topLink) {
-     const updateVisibility = () => {
-       if (window.scrollY > 400) {
-         topLink.classList.remove('hidden');
-       } else {
-         topLink.classList.add('hidden');
-       }
-     };
-     // Check on load (deep-link, browser restore)
-     updateVisibility();
- 
-     let ticking = false;
-     window.addEventListener('scroll', () => {
-       if (!ticking) {
-         requestAnimationFrame(() => {
-           updateVisibility();
-           ticking = false;
-         });
-         ticking = true;
-       }
-     });
-     topLink.addEventListener('click', () => {
-       const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
-       window.scrollTo({ top: 0, behavior: prefersReduced ? 'auto' : 'smooth' });
-     });
-   }
- </script>
```

Replace with:

```astro
<script>
  // Keep copyright year current
  const yearEl = document.getElementById('copyright-year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  import { initScrollTop } from '../scripts/scroll-top';
  initScrollTop();
</script>
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

Expected: build succeeds.

- [ ] **Step 3: Manual test**

```bash
npm run preview
```

- Scroll down past 400px — button appears
- Click — smooth scrolls to top (or instant if reduced-motion is set)
- Page load without scroll — button stays hidden

- [ ] **Step 4: Commit**

```bash
git add src/components/layout/Footer.astro
git commit -m "refactor: use scroll-top module in Footer

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 8: Create `src/scripts/locale-switch.ts`

**Files:**
- Create: `src/scripts/locale-switch.ts`

- [ ] **Step 1: Create the file**

```typescript
// src/scripts/locale-switch.ts

/**
 * Initialize the locale switcher link.
 * On click, tries HEAD request to the translated page;
 * falls back to locale home page if 404.
 */
export function initLocaleSwitch(): void {
  const btn = document.getElementById('locale-switch');
  if (!btn) return;

  btn.addEventListener('click', async (e) => {
    e.preventDefault();
    const otherLocale = btn.dataset.otherLocale;
    if (!otherLocale) return;

    const target = window.location.pathname.replace(
      /^\/(en|zh)\//,
      `/${otherLocale}/`,
    );

    try {
      const res = await fetch(target, { method: 'HEAD' });
      window.location.href = res.ok ? target : `/${otherLocale}/`;
    } catch {
      window.location.href = `/${otherLocale}/`;
    }
  });
}
```

- [ ] **Step 2: Verify build**

```bash
npm run build
```

Expected: build succeeds.

- [ ] **Step 3: Commit**

```bash
git add src/scripts/locale-switch.ts
git commit -m "feat: add locale-switch module

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 9: Update Header.astro to use locale-switch.ts

**Files:**
- Modify: `src/components/layout/Header.astro`

- [ ] **Step 1: Replace the inline locale-switch script**

Remove lines 65-80 from `src/components/layout/Header.astro`:

```diff
- <script>
-   // Locale switcher: HEAD precheck, fallback to home
-   const btn = document.getElementById('locale-switch');
-   btn?.addEventListener('click', async (e) => {
-     e.preventDefault();
-     const otherLocale = btn.dataset.otherLocale!;
-     // Build target URL by replacing current locale prefix
-     const target = window.location.pathname.replace(/^\/(en|zh)\//, `/${otherLocale}/`);
-     try {
-       const res = await fetch(target, { method: 'HEAD' });
-       window.location.href = res.ok ? target : `/${otherLocale}/`;
-     } catch {
-       window.location.href = `/${otherLocale}/`;
-     }
-   });
- </script>
```

Replace with:

```astro
<script>
  import { initLocaleSwitch } from '../scripts/locale-switch';
  initLocaleSwitch();
</script>
```

- [ ] **Step 2: Verify build and manual test**

```bash
npm run build && npm run preview
```

Manual check: click the locale switcher (中文/EN) — should navigate to the translated version of the current page, or the locale home if the page doesn't exist in that language.

- [ ] **Step 3: Commit**

```bash
git add src/components/layout/Header.astro
git commit -m "refactor: use locale-switch module in Header

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### Task 10: Final integration test

**Files:** (none — verification only)

- [ ] **Step 1: Full build + preview**

```bash
npm run build && npm run preview
```

- [ ] **Step 2: Smoke test checklist**

Visit the preview URL and verify:

| Check | Expected |
|-------|----------|
| Page loads, no console errors | No red in DevTools |
| Theme toggle (click sun/moon icon) | Theme switches, persists on reload |
| System theme change (DevTools → Rendering → prefers-color-scheme) | Theme follows system when no user preference stored |
| Code block hover → Copy button appears | Button visible, click copies to clipboard |
| Scroll down > 400px → Top button appears | Button fades in, click scrolls to top |
| Locale switcher (中文/EN) | Navigates to translated page or locale home |
| Search page | Works as before (Pagefind was not touched) |
| Knowledge graph | Works as before (graph-loader was not touched) |

- [ ] **Step 3: Commit if any straggling changes**

```bash
git status
# Should show clean working tree — all changes committed
```

---

## Rollback Plan

Each task is an independent commit. If any task breaks, revert its commit:

```bash
git revert <commit-hash>
```

The anti-flash script in `BaseLayout.astro` is never touched by this plan (it stays as `is:inline`), so theme flash protection is preserved regardless.
