# AGENT.md — Project Memory & Architecture Guide

## 1. Project Overview & Vision
- **Project**: **ZETICA Creative Suite & Hub** (100% native Rust desktop creative ecosystem).
- **Developer**: **Sam Pangilinan** (`ZETICUZ` / `ZETIC7Z` / `TECHNOLOHIYA`), Portfolio: `https://www.zeticuz.xyz/`.
- **Primary Brand Name**: **ZETICA** (ALL CAPS).
- **Official Brand Logo**: **ZE** monogram vector (`branding/zetica-monogram.svg` / `site/assets/images/zetica-monogram.svg`), extracted from `C:\Users\ZETICUZ\Downloads\ZE.svg`.
  - **Dynamic Theme Inversion**:
    - **Dark Mode**: Logo turns radiant solid **WHITE** (`#FFFFFF`), perfectly matching the white typography.
    - **Light Mode**: Logo turns crisp solid **BLACK** (`#000000`), perfectly matching the dark typography.
    - Reacts instantly to the header navigation theme toggle and system OS appearance changes.
- **Official Developer Logo**: `C:\Users\ZETICUZ\Downloads\zeticuz-logo.svg`.
- **Standard Footer Signature**:
  - Centered: `[zeticuz-logo.svg] SITE DEVELOPED BY: Sam Pangilinan · © 2026`
  - Interactive button opening `https://www.zeticuz.xyz/` in a new tab without showing raw URL string.

---

## 2. Repositories & GitHub Infrastructure (`ZETIC7Z`)

