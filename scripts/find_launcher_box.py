from PIL import Image

im = Image.open(r'c:\Users\ZETICUZ\Documents\artcraft\branding\top_header_full.png')
print('Size of top_header_full:', im.size)

# Scan for pure white background (the white box of LAUNCHER)
white_box = []
for y in range(im.size[1]):
    for x in range(im.size[0]):
        r, g, b, a = im.getpixel((x, y))
        if r > 240 and g > 240 and b > 240:
            white_box.append((x, y))

if white_box:
    min_x = min(p[0] for p in white_box)
    max_x = max(p[0] for p in white_box)
    min_y = min(p[1] for p in white_box)
    max_y = max(p[1] for p in white_box)
    print(f'White pixels in header crop: x={min_x}..{max_x}, y={min_y}..{max_y}')

    # Let's find contiguous white box
    box_x = [p[0] for p in white_box if p[1] == 18 and p[0] > 190]
    if box_x:
        print(f'White LAUNCHER box: x={min(box_x)}..{max(box_x)}')
