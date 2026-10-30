import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\ZETICUZ\Documents\artcraft\site\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

targets = ['hero', 'apps', 'studio', 'features', 'ownership', 'made-with', 'community', 'start']
for t in targets:
    pos = content.find(f'id="{t}"')
    if pos != -1:
        print(f"Found id='{t}' at pos {pos}")
    else:
        print(f"NOT found: id='{t}'")
