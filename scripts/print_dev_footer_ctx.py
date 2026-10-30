with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    c = f.read()

pos = c.find('zeticuz-dev-footer')
print('pos:', pos)
print(c[pos-200:pos+300])
