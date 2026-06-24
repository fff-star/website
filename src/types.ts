/** Locale type and constants — separate from Astro content config so i18n modules can import without pulling in astro:content. */
export type Locale = 'en' | 'zh';
export const locales: Locale[] = ['en', 'zh'];
export const defaultLocale: Locale = 'en';
