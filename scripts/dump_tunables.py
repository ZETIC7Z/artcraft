import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js\032cmaav6g8-m-215a21ba.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = 61792
print(text[pos:pos+3000])
