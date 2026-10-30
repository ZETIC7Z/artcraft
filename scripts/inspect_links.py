import re
import os

files_to_check = ['site/index.html', 'site/download.html']

for rel_path in files_to_check:
    if not os.path.exists(rel_path):
        continue
    print(f"=== {rel_path} ===")
    with open(rel_path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.DOTALL | re.IGNORECASE)
    for href, inner in matches:
        clean = re.sub(r'<[^>]+>', '', inner).strip()
        if any(w in href.lower() or w in clean.lower() for w in ['download', 'exe', 'zip', 'get', 'hub', 'installer']):
            print(f"  [{clean}] -> {href}")
