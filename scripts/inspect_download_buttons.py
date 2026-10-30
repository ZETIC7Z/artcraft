import re

with open('site/index.html', 'r', encoding='utf-8', errors='ignore') as f:
    c = f.read()

# Look for all <a> tags that have href with download or button
links = re.findall(r'<a\s+[^>]*href=["\'][^"\']+["\'][^>]*>[\s\S]*?</a>', c)
print(f"Total links: {len(links)}")
for l in links:
    if 'download' in l.lower() or 'launcher' in l.lower() or 'zetica-hub' in l.lower() or 'get-it' in l.lower():
        print("---")
        print(l[:300])

# Also look for Next.js JSON payload entries for downloads
print("\n--- NEXT.JS PAYLOAD MATCHES ---")
payload_matches = re.findall(r'https?://[^\s"\'\\]+(?:zetica-hub|craft-launcher|artcraft-launcher)[^\s"\'\\]*', c)
for pm in set(payload_matches):
    print(pm)
