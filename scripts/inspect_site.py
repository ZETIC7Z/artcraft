import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\ZETICUZ\Documents\artcraft\site\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("File size:", len(content))

# Look for section tags or IDs
sections = re.findall(r'<section[^>]*id="([^"]+)"[^>]*>', content)
print("Sections with IDs:", sections)

# Look for h1, h2 tags or wordmark
h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
print("H1 count:", len(h1s))
for h in h1s[:5]:
    print("H1:", re.sub(r'<[^>]+>', '', h).strip()[:100])

# Look for scripts included
scripts = re.findall(r'<script[^>]*src="([^"]+)"', content)
print("Scripts:", scripts)
