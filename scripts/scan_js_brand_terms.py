import glob
import os
import re

site_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js"
js_files = glob.glob(os.path.join(site_dir, "*.js"))

patterns = [
    r'artcraft',
    r'storytold',
    r'storyteller',
    r'getartcraft\.com',
]

results = {p: 0 for p in patterns}
for jf in js_files:
    with open(jf, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read().lower()
    for p in patterns:
        results[p] += len(re.findall(p, content))

for p, count in results.items():
    print(f"JS Pattern '{p}': {count} occurrences across {len(js_files)} JS files")
