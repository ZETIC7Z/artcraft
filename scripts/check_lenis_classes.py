with open(r'c:\Users\ZETICUZ\Documents\artcraft\site\assets\js\lenis.min.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'.{0,40}classList.{0,40}', text)
for m in matches:
    print(m)
