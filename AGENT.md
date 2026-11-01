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

## 4. Zetica Hub Desktop Launcher Rebranding (`craft-launcher`)

### 1. Two-Tone Brand Typography Engine (`crates/ui-egui/src/widgets.rs`):
- Formats every official suite app card, table row, and details drawer as **`ZETICA [APP]`** in exact two-tone coloring:
  - **`ZETICA `**: App category accent color (`t.app_ink(app)`).
    - Pink (`#FF7AB8`) for **`ZETICA EFFECT`**
    - Emerald Green (`#4FD68A`) for **`ZETICA GRID`**
    - Sky Blue (`#7CC8FF`) for **`ZETICA CAD`**
    - Vibrant Orange (`#FFA060`) for **`ZETICA DECK`**
    - Lime (`#A6E04A`) for **`ZETICA DESIGN`**
    - Cornflower Blue (`#7FB0FF`) for **`ZETICA PHOTO`**
    - Coral/Red (`#FF8A70`) for **`ZETICA VECTOR`**
    - Purple (`#B69CFF`) for **`ZETICA FILM`**
    - Amber/Gold (`#FFC14D`) for **`ZETICA LIGHT`**
    - Crimson (`#F23A62`) for **`ZETICA PDF`**
    - Teal (`#4FE8B6`) for **`ZETICA FIG`**
    - Indigo (`#8EA2FF`) for **`ZETICA WORD`**
    - Cyan (`#5FD0EE`) for **`ZETICA SOUND`**
  - **`[APP]`**: Solid bright ink / pure white (`t.ink_strong` / `#FFFFFF`).
  - Font styling: `egui::FontId::new(size, theme::display())` with `-0.02 * size` kerning.

### 2. Header & Surface Polishing (`crates/ui-egui/src/views.rs`):
- Center top header bar: Rebranded from `CRAFT APP SUITE` to **`ZETICA APP SUITE`**.
- Window title: Set to **`Zetica Hub`**.
- Monogram logo: Vector ZE logo with alt text `ZETICA`.
- Redundant badge elimination: Removed `[BY ZETICA]` badge next to official apps since the title itself starts with `ZETICA `.

### 3. Windows MSI Installer & Setup Wizard (`packaging/windows/`):
- **Package**: `zetica-hub-windows-x64.msi` (20.3 MB production release).
- **Setup Wizard Branding**:
  - Custom 493x312 left sidebar dialog (`WixUI_Bmp_Dialog`) featuring:
    - Clean white squircle desktop box with crisp black ZE monogram centered inside.
    - White `ZETICA` wordmark rendered in Archivo Variable typography.
    - `HUB` mono system label in Geist Mono.
    - 13 Zetica Suite animal/tool icons arranged in a clean hairline grid.
    - Vertical pink accent divider line (`#E0368F`).
  - Custom 493x58 banner header (`WixUI_Bmp_Banner`) with right dark cell containing the squircle logo and pink accent line.
  - Setup wizard copy:
    - Welcome title: `"Welcome to Zetica Hub 0.10.0"`
    - Description: `"Zetica Hub installs, updates and opens the Zetica App Suite: ZETICA PHOTO, ZETICA VECTOR, ZETICA FILM and the rest of the open-source Zetica apps. It installs for you only, so no administrator rights are needed. Click Next to continue."`
    - Folder Selection: Includes `PathEdit` with `"Change..."` button allowing users to choose the target drive or directory.
    - Optional desktop shortcut checkbox: Defaults to checked on initial install.
    - Exit dialog: `"Zetica Hub 0.10.0 is installed. Start it any time from the Start menu or desktop to install and update the Zetica App Suite."` with `"Launch Zetica Hub"` checkbox.
- **Desktop & Start Menu Shortcut Icon**:
  - High-resolution squircle tile design inspired by ArtCraft app icons and Antigravity desktop icon:
    - Pure white rounded square box (radius 210px) with subtle 2.5px light perimeter border (`#D2D6DE`).
    - Crisp solid black ZE monogram (`#0C0D11`) centered inside.
  - Multi-resolution Windows ICO (`artcraft-launcher.ico`) containing 16x16, 24x24, 32x32, 48x48, 64x64, 128x128, and 256x256 mipmaps.
  - Injected directly into the executable's `RT_GROUP_ICON` / `RT_ICON` PE resources so Windows Explorer and Desktop display the squircle icon natively.
