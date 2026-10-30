import re

with open('site/download.html', 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

urls = sorted(set(re.findall(r'https?://[^\s"\'\\]+launcher[^\s"\'\\]*', c)))
for u in urls:
    print(u)
