import re

with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', text)
print(f'Total script tags: {len(scripts)}')
for s in scripts:
    print(' ', s)
