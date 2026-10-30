from PIL import Image

im = Image.open(r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png')

# Let's inspect the banner "UPDATE" button:
# Blue rectangle coordinates
# Find where blue color (approx (30, 110, 240)) is located
blue_pixels = []
for y in range(40, 100):
    for x in range(20, 150):
        r, g, b, a = im.getpixel((x, y))
        if b > 200 and r < 100:
            blue_pixels.append((x, y))

if blue_pixels:
    min_x = min(p[0] for p in blue_pixels)
    max_x = max(p[0] for p in blue_pixels)
    min_y = min(p[1] for p in blue_pixels)
    max_y = max(p[1] for p in blue_pixels)
    print(f'UPDATE button: x={min_x}..{max_x}, y={min_y}..{max_y}')

# Let's inspect "ArtCraft Launcher" text:
# To the right of UPDATE button
# The banner background is around min_y - 10 to max_y + 10
# Let's check banner border
banner_y1 = min_y - 6
banner_y2 = max_y + 6
print(f'Banner vertical range: {banner_y1}..{banner_y2}')

# Top bar ARTCRAFT text coordinates:
# Find white pixels in x: 10..220, y: 10..40
white_top = []
for y in range(10, 45):
    for x in range(10, 235):
        r, g, b, a = im.getpixel((x, y))
        if r > 200 and g > 200 and b > 200:
            white_top.append((x, y))
if white_top:
    print(f'ARTCRAFT text: x={min(p[0] for p in white_top)}..{max(p[0] for p in white_top)}, y={min(p[1] for p in white_top)}..{max(p[1] for p in white_top)}')

# "CRAFT APP SUITE" text:
white_suite = []
for y in range(10, 45):
    for x in range(350, 600):
        r, g, b, a = im.getpixel((x, y))
        if r > 80 and g > 80 and b > 80:
            white_suite.append((x, y))
if white_suite:
    print(f'CRAFT APP SUITE: x={min(p[0] for p in white_suite)}..{max(p[0] for p in white_suite)}, y={min(p[1] for p in white_suite)}..{max(p[1] for p in white_suite)}')
