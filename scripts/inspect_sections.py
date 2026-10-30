import re

with open(r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's inspect all <section> tags
sections = re.findall(r'<section\b[^>]*>(.*?)</section>', html, re.DOTALL)
print(f"Total <section> tags: {len(sections)}")
for i, sec in enumerate(sections):
    headings = re.findall(r'<(h[1-6])[^>]*>(.*?)</\1>', sec, re.DOTALL)
    h_clean = [re.sub(r'<[^>]+>', '', h[1]).strip() for h in headings]
    print(f"Section {i} length {len(sec)}: headings={h_clean[:3]}")

# Let's check footer
footer = re.findall(r'<footer\b[^>]*>(.*?)</footer>', html, re.DOTALL)
print(f"Total <footer> tags: {len(footer)}")
if footer:
    print("Footer snippet:")
    clean_f = re.sub(r'<[^>]+>', ' ', footer[0])
    clean_f = re.sub(r'\s+', ' ', clean_f)
    print(clean_f[:500])
