import re

index_path = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Let's find all text inside headings and major sections
headings = re.findall(r'<(h[1-6])[^>]*>(.*?)</\1>', html, re.DOTALL)
print(f"Total headings: {len(headings)}")
for tag, text in headings[:25]:
    clean = re.sub(r'<[^>]+>', '', text).strip()
    clean = re.sub(r'\s+', ' ', clean)
    print(f"[{tag}] {clean}")

# Let's find all images
imgs = re.findall(r'<img[^>]*src=[\'"](.*?)[\'"][^>]*alt=[\'"](.*?)[\'"]', html)
print(f"\nTotal imgs with alt: {len(imgs)}")
for src, alt in imgs[:15]:
    print(f"  {alt} -> {src}")
