import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_ref/hero-galaxy.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('fragmentShader:')
print(text[idx:idx+1500])
