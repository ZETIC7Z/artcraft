import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js\29wilaqtb26u5.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('heroLead')
while pos != -1:
    print("HEROLEAD AT:", pos)
    print(text[pos-100:pos+300])
    pos = text.find('heroLead', pos + 1)
