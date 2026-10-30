import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\ZETICUZ\Documents\artcraft\site\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

idx = content.find('id="hero-wordmark-masthead"')
if idx != -1:
    print(content[idx:idx+1500])
else:
    print("Not found")
