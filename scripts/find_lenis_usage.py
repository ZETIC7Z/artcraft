import os
import re

site_dir = r'c:\Users\ZETICUZ\Documents\artcraft\site'
for root, dirs, files in os.walk(site_dir):
    for f in files:
        if f.endswith('.js') or f.endswith('.html'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                content = fl.read()
                if 'Lenis' in content or '__lenis' in content or 'new window.Lenis' in content:
                    print(f"File {f} mentions Lenis:")
                    for m in re.finditer(r'.{0,40}(?:Lenis|__lenis).{0,40}', content):
                        print("   ", m.group(0).strip())
