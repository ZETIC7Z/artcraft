from PIL import Image

im = Image.open(r'c:\Users\ZETICUZ\Documents\artcraft\branding\entire_top_bar.png')

# Find all pixels that are pure white (255,255,255)
# In y: 5..35, x: 100..400
white_pts = []
for y in range(5, 35):
    for x in range(100, 400):
        if im.getpixel((x, y))[:3] == (255, 255, 255):
            white_pts.append((x, y))

xs = [p[0] for p in white_pts]
ys = [p[1] for p in white_pts]
print(f'White box in entire_top_bar: x={min(xs)}..{max(xs)}, y={min(ys)}..{max(ys)}')

# Find gray text CRAFT APP SUITE
text_pts = []
for y in range(min(ys), max(ys)):
    for x in range(max(xs)+1, max(xs)+250):
        p = im.getpixel((x, y))[:3]
        if p[0] > 90 and p[0] < 200:
            text_pts.append((x, y))

txs = [p[0] for p in text_pts]
tys = [p[1] for p in text_pts]
print(f'Text to right of white box: x={min(txs)}..{max(txs)}, y={min(tys)}..{max(tys)}')
