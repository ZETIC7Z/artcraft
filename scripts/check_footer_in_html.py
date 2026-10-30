with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('zeticuz-dev-footer')
print('pos of zeticuz-dev-footer in output_neuraflas/index.html:', pos)
if pos != -1:
    print(html[pos:pos+400])
