import { dict, type Locale, type TranslationKey, defaultLocale } from './dict.ts';

export { type Locale, type TranslationKey, defaultLocale };

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
 * Build a locale-prefixed path.
 * path("/blog/", "en") → "/en/blog/"
 */
export function localePath(path: string, locale: Locale): string {
  const clean = path.replace(/\/$/, '') || '';
  return `/${locale}${clean}`;
}

/**
 * Get the other locale (for language switcher).
 */
export function otherLocale(locale: Locale): Locale {
  return locale === 'en' ? 'zh' : 'en';
}
