import re

index_path = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

body_start = html.find("<body")
print("body starts at:", body_start)

# find in body
pos = html.find("Capable tools", body_start)
if pos != -1:
    print("Found 'Capable tools' in body at:", pos)
    print("--- SNIPPET ---")
    print(html[pos-300:pos+1500])
else:
    print("Not found in body!")
