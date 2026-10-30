with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('Automate')
if pos != -1:
    print('Found "Automate" in index.html at pos:', pos)
    print(html[pos-100:pos+250])
else:
    print('"Automate" not found in index.html')
