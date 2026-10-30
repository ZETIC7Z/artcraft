import re

with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Capable tools')
if idx != -1:
    print("=== Context before Capable tools ===")
    print(text[max(0, idx - 1200):idx + 200])
