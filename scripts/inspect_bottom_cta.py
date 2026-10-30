with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('zeticuz-footer-attribution')
print('pos of zeticuz-footer-attribution:', pos)
if pos != -1:
    print(html[pos-100:pos+300])

# Check bottom CTA text
pos2 = html.find('Start leveraging the power of AI')
print('pos of bottom CTA:', pos2)
if pos2 != -1:
    print(html[pos2-200:pos2+200])

# Check Design Monks
pos3 = html.find('Design Monks')
print('pos of Design Monks:', pos3)
if pos3 != -1:
    print(html[pos3-100:pos3+200])
