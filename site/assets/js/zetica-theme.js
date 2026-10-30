/**
 * ZETICA Light / Dark Mode & Logo Inversion Engine
 * Synchronizes document theme, navigation moon/sun toggle,
 * header/hero/footer logo inversion, and Three.js 3D galaxy scene.
 */

(function () {
  'use strict';

  // SVG Icons for Moon and Sun
  const MOON_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-moon h-4 w-4" aria-hidden="true"><path d="M20.985 12.486a9 9 0 1 1-9.473-9.472c.405-.022.617.46.402.803a6 6 0 0 0 8.268 8.268c.344-.215.825-.004.803.401"></path></svg>`;
  
  const SUN_SVG = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-sun h-4 w-4" aria-hidden="true"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2"></path><path d="M12 20v2"></path><path d="m4.93 4.93 1.41 1.41"></path><path d="m17.66 17.66 1.41 1.41"></path><path d="M2 12h2"></path><path d="M20 12h2"></path><path d="m6.34 17.66-1.41 1.41"></path><path d="m19.07 4.93-1.41 1.41"></path></svg>`;

  function getStoredTheme() {
    try {
      const saved = localStorage.getItem('artcraft-theme') || localStorage.getItem('zetica-theme');
      if (saved === 'dark' || saved === 'light') return saved;
    } catch (e) {}
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    try {
      localStorage.setItem('artcraft-theme', theme);
      localStorage.setItem('zetica-theme', theme);
    } catch (e) {}

    // Update all theme toggle buttons
    const btns = document.querySelectorAll('button[aria-label="Toggle color theme"], #theme-toggle, .theme-toggle-btn');
    btns.forEach(btn => {
      // In dark mode show Sun (click to go light); in light mode show Moon (click to go dark)
      btn.innerHTML = theme === 'dark' ? SUN_SVG : MOON_SVG;
    });

    // Notify galaxy and other components
    window.dispatchEvent(new CustomEvent('zetica-theme-change', { detail: { theme: theme } }));
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || getStoredTheme();
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  }

  function initTheme() {
    const initial = getStoredTheme();
    applyTheme(initial);

    // Wire click listener to theme buttons
    document.addEventListener('click', (e) => {
      const btn = e.target.closest('button[aria-label="Toggle color theme"], #theme-toggle, .theme-toggle-btn, button:has(.lucide-moon), button:has(.lucide-sun)');
      if (btn) {
        e.preventDefault();
        e.stopPropagation();
        toggleTheme();
      }
    });

    // Watch OS system preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
      try {
        const saved = localStorage.getItem('artcraft-theme') || localStorage.getItem('zetica-theme');
        if (!saved) {
          applyTheme(e.matches ? 'dark' : 'light');
        }
      } catch (err) {}
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTheme);
  } else {
    initTheme();
  }

  window.zeticaToggleTheme = toggleTheme;
  window.zeticaApplyTheme = applyTheme;
})();
