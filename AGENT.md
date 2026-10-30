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
- Faithful port of `scroll-ruler.tsx`, `heading-flow.tsx`, and `ruler-tunables.ts`.
- **Lenis Smooth Scrolling**: Powered by `site/assets/js/lenis.min.js` at 60fps with exponential easing.
- **Vertical Tick Rail**:
  - 1% minor ticks and 5% major labeled ticks (`00` through `100`).
  - Traveling accent needle with rolling odometer percentage readout (`000%` - `100%`).
  - Clicking any point on the rail jumps smoothly to that scroll percentage using Lenis.
- **3-Home Lifecycle per Section**:
  1. **Bottom Queue**: Flush right-aligned compact links stacked at bottom-right (`ZETICA APPS`, `ZETICA STUDIO`, `FEATURES`, `OWNERSHIP`, `COMMUNITY`, `GET STARTED`).
  2. **Riding Rail**: Vertically riding words with letters rotated -90 degrees on the right tick rail tracking document scroll 1:1.
  3. **Top Stack**: Stacked compact titles under the top navbar (`ZETICA`, `ZETICA APPS`, `ZETICA STUDIO`), with the active section heading rendered in bold 32px display type.
- **Hero Wordmark Flight**: `ZETICA` glides smoothly from center hero into the top stack slot via an inward-curved quadratic bezier arc as scroll advances from 20px to 340px.
- Deployed across all 40 HTML pages.

### 3. Light / Dark Mode Toggle (`site/assets/js/zetica-theme.js` & `site/assets/css/zetica-enhancements.css`):
- Interactively toggles theme via moon/sun navigation button.
- Synchronizes `localStorage` and `data-theme` attribute on `<html>`.
- Inverts logo to bright pure white in dark mode, and solid black in light mode.
- Deployed across all 40 HTML pages.

---

## 4. Live Browser Verification Artifacts
Captured and verified in Microsoft Edge:
- `branding/verification/live_dark_scroll_0.png`: Dark mode resting hero with white ZE monogram, center `ZETICA`, and bottom-right queue.
- `branding/verification/live_dark_scroll_350.png`: `ZETICA` wordmark transferring into top-right stack and `ZETICA APPS` riding vertically on right tick rail.
- `branding/verification/live_dark_scroll_1000.png`: `ZETICA APPS` active heading in 32px bold, `ZETICA` stacked at top, and `ZETICA STUDIO` riding rail.
- `branding/verification/live_dark_scroll_features.png`: `FEATURES` section active, stacked titles at top-right (`ZETICA`, `ZETICA APPS`, `ZETICA STUDIO`), cyan needle at 34%, and bottom queue.
- `branding/verification/live_light_scroll_features.png`: Clean paper light mode with black typography, black ZE monogram, and cobalt accent needle.
- `branding/verification/live_light_scroll_0.png`: Light mode hero with black ZE monogram, neon pulses, and bottom-right queue.
- `branding/verification/footer_verification.png`: Sam Pangilinan footer attribution standard and interactive button.
