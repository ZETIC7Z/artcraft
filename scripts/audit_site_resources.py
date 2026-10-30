import os
import glob
import re
from urllib.parse import urlparse, unquote

def audit():
    html_files = glob.glob('site/**/*.html', recursive=True)
    print(f'Auditing {len(html_files)} HTML pages...')

    missing_assets = {}
    external_links = {}

    for path in html_files:
        page_dir = os.path.dirname(path)
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        # Find img src, source src, link href, video src
        patterns = [
            r'<img[^>]+src=[\'"]([^\'"]+)[\'"]',
            r'<source[^>]+src=[\'"]([^\'"]+)[\'"]',
            r'<video[^>]+src=[\'"]([^\'"]+)[\'"]',
            r'<link[^>]+href=[\'"]([^\'"]+)[\'"]',
        ]

        for p in patterns:
            for match in re.finditer(p, content, re.IGNORECASE):
                url = match.group(1).strip()
                if not url or url.startswith('data:') or url.startswith('#') or url.startswith('javascript:'):
                    continue
                if url.startswith('http://') or url.startswith('https://'):
                    external_links[url] = external_links.get(url, 0) + 1
                    continue

                # Strip query strings and hash
                clean_url = url.split('?')[0].split('#')[0]
                clean_url = unquote(clean_url)

                # Local resolution
                if clean_url.startswith('/'):
                    # relative to site root
                    target_file = os.path.normpath(os.path.join('site', clean_url.lstrip('/\\')))
                else:
                    target_file = os.path.normpath(os.path.join(page_dir, clean_url))

                if not os.path.exists(target_file):
                    if target_file not in missing_assets:
                        missing_assets[target_file] = []
                    missing_assets[target_file].append((path, url))

    print(f'\n--- MISSING LOCAL ASSETS ({len(missing_assets)}) ---')
    for target, occurrences in missing_assets.items():
        print(f'Missing: {target} (referenced in {len(occurrences)} files, e.g. {occurrences[0][0]} -> {occurrences[0][1]})')

if __name__ == '__main__':
    audit()
