import glob
import re
import urllib.request
import urllib.parse

def check_all_images():
    html_files = glob.glob('site/**/*.html', recursive=True)
    print(f'Checking images across {len(html_files)} HTML pages...')

    all_images = set()
    for path in html_files:
        rel_page = os.path.relpath(path, 'site').replace('\\', '/')
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        imgs = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', content, re.IGNORECASE)
        for img_src in imgs:
            img_src = img_src.strip()
            if not img_src or img_src.startswith('data:'):
                continue
            all_images.add((rel_page, img_src))

    print(f'Found {len(all_images)} unique (page, image_src) pairs.')

    failed = []
    success = 0
    for page, img_src in all_images:
        if img_src.startswith('http://') or img_src.startswith('https://'):
            continue
        
        # Build URL against http://localhost:8792
        # If relative, resolve against page dir
        page_dir = os.path.dirname(page)
        if img_src.startswith('/'):
            target_path = img_src
        else:
            target_path = '/' + os.path.normpath(os.path.join(page_dir, img_src)).replace('\\', '/')

        url = f'http://localhost:8792{target_path}'
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as resp:
                if resp.status == 200:
                    success += 1
                else:
                    failed.append((page, img_src, url, resp.status))
        except Exception as e:
            failed.append((page, img_src, url, str(e)))

    print(f'HTTP Check completed: {success} OK, {len(failed)} FAILED.')
    if failed:
        print('FAILED IMAGES:')
        for f in failed:
            print(' ', f)

if __name__ == '__main__':
    import os
    check_all_images()
