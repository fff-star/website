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
  const next: Theme =
    document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark';
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