- **Website Direct Download Pipeline**:
  - All 40 HTML pages updated across `site/*.html` and `UNCAGE/output/getartcraft.com/*.html` to link "DOWNLOAD ZETICA HUB" / "DOWNLOAD LAUNCHER" directly to:
    `/zetica-hub-windows-x64.msi` (`download="zetica-hub-windows-x64.msi"`).
  - Also served from `C:\Users\ZETICUZ\Downloads\zetica-hub-windows-x64.msi` and `C:\Users\ZETICUZ\Desktop\zetica-hub-windows-x64.msi`.
  - Zero `.zip` downloads; users download the native MSI directly.

### 4. Release Build Pipeline & Automated Artifacts:
- Updated `.github/workflows/release-zetica.yml` in `ZETIC7Z/craft-launcher`:
  - Automatically installs WiX Toolset v5 (`wix 5.0.2`, `WixToolset.UI.wixext`, `WixToolset.Util.wixext`).
  - Builds the release binary and packages both `zetica-hub-windows-x64.msi` and `zetica-hub-windows-x64.zip`.
  - Releases both assets on GitHub Releases.
- Committed all WiX configuration files (`artcraft-launcher.wxs`, `artcraft-launcher.en-us.wxl`, `package.ps1`).

---

## 5. Live Verification Artifacts
- `branding/verification/test_installer_dialog.bmp`: 493x312 pixel-perfect MSI installer dialog with squircle logo, white ZETICA wordmark, HUB label, 13 app icons, and pink accent divider.
- `branding/verification/test_installer_banner.bmp`: 493x58 banner header with right squircle logo cell and pink divider.
- `extracted_payload/updated_icon.png`: Verified squircle icon extracted from the PE resources of `zetica-hub.exe`.
- `test_extract_rebranded/verified_icon.png`: Verified squircle icon extracted from inside the MSI payload.
- `zetica-hub-windows-x64.msi`: 20,348,928 bytes valid Windows Installer MSI file, tested and verified with `msiexec /a` extraction and table verification.

---

## 6. JetBrains Student Pack & Tooling Integration
- **License Holder**: Lucas Navarro
- **License ID**: `A3840R48X0`
- **Subscription Expiry**: September 29, 2027
- **Included JetBrains Tooling**:
  - CLion, DataGrip, dotCover, dotMemory, dotTrace, GoLand, IntelliJ IDEA Ultimate, PhpStorm, PyCharm Professional, ReSharper, ReSharper C++, ReSharper SQL support, Rider, RubyMine, RustRover, WebStorm.
- **Local Installation**:
  - WebStorm 2026.2.2: `C:\Program Files\JetBrains\WebStorm 2026.2.2`

---

