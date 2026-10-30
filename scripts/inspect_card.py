with open(r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find("Image to Location")
if pos != -1:
    print(text[pos-400:pos+800])
