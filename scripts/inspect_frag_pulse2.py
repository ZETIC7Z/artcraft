import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_ref/hero-galaxy.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('pulseMat')
idx_frag = text.find('fragmentShader', idx)
print(text[idx_frag:idx_frag+1500])
