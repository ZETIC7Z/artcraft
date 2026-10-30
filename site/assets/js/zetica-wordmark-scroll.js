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

    const logo = document.getElementById('wm-letter-0');
    const letters = Array.from(document.querySelectorAll('.wm-letter:not(#wm-letter-0)'));
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

    // Intro Animation (Monogram glide + blade letter slide)
    if (typeof gsap !== 'undefined') {
      const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

      // Initial state
      gsap.set(logo, { x: 80, scale: 0.95, opacity: 0 });
      gsap.set(letters, { x: -40, opacity: 0, clipPath: 'inset(0% 100% 0% 0%)' });

      // Animate Monogram to resting position
      tl.to(logo, {
        x: 0,
        scale: 1,
        opacity: 1,
        duration: 0.8,
        ease: 'power2.out'
      });

      // Animate letters sliding out from behind the monogram
      tl.to(letters, {
        x: 0,
        opacity: 1,
        clipPath: 'inset(0% 0% 0% 0%)',
        stagger: 0.04,
        duration: 0.7,
        ease: 'power3.out'
      }, '-=0.4');

      // Reveal headline, copy, and download buttons
      tl.to(revealEls, {
        opacity: 1,
        filter: 'blur(0px)',
        transform: 'translate(0px, 0px)',
        visibility: 'visible',
        stagger: 0.1,
        duration: 0.8,
        ease: 'power2.out',
        onComplete: () => {
          // Clear any inline clipPath or transform from intro so HeadingFlow has full control
          letters.forEach(l => {
            l.style.clipPath = '';
            l.style.transform = '';
          });
          if (logo) logo.style.transform = '';
        }
      }, '-=0.3');
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
