# AGENT.md — Project Memory & Architecture Guide

## 1. Project Overview & Vision
- **Project**: **ZETICA Creative Suite & Hub** (100% native Rust desktop creative ecosystem).
- **Developer**: **Sam Pangilinan** (`ZETICUZ` / `ZETIC7Z` / `TECHNOLOHIYA`), Portfolio: `https://www.zeticuz.xyz/`.
- **Primary Brand Name**: **ZETICA** (ALL CAPS).
- **Official Brand Logo**: Pure black **ZE** monogram vector (`branding/zetica-monogram-black.svg` / `site/assets/images/zetica-monogram.svg`), extracted from `C:\Users\ZETICUZ\Downloads\ZE.svg`.
  - Replaced the previous 3D ember cube logo; crisp, solid black, retina-sharp (`1823x1275` aspect ratio 1.43).
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

### Automated Synchronization & Releases:
- **Daily Upstream Sync**: All three repositories run automated daily synchronization (`cron: 0 0 * * *`) pulling updates from `storytold` while preserving all ZETICA brand assets and metadata.
- **Standalone Release Workflows**: GitHub Actions builds Windows x64 portable binaries (`zetica-hub.exe`, `zetica-motion.exe`), packages `.zip` archives, and publishes GitHub releases automatically.
- **Direct Installer Delivery**: All 40 cloned site pages have had their download buttons wired directly to the published releases (`https://github.com/ZETIC7Z/craft-launcher/releases/download/v0.10.0/zetica-hub-windows-x64.zip`).

---

## 3. Rebranded Website & Motion System (`site/`)
- **Source**: Cloned from `https://getartcraft.com/` using **UNCAGE** (`C:\Users\ZETICUZ\Documents\UNCAGE`), fully converted and enhanced with local Three.js & GSAP animation engines.
- **Pages**: 40 Static HTML pages (`index.html`, `download.html`, `pricing.html`, `apps.html`, 13 app detail pages, FAQ, tutorials, news).
- **Core Visual Assets**:
  - Official solid black ZE monogram vector deployed to top navigation, hero watermark, and footer.
  - Zero colored ember shadow on hero monogram for an ultra-clean, modern aesthetic.
  - 13 app cards with colored icons and updated Zetica suite names:
    - **Zetica Photo**, **Zetica Vector**, **Zetica Film**, **Zetica Light**, **Zetica PDF**, **Zetica Motion**, **Zetica Design**, **Zetica Fig**, **Zetica Word**, **Zetica Sound**, **Zetica Deck**, **Zetica CAD**, **Zetica Grid**.
  - Developer attribution footer integrated across all 40 pages with interactive portfolio link.

### 4. 3D WebGL Galaxy & Scroll Animation Engine:
- **3D Hero Galaxy (`site/assets/js/zetica-hero-galaxy.js`)**:
  - Faithfully ported from `storytold/artcraft-services` -> `frontend/apps/artcraft-website-next/src/components/landing/hero-galaxy.tsx`.
  - 6 Archimedean spiral arms with hairline guide curves, construction circle, and perpendicular ticks.
  - 30 floating showcase cards with custom vertex and fragment shaders:
    - 3D plane bowing towards camera (`world.z += uCurve * (0.25 - d2) * 2.0;`).
    - 12-tap Poisson disk blur nebula near origin.
    - Chromatic dispersion / aberration on outer cards.
    - Rounded-rect SDF corner clipping and hairline glowing borders.
    - Preloaded artwork still textures + 7 live looping WebM feature video textures.
  - Continuous forward idle conveyor drift (`0.57 cyc/min`), slow global rotation (`-50 deg/min`), scroll scrubbing, and critically damped mouse parallax tilt.
- **Hero Wordmark & Scroll Transfer (`site/assets/js/zetica-wordmark-scroll.js`)**:
  - Ported from `hero-wordmark.tsx` and `heading-flow.tsx`.
  - Page load intro: ZE monogram glides from center to left while `Z`, `E`, `T`, `I`, `C`, `A` emerge via blade-clip wipe.
  - Scroll transfer: As user scrolls down past hero, the wordmark condenses and translates towards the top navbar header slot, reversing cleanly on scroll up.

---

## 5. Live Browser Verification & Testing
- Tested and verified on `http://localhost:8792`.
- Verification captures saved in `branding/verification/`:
  - `hero_3d_galaxy_live.png`: Hero at rest showing rotating 3D galaxy with video cards, hairline spiral ticks, and clean black ZE monogram.
  - `hero_wordmark_scroll_250px.png`: Wordmark condensing and transferring upward during scroll.
  - `features_scroll_500px.png`: Thirteen Zetica apps row with background galaxy pass-through.
  - `footer_verification.png`: Sam Pangilinan developer footer signature and interactive portfolio button.
  - `ze_black_svg_render.png`: Clean standalone vector render of `ZE.svg` monogram.
- Browser console: 0 errors, 0 broken requests.