## 7. App Suite Rebranding & Automation Architecture
- **Zetica Deck (`ZETIC7Z/deckcraft`)**:
  - 100% pure Rust presentation app rebranded from DeckCraft.
  - Window Title: `Zetica Deck` / `Presenter View — Zetica Deck`.
  - Ribbon & Backstage: Rebranded header, links, and About modal with Sam Pangilinan attribution (`https://www.zeticuz.xyz/`).
  - Native Windows Packaging:
    - Dual-scope installation (`perUserOrMachine`).
    - Suite Directory: `Zetica\Deck` (`[LocalAppDataFolder]Programs\Zetica\Deck\` and `[%ProgramW6432]\Zetica\Deck\`).
    - Registry Paths: `Software\ZETICA\Deck` and `App Paths\zetica-deck.exe`.
- **Packaging Policy & Validation Rules**:
  - `check-icons.ps1`: AppUserModelID must match `xyz.zeticuz.zetica-hub`.
  - `check-install-policy.ps1`: Validates that suite folder allows `Zetica` or `ArtCraft`.
  - `install-policy.json`: Aligned registry keys with `Software\ZETICA\Zetica Hub`.
- **Continuous Upstream Synchronization**:
  - `.github/workflows/sync-upstream.yml` scheduled daily at `00:00 UTC` to pull upstream core engine updates while preserving the ZETICA brand identity layer.

---

## 8. Complete 14-App Suite Status & Production Releases (`ZETIC7Z`)

All 14 applications in the Zetica Suite are officially published with native Windows Installer (`.msi`) and portable standalone (`.zip`) releases on GitHub:

| # | Application | Repository | Latest Tag | Published Packages | Local State |
|---|---|---|---|---|---|
| 1 | **Zetica Hub** | `ZETIC7Z/craft-launcher` | `v0.10.4` | `zetica-hub-windows-x64.msi`<br>`zetica-hub-windows-x64.zip` | Installed (`v0.10.4`) |
| 2 | **Zetica Deck** | `ZETIC7Z/deckcraft` | `v0.12.0` | `zetica-deck-0.12.0-windows-x64.msi`<br>`zetica-deck-0.12.0-windows-x64-portable.zip` | Installed (`v0.12.0`) |
| 3 | **Zetica Design** | `ZETIC7Z/designcraft` | `v0.14.0` | `zetica-design-0.14.0-windows-x64.msi`<br>`zetica-design-0.14.0-windows-x64-portable.zip` | Installed (`v0.14.0`) |
| 4 | **Zetica Motion** | `ZETIC7Z/effectcraft` | `v0.19.0` | `zetica-motion-0.19.0-windows-x64.msi`<br>`zetica-motion-0.19.0-windows-x64-portable.zip` | Installed (`v0.19.0`) |
| 5 | **Zetica Sound** | `ZETIC7Z/soundcraft` | `v0.14.0` | `zetica-sound-0.14.0-windows-x64.msi`<br>`zetica-sound-0.14.0-windows-x64-portable.zip` | Installed (`v0.14.0`) |
| 6 | **Zetica PDF** | `ZETIC7Z/pdfcraft` | `v0.15.0` | `zetica-pdf-0.15.0-windows-x64.msi`<br>`zetica-pdf-0.15.0-windows-x64-portable.zip` | Installed (`v0.15.0`) |
| 7 | **Zetica Light** | `ZETIC7Z/lightcraft` | `v0.16.0` | `zetica-light-0.16.0-windows-x64.msi`<br>`zetica-light-0.16.0-windows-x64-portable.zip` | Installed (`v0.16.0`) |
| 8 | **Zetica Photo** | `ZETIC7Z/photocraft` | `v0.15.0` | `zetica-photo-0.17.0-windows-x64.msi`<br>`zetica-photo-0.17.0-windows-x64-portable.zip` | Available |
| 9 | **Zetica Vector** | `ZETIC7Z/vectorcraft` | `v0.15.0` | `zetica-vector-0.18.0-windows-x64.msi`<br>`zetica-vector-0.18.0-windows-x64-portable.zip` | Available |
| 10 | **Zetica Film** | `ZETIC7Z/filmcraft` | `v0.13.0` | `zetica-film-0.14.0-windows-x64.msi`<br>`zetica-film-0.14.0-windows-x64-portable.zip` | Available |
| 11 | **Zetica CAD** | `ZETIC7Z/cadcraft` | `v0.14.0` | `zetica-cad-0.14.0-windows-x64.msi`<br>`zetica-cad-0.14.0-windows-x64-portable.zip` | Available |
| 12 | **Zetica Grid** | `ZETIC7Z/gridcraft` | `v0.13.0` | `zetica-grid-0.13.0-windows-x64.msi`<br>`zetica-grid-0.13.0-windows-x64-portable.zip` | Available |
| 13 | **Zetica Fig** | `ZETIC7Z/figcraft` | `v0.12.0` | `zetica-fig-0.12.1-windows-x64.msi`<br>`zetica-fig-0.12.1-windows-x64-portable.zip` | Available |
| 14 | **Zetica Word** | `ZETIC7Z/wordcraft` | `v0.12.0` | `zetica-word-0.12.0-windows-x64.msi`<br>`zetica-word-0.12.0-windows-x64-portable.zip` | Available |

### Release Feed Architecture & BOM Resolution:
- **Feed Endpoint**: `https://zetica.vercel.app/api/v1/release_info`
- **Root Cause & Fix**: PowerShell default UTF-8 output appends a 3-byte Byte Order Mark (`0xEF 0xBB 0xBF`), which causes strict JSON parsers (such as Rust's `serde_json::from_str`) to fail with "unexpected value at line 1 column 1".
- **Resolution**: Updated `scripts/generate_release_feed.ps1` to use `[System.Text.UTF8Encoding]::new($false)` (UTF-8 without BOM). Deployed to Vercel production with `Content-Type: application/json` and `Access-Control-Allow-Origin: *`.
- **Zetica Hub Detection Engine**:
  - `FEED_URL` pointed to `https://zetica.vercel.app/api/v1/release_info`.
  - Windows registry detection accepts `Publisher: "ZETICA / Sam Pangilinan"`.
  - Exe resolver detects `AppData\Local\Programs\Zetica\<App>`.
  - Desktop shortcuts point to `Zetica <App>.lnk` with custom branded icons and descriptions.

