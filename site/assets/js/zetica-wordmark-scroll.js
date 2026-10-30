/**
 * ZETICA Hero Wordmark Intro Reveal Animation
 * Ports storytold/artcraft hero-wordmark.tsx & intro choreography
 * Orchestrates intro monogram glide, blade-clip letter reveal,
 * and headlines/CTA entrance. Hands off scroll-driven flight to zetica-scroll-ruler.js.
 */

(function () {
  'use strict';

  function initWordmarkAnimation() {
    const masthead = document.getElementById('hero-wordmark-masthead');
    if (!masthead) return;

    const letters = Array.from(document.querySelectorAll('.wm-letter'));
    const revealEls = Array.from(document.querySelectorAll('[data-reveal="true"]'));

    // Check prefers-reduced-motion
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (reducedMotion) {
      revealEls.forEach(el => {
        el.style.opacity = '1';
        el.style.filter = 'none';
        el.style.transform = 'none';
        el.style.visibility = 'visible';
      });
      return;
    }

    // Intro Animation (Staggered letter rise and blur focus, matching ArtCraft)
    if (typeof gsap !== 'undefined') {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

      // Initial state: letters start slightly offset with soft blur
      gsap.set(letters, { y: 24, opacity: 0, filter: 'blur(10px)' });

      // Animate letters to resting position
      tl.to(letters, {
        y: 0,
        opacity: 1,
        filter: 'blur(0px)',
        stagger: 0.05,
        duration: 0.8,
        ease: 'power3.out',
        onComplete: () => {
          letters.forEach(l => {
            l.style.filter = '';
            l.style.transform = '';
          });
        }
      });

      // Reveal headline, copy, and download buttons
      tl.to(revealEls, {
        opacity: 1,
        filter: 'blur(0px)',
        transform: 'translate(0px, 0px)',
        visibility: 'visible',
        stagger: 0.1,
        duration: 0.8,
        ease: 'power2.out'
      }, '-=0.4');
    } else {
      // Fallback if GSAP is not yet loaded
      revealEls.forEach(el => {
        el.style.opacity = '1';
        el.style.filter = 'none';
        el.style.transform = 'none';
        el.style.visibility = 'visible';
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWordmarkAnimation);
  } else {
    initWordmarkAnimation();
  }
})();
