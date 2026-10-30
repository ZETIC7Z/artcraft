from PIL import Image

im = Image.open(r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png')

# Inspect top header x: 180 to 400, y: 5 to 35
print('Top header pixels around 240..300:')
for x in range(220, 380, 20):
    print(f'x={x}, y=15: {im.getpixel((x, 15))}')

# Where does the bottom bar start?
for y in range(515, 530):
    print(f'y={y}, x=50: {im.getpixel((50, y))}')
