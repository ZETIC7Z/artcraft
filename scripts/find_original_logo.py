import re
import glob

# Search for artcraft-logo in js files or html
for js_file in glob.glob('site/assets/js/*.js')[:10]:
    with open(js_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if 'artcraft-logo' in content:
        print(f"Found in {js_file}")

# Let's search in all html files for what the logo img had
with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<img[^>]+>', text):
    tag = m.group(0)
    if 'logo' in tag or 'icon' in tag or 'artcraft' in tag or 'zetica' in tag:
        print("IMG:", tag[:150])
