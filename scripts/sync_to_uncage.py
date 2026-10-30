import sys
import shutil
import os

sys.stdout.reconfigure(encoding='utf-8')

src_dir = r'c:\Users\ZETICUZ\Documents\artcraft\site'
dst_dir = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com'

files_to_copy = [
    ('assets/js/lenis.min.js', 'assets/js/lenis.min.js'),
    ('assets/js/zetica-scroll-ruler.js', 'assets/js/zetica-scroll-ruler.js'),
    ('assets/js/zetica-wordmark-scroll.js', 'assets/js/zetica-wordmark-scroll.js'),
    ('assets/css/zetica-enhancements.css', 'assets/css/zetica-enhancements.css'),
    ('index.html', 'index.html'),
]

for src_rel, dst_rel in files_to_copy:
    src_path = os.path.join(src_dir, src_rel)
    dst_path = os.path.join(dst_dir, dst_rel)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    shutil.copy2(src_path, dst_path)
    print(f"Copied {src_rel} -> {dst_rel} ({os.path.getsize(dst_path)} bytes)")

print("Sync completed successfully!")
