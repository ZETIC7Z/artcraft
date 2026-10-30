from PIL import Image

orig = Image.open(r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png')
# Save a fresh crop of the top header from the original unmodified file
crop = orig.crop((0, 0, 560, 45))
crop.save(r'c:\Users\ZETICUZ\Documents\artcraft\branding\orig_top_header.png')
print('Saved orig_top_header.png from original image.')

white_box = []
for y in range(crop.size[1]):
    for x in range(crop.size[0]):
        r, g, b, a = crop.getpixel((x, y))
        if r > 240 and g > 240 and b > 240:
            white_box.append((x, y))

box_x = [p[0] for p in white_box if p[1] == 18 and p[0] > 190]
if box_x:
    print(f'Original White LAUNCHER box at y=18: x={min(box_x)}..{max(box_x)}')
