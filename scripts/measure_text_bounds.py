from PIL import Image

im = Image.open(r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png')

print('Top bar bg color at (200, 16):', im.getpixel((200, 16)))
print('Banner bg color at (72, 63):', im.getpixel((72, 63)))
print('Banner bg color at (300, 63):', im.getpixel((300, 63)))

# Find exact bounds of "ArtCraft Launcher 0.10.0 is available."
# In y: 55..72, x: 70..350
banner_text = []
for y in range(54, 73):
    for x in range(70, 350):
        r, g, b, a = im.getpixel((x, y))
        if r > 150 and g > 150 and b > 150:
            banner_text.append((x, y))
if banner_text:
    print(f'Banner text range: x={min(p[0] for p in banner_text)}..{max(p[0] for p in banner_text)}, y={min(p[1] for p in banner_text)}..{max(p[1] for p in banner_text)}')

# Bottom status bar text:
# In y: 520..540, x: 10..300
bot_text = []
for y in range(520, 544):
    for x in range(10, 300):
        r, g, b, a = im.getpixel((x, y))
        if r > 80 and g > 80 and b > 80:
            bot_text.append((x, y))
if bot_text:
    print(f'Bottom text range: x={min(p[0] for p in bot_text)}..{max(p[0] for p in bot_text)}, y={min(p[1] for p in bot_text)}..{max(p[1] for p in bot_text)}')
