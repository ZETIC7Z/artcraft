/**
 * ZETICA Scroll Ruler & Queued Section Navigation
 * Faithful port of storytold/artcraft scroll-ruler.tsx & heading-flow.tsx
 * Renders the bottom-right section queue and tracks scroll progress with active highlights.
 */

(function () {
  'use strict';

  function initScrollRuler() {
    // Only mount on pages with a main narrative flow
    const hero = document.getElementById('hero');
    if (!hero) return;

    // Check if already mounted
    if (document.getElementById('ruler-bottom-queue')) return;

    // Create the Bottom-Right Queue Container
    const queue = document.createElement('div');
    queue.id = 'ruler-bottom-queue';
    queue.setAttribute('aria-label', 'Section navigation');

    const sections = [
      { id: 'apps', label: 'ZETICA APPS' },
      { id: 'studio', label: 'ZETICA STUDIO', href: './download.html' },
      { id: 'features', label: 'FEATURES' },
      { id: 'ownership', label: 'OWNERSHIP' },
      { id: 'community', label: 'COMMUNITY' },
      { id: 'start', label: 'GET STARTED' }
    ];

    sections.forEach(sec => {
      const link = document.createElement('a');
      link.href = sec.href || `#${sec.id}`;
      link.className = 'ruler-queue-item';
      link.dataset.target = sec.id;
      link.textContent = sec.label;

      link.addEventListener('click', (e) => {
        if (sec.href && !sec.href.startsWith('#')) return;
        const targetEl = document.getElementById(sec.id);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({ behavior: 'smooth' });
        }
      });

      queue.appendChild(link);
    });

    document.body.appendChild(queue);

    // Track Active Section on Scroll
    const items = queue.querySelectorAll('.ruler-queue-item');

    function onScroll() {
      const scrollPos = window.scrollY + window.innerHeight * 0.35;
      let activeId = '';

      sections.forEach(sec => {
        const el = document.getElementById(sec.id);
        if (el) {
          const top = el.offsetTop;
          const height = el.offsetHeight;
          if (scrollPos >= top && scrollPos < top + height) {
            activeId = sec.id;
          }
        }
      });

      items.forEach(item => {
        if (item.dataset.target === activeId) {
          item.classList.add('active');
        } else {
          item.classList.remove('active');
        }
      });
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initScrollRuler);
  } else {
    initScrollRuler();
  }
})();
