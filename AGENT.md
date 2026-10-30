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
- **Lenis Smooth Scrolling**: Powered by `site/assets/js/lenis.min.js` at 60fps with exponential easing across all pages.
- **Vertical Tick Rail**:
  - 1% minor ticks and 5% major labeled ticks (`00` through `100`).
  - Traveling accent needle with rolling odometer percentage readout (`000%` - `100%`).
  - Clicking any point on the rail jumps smoothly to that scroll percentage using Lenis.
- **Permanent Elimination of White Box in Top-Right Corner**:
  - Cloned static SSR HTML contained pre-baked `<div role="scrollbar">` elements with light-mode backgrounds.
  - Successfully purged via `scripts/remove_dead_scrollbars.py` across all 39 static HTML pages in `site/` and synchronized to UNCAGE output.
- **Zero-Duplicate Hero Wordmark Flight**:
  - Eliminated clone `.flow-word-box[data-label="ZETICA"]`.
  - Animates the *actual* `#hero-wordmark-masthead` letter spans (`#wm-letter-0` to `#wm-letter-6`) directly in viewport space.
  - At scroll 0, letters sit naturally with zero clones; from scroll 20px to 320px, they glide smoothly along an inward quadratic bezier curve straight to the top stack slot.
- **Exact ArtCraft Typography & Metrics (`src_ref/ruler-tunables.ts`)**:
  - Active Section Heading: **`34px`** display type, `font-weight: 800`, active bright ink (`#FFFFFF` in dark, `#09090b` in light) with crisp contrast drop shadow.
  - Riding Word on Rail: **`20px`** uppercase, `font-weight: 700`, rotated `-90deg` along the tick line.
  - Stacked Headings & Bottom Queue: **`16px`** bold uppercase (`font-weight: 700`), letter-spacing `0.04em`.
  - Slot Spacing: `22px`; gap to active heading: `28px`.
  - Right Alignment: Flush right to guide line `vw - (railW + textPad)` (24px inset from 60px rail).
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
Captured and verified in Microsoft Edge and Chromium with 0 PageErrors:
- `branding/verification/perfect_dark_scroll_0.png`: Dark mode resting hero with white ZE monogram, center `ZETICA`, zero duplicate text, zero white boxes in the top-right corner, and bottom-right queue.
- `branding/verification/verified_resources_hover.png`: Interactive Resources dropdown open showing `TUTORIALS`, `NEWS`, `FAQ`, and `PRESS KIT`.
- `branding/verification/perfect_resources_dropdown_dark.png`: High-contrast dark mode Resources dropdown under the navbar.
- `branding/verification/perfect_dark_scroll_350.png`: Actual `ZETICA` wordmark letters in flight into the top-right stack, with `ZETICA APPS` riding vertically along the tick rail.
- `branding/verification/perfect_dark_scroll_features.png`: `FEATURES` active in 34px bold display type, `ZETICA`, `ZETICA APPS`, `ZETICA STUDIO` stacked at top-right, cyan needle at 34%, and bottom queue.
- `branding/verification/perfect_dark_scroll_community.png`: `COMMUNITY` active in 34px bold display type (matching user reference image 2), `GET STARTED` riding rail, needle at 083%.
- `branding/verification/perfect_light_scroll_features.png`: Clean paper light mode with black typography, black ZE monogram, and sky blue accent needle.
- `branding/verification/footer_verification.png`: Sam Pangilinan footer attribution standard and interactive developer portfolio button.

