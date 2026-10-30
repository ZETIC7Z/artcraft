from PIL import Image

im = Image.open(r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png')

# Print letters in y=15 from x=150 to x=360
for x in range(150, 360, 5):
    p = im.getpixel((x, 15))
    if p[0] > 100:
        print(f'Bright pixel at x={x}: {p}')
