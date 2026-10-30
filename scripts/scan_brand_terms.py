import glob
import os
import re

site_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com"
html_files = glob.glob(os.path.join(site_dir, "**", "*.html"), recursive=True)

patterns = [
    r'artcraft',
    r'storytold',
    r'storyteller',
    r'getartcraft\.com',
]

results = {p: 0 for p in patterns}
for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read().lower()
    for p in patterns:
        results[p] += len(re.findall(p, content))

for p, count in results.items():
    print(f"Pattern '{p}': {count} occurrences across {len(html_files)} HTML files")
