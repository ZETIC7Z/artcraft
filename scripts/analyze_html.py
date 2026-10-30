import re
import os

html_path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

imgs = re.findall(r'src="([^"]+)"', html)
print(f'Total img src: {len(imgs)}')
for s in sorted(set(imgs)):
    print('  src:', s)

srcsets = re.findall(r'srcset="([^"]+)"', html)
print(f'\nTotal srcset: {len(srcsets)}')
for s in sorted(set(srcsets)):
    print('  srcset:', s[:120])
