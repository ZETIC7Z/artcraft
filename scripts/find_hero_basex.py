import sys, os
sys.stdout.reconfigure(encoding='utf-8')

js_dir = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js'
for f in os.listdir(js_dir):
    if f.endswith('.js') and not f.startswith('zetica'):
        path = os.path.join(js_dir, f)
        try:
            with open(path, 'r', encoding='utf-8') as fl:
                text = fl.read()
                pos = text.find('heroWordmark')
                if pos != -1 and ('baseDocY' in text or 'baseX' in text):
                    print(f"File {f} pos {pos}")
                    # print snippet where baseX is assigned
                    bx = text.find('baseX')
                    print("BASEX SNIPPET:")
                    print(text[max(0, bx - 300):min(len(text), bx + 300)])
                    break
        except Exception:
            pass
