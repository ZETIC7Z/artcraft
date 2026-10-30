import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js\29wilaqtb26u5.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('font-display absolute top-0 left-0')
if idx != -1:
    start = max(0, idx - 1500)
    end = min(len(text), idx + 1500)
    print("SNIPPET:")
    print(text[start:end])
else:
    print("Not found")
