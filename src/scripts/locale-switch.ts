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
