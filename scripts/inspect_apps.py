import re

with open(r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html", "r", encoding="utf-8") as f:
    html = f.read()

pos = html.find("Thirteen apps")
if pos != -1:
    snippet = html[pos:pos+15000]
    links = re.findall(r'<a\b[^>]*href=[\'"]([^\'"]*apps[^\'"]*)[\'"][^>]*>(.*?)</a>', snippet, re.DOTALL)
    print(f"Found {len(links)} app links:")
    for href, content in links:
        text = re.sub(r'<[^>]+>', ' ', content).strip()
        text = re.sub(r'\s+', ' ', text)
        img = re.findall(r'src=[\'"]([^\'"]*)[\'"]', content)
        print(f"  {href} -> {text[:40]} | img: {img}")
