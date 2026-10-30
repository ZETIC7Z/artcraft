import glob
import os
import re

site_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com"

# 1. Gather all HTML files
html_files = glob.glob(os.path.join(site_dir, "**", "*.html"), recursive=True)
print(f"Processing {len(html_files)} HTML files...")

reveal_css = """
<style id="zetica-reveal-styles">
  [data-reveal], [data-draw-eyebrow] {
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
    filter: none !important;
    transition: opacity 0.5s ease-out, transform 0.5s ease-out, filter 0.5s ease-out;
  }
  [data-draw-rule] {
    transform: scale(1, 1) !important;
  }
  [data-draw-tick] {
    opacity: 1 !important;
    transform: scale(1, 1) !important;
  }
</style>
"""

for hf in html_files:
    rel_depth = len(os.path.relpath(hf, site_dir).split(os.sep)) - 1
    prefix = "../" * rel_depth if rel_depth > 0 else "./"
    
    with open(hf, "r", encoding="utf-8") as f:
        html = f.read()

    # Inject reveal styles into head
    if "zetica-reveal-styles" not in html:
        html = html.replace("</head>", f"{reveal_css}</head>")

    # Replace Hero Watermark in index.html
    if os.path.basename(hf) == "index.html" and rel_depth == 0:
        # Pattern to replace wm-letter container
        wm_pattern = r'<div role="img" aria-label="ARTCRAFT"[^>]*>.*?</div></div><h1'
        zetica_wm = f'''<div role="img" aria-label="ZETICA" class="relative whitespace-pre text-ink-strong my-4" style="font-family: var(--font-archivo), system-ui, sans-serif; font-weight: 850; font-stretch: 125%; font-size: clamp(48px, 9vw, 96px); line-height: 1; letter-spacing: 0.08em; display: flex; align-items: center; justify-content: center; gap: 0.35em;">
  <img src="{prefix}assets/images/zetica-icon.svg" alt="ZETICA" style="height: 0.82em; width: auto; vertical-align: -0.05em; filter: drop-shadow(0 0 1.2vw rgba(255, 120, 0, 0.45)) drop-shadow(0 0.4vw 2vw rgba(0, 180, 255, 0.35));" />
  <span>ZETICA</span>
</div><h1'''
        html = re.sub(wm_pattern, zetica_wm, html, flags=re.DOTALL)

    # Make videos autoplay & fix relative path
    html = re.sub(r'src="/videos/features/', f'src="{prefix}videos/features/', html)
    html = html.replace('<video src="', '<video autoplay="" loop="" muted="" playsinline="" src="')

    # Replace footer bottom bar with developer signature standard
    footer_bottom_pattern = r'<div class="border-t border-line py-6">\s*<div class="flex flex-col items-center justify-between gap-4 sm:flex-row">.*?</div>\s*</div>'
    zetica_footer = f'''<div class="border-t border-line py-8">
  <div class="flex flex-col items-center justify-center gap-4 text-center">
    <div class="flex items-center justify-center gap-3">
      <img src="{prefix}assets/images/zeticuz-logo.svg" alt="Sam Pangilinan" class="h-6 w-auto" />
      <span class="hud-label text-xs uppercase tracking-widest text-muted">SITE DEVELOPED BY: <strong class="text-ink font-semibold">Sam Pangilinan</strong> · © 2026</span>
    </div>
    <a href="https://www.zeticuz.xyz/" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-4 py-2 border border-line bg-bg hover:bg-invert-bg hover:text-invert-fg transition-all text-xs font-mono font-medium tracking-wider">
      <span>VISIT DEVELOPER PORTFOLIO</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7"></path><path d="M7 7h10v10"></path></svg>
    </a>
  </div>
</div>'''
    html = re.sub(footer_bottom_pattern, zetica_footer, html, flags=re.DOTALL)

    # Core brand text replacements (order matters: specific phrases first)
    replacements = [
        ("ArtCraft Studio", "Zetica Studio"),
        ("ARTCRAFT STUDIO", "ZETICA STUDIO"),
        ("artcraft studio", "zetica studio"),
        ("All Crafting Apps", "All Zetica Apps"),
        ("Explore Crafting Apps", "Explore Zetica Apps"),
        ("EXPLORE CRAFTING APPS", "EXPLORE ZETICA APPS"),
        ("Crafting Apps", "Zetica Apps"),
        ("CRAFTING APPS", "ZETICA APPS"),
        ("Craft Apps", "Zetica Apps"),
        ("CRAFT APPS", "ZETICA APPS"),
        ("craft apps", "zetica apps"),
        ("ArtCraft Launcher", "Zetica Hub"),
        ("ARTCRAFT LAUNCHER", "ZETICA HUB"),
        ("Craft Launcher", "Zetica Hub"),
        ("CRAFT LAUNCHER", "ZETICA HUB"),
        ("craft launcher", "zetica hub"),
        ("Download Launcher", "Download Zetica Hub"),
        ("DOWNLOAD LAUNCHER", "DOWNLOAD ZETICA HUB"),
        ("EffectCraft", "Zetica Motion"),
        ("EFFECTCRAFT", "ZETICA MOTION"),
        ("effectcraft", "zetica-motion"),
        ("PhotoCraft", "Zetica Photo"),
        ("VectorCraft", "Zetica Vector"),
        ("FilmCraft", "Zetica Film"),
        ("LightCraft", "Zetica Light"),
        ("PdfCraft", "Zetica PDF"),
        ("DesignCraft", "Zetica Design"),
        ("FigCraft", "Zetica Fig"),
        ("WordCraft", "Zetica Word"),
        ("SoundCraft", "Zetica Sound"),
        ("DeckCraft", "Zetica Deck"),
        ("CADCraft", "Zetica CAD"),
        ("GridCraft", "Zetica Grid"),
        ("ARTCRAFT", "ZETICA"),
        ("ArtCraft", "Zetica"),
        ("Artcraft", "Zetica"),
        ("https://github.com/storytold/craft-launcher", "https://github.com/ZETIC7Z/craft-launcher"),
        ("https://github.com/storytold/effectcraft", "https://github.com/ZETIC7Z/effectcraft"),
        ("https://github.com/storytold/artcraft", "https://github.com/ZETIC7Z/artcraft"),
        ("https://github.com/storytold", "https://github.com/ZETIC7Z"),
        ("storytold", "ZETIC7Z"),
        ("hello@storyteller.ai", "contact@zeticuz.xyz"),
        ("https://getartcraft.com", "https://zetica.xyz"),
        ("getartcraft.com", "zetica.xyz"),
    ]

    for old, new in replacements:
        html = html.replace(old, new)

    with open(hf, "w", encoding="utf-8") as f:
        f.write(html)