| Repository | Role | Upstream | Workflows Active | Releases |
|---|---|---|---|---|
| **[ZETIC7Z/craft-launcher](https://github.com/ZETIC7Z/craft-launcher)** | **Zetica Hub** (Native desktop installer, hub & updater) | `storytold/craft-launcher` | `.github/workflows/sync-upstream.yml`<br>`.github/workflows/release-zetica.yml` | **v0.10.0** (`zetica-hub-windows-x64.zip`) |
| **[ZETIC7Z/effectcraft](https://github.com/ZETIC7Z/effectcraft)** | **Zetica Motion** (Motion graphics & 3D VFX compositor in pure Rust) | `storytold/effectcraft` | `.github/workflows/sync-upstream.yml`<br>`.github/workflows/release-zetica.yml` | **v0.17.0** (Published) |
| **[ZETIC7Z/artcraft](https://github.com/ZETIC7Z/artcraft)** | **Zetica Ecosystem** (Website, brand assets, tooling) | `storytold/artcraft` | `.github/workflows/sync-upstream.yml` | Pushed to `master` |

---

## 3. Motion Systems & Visual Engines (`site/`)

### 1. 3D WebGL Galaxy with Traveling Neon Pulses (`site/assets/js/zetica-hero-galaxy.js`):
- Faithful port of `hero-galaxy.tsx` and `hero-galaxy-tunables.ts`.
- **6 Extruded Ribbon Spiral Arms**:
  - Vertices extruded along Archimedean curve normals with vertex/fragment pulse shaders (`PULSE_VERT` and `PULSE_FRAG`).
  - Traveling comets of light with YIQ hue rotation:
    - Vivid emerald green, electric cyan, vibrant purple/violet, hot magenta, golden orange, and lime arcs sweeping along the spiral arms.
    - Swells dynamically as pulses pass (`uPulseW: 5.5px`).
- **32 3D Floating Showcase Cards**:
  - Custom vertex shader with 3D plane bowing toward camera (`world.z += uCurve * (0.25 - d2) * 2.0`).
  - 12-tap Poisson disk blur for the central soft nebula.
  - Chromatic dispersion / aberration on outer cards.
  - Rounded-rect SDF corner clipping and hairline glowing frame borders.
  - Preloaded artwork still textures + live looping WebM feature videos.
- **Physics**: Continuous forward idle drift (`0.57 cyc/min`), slow global rotation (`-50 deg/min`), scroll scrubbing, and critically damped mouse parallax tilt.
- **Theme Reactivity**: Listens to `zetica-theme-change` to instantly swap background and line colors between dark obsidian (`#040404`) and clean paper light (`#fafaf9`).

### 2. Scroll Ruler & 3-Home HeadingFlow Engine (`site/assets/js/zetica-scroll-ruler.js`):
- Faithful 1:1 port of `scroll-ruler.tsx`, `heading-flow.tsx`, and `ruler-tunables.ts` from `storytold/artcraft`.
- **Lenis Smooth 60fps Scrolling with Native Wheel Hook**:
  - Powered by `site/assets/js/lenis.min.js` (`lerp: 0.12, smoothWheel: true`).
  - Resolved mouse wheel blocking: Lenis virtual scroll is continuously stepped by passing high-resolution timestamps via `lenisInstance.raf(time)` inside `renderLoop(time)` at 60fps.
  - Verified full scroll playthrough via mouse wheel from top (`0px`) to footer (`5900px`) and back up (`0px`) with zero hitching.
- **Vertical Tick Rail**:
  - 1% minor ticks and 5% major labeled ticks (`00` through `100`).
  - Traveling accent needle with rolling odometer percentage readout (`000%` - `100%`).
  - Clicking any point on the rail jumps smoothly to that scroll percentage using Lenis.
- **Pure Text Hero Wordmark (`Z E T I C A`) & Zero-Logo Masthead**:
  - Hero masthead `#hero-wordmark-masthead` contains 100% pure text letters (`Z E T I C A`), with no inline logo, matching `getartcraft.com` 1:1.
  - Official **ZE** monogram logo resides in the header navbar (`.site-logo-img`), white in dark mode and solid black in light mode.
  - Animates the *actual* `#hero-wordmark-masthead` letter spans (`#wm-letter-0` to `#wm-letter-5`) directly in viewport space.
  - At scroll 0, letters sit naturally in the hero; from scroll 20px to 320px, they glide smoothly along an inward quadratic bezier curve straight to top stack slot 0.
- **Exact ArtCraft Subpixel DOM Measurement (Zero Canvas Bug)**:
  - Replaced canvas measurement with a temporary hidden DOM container (`font-size: 100px; line-height: 1; font-weight: 620; white-space: pre;`).
  - Eliminates the browser Canvas 2D CSS variable fallback bug that previously distorted letter advances.
  - Re-measures accurately on `window.resize` and `document.fonts.ready`.
- **Exact ArtCraft Typography, Unified 16px Sizing & Slot Spacing**:
  - Active Section Heading: **`34px`** display type, `font-weight: 620`, active bright ink (`#FFFFFF` in dark, `#09090b` in light) with crisp contrast drop shadow.
  - Stacked Headings & Bottom Queue: **`16px`** uppercase bold (`font-weight: 620`), `line-height: 1`. Every stacked word (`ZETICA`, `ZETICA APPS`, `ZETICA STUDIO`, `FEATURES`, `OWNERSHIP`, `COMMUNITY`, `GET STARTED`) renders at the **EXACT SAME 16px FONT SIZE**.
  - Vertical Slot Spacing: **`20px`** exact row pitch (identical for top pile and bottom queue).
  - Current Heading Gap: **`26px`** extra spacing above the 34px active heading.
  - Right Alignment: Flush right to guide line `vw - (railW + textPad)` (railW = 60px, textPad = 0px).
- **Interactive Resources Dropdown in Navbar**:
  - Added interactive hover & click dropdown with a 180ms debounce grace period to the Resources button in the header nav.
  - Links to `./tutorials.html`, `./news.html`, `./faq.html`, and `./press-kit.html`.
  - Frosted blur background, crisp 1px borders, and auto-inverting text colors matching active theme.

### 3. Light / Dark Mode Toggle (`site/assets/js/zetica-theme.js` & `site/assets/css/zetica-enhancements.css`):
- Interactively toggles theme via moon/sun navigation button.
- Synchronizes `localStorage` and `data-theme` attribute on `<html>`.
- Inverts logo to bright pure white in dark mode, and solid black in light mode.
- Deployed across all 40 HTML pages.

---

## 4. Live Browser Verification Artifacts
Captured and verified in Microsoft Edge and Chromium with 0 PageErrors and 0 Console Errors:
- `branding/verification/perfect_dark_scroll_0.png`: Dark mode resting hero with pure text `Z E T I C A` (zero inline logo), white ZE navbar monogram, and bottom-right queue (`ZETICA APPS` to `GET STARTED` all at 16px).
- `branding/verification/perfect_light_scroll_0.png`: Light mode resting hero with black ZE navbar monogram and pure text dark `Z E T I C A`.
- `branding/verification/perfect_dark_scroll_500.png`: `ZETICA` wordmark letters in flight into top-right stack, `ZETICA APPS` riding vertically along tick rail, and bottom queue.
- `branding/verification/perfect_dark_scroll_1500.png`: Top stack with `ZETICA` (16px) and `ZETICA APPS` (16px) stacked with exact 20px spacing, `ZETICA STUDIO` active in 34px bold display type, `FEATURES` riding on vertical rail, and bottom queue (`OWNERSHIP`, `COMMUNITY`, `GET STARTED` all at 16px).
- `branding/verification/perfect_dark_scroll_3500.png`: Deep scroll showing full stack with consistent 16px sizing and 0 console errors.
- `branding/verification/perfect_resources_dropdown.png`: Interactive Resources dropdown open showing `TUTORIALS`, `NEWS`, `FAQ`, and `PRESS KIT`.

