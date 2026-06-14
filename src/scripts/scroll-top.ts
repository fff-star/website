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
