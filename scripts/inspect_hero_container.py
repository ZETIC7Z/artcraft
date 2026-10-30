import re

with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('ihRdyAqkJP0yCygC1qHb8txaCo')
if pos != -1:
    start = max(0, pos - 1500)
    end = min(len(html), pos + 1500)
    print('Context around ihRdy:')
    print(html[start:end])
else:
    print('Not found')
