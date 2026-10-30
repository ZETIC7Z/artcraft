with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('Free 3 Month')
start = max(0, pos - 800)
end = min(len(html), pos + 1000)
print(html[start:end])
