# AGENT.md — Project Memory & Architecture Guide

## 1. Project Overview & Vision
- **Project**: **ZETICA Creative Suite & Hub** (100% native Rust desktop creative ecosystem).
- **Developer**: **Sam Pangilinan** (`ZETICUZ` / `ZETIC7Z` / `TECHNOLOHIYA`), Portfolio: `https://www.zeticuz.xyz/`.
- **Primary Brand Name**: **ZETICA** (ALL CAPS).
- **Official Brand Logo**: `C:\Users\ZETICUZ\Downloads\Powe.svg` (3D neon-ember chrome monogram).
- **Official Developer Logo**: `C:\Users\ZETICUZ\Downloads\zeticuz-logo.svg`.
- **Standard Footer Signature**:
  - Centered: `[zeticuz-logo.svg] SITE DEVELOPED BY: Sam Pangilinan · © 2026`
  - Interactive button opening `https://www.zeticuz.xyz/` in a new tab without showing raw URL string.

---

## 2. Repositories & GitHub Infrastructure (`ZETIC7Z`)

| Repository | Role | Upstream | Workflows Active | Releases |
|---|---|---|---|---|
| **[ZETIC7Z/craft-launcher](https://github.com/ZETIC7Z/craft-launcher)** | **Zetica Hub** (Native desktop installer, hub & updater) | `storytold/craft-launcher` | `.github/workflows/sync-upstream.yml`<br>`.github/workflows/release-zetica.yml` | **v0.10.0** (`zetica-hub-windows-x64.zip`) |
| **[ZETIC7Z/effectcraft](https://github.com/ZETIC7Z/effectcraft)** | **Zetica Motion** (Motion graphics & 3D VFX compositor in pure Rust) | `storytold/effectcraft` | `.github/workflows/sync-upstream.yml`<br>`.github/workflows/release-zetica.yml` | **v0.17.0** (Building) |
| **[ZETIC7Z/artcraft](https://github.com/ZETIC7Z/artcraft)** | **Zetica Ecosystem** (Website, brand assets, tooling) | `storytold/artcraft` | `.github/workflows/sync-upstream.yml` | Pushed to `master` |

### Automated Synchronization & Releases:
- **Daily Upstream Sync**: All three repositories (`artcraft`, `craft-launcher`, and `effectcraft`) run automated daily synchronization (`cron: 0 0 * * *`) pulling updates from `storytold` while preserving all ZETICA brand assets and metadata.
- **Standalone Release Workflows**: GitHub Actions builds Windows x64 portable binaries (`zetica-hub.exe`, `zetica-motion.exe`), packages `.zip` archives, and publishes GitHub releases automatically.
- **Direct Installer Delivery**: All 40 cloned site pages have had their download buttons wired directly to the published releases (`https://github.com/ZETIC7Z/craft-launcher/releases/download/v0.10.0/zetica-hub-windows-x64.zip`).

---

## 3. Cloned & Rebranded Website (`site/`)
- **Source**: Cloned directly from `https://getartcraft.com/` using **UNCAGE** (`C:\Users\ZETICUZ\Documents\UNCAGE`).
- **Pages**: 40 Static HTML pages (`index.html`, `download.html`, `pricing.html`, `apps.html`, 13 app detail pages, FAQ, tutorials, news).
- **Visual Assets & Motion**:
  - Official 3D chrome emblem (`zetica-icon.svg`) embedded into top-nav and hero watermark.
  - 7 downloaded local feature WebM videos (`videos/features/*.webm`) with autoplay and looped playback.
  - 13 app cards with colored icons and updated Zetica suite names:
    - **Zetica Photo**, **Zetica Vector**, **Zetica Film**, **Zetica Light**, **Zetica PDF**, **Zetica Motion**, **Zetica Design**, **Zetica Fig**, **Zetica Word**, **Zetica Sound**, **Zetica Deck**, **Zetica CAD**, **Zetica Grid**.
  - Developer attribution footer integrated across all 40 pages with interactive portfolio link.
- **Local Testing**:
  - Tested on `http://localhost:8792`.
  - Visual verification proof captured in `branding/zetica_live_hero.png`, `zetica_live_apps.png`, `zetica_live_features.png`, `zetica_live_footer.png`, and `zetica_live_full.png`.

---

## 4. Legal & Licensing
- Engine code is dual-licensed under **MIT OR Apache-2.0**.
- Upstream trademark compliance verified: all ArtCraft trademarks and "A" logos removed and replaced with official ZETICA branding.
