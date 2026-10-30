import re

index_path = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Total HTML length: {len(html)}")

# Find all script tags
scripts = re.findall(r'<script\b[^>]*>(.*?)</script>', html, re.DOTALL)
print(f"Inline scripts count: {len(scripts)}")

script_srcs = re.findall(r'<script\b[^>]*src=[\'"](.*?)[\'"]', html)
print(f"External scripts count: {len(script_srcs)}")
print("External scripts:", script_srcs)

# Check for Next.js data or hydration
print("Contains __NEXT_DATA__?", "__NEXT_DATA__" in html)

# Check styles
css_links = re.findall(r'<link\b[^>]*rel=[\'"]stylesheet[\'"][^>]*href=[\'"](.*?)[\'"]', html)
print(f"CSS links: {css_links}")
