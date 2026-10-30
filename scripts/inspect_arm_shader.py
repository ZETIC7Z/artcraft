import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_ref/hero-galaxy.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('armGeoms')
# find shader for arms
idx2 = text.find('ShaderMaterial', idx)
print(text[idx2-100:idx2+1800])
