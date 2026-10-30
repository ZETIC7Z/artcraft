import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js\29wilaqtb26u5.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('c.heroWordmark.metrics')
if pos != -1:
    start = max(0, pos - 1500)
    end = min(len(text), pos + 1500)
    print("CODE:")
    print(text[start:end])
