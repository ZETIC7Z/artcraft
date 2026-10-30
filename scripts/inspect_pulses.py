import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_ref/hero-galaxy.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Arm guides as thin RIBBON meshes')
if idx != -1:
    print(text[idx-50:idx+2500])
