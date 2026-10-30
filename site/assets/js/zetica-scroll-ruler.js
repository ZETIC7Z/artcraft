/**
 * ZETICA Scroll-Ruler Instrument & Floating Typography Flight System
 * Faithful 1:1 port of storytold/artcraft ruler-layout, ruler-motion, and heading-flow.
 *
 * Coordinates:
 * 1. Precision 0-100% tick rail and odometer needle on the right edge.
 * 2. Hero wordmark "ZETICA" (pure text, 6 letters) flight into slot 0 of the top stack.
 * 3. Bottom queue of upcoming section titles, horizontal-to-vertical rail morph,
 *    and vertical-to-horizontal flip into active 34px headings and 16px compact stack rows.
 * 4. Exact 16px unified font size and 20px slot spacing for all stacked and queued titles.
 */

(function () {
  'use strict';

  // 1. Desktop & Motion Capability Checks
  function isDesktop() {
    const isMobile = /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    const hasPointer = window.matchMedia('(pointer: fine) and (hover: hover) and (min-width: 1024px)').matches;
    return !isMobile && hasPointer;
  }

  function clamp01(v) {
    return Math.max(0, Math.min(1, v));
  }

  function easeInOutCubic(v) {
    return v < 0.5 ? 4 * v * v * v : 1 - Math.pow(-2 * v + 2, 3) / 2;
  }

  // 2. Exact ArtCraft Layout & Motion Tunables
  const NAV_H = 48;

  const LAYOUT = {
    railW: 60,         // Width of the tick rail at viewport edge
    textPad: 0,        // Horizontal gap between tick rail and heading text (ArtCraft = 0)
    edgePad: 12,       // Inset from navbar and viewport bottom
    minorPct: 1,       // Tick every 1%
    labelPct: 5,       // Major labeled tick every 5%
    thresholdPct: 12,  // 12vh flip line
    headingPx: 34,     // Active section heading size (34px)
    ridingPx: 20,      // Vertical riding text on rail (20px)
    queuePx: 16,       // Stacked titles and queue size (16px)
    topPad: 28,        // Distance below navbar to first stacked title (28px)
    currentGap: 26,    // Extra gap separating 34px active heading from compact stack (26px)
    queueSlot: 20,     // Vertical spacing between stacked titles (20px)
    queuePad: 36,      // Bottom margin for queue (36px)
    queueAlpha: 0.38   // Opacity of inactive queue / stack items
  };

  const MOTION = {
    flipZone: 200,     // Scroll distance over which vertical-to-horizontal flip plays out
    detachZone: 240,   // Scroll distance over which queued heading morphs onto rail
    stagger: 0.16,     // Letter stagger fraction
    arc: 28,           // Inward curve flight arc (28px)
    heroLead: 100,     // Scroll offset before hero flight triggers
    heroZone: 320      // Scroll distance for hero wordmark flight
  };

  // Section Roster (Hero is index 0, followed by sections present in DOM)
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

  // 3. Exact Subpixel Letter Measurement (Direct DOM, No Canvas Var Failure)
  function measureLabels(labels) {
    const div = document.createElement('div');
    div.className = 'font-display';
    div.style.cssText = 'position:absolute;left:-9999px;top:0;visibility:hidden;white-space:pre;font-size:100px;line-height:1;font-weight:620;letter-spacing:normal;font-family:var(--font-archivo), "Space Grotesk", system-ui, sans-serif;';
    document.body.appendChild(div);

    const metrics = {};
    for (const label of labels) {
      div.textContent = '';
      const adv = label.split('').map((ch) => {
        const span = document.createElement('span');
        span.textContent = ch === ' ' ? '\u00A0' : ch;
        div.appendChild(span);
        return span.getBoundingClientRect().width / 100;
      });
      const cum = [];
      let total = 0;
      for (const w of adv) {
        cum.push(total);
        total += w;
      }
      metrics[label] = { adv, cum, total };
    }
    div.remove();
    return metrics;
  }

  // 4. Interactive Resources Dropdown in Navbar
  function initResourcesDropdown() {
    const trigger = document.querySelector('button[id*="trigger"][id*="ailb"], button:has(svg.lucide-chevron-down)');
    if (!trigger) return;

    const parentLi = trigger.closest('li');
    if (!parentLi || parentLi.querySelector('.zetica-resources-dropdown')) return;

    parentLi.style.position = 'relative';

    const menu = document.createElement('div');
    menu.className = 'zetica-resources-dropdown';
    menu.innerHTML = `
      <a href="./tutorials.html" class="resources-dropdown-item">TUTORIALS</a>
      <a href="./news.html" class="resources-dropdown-item">NEWS</a>
      <a href="./faq.html" class="resources-dropdown-item">FAQ</a>
      <a href="./press-kit.html" class="resources-dropdown-item">PRESS KIT</a>
    `;
    parentLi.appendChild(menu);

    let isOpen = false;
    let closeTimer = null;

    function openMenu() {
      if (closeTimer) {
        clearTimeout(closeTimer);
        closeTimer = null;
      }
      isOpen = true;
      menu.classList.add('open');
      trigger.setAttribute('aria-expanded', 'true');
      const chev = trigger.querySelector('.lucide-chevron-down');
      if (chev) chev.style.transform = 'rotate(180deg)';
    }

    function scheduleClose() {
      if (closeTimer) clearTimeout(closeTimer);
      closeTimer = setTimeout(() => {
        closeMenu();
      }, 180);
    }

    function closeMenu() {
      if (closeTimer) {
        clearTimeout(closeTimer);
        closeTimer = null;
      }
      isOpen = false;
      menu.classList.remove('open');
      trigger.setAttribute('aria-expanded', 'false');
      const chev = trigger.querySelector('.lucide-chevron-down');
      if (chev) chev.style.transform = 'rotate(0deg)';
    }

    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      e.stopPropagation();
      if (isOpen) closeMenu();
      else openMenu();
    });

    parentLi.addEventListener('mouseenter', openMenu);
    parentLi.addEventListener('mouseleave', scheduleClose);

    document.addEventListener('click', (e) => {
      if (!parentLi.contains(e.target)) closeMenu();
    });
  }

  // 5. Main Instrument & Typography Flight Engine
  function initInstrument() {
    if (!isDesktop()) return;

    // Clean up any stale instances
    const oldInstrument = document.getElementById('zetica-ruler-instrument');
    if (oldInstrument) oldInstrument.remove();
    const oldFlow = document.getElementById('zetica-heading-flow');
    if (oldFlow) oldFlow.remove();

    document.documentElement.dataset.ruler = 'on';
    document.documentElement.dataset.rulerSide = 'right';
    document.documentElement.style.setProperty('--ruler-rail', `${LAYOUT.railW}px`);

    // A. Ruler Rail Container
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

    // B. Build Ticks inside TickTrack
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

    // C. Measure Sections in DOM
    const measuredSections = [];
    SECTIONS_CONFIG.forEach((cfg) => {
      if (cfg.isHero) {
        measuredSections.push({
          id: cfg.id,
          label: cfg.label,
          isHero: true,
          anchor: 0,
          bottom: window.innerHeight,
          href: '#hero'
        });
        return;
      }
      let el = document.getElementById(cfg.id);
      if (!el && cfg.alias) el = document.getElementById(cfg.alias);
      if (el) {
        const rect = el.getBoundingClientRect();
        const anchor = rect.top + window.scrollY;
        measuredSections.push({
          id: cfg.id,
          label: cfg.label,
          isHero: false,
          el,
          anchor,
          bottom: rect.bottom + window.scrollY,
          href: cfg.href || `#${cfg.id}`
        });
      }
    });

    // D. Compute Exact Metrics for All Labels
    let labelMetrics = measureLabels(measuredSections.map(s => s.label));

    // E. Measure Actual Hero Masthead Letters
    const heroMasthead = document.getElementById('hero-wordmark-masthead');
    const heroLetters = heroMasthead ? Array.from(heroMasthead.querySelectorAll('.wm-letter')) : [];
    let heroBaseMetrics = null;

    function measureHeroLetters() {
      if (!heroMasthead || !heroLetters.length) return;
      const savedTransforms = heroLetters.map(el => el.style.transform);
      heroLetters.forEach(el => el.style.transform = '');

      const rects = heroLetters.map(el => el.getBoundingClientRect());
      const scrollY = window.scrollY || 0;
      const cs = window.getComputedStyle(heroLetters[0] || heroMasthead);
      const fontPx = parseFloat(cs.fontSize) || 72;

      const adv = rects.map(r => r.width / fontPx);
      const cum = [];
      let total = 0;
      for (const w of adv) {
        cum.push(total);
        total += w;
      }

      heroBaseMetrics = {
        els: heroLetters,
        baseX: rects.map(r => r.left + r.width / 2),
        baseDocY: rects.map(r => r.top + scrollY + r.height / 2),
        fontPx,
        metrics: { adv, cum, total }
      };

      heroLetters.forEach((el, idx) => el.style.transform = savedTransforms[idx]);
    }
    measureHeroLetters();

    // Re-measure on window resize and font load
    window.addEventListener('resize', () => {
      labelMetrics = measureLabels(measuredSections.map(s => s.label));
      measureHeroLetters();
    });
    if (document.fonts && document.fonts.ready) {
      document.fonts.ready.then(() => {
        labelMetrics = measureLabels(measuredSections.map(s => s.label));
        measureHeroLetters();
      });
    }

    // F. Create HeadingFlow Container & Non-Hero Letter Spans
    const flowContainer = document.createElement('div');
    flowContainer.id = 'zetica-heading-flow';
    flowContainer.className = 'zetica-heading-flow pointer-events-none fixed inset-0 z-40';
    document.body.appendChild(flowContainer);

    const lenisInstance = window.__lenis || (window.Lenis ? new window.Lenis() : null);

    const sectionDOMRefs = measuredSections.map((s) => {
      if (s.isHero) {
        return { isHero: true, letterEls: heroLetters, hit: null };
      }

      const letterEls = [];
      for (let i = 0; i < s.label.length; i++) {
        const ch = s.label[i];
        const span = document.createElement('span');
        span.className = 'flow-letter font-display absolute top-0 left-0 whitespace-pre text-ink-strong';
        span.setAttribute('aria-hidden', 'true');
        span.textContent = ch === ' ' ? '\u00A0' : ch;
        span.style.fontSize = `${LAYOUT.headingPx}px`;
        span.style.lineHeight = '1';
        span.style.opacity = '0';
        span.style.willChange = 'transform, opacity';
        flowContainer.appendChild(span);
        letterEls.push(span);
      }

      const hit = document.createElement('a');
      hit.className = 'flow-word-hit pointer-events-auto absolute cursor-pointer';
      hit.href = s.href || `#${s.id}`;
      hit.setAttribute('aria-label', `Jump to ${s.label}`);
      hit.addEventListener('click', (e) => {
        if (s.href && !s.href.startsWith('#')) return;
        e.preventDefault();
        const targetEl = s.el || document.getElementById(s.id);
        if (targetEl) {
          const targetY = targetEl.getBoundingClientRect().top + window.scrollY - NAV_H;
          if (lenisInstance) {
            lenisInstance.scrollTo(targetY, { duration: 1.25 });
          } else {
            window.scrollTo({ top: targetY, behavior: 'smooth' });
          }
        }
      });
      flowContainer.appendChild(hit);

      return { isHero: false, letterEls, hit };
    });

    // G. Rail Click Jumps
    rulerContainer.addEventListener('click', (e) => {
      const vh = window.innerHeight;
      const map = rulerMap(vh);
      const relY = e.clientY - map.base;
      const targetP = clamp01(relY / map.span);
      const maxScroll = Math.max(1, document.documentElement.scrollHeight - vh);
      const targetScroll = targetP * maxScroll;
      if (lenisInstance) {
        lenisInstance.scrollTo(targetScroll, { duration: 1.25 });
      } else {
        window.scrollTo({ top: targetScroll, behavior: 'smooth' });
      }
    });

    // H. Digits & Odometer Tracking
    const digitCols = [
      document.getElementById('rd-col-0'),
      document.getElementById('rd-col-1'),
      document.getElementById('rd-col-2')
    ];
    let prevDigits = [-1, -1, -1];
    let prevPct = -1;

    // I. Animation Frame Loop (1:1 ArtCraft HeadingFlow Execution)
    function renderLoop() {
      const docH = document.documentElement.scrollHeight;
      const vh = window.innerHeight;
      const vw = window.innerWidth;
      const scrollY = window.scrollY || window.pageYOffset || 0;
      const maxScroll = Math.max(1, docH - vh);
      const progress = clamp01(scrollY / maxScroll);

      const map = rulerMap(vh);
      const drift = map.drift(progress);

      // 1. Move Tick Track & Traveling Needle
      tickTrack.style.transform = `translate3d(0, ${-scrollY + drift}px, 0)`;
      const ny = map.base + progress * map.span;
      needle.style.transform = `translate3d(0, ${ny}px, 0)`;
      needle.style.opacity = String(clamp01(progress / 0.02));

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

      // 3. Layout Constants
      const L = (LAYOUT.thresholdPct / 100) * vh;
      const A = NAV_H + LAYOUT.topPad;
      const I = vh - LAYOUT.queuePad;
      const D = LAYOUT.headingPx;                  // 34px
      const _ = LAYOUT.ridingPx / D;               // 20 / 34 ≈ 0.588235
      const z = LAYOUT.queuePx / D;                // 16 / 34 ≈ 0.470588
      const W = vw - LAYOUT.railW / 2;             // Rail center X

      // 4. Hero Flight Trigger Geometry
      const heroReady = heroBaseMetrics && heroBaseMetrics.els.length > 0;
      const heroStartY = heroReady
        ? Math.max(0, (heroBaseMetrics.baseDocY[0] - 0.5 * heroBaseMetrics.fontPx) - NAV_H - MOTION.heroLead)
        : 20;
      const heroFlipP = clamp01((scrollY - heroStartY) / MOTION.heroZone);

      // 5. Compute Phases for All Sections
      const phases = measuredSections.map((s) => {
        if (s.isHero) {
          return { v: 0, rideLen: 0, flipP: heroFlipP, detachP: 1, yq: I };
        }
        const u = labelMetrics[s.label];
        const rideLen = (u ? u.total : 0) * D * _;
        const v = s.anchor - scrollY + drift;
        let flipP = clamp01((L + MOTION.flipZone - v) / MOTION.flipZone);
        if (s.anchor - maxScroll > L) {
          const endStart = Math.min(s.bottom - vh, maxScroll - 24);
          const zone = Math.max(24, maxScroll - endStart);
          flipP = Math.max(flipP, clamp01((scrollY - endStart) / zone));
        }
        return { v, rideLen, flipP, detachP: 0, yq: I };
      });

      // Backward pass: Queue positions & detach ramp
      let belowCount = 0;
      for (let wi = measuredSections.length - 1; wi >= 0; wi--) {
        if (measuredSections[wi].isHero) continue;
        const ph = phases[wi];
        ph.yq = I - LAYOUT.queueSlot * belowCount;
        ph.detachP = clamp01((ph.yq + MOTION.detachZone - (ph.v + ph.rideLen)) / MOTION.detachZone);
        belowCount += 1 - ph.detachP;
      }

      // Count stacked sections & flip transition progress
      let stackedCount = 0;
      let flipShift = 0;
      for (const p of phases) {
        if (p.flipP >= 1) stackedCount++;
        else if (p.flipP > 0) flipShift += p.flipP;
      }

      // 6. Pose Helpers (Flush Right-Aligned to Guide, 1:1 ArtCraft Formula)
      const B = (u, t, yLine, scale, alpha) => {
        const s = (u.cum[t] + u.adv[t] / 2) * D * scale;
        const a = LAYOUT.railW + LAYOUT.textPad + (u.total * D * scale - s);
        return {
          x: vw - a,
          y: yLine,
          rot: 0,
          scale: scale,
          alpha: alpha
        };
      };

      const Z = (u, t, top) => ({
        x: W,
        y: top + (u.total - u.cum[t] - u.adv[t] / 2) * D * _,
        rot: -90,
        scale: _,
        alpha: LAYOUT.queueAlpha
      });

      // 7. Render Each Section's Letters
      measuredSections.forEach((s, wi) => {
        const domRef = sectionDOMRefs[wi];
        if (!domRef) return;
        const ph = phases[wi];
        const isHero = s.isHero && heroReady;
        const u = isHero ? heroBaseMetrics.metrics : labelMetrics[s.label];
        if (!u) return;

        const N = u.adv.length;
        let p, fromPose, toPose;
        let isFlipping = false;

        if (isHero) {
          p = ph.flipP;
          isFlipping = true;
          fromPose = (i) => ({
            x: heroBaseMetrics.baseX[i],
            y: heroBaseMetrics.baseDocY[i] - scrollY,
            rot: 0,
            scale: heroBaseMetrics.fontPx / D,
            alpha: 1
          });

          if (ph.flipP >= 1) {
            const isCurrent = (stackedCount === 1);
            const demote = isCurrent ? flipShift : 1;
            const y = A + 0 * LAYOUT.queueSlot + LAYOUT.currentGap * (1 - demote);
            const scale = 1 - (1 - z) * demote;
            const alpha = 1 - (1 - LAYOUT.queueAlpha) * demote;
            toPose = (i) => B(u, i, y, scale, alpha);
          } else {
            toPose = (i) => B(u, i, A + LAYOUT.currentGap, 1, 1);
          }
        } else {
          if (ph.flipP > 0) {
            p = ph.flipP;
            isFlipping = true;
            fromPose = (i) => Z(u, i, ph.v);
            if (ph.flipP >= 1) {
              const isCurrent = (wi === stackedCount - 1);
              const demote = isCurrent ? flipShift : 1;
              const y = A + wi * LAYOUT.queueSlot + LAYOUT.currentGap * (1 - demote);
              const scale = 1 - (1 - z) * demote;
              const alpha = 1 - (1 - LAYOUT.queueAlpha) * demote;
              toPose = (i) => B(u, i, y, scale, alpha);
            } else {
              toPose = (i) => B(u, i, A + wi * LAYOUT.queueSlot + LAYOUT.currentGap, 1, 1);
            }
          } else if (ph.detachP < 1) {
            p = ph.detachP;
            const vForm = ph.yq - ph.rideLen;
            toPose = (i) => Z(u, i, vForm);
            fromPose = (i) => B(u, i, ph.yq, z, LAYOUT.queueAlpha);
          } else {
            p = 1;
            fromPose = toPose = (i) => Z(u, i, ph.v);
          }
        }

        // Letter flight execution with inward quadratic bezier curve
        const sf = MOTION.stagger;
        const span = 1 + (N - 1) * sf;
        let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;

        for (let i = 0; i < N; i++) {
          const el = domRef.letterEls[i];
          if (!el) continue;

          const si = isFlipping ? (N - 1 - i) : i;
          const pi = clamp01(p * span - si * sf);
          const e = easeInOutCubic(pi);

          const a = fromPose(i);
          const b = toPose(i);

          const cx = (a.x + b.x) / 2 - MOTION.arc;
          const cy = (a.y + b.y) / 2;
          const inv = 1 - e;

          const curX = inv * inv * a.x + 2 * inv * e * cx + e * e * b.x;
          const curY = inv * inv * a.y + 2 * inv * e * cy + e * e * b.y;
          const curRot = a.rot + (b.rot - a.rot) * e;
          const curScale = a.scale + (b.scale - a.scale) * e;
          const curAlpha = a.alpha + (b.alpha - a.alpha) * e;

          if (isHero) {
            if (p <= 0) {
              el.style.transform = '';
              el.style.opacity = '1';
              el.style.color = '';
            } else {
              const deltaX = curX - heroBaseMetrics.baseX[i];
              const deltaY = curY - (heroBaseMetrics.baseDocY[i] - scrollY);
              const totalScale = curScale * (D / heroBaseMetrics.fontPx);
              el.style.transform = `translate3d(${deltaX.toFixed(2)}px, ${deltaY.toFixed(2)}px, 0) rotate(${curRot.toFixed(1)}deg) scale(${totalScale.toFixed(4)})`;
              el.style.opacity = '1';
              const alphaC = clamp01(curAlpha);
              el.style.color = alphaC >= 0.98
                ? 'var(--ink-strong, #ffffff)'
                : `color-mix(in srgb, var(--ink-strong, #ffffff) ${(100 * alphaC).toFixed(1)}%, var(--bg, #000000))`;
            }
          } else {
            el.style.transform = `translate3d(${curX.toFixed(2)}px, ${curY.toFixed(2)}px, 0) translate(-50%, -50%) rotate(${curRot.toFixed(1)}deg) scale(${curScale.toFixed(4)})`;
            el.style.opacity = '1';
            const alphaC = clamp01(curAlpha);
            el.style.color = alphaC >= 0.98
              ? 'var(--ink-strong, #ffffff)'
              : `color-mix(in srgb, var(--ink-strong, #ffffff) ${(100 * alphaC).toFixed(1)}%, var(--bg, #000000))`;
          }

          // Calculate bounding box for hit link
          const charHalfW = (u.adv[i] * D * curScale) / 2 + 2;
          const charHalfH = (D * curScale) / 2 + 2;
          const isRot = Math.abs(curRot) > 45;
          const boxW = isRot ? charHalfH : charHalfW;
          const boxH = isRot ? charHalfW : charHalfH;
          if (curX - boxW < minX) minX = curX - boxW;
          if (curX + boxW > maxX) maxX = curX + boxW;
          if (curY - boxH < minY) minY = curY - boxH;
          if (curY + boxH > maxY) maxY = curY + boxH;
        }

        // Update clickable hit bounding box
        if (domRef.hit && isFinite(minX)) {
          domRef.hit.style.left = `${(minX - 4).toFixed(1)}px`;
          domRef.hit.style.top = `${(minY - 4).toFixed(1)}px`;
          domRef.hit.style.width = `${(maxX - minX + 8).toFixed(1)}px`;
          domRef.hit.style.height = `${(maxY - minY + 8).toFixed(1)}px`;
        }
      });

      requestAnimationFrame(renderLoop);
    }

    requestAnimationFrame(renderLoop);
  }

  // 6. Bootstrap on DOM Ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      initResourcesDropdown();
      initInstrument();
    });
  } else {
    initResourcesDropdown();
    initInstrument();
  }
})();
