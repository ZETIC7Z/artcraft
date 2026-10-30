import os
import re

js_dir = r'c:\Users\ZETICUZ\Documents\artcraft\site\assets\js'
for f in os.listdir(js_dir):
    if f.endswith('.js'):
        path = os.path.join(js_dir, f)
        with open(path, 'r', encoding='utf-8') as fl:
            content = fl.read()
            if 'wheel' in content:
                print(f"=== {f} has 'wheel' ===")
                matches = re.finditer(r'.{0,50}wheel.{0,50}', content)
                for m in list(matches)[:5]:
                    print('   ', m.group(0).strip())
