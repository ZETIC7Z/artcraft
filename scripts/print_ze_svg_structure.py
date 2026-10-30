import re

with open(r'C:\Users\ZETICUZ\Downloads\ZE.svg', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove base64 data for printing
clean = re.sub(r'href="data:image/[^;]+;base64,[^"]+"', 'href="data:..."', text)
clean = re.sub(r'xlink:href="data:image/[^;]+;base64,[^"]+"', 'xlink:href="data:..."', clean)
print(clean)
