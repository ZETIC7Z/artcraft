import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\ZETICUZ\Documents\artcraft\site\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

scripts = re.findall(r'<script[^>]*src="([^"]+)"[^>]*></script>', content)
print("Scripts found:")
for s in scripts:
    print(" -", s)
