import type { Locale } from '../content.config';

export interface SiteConfig {
  title: string;
  description: string; // may contain **markdown**
  author: string;
}

const configs: Record<Locale, SiteConfig> = {
  en: {
    title: 'fff-star',
    description:
      'Hi, I\'m fff-star. I am currently a **Sophomore (2nd-year)** undergraduate student. I am interested in **Cryptography**, **Coding Theory** and **Mathematics**.',
    author: 'fff',
  },
  zh: {
    title: 'fff-star',
    description:
      '你好，我是 fff-star，目前是一名**大二**本科生。我对**密码学**、**编码理论**和**数学**感兴趣。',
    author: 'fff',
  },
};

export function getSiteConfig(locale: Locale): SiteConfig {
  return configs[locale];
}

/** Shared across locales — not language-dependent */
export const SITE = {
  url: 'https://fff-star.pages.dev',
  social: {
    github: 'https://github.com/fff-star',
    codeberg: 'https://codeberg.org/fff-star',
  },
} as const;
