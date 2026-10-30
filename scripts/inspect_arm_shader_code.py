import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_ref/hero-galaxy.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Arm lines get their own shader')
print(text[idx:idx+2500])
