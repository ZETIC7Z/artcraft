import sys
import urllib.request
import ssl

sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "https://cdn.jsdelivr.net/npm/lenis@1.1.18/dist/lenis.min.js",
    "https://unpkg.com/lenis@1.1.18/dist/lenis.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/lenis/1.1.18/lenis.min.js"
]

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

success = False
for url in urls:
    try:
        print(f"Trying {url}...")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = resp.read()
            with open('site/assets/js/lenis.min.js', 'wb') as f:
                f.write(data)
            print(f"Success! Saved {len(data)} bytes to site/assets/js/lenis.min.js")
            success = True
            break
    except Exception as e:
        print(f"Failed {url}: {e}")

if not success:
    print("Could not download via urllib, writing fallback self-contained smooth scroller")
