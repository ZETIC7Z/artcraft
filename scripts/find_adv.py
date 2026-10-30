import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js\29wilaqtb26u5.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = 0
matches = []
for term in ['.adv', 'adv:', 'adv=']:
    idx = 0
    while True:
        pos = text.find(term, idx)
        if pos == -1:
            break
        matches.append((term, pos))
        idx = pos + 1

print(f"Found {len(matches)} matches")
for term, m in matches[:5]:
    start = max(0, m - 300)
    end = min(len(text), m + 300)
    print(f"--- MATCH {term} ---")
    print(text[start:end])
