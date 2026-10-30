/**
 * ZETICA Hero Wordmark Intro & Scroll-Driven Transfer Animation
 * Ports storytold/artcraft hero-wordmark.tsx & heading-flow.tsx
 * Orchestrates intro monogram glide, blade-clip letter reveal,
 * and scroll-driven wordmark transfer into the top navbar/ruler.
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

    // 1. Intro Animation (Monogram glide + blade letter slide)
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
        ease: 'power2.out'
      }, '-=0.3');

      // 2. Scroll-Driven Wordmark Transfer (HeadingFlow)
      // When scrolling out of the hero, the wordmark condenses and transfers upward
      const nav = document.getElementById('site-nav') || document.querySelector('nav');
      const navH = nav ? nav.offsetHeight : 48;

      let ticking = false;
      function onScroll() {
        if (!ticking) {
          requestAnimationFrame(updateScrollMorph);
          ticking = true;
        }
      }

      function updateScrollMorph() {
        ticking = false;
        const scrollY = window.scrollY || window.pageYOffset || 0;
        const heroHeight = window.innerHeight || 800;
        
        // Progress of hero exit: 0 to 1 over first 350px
        const maxScroll = Math.min(380, heroHeight * 0.5);
        const progress = Math.max(0, Math.min(1, scrollY / maxScroll));

        if (progress <= 0) {
          masthead.style.transform = '';
          masthead.style.opacity = '1';
          letters.forEach(l => l.style.transform = '');
          return;
        }

        // Smooth cubic ease
        const ease = progress < 0.5 ? 4 * progress * progress * progress : 1 - Math.pow(-2 * progress + 2, 3) / 2;

        // Scale down from full hero size to compact header title
        const scale = 1 - ease * 0.42;
        
        // Translate upward towards the top edge / nav slot
        const translateY = -ease * 140;

        // Letter spreading / condensation
        masthead.style.transform = `translate3d(0px, ${translateY.toFixed(1)}px, 0px) scale(${scale.toFixed(3)})`;
        masthead.style.transformOrigin = 'center center';
        
        // Fade gracefully as user scrolls past into features
        if (progress > 0.85) {
          const fade = 1 - ((progress - 0.85) / 0.15);
          masthead.style.opacity = Math.max(0, fade).toFixed(2);
        } else {
          masthead.style.opacity = '1';
        }

        // Slight progressive letter stagger
        letters.forEach((l, idx) => {
          const letterOffset = (idx - 2.5) * (1 - ease) * 2;
          l.style.transform = `translate3d(${letterOffset.toFixed(1)}px, 0px, 0px)`;
        });
      }

      window.addEventListener('scroll', onScroll, { passive: true });
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
