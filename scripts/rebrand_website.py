import os
import shutil
import re

root_dir = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas'
html_path = os.path.join(root_dir, 'index.html')
js_dir = os.path.join(root_dir, 'assets', 'js')
images_dir = os.path.join(root_dir, 'assets', 'images')

# 1. Copy logos
src_nav_logo = r'c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_nav_logo.svg'
dest_nav1 = os.path.join(images_dir, 'SSqo2xpb8BFyqexlL0GXm9AUGw-8ce4293f.svg')
dest_nav2 = os.path.join(images_dir, 'SSqo2xpb8BFyqexlL0GXm9AUGw.svg')
shutil.copyfile(src_nav_logo, dest_nav1)
shutil.copyfile(src_nav_logo, dest_nav2)

src_zlogo = r'C:\Users\ZETICUZ\Downloads\zeticuz-logo.svg'
dest_zlogo = os.path.join(images_dir, 'zeticuz-logo.svg')
shutil.copyfile(src_zlogo, dest_zlogo)
print('Copied nav logo and zeticuz logo to assets/images')

# 2. Update index.html
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Update page title
html = re.sub(r'<title>.*?</title>', '<title>ZETICA &mdash; Open-Source Native Creative Suite</title>', html, flags=re.DOTALL)

# Inject CSS to hide Framer badge and template voucher
custom_css = '''
<style id="zetica-custom-overrides">
  .framer-1bh5pfw-container, #__framer-badge-container { display: none !important; }
  .zeticuz-footer-attribution a:hover {
    background: rgba(255,255,255,0.14) !important;
    border-color: #38bdf8 !important;
  }
</style>
'''
if 'id="zetica-custom-overrides"' not in html:
    html = html.replace('</head>', custom_css + '\n</head>')

# Text replacements in index.html
replacements = [
    ('Supercharge Your Business With AI-Powered Intelligence', 'Supercharge Your Creativity With Native Rust Intelligence'),
    ('Supercharge Your Business', 'Supercharge Your Creativity'),
    ('With AI-Powered', 'With Native Rust'),
    ('Get Started for Free', 'Download Now'),
    ('Get This Template', 'Download Hub'),
    ('About Us', 'Motion'),
    ('NeuraFlas', 'ZETICA'),
    ('NeuraFlow&#39;s', 'ZETICA&#39;s'),
    ("NeuraFlow's", "ZETICA's"),
    ('NeuraFlow', 'ZETICA'),
    ('Automate workflows, predict trends, and make smarter decisions with NeuraFlow&#39;s cutting-edge AI platform', 'Unleash GPU-accelerated VFX, Vector, Photo, Audio, and Publishing tools with ZETICA&#39;s lightweight native platform.'),
    ("Automate workflows, predict trends, and make smarter decisions with NeuraFlow's cutting-edge AI platform", "Unleash GPU-accelerated VFX, Vector, Photo, Audio, and Publishing tools with ZETICA's lightweight native platform.")
]

for old, new in replacements:
    count = html.count(old)
    html = html.replace(old, new)
    print(f'Replaced in HTML: "{old[:30]}..." -> "{new[:30]}..." ({count} occurrences)')

# Replace hero image src and srcset to point to local assets
hero_img_pattern = r'srcset="[^"]*ihRdyAqkJP0yCygC1qHb8txaCo[^"]*"\s+src="[^"]*ihRdyAqkJP0yCygC1qHb8txaCo[^"]*"'
hero_img_replacement = 'srcset="./assets/images/ihRdyAqkJP0yCygC1qHb8txaCo.png 1x, ./assets/images/ihRdyAqkJP0yCygC1qHb8txaCo.png 2x" src="./assets/images/ihRdyAqkJP0yCygC1qHb8txaCo.png"'
html = re.sub(hero_img_pattern, hero_img_replacement, html)

# Footer attribution injection
footer_attribution_html = '''
<div class="zeticuz-footer-attribution" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:12px;margin-top:28px;padding:18px 20px;border-top:1px solid rgba(255,255,255,0.08);width:100%;text-align:center;">
  <img src="./assets/images/zeticuz-logo.svg" alt="ZETICUZ Developer Logo" style="height:26px;width:auto;display:inline-block;vertical-align:middle;" />
  <span style="font-family:system-ui, -apple-system, sans-serif;font-size:13px;font-weight:600;letter-spacing:0.8px;color:#9ca3af;">
    SITE DEVELOPED BY: <span style="color:#ffffff;">Sam Pangilinan</span> · © 2026
  </span>
  <a href="https://www.zeticuz.xyz/" target="_blank" rel="noopener noreferrer" style="margin-left:8px;padding:6px 14px;background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);border-radius:6px;color:#ffffff;font-size:12px;font-weight:600;letter-spacing:0.5px;text-decoration:none;transition:all 0.2s ease;display:inline-flex;align-items:center;gap:6px;">
    <span>View Developer Portfolio</span>
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17l9.2-9.2M17 17V8H8"/></svg>
  </a>
</div>
'''
if 'zeticuz-footer-attribution' not in html:
    html = html.replace('</footer>', footer_attribution_html + '\n</footer>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated index.html successfully')

# 3. Update all JS bundles in assets/js
js_replacements = [
    ('Supercharge Your Business With AI-Powered Intelligence', 'Supercharge Your Creativity With Native Rust Intelligence'),
    ('Supercharge Your Business', 'Supercharge Your Creativity'),
    ('With AI-Powered', 'With Native Rust'),
    ('Get Started for Free', 'Download Now'),
    ('Get This Template', 'Download Hub'),
    ('About Us', 'Motion'),
    ('NeuraFlas', 'ZETICA'),
    ("NeuraFlow's", "ZETICA's"),
    ('NeuraFlow', 'ZETICA'),
    ("Automate workflows, predict trends, and make smarter decisions with NeuraFlow's cutting-edge AI platform", "Unleash GPU-accelerated VFX, Vector, Photo, Audio, and Publishing tools with ZETICA's lightweight native platform."),
    ('https://framerusercontent.com/images/ihRdyAqkJP0yCygC1qHb8txaCo.png', './assets/images/ihRdyAqkJP0yCygC1qHb8txaCo.png')
]

js_updated_count = 0
for f in os.listdir(js_dir):
    if f.endswith('.js'):
        p = os.path.join(js_dir, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            js_content = fp.read()
        
        modified = False
        for old, new in js_replacements:
            if old in js_content:
                js_content = js_content.replace(old, new)
                modified = True
        
        if modified:
            with open(p, 'w', encoding='utf-8') as fp:
                fp.write(js_content)
            js_updated_count += 1
            print(f'Updated JS bundle: {f}')

print(f'Done! Updated {js_updated_count} JS bundles.')
