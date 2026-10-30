with open(r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.rfind("MADE BY ARTISTS")
if pos != -1:
    print(text[pos-400:pos+300])
else:
    print("Not found")
