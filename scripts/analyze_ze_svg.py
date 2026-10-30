import re

with open(r'C:\Users\ZETICUZ\Downloads\ZE.svg', 'r', encoding='utf-8') as f:
    text = f.read()

# Check tags inside
tags = re.findall(r'<([a-zA-Z0-9]+)', text)
tag_counts = {}
for t in tags:
    tag_counts[t] = tag_counts.get(t, 0) + 1

print("Tags:", tag_counts)

# Let's find path elements or image elements
m = re.findall(r'<path[^>]*>', text)
print(f"Path elements count: {len(m)}")
if m:
    for p in m[:5]:
        print(p[:150])

# Check what color it is:
print("Fills/strokes:", re.findall(r'fill="[^"]+"', text)[:10])
