import re

with open(r'c:\Users\ZETICUZ\Documents\artcraft\site\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# find all id="..."
ids = re.findall(r'id=["\']([^"\']+)["\']', html)
print("IDs in index.html:")
for target in ['hero', 'apps', 'studio', 'features', 'ownership', 'made-with', 'community', 'start', 'pricing', 'download']:
    matches = [i for i in ids if target in i.lower()]
    print(f"Target '{target}': {matches}")
