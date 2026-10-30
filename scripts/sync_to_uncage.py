import sys
import shutil
import os
import glob

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r'c:\Users\ZETICUZ\Documents\artcraft\site'
dst_dir = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com'

# Sync JS & CSS
asset_files = [
    ('assets/js/lenis.min.js', 'assets/js/lenis.min.js'),
    ('assets/js/zetica-scroll-ruler.js', 'assets/js/zetica-scroll-ruler.js'),
    ('assets/js/zetica-wordmark-scroll.js', 'assets/js/zetica-wordmark-scroll.js'),
    ('assets/js/zetica-theme.js', 'assets/js/zetica-theme.js'),
    ('assets/js/zetica-hero-galaxy.js', 'assets/js/zetica-hero-galaxy.js'),
    ('assets/css/zetica-enhancements.css', 'assets/css/zetica-enhancements.css'),
]

for src_rel, dst_rel in asset_files:
    src_path = os.path.join(src_dir, src_rel)
    dst_path = os.path.join(dst_dir, dst_rel)
    if os.path.exists(src_path):
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.copy2(src_path, dst_path)
        print(f"Copied {src_rel} ({os.path.getsize(dst_path)} bytes)")

# Sync all HTML files
html_files = glob.glob(os.path.join(src_dir, '**/*.html'), recursive=True)
for hf in html_files:
    rel = os.path.relpath(hf, src_dir)
    target = os.path.join(dst_dir, rel)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copy2(hf, target)

print(f"Synchronized {len(html_files)} HTML files to UNCAGE output folder!")
print("Full sync completed successfully!")
