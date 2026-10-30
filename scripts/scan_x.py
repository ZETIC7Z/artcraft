from PIL import Image

im = Image.open(r'c:\Users\ZETICUZ\Documents\artcraft\branding\orig_top_header.png')
print('Pixels in y=18 across x=170..350:')
for x in range(170, 350):
    p = im.getpixel((x, 18))
    if p[0] > 100:
        print(f'x={x}: {p}')
