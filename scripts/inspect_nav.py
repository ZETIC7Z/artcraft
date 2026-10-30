import re

with open(r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Let's find <header> or <nav>
navs = re.findall(r'<header\b[^>]*>(.*?)</header>', html, re.DOTALL)
if navs:
    print("Found header length:", len(navs[0]))
    print(navs[0][:2000])
else:
    print("No header tag found, searching for top nav:")
    pos = html.find("LAUNCH APP")
    if pos != -1:
        print(html[max(0, pos-2500):pos+500])
