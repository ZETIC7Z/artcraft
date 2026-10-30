/**
 * ZETICA Scroll Ruler & HeadingFlow Engine
 * Complete, faithful port of storytold/artcraft scroll-ruler.tsx & heading-flow.tsx
 * 
 * Features:
 * 1. Lenis Smooth Scrolling at 60fps
 * 2. Precision Vertical Scroll Ruler with 1% minor / 5% major ticks & odometer readout
 * 3. 3-Home HeadingFlow Lifecycle:
 *    - Bottom Queue: Horizontal links flush-aligned at bottom-right
 *    - Riding Rail: Vertically riding words with letters rotated -90deg on the right tick rail tracking scroll
 *    - Top Stack: Horizontal stack below navbar, with current active heading in bold display type
 * 4. Hero Wordmark Flight: ZETICA letters transfer from center hero into the top stack slot
 * 5. Full Light/Dark mode responsiveness with seamless theme reaction
 */

(function () {
  'use strict';

  function isDesktop() {
    return window.innerWidth >= 1024 && !/Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
  }

  function clamp01(x) { return Math.max(0, Math.min(1, x)); }
  function easeInOutCubic(t) { return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; }

  // 1. Initialize Lenis Smooth Scroll
  let lenisInstance = null;
  function initLenis() {
    if (typeof Lenis !== 'undefined' && !lenisInstance) {
      lenisInstance = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
        wheelMultiplier: 1.05,
        touchMultiplier: 1.8,
      });
      window.__lenis = lenisInstance;

      function raf(time) {
        lenisInstance.raf(time);
        requestAnimationFrame(raf);
      }
      requestAnimationFrame(raf);
    }
  }

  // 2. Metrics & Configuration
  const NAV_H = 48;
  const LAYOUT = {
    edgePad: 12,
    railW: 60,
    textPad: 20, // gap from tick rail to right-aligned text
    minorPct: 1,
    labelPct: 5,
    thresholdPct: 12, // 12% vh flip threshold
    headingPx: 32, // full size active heading
    ridingPx: 18,  // vertical riding word size
    queuePx: 14,   // compact stacked/queued size
    topPad: 20,
    currentGap: 24,
    queueSlot: 20,
    queuePad: 36
  };

  const MOTION = {
    flipZone: 200,
    detachZone: 240,
    stagger: 0.14,
    arc: 36,
    heroStart: 20,
    heroZone: 320
  };

  const SECTIONS_CONFIG = [
    { id: 'hero', label: 'ZETICA', isHero: true },
    { id: 'apps', label: 'ZETICA APPS' },
    { id: 'studio', label: 'ZETICA STUDIO', href: './download.html' },
    { id: 'features', label: 'FEATURES' },
    { id: 'ownership', label: 'OWNERSHIP' },
    { id: 'made-with', label: 'COMMUNITY', alias: 'community' },
    { id: 'start', label: 'GET STARTED' }
  ];

  function rulerMap(vh) {
    const base = NAV_H + LAYOUT.edgePad;
    return {
      base,
      span: Math.max(1, vh - NAV_H - 2 * LAYOUT.edgePad),
      drift: (p) => base - p * (NAV_H + 2 * LAYOUT.edgePad)
    };
  }

  let measureCtx = null;
  function getWordMetrics(text, fontPx) {
    if (!measureCtx) {
      const c = document.createElement('canvas');
      measureCtx = c.getContext('2d');
    }
    measureCtx.font = `800 ${fontPx}px var(--font-archivo), "Space Grotesk", sans-serif`;
    const adv = [];
    const cum = [];
    let cur = 0;
    for (let i = 0; i < text.length; i++) {
      cum.push(cur);
      const w = measureCtx.measureText(text[i]).width;
      adv.push(w / fontPx);
      cur += w / fontPx;
    }
    return { adv, cum, total: cur };
  }

  function initInstrument() {
    if (!isDesktop()) return;

    const oldQueue = document.getElementById('ruler-bottom-queue');
    if (oldQueue) oldQueue.remove();

    if (document.getElementById('zetica-ruler-instrument')) return;

    document.documentElement.dataset.ruler = 'on';
    document.documentElement.dataset.rulerSide = 'right';
    document.documentElement.style.setProperty('--ruler-rail', `${LAYOUT.railW}px`);

    // A. Create Ruler Rail Container
    const rulerContainer = document.createElement('div');
    rulerContainer.id = 'zetica-ruler-instrument';
    rulerContainer.className = 'zetica-ruler-instrument';
    rulerContainer.setAttribute('aria-hidden', 'true');

    const frost = document.createElement('div');
    frost.className = 'ruler-frost-gutter';
    rulerContainer.appendChild(frost);

    const tickTrack = document.createElement('div');
    tickTrack.id = 'ruler-tick-track';
    tickTrack.className = 'ruler-tick-track';
    rulerContainer.appendChild(tickTrack);

    const needle = document.createElement('div');
    needle.id = 'ruler-needle';
    needle.className = 'ruler-needle';
    needle.innerHTML = `
      <span class="needle-bar"></span>
      <span class="needle-readout">
        <span class="ruler-digits">
          <span class="ruler-digit-col" id="rd-col-0"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span></span>
          <span class="ruler-digit-col" id="rd-col-1"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span></span>
          <span class="ruler-digit-col" id="rd-col-2"><span>0</span><span>1</span><span>2</span><span>3</span><span>4</span><span>5</span><span>6</span><span>7</span><span>8</span><span>9</span></span>
        </span>%
      </span>
    `;
    rulerContainer.appendChild(needle);
    document.body.appendChild(rulerContainer);

    // B. Create HeadingFlow Container
    const flowContainer = document.createElement('div');
    flowContainer.id = 'zetica-heading-flow';
    flowContainer.className = 'zetica-heading-flow';
    document.body.appendChild(flowContainer);

    // Measure Sections
    const measuredSections = [];
    SECTIONS_CONFIG.forEach((cfg) => {
      let el = document.getElementById(cfg.id);
      if (!el && cfg.alias) el = document.getElementById(cfg.alias);
      if (el) {
        const rect = el.getBoundingClientRect();
        const anchor = rect.top + window.scrollY;
        measuredSections.push({
          id: cfg.id,
          label: cfg.label,
          el,
          isHero: !!cfg.isHero,
          anchor,
          bottom: rect.bottom + window.scrollY,
          metrics: getWordMetrics(cfg.label, LAYOUT.headingPx),
          href: cfg.href
        });
      }
    });

    // Populate Ticks inside TickTrack
    const docH = document.documentElement.scrollHeight;
    for (let p = 0; p <= 100; p += LAYOUT.minorPct) {
      const isMajor = p % LAYOUT.labelPct === 0;
      const tickRow = document.createElement('div');
      tickRow.className = `ruler-tick-row ${isMajor ? 'major' : 'minor'}`;
      tickRow.style.top = `${(p / 100) * docH}px`;

      const tickLine = document.createElement('span');
      tickLine.className = 'ruler-tick-line';
      tickRow.appendChild(tickLine);

      if (isMajor) {
        const tickLabel = document.createElement('span');
        tickLabel.className = 'ruler-tick-label';
        tickLabel.textContent = String(p).padStart(2, '0');
        tickRow.appendChild(tickLabel);
      }
      tickTrack.appendChild(tickRow);
    }

    // Build DOM for all HeadingFlow sections (including Hero)
    const wordRefs = [];
    measuredSections.forEach((s) => {
      const wordBox = document.createElement('div');
      wordBox.className = 'flow-word-box';
      wordBox.dataset.label = s.label;

      const letterEls = [];
      for (let i = 0; i < s.label.length; i++) {
        const ch = s.label[i];
        const span = document.createElement('span');
        span.className = 'flow-letter';
        span.textContent = ch === ' ' ? '\u00A0' : ch;
        wordBox.appendChild(span);
        letterEls.push(span);
      }

      const hit = document.createElement('a');
      hit.className = 'flow-word-hit';
      hit.href = s.href || `#${s.id}`;
      hit.setAttribute('aria-label', s.label);
      hit.addEventListener('click', (e) => {
        if (s.href && !s.href.startsWith('#')) return;
        e.preventDefault();
        const targetEl = document.getElementById(s.id) || (s.alias ? document.getElementById(s.alias) : null);
        if (targetEl) {
          if (lenisInstance) {
            lenisInstance.scrollTo(targetEl, { duration: 1.2 });
          } else {
            targetEl.scrollIntoView({ behavior: 'smooth' });
          }
        }
      });
      wordBox.appendChild(hit);

      flowContainer.appendChild(wordBox);
      wordRefs.push({ wordBox, letterEls, hit });
    });

    const heroMasthead = document.getElementById('hero-wordmark-masthead');

    // C. Click on rail jumps to progress
    rulerContainer.addEventListener('click', (e) => {
      const vh = window.innerHeight;
      const map = rulerMap(vh);
      const relY = e.clientY - map.base;
      const targetP = clamp01(relY / map.span);
      const maxScroll = Math.max(1, document.documentElement.scrollHeight - vh);
      const targetScroll = targetP * maxScroll;
      if (lenisInstance) {
        lenisInstance.scrollTo(targetScroll, { duration: 1.2 });
      } else {
        window.scrollTo({ top: targetScroll, behavior: 'smooth' });
      }
    });

    // D. Animation Frame Loop
    const digitCols = [
      document.getElementById('rd-col-0'),
      document.getElementById('rd-col-1'),
      document.getElementById('rd-col-2')
    ];
    let prevDigits = [-1, -1, -1];
    let prevPct = -1;

    function renderLoop() {
      const docH = document.documentElement.scrollHeight;
      const vh = window.innerHeight;
      const vw = window.innerWidth;
      const scrollY = window.scrollY || window.pageYOffset || 0;
      const maxScroll = Math.max(1, docH - vh);
      const progress = clamp01(scrollY / maxScroll);

      const map = rulerMap(vh);
      const drift = map.drift(progress);

      // 1. Move Tick Track & Needle
      tickTrack.style.transform = `translate3d(0, ${-scrollY + drift}px, 0)`;
      const ny = map.base + progress * map.span;
      needle.style.transform = `translate3d(0, ${ny}px, 0)`;
      needle.style.opacity = String(clamp01(progress / 0.025));

      // 2. Update Odometer Digits
      const pct = Math.round(progress * 100);
      if (pct !== prevPct) {
        prevPct = pct;
        const str = String(pct).padStart(3, '0');
        for (let c = 0; c < 3; c++) {
          const d = str.charCodeAt(c) - 48;
          if (d !== prevDigits[c]) {
            prevDigits[c] = d;
            if (digitCols[c]) {
              digitCols[c].style.transform = `translateY(${-d}em)`;
            }
          }
        }
      }

      // 3. HeadingFlow Layout Geometry
      const T = (LAYOUT.thresholdPct / 100) * vh;
      const yTopLine = NAV_H + LAYOUT.topPad;
      const yQueueLine = vh - LAYOUT.queuePad;
      const hp = LAYOUT.headingPx; // 32
      const rs = LAYOUT.ridingPx / hp; // 18 / 32
      const qs = LAYOUT.queuePx / hp;  // 14 / 32
      const rightGuideX = vw - LAYOUT.railW - LAYOUT.textPad;
      const railCenterX = vw - LAYOUT.railW / 2;

      // Phase pass per section
      const phases = measuredSections.map((s) => {
        const m = s.metrics;
        const rideLen = m.total * hp * rs;
        const v = s.anchor - scrollY + drift;
        let flipP = 0;
        let detachP = 0;

        if (s.isHero) {
          detachP = 1;
          flipP = clamp01((scrollY - MOTION.heroStart) / MOTION.heroZone);
        } else {
          flipP = clamp01((T + MOTION.flipZone - v) / MOTION.flipZone);
          if (s.anchor - maxScroll > T) {
            const endStart = Math.min(s.bottom - vh, maxScroll - 24);
            const zone = Math.max(24, maxScroll - endStart);
            flipP = Math.max(flipP, clamp01((scrollY - endStart) / zone));
          }
        }
        return { v, rideLen, flipP, detachP, yq: yQueueLine };
      });

      // Hero masthead opacity fade as scroll advances
      if (heroMasthead) {
        const heroP = phases[0]?.flipP || 0;
        heroMasthead.style.opacity = String(Math.max(0, 1 - heroP * 2));
      }

      // Backward pass for queue stacking
      let below = 0;
      for (let wi = measuredSections.length - 1; wi >= 0; wi--) {
        if (measuredSections[wi].isHero) continue;
        const ph = phases[wi];
        ph.yq = yQueueLine - LAYOUT.queueSlot * below;
        ph.detachP = clamp01((ph.yq + MOTION.detachZone - (ph.v + ph.rideLen)) / MOTION.detachZone);
        below += 1 - ph.detachP;
      }

      let stackedCount = 0;
      let flipShift = 0;
      for (const p of phases) {
        if (p.flipP >= 1) stackedCount++;
        else if (p.flipP > 0) flipShift += p.flipP;
      }

      // Horizontal pose: flush right against rightGuideX
      const horizPose = (m, i, yLine, s, alpha) => {
        const along = (m.cum[i] + m.adv[i] / 2) * hp * s;
        const totalW = m.total * hp * s;
        const x = rightGuideX - (totalW - along);
        return { x, y: yLine, rot: 0, scale: s, alpha };
      };

      // Riding pose: vertical column on tick rail
      const ridePose = (m, i, top) => {
        const along = (m.cum[i] + m.adv[i] / 2) * hp * rs;
        const totalH = m.total * hp * rs;
        const y = top + (totalH - along);
        return { x: railCenterX, y, rot: -90, scale: rs, alpha: 0.55 };
      };

      // 4. Update Each Section Heading
      measuredSections.forEach((s, wi) => {
        const refs = wordRefs[wi];
        if (!refs) return;
        const ph = phases[wi];
        const m = s.metrics;
        const n = m.adv.length;

        let p, from, to;

        if (s.isHero) {
          p = ph.flipP;
          // Hero rest position: centered in hero viewport
          const heroRestX = vw / 2;
          const heroRestY = Math.max(140, vh * 0.38) - scrollY;
          const heroRestScale = 72 / hp;
          const heroRestW = m.total * hp * heroRestScale;
          const heroStartX = heroRestX - heroRestW / 2;

          from = (i) => ({
            x: heroStartX + (m.cum[i] + m.adv[i] / 2) * hp * heroRestScale,
            y: heroRestY,
            rot: 0,
            scale: heroRestScale,
            alpha: 1
          });

          // Stacked at top: compact entry
          const demote = wi === stackedCount - 1 ? flipShift : 1;
          const y = yTopLine + wi * LAYOUT.queueSlot;
          to = (i) => horizPose(m, i, y, qs, 0.5);
        } else {
          const isFlipping = ph.flipP > 0;
          const isDetaching = ph.detachP < 1;

          if (isFlipping) {
            p = ph.flipP;
            from = (i) => ridePose(m, i, ph.v);
            if (ph.flipP >= 1) {
              const demote = wi === stackedCount - 1 ? flipShift : 1;
              const y = yTopLine + wi * LAYOUT.queueSlot + LAYOUT.currentGap * (1 - demote);
              const scale = 1 - (1 - qs) * demote;
              const alpha = 1 - (1 - 0.5) * demote;
              to = (i) => horizPose(m, i, y, scale, alpha);
            } else {
              to = (i) => horizPose(m, i, yTopLine + wi * LAYOUT.queueSlot + LAYOUT.currentGap, 1, 1);
            }
          } else if (isDetaching) {
            p = ph.detachP;
            const vForm = ph.yq - ph.rideLen;
            to = (i) => ridePose(m, i, vForm);
            from = (i) => horizPose(m, i, ph.yq, qs, 0.55);
          } else {
            p = 1;
            from = to = (i) => ridePose(m, i, ph.v);
          }
        }

        // Apply Letter Transforms
        const sf = MOTION.stagger;
        const span = 1 + (n - 1) * sf;
        let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;

        // Hide hero flow letters at scroll 0 so resting masthead is shown
        if (s.isHero && p <= 0.01) {
          refs.letterEls.forEach(el => el.style.opacity = '0');
          return;
        }

        for (let i = 0; i < n; i++) {
          const el = refs.letterEls[i];
          if (!el) continue;
          const si = n - 1 - i;
          const pi = clamp01(p * span - si * sf);
          const e = easeInOutCubic(pi);
          const a = from(i);
          const b = to(i);

          const cx = (a.x + b.x) / 2 - MOTION.arc;
          const cy = (a.y + b.y) / 2;
          const u = 1 - e;
          const x = u * u * a.x + 2 * u * e * cx + e * e * b.x;
          const y = u * u * a.y + 2 * u * e * cy + e * e * b.y;
          const rot = a.rot + (b.rot - a.rot) * e;
          const scale = a.scale + (b.scale - a.scale) * e;
          const alpha = a.alpha + (b.alpha - a.alpha) * e;

          el.style.transform = `translate3d(${x}px, ${y}px, 0) translate(-50%, -50%) rotate(${rot}deg) scale(${scale})`;
          el.style.opacity = String(alpha);

          // Active heading gets crisp high ink & bold weight
          if (scale > 0.85 && Math.abs(rot) < 5) {
            el.style.fontWeight = '800';
            el.classList.add('active');
          } else {
            el.style.fontWeight = '600';
            el.classList.remove('active');
          }

          if (x < minX) minX = x;
          if (x > maxX) maxX = x;
          if (y < minY) minY = y;
          if (y > maxY) maxY = y;
        }

        if (refs.hit && minX < Infinity) {
          refs.hit.style.left = `${minX - 8}px`;
          refs.hit.style.top = `${minY - 4}px`;
          refs.hit.style.width = `${Math.max(20, maxX - minX + 16)}px`;
          refs.hit.style.height = `${Math.max(20, maxY - minY + 8)}px`;
        }
      });

      requestAnimationFrame(renderLoop);
    }

    requestAnimationFrame(renderLoop);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initLenis();
      initInstrument();
    });
  } else {
    initLenis();
    initInstrument();
  }
})();
