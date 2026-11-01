import os
import re
import glob

html_files = glob.glob('site/**/*.html', recursive=True)
count = 0

old_patterns = [
    r'https://github\.com/ZETIC7Z/craft-launcher/releases/download/v[0-9\.]+/zetica-hub-windows-x64\.zip',
    r'/zetica-hub-windows-x64\.zip',
    r'zetica-hub-windows-x64\.zip'
]

new_url = 'https://github.com/ZETIC7Z/craft-launcher/releases/download/v0.10.2/zetica-hub-windows-x64.msi'

for fpath in html_files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = content
    for pattern in old_patterns:
        modified = re.sub(pattern, new_url, modified)

    if modified != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(modified)
        print(f"Updated {fpath}")
        count += 1

print(f"Total updated HTML files: {count}")
