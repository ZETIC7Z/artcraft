import os
import glob
import re

directories = [
    r'c:\Users\ZETICUZ\Documents\artcraft\site',
    r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com'
]

CSS_STYLE = """<style id="zetica-reveal-styles">
  [data-reveal], [data-draw-eyebrow], [data-choreo], section, article, figure, div[style*="opacity: 0"], div[style*="visibility: hidden"] {
    opacity: 1 !important;
    visibility: visible !important;
    transform: none !important;
    filter: none !important;
  }
  [data-draw-rule] {
    transform: scale(1, 1) !important;
  }
  [data-draw-tick] {
    opacity: 1 !important;
    transform: scale(1, 1) !important;
  }
  img.themed-logo {
    height: 24px !important;
    max-height: 24px !important;
    max-width: 48px !important;
    width: auto !important;
    object-fit: contain !important;
    display: inline-block !important;
  }
  footer img.themed-logo {
    height: 32px !important;
    max-height: 32px !important;
    max-width: 64px !important;
  }
</style>"""

for base_dir in directories:
    if not os.path.exists(base_dir):
        continue
    html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)
    for fpath in html_files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        if '<style id="zetica-reveal-styles">' in content:
            new_content = re.sub(r'<style id="zetica-reveal-styles">.*?</style>', CSS_STYLE, content, flags=re.DOTALL)
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Enhanced reveal styles in: {fpath}")

print("Enhanced reveal styles complete!")
