import re

with open(r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html", "r", encoding="utf-8") as f:
    html = f.read()

sections = re.findall(r'<section\b[^>]*>(.*?)</section>', html, re.DOTALL)

for i in [2, 3, 5, 6]:
    sec = sections[i]
    print(f"=== SECTION {i} ===")
    print("Videos:", len(re.findall(r'<video\b', sec)))
    print("Canvases:", len(re.findall(r'<canvas\b', sec)))
    print("Iframes:", len(re.findall(r'<iframe\b', sec)))
    print("Imgs:", len(re.findall(r'<img\b', sec)))
    img_srcs = re.findall(r'<img\b[^>]*src=[\'"]([^\'"]*)[\'"]', sec)
    print("Img srcs:", img_srcs[:5])
    video_srcs = re.findall(r'<video\b[^>]*src=[\'"]([^\'"]*)[\'"]', sec)
    print("Video srcs:", video_srcs[:5])
    # check styles
    hidden_count = len(re.findall(r'opacity:\s*0', sec))
    print(f"Elements with opacity:0: {hidden_count}")
