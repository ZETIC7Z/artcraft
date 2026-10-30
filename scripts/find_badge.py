with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

terms = ['Free 3 Month', 'GIFT VOUCHER', 'Made in Framer', '__framer-badge']
for t in terms:
    pos = html.find(t)
    print(f'Term "{t}": pos={pos}')
    if pos != -1:
        print('  Snippet:', html[max(0, pos-200):min(len(html), pos+300)])
