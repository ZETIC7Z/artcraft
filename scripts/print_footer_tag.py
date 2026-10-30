with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.rfind('<footer')
pos_end = html.find('</footer>', pos)
print(html[pos:pos_end+9])
