import { dict, type Locale, type TranslationKey, defaultLocale } from './dict';

/**
 * Resolve the current locale from a URL pathname or query param.
 * Production: "/en/notes/" → "en", "/notes/" → "zh"
 * Dev fallback: "/notes/?lang=en" → "en"
 */
export function localeFromPath(pathname: string, search?: string): Locale {
  // Check path prefix first (production)
  const seg = pathname.split('/')[1];
  if (seg === 'en') return 'en';
  // Check ?lang= query param (dev mode fallback)
  if (search) {
    const m = search.match(/[?&]lang=([a-z]{2})/);
    if (m && (m[1] === 'en' || m[1] === 'zh')) return m[1] as Locale;
  }
  return defaultLocale;
}

/**
 * Return a translation function bound to a locale.
 * Usage: const t = useTranslations(locale); t('nav.notes')
 */
export function useTranslations(locale: Locale) {
  return function t(key: TranslationKey, vars?: Record<string, string | number>): string {
    let text = dict[locale][key] ?? dict[defaultLocale][key] ?? key;
    if (vars) {
      for (const [k, v] of Object.entries(vars)) {
        text = text.replace(`{${k}}`, String(v));
      }
    }
    return text;
  };
}

/**
 * Get the locale-prefixed path for a given locale.
 * "/notes/" in "en" → "/en/notes/"
 */
export function localePath(path: string, locale: Locale): string {
  const clean = path.replace(/\/$/, '') || '';
  if (locale === defaultLocale) return clean || '/';
  return `/${locale}${clean}`;
}
