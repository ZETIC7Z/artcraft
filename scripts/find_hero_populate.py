import sys, os
sys.stdout.reconfigure(encoding='utf-8')

js_dir = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js'
for f in os.listdir(js_dir):
    if f.endswith('.js') and not f.startswith('zetica'):
        path = os.path.join(js_dir, f)
        try:
            with open(path, 'r', encoding='utf-8') as fl:
                text = fl.read()
                pos = text.find('heroWordmark.ready =')
                if pos == -1:
                    pos = text.find('heroWordmark.ready=!0')
                if pos == -1:
                    pos = text.find('.heroWordmark.ready=!0')
                if pos != -1:
                    print(f"File {f} pos {pos}")
                    print("SNIPPET:")
                    print(text[max(0, pos - 400):min(len(text), pos + 400)])
                    break
        except Exception:
            pass
