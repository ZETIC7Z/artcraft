import re

index_path = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

# Let's search for "ARTCRAFT" or "Capable tools" in index.html
pos = html.find("Capable tools")
if pos != -1:
    print("Found 'Capable tools' around pos:", pos)
    print("Context (before 500, after 1000):")
    print(html[max(0, pos-500):pos+1000])
else:
    print("Not found 'Capable tools'")
