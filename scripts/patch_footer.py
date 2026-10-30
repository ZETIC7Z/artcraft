import glob
import os
import re

site_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com"
html_files = glob.glob(os.path.join(site_dir, "**", "*.html"), recursive=True)

pattern = r'<div class="flex flex-col gap-2 border-t border-line px-6 py-4 md:flex-row md:items-center md:justify-between md:px-10">.*?</div>'

for hf in html_files:
    rel_depth = len(os.path.relpath(hf, site_dir).split(os.sep)) - 1
    prefix = "../" * rel_depth if rel_depth > 0 else "./"
    
    with open(hf, "r", encoding="utf-8") as f:
        html = f.read()

    replacement = f'''<div class="border-t border-line px-6 py-8 md:px-10 bg-bg">
  <div class="flex flex-col items-center justify-center gap-4 text-center">
    <div class="flex items-center justify-center gap-3">
      <img src="{prefix}assets/images/zeticuz-logo.svg" alt="Sam Pangilinan" class="h-6 w-auto" />
      <span class="hud-label text-xs uppercase tracking-widest text-muted">SITE DEVELOPED BY: <strong class="text-ink font-semibold">Sam Pangilinan</strong> · © 2026</span>
    </div>
    <a href="https://www.zeticuz.xyz/" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-2 px-5 py-2.5 border border-line bg-bg hover:bg-invert-bg hover:text-invert-fg transition-all text-xs font-mono font-medium tracking-wider">
      <span>VISIT DEVELOPER PORTFOLIO</span>
      <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17 17 7"></path><path d="M7 7h10v10"></path></svg>
    </a>
  </div>
</div>'''

    new_html = re.sub(pattern, replacement, html, flags=re.DOTALL)
    if new_html != html:
        with open(hf, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"Patched footer in {os.path.basename(hf)}")

print("All footers successfully patched!")
