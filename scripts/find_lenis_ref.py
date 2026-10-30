import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js\29wilaqtb26u5.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
while True:
    pos = text.find('lenisRef', idx)
    if pos == -1:
        break
    print("MATCH AT:", pos)
    print(text[max(0, pos - 200):min(len(text), pos + 300)])
    idx = pos + 1
