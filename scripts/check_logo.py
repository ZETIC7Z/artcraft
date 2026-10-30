import re

with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<a[^>]*href="\./index\.html"[^>]*>.*?</a>', text)
if m:
    print("Logo link in index.html:")
    print(m.group(0))
