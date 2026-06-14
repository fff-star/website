/**
 * Returns true if the user has requested reduced motion.
 * Use this before any JS-driven animation or smooth scroll.
 */
export function prefersReducedMotion(): boolean {
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}
