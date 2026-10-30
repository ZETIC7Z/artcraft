import glob
import os
import re

site_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com"
html_files = glob.glob(os.path.join(site_dir, "**", "*.html"), recursive=True)

all_videos = set()
for hf in html_files:
    with open(hf, "r", encoding="utf-8") as f:
        content = f.read()
    vids = re.findall(r'<video\b[^>]*src=[\'"]([^\'"]*)[\'"]', content)
    for v in vids:
        all_videos.add(v)
    vids_source = re.findall(r'<source\b[^>]*src=[\'"]([^\'"]*)[\'"]', content)
    for v in vids_source:
        all_videos.add(v)

print(f"Total unique video URLs found across {len(html_files)} HTML files: {len(all_videos)}")
for v in sorted(all_videos):
    print(" ", v)
