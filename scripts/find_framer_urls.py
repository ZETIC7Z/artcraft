import re

with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

framer_urls = re.findall(r'https://framerusercontent\.com[^\s"\'<>]+', c)
print(f'Total framerusercontent URLs: {len(framer_urls)}')
for u in sorted(set(framer_urls)):
    print('  ', u)