print("HTML files updated successfully!")

# 2. Update JS files for hydration consistency
js_files = glob.glob(os.path.join(site_dir, "assets", "js", "*.js"))
print(f"Updating {len(js_files)} JS bundles...")

js_replacements = [
    ("ARTCRAFT", "ZETICA"),
    ("ArtCraft", "Zetica"),
    ("Artcraft", "Zetica"),
    ("Craft Apps", "Zetica Apps"),
    ("Crafting Apps", "Zetica Apps"),
    ("EffectCraft", "Zetica Motion"),
    ("PhotoCraft", "Zetica Photo"),
    ("VectorCraft", "Zetica Vector"),
    ("FilmCraft", "Zetica Film"),
    ("LightCraft", "Zetica Light"),
    ("PdfCraft", "Zetica PDF"),
    ("DesignCraft", "Zetica Design"),
    ("FigCraft", "Zetica Fig"),
    ("WordCraft", "Zetica Word"),
    ("SoundCraft", "Zetica Sound"),
    ("DeckCraft", "Zetica Deck"),
    ("CADCraft", "Zetica CAD"),
    ("GridCraft", "Zetica Grid"),
    ("hello@storyteller.ai", "contact@zeticuz.xyz"),
    ("storytold", "ZETIC7Z"),
    ("getartcraft.com", "zetica.xyz"),
]

for jf in js_files:
    try:
        with open(jf, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        modified = content
        for old, new in js_replacements:
            if old in modified:
                modified = modified.replace(old, new)
        if modified != content:
            with open(jf, "w", encoding="utf-8") as f:
                f.write(modified)
    except Exception as e:
        print(f"Error on {jf}: {e}")

print("Rebrand completed across all HTML and JS assets!")
