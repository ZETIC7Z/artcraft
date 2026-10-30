# AGENT.md — Project Memory & Architecture Guide

## 1. Project Overview & Vision
- **Project**: **Zetica Creative Suite** (formerly ArtCraft fork).
- **Core Goal**: A completely independent, customized, and branded creative desktop software ecosystem with a unified native installer/launcher (`Zetica Hub`) and standalone creative applications (VFX, Photo, Vector, Video, UI/UX, Audio, CAD, and PDF), rebranded under **Sam Pangilinan (`ZETICUZ`)**.
- **Foundational Repositories**:
  - Main Launcher: `storytold/craft-launcher` -> Forked & rebranded as `Zetica Hub` (`zetica-launcher`)
  - VFX & Motion Graphics: `storytold/effectcraft` -> Forked & rebranded as `Zetica Motion`
  - Supporting Apps: `photocraft`, `vectorcraft`, `filmcraft`, `lightcraft`, `figcraft`, `soundcraft`, `cadcraft`, `pdfcraft`.

## 2. Developer & Brand Identity
- **Developer**: Sam Pangilinan (`ZETICUZ` / `ZETIC7Z` / `TECHNOLOHIYA`)
- **Portfolio**: `https://www.zeticuz.xyz/`
- **Primary Brand Name**: **ZETICA** (or **ZETICA STUDIO** / **ZETICRAFT**)
- **Visual Motif**: The official ZETICUZ crimson-metallic angular winged crest (`#E50914` / `#A30010`) on matte obsidian squircle plates (`#0B0B0E` / `#15161C`).
- **Footer Attribution Standard**: `[zeticuz-logo.svg] SITE DEVELOPED BY: Sam Pangilinan · © 2026` linking to `https://www.zeticuz.xyz/`.

## 3. Legal & Licensing Mandates
- **Engine Code License**: Dual-licensed under **MIT OR Apache-2.0**. Full legal authorization to fork, modify, rename, compile, and distribute.
- **Trademark Compliance**: The upstream authors explicitly stipulate that *the ArtCraft name, logo, and "A" mark must be removed in all forks and modified versions*. Rebranding to Zetica is directly compliant with upstream licensing.

## 4. Architecture & Workspace Map
```text
c:\Users\ZETICUZ\Documents\artcraft\
├── AGENT.md                    # Project context & architecture guide (this file)
├── branding/                   # Vector SVGs, icon sets, color tokens & design guidelines
│   ├── zetica-logo.svg         # Master horizontal brand lockup
│   ├── zetica-hub-icon.svg     # Master launcher icon
│   ├── zetica-motion-icon.svg  # Motion & VFX app icon (EffectCraft)
│   ├── zetica-canvas-icon.svg  # Photo editor app icon (PhotoCraft)
│   ├── zetica-vector-icon.svg  # Vector drawing app icon (VectorCraft)
│   ├── zetica-cinema-icon.svg  # Video editor app icon (FilmCraft)
│   ├── zetica-raw-icon.svg     # RAW development app icon (LightCraft)
│   ├── zetica-frame-icon.svg   # UI/UX prototyping app icon (FigCraft)
│   ├── zetica-wave-icon.svg    # Digital audio app icon (SoundCraft)
│   ├── zetica-dimension-icon.svg # CAD & 3D app icon (CADCraft)
│   └── zetica-doc-icon.svg     # PDF studio app icon (PdfCraft)
├── catalog/                    # App metadata, release feeds & update schemas
│   └── apps.json               # Defines apps, platforms, download URLs, SHA256 feeds
└── scripts/                    # Automation scripts for toolchain setup, builds, & packaging
```

## 5. Technology Stack
- **Languages**: Pure Rust (1.90+). Zero Electron, zero webview dependencies.
- **GUI Framework**: Native `egui` and `eframe` (low memory, 60fps native rendering).
- **Windows Packaging**: WiX Toolset v3/v4 (`.msi`) or Inno Setup / NSIS (`.exe` setup).
- **CI/CD Automation**: GitHub Actions for automated cross-compilation, checksum calculation (`SHA256SUMS.txt`), and automatic GitHub Releases deployment.
