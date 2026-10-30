import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js\29wilaqtb26u5.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('scale(${E*_})')
if pos == -1:
    pos = text.find('scale(${E*')
print("POS:", pos)
if pos != -1:
    print(text[max(0, pos - 500):min(len(text), pos + 500)])
