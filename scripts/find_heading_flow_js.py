import os

js_dir = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js'
for f in os.listdir(js_dir):
    if f.endswith('.js'):
        path = os.path.join(js_dir, f)
        try:
            with open(path, 'r', encoding='utf-8') as fl:
                content = fl.read()
                if '0.470588' in content or 'font-display absolute top-0 left-0' in content or 'text-ink-strong' in content:
                    print(f"MATCH: {f}")
        except Exception:
            pass
