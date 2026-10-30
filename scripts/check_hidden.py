import re

index_path = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Find all occurrences of opacity: 0; visibility: hidden
matches = re.findall(r'filter:\s*blur\(8px\);\s*transform:\s*translate\(0px,\s*28px\);\s*opacity:\s*0;\s*visibility:\s*hidden;', html)
print(f"Elements with hidden initial reveal styles: {len(matches)}")

# Let's inspect the big central 'A' logo in the hero that was visible in the screenshot
# What element is it?
a_logo = re.findall(r'<svg[^>]*>.*?</svg>', html, re.DOTALL)
print(f"Total SVGs: {len(a_logo)}")
for i, svg in enumerate(a_logo[:5]):
    print(f"SVG {i} length {len(svg)} snippet: {svg[:100]}...")
