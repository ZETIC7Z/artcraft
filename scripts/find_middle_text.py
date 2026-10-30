from PIL import Image

im = Image.open(r'c:\Users\ZETICUZ\Documents\artcraft\branding\orig_top_header.png')
print('Non-background pixels in y=10..30, x=180..340:')
for y in range(10, 25):
    for x in range(180, 340):
        r, g, b, a = im.getpixel((x, y))
        if r > 100 or g > 100 or b > 100:
            print(f'x={x}, y={y}: ({r},{g},{b})')
            break
