with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'container-type:inline-size[^\"]*', text)
for m in matches:
    print("Match:", m[:200])

for m in re.finditer(r'aria-label=[\"\']([^\"\']+)[\"\']', text):
    if any(k in m.group(1).lower() for k in ['artcraft', 'zetica', 'logo']):
        print("Aria:", m.group(0))
