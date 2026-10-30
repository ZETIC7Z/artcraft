import os
from PIL import Image, ImageDraw, ImageFont

# Load original launcher screenshot
src_path = r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png'
im = Image.open(src_path).convert('RGBA')
draw = ImageDraw.Draw(im)

# 1. Top left logo replacement
# Fill top left ARTCRAFT area: x=10..205, y=5..27 with (21, 22, 25)
draw.rectangle([10, 5, 205, 27], fill=(21, 22, 25, 255))

# Scale powe emblem
powe = Image.open(r'c:\Users\ZETICUZ\Documents\artcraft\branding\powe_rgba.png')
emblem_h = 18
emblem_w = int(emblem_h * (powe.width / powe.height))
emblem_scaled = powe.resize((emblem_w, emblem_h), Image.Resampling.LANCZOS)
im.paste(emblem_scaled, (14, 6), emblem_scaled)

# Draw ZETICA text
try:
    font_logo = ImageFont.truetype('C:/Windows/Fonts/bahnschrift.ttf', 14)
except Exception:
    font_logo = ImageFont.load_default()
draw.text((14 + emblem_w + 8, 7), 'ZETICA', font=font_logo, fill=(255, 255, 255, 255))

# Replace CRAFT APP SUITE with CREATIVE SUITE
draw.rectangle([370, 10, 520, 26], fill=(21, 22, 25, 255))
try:
    font_suite = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 9)
except Exception:
    font_suite = ImageFont.load_default()
draw.text((380, 13), 'CREATIVE SUITE', font=font_suite, fill=(125, 130, 140, 255))

# 2. Update notification banner text
# Clear x: 74..245, y: 56..71 with (21, 30, 46)
draw.rectangle([74, 56, 250, 71], fill=(21, 30, 46, 255))
try:
    font_banner = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 10)
except Exception:
    font_banner = ImageFont.load_default()
draw.text((76, 58), 'Zetica Hub 0.10.0 is available.', font=font_banner, fill=(255, 255, 255, 255))

# 3. Bottom status bar
# Clear x: 12..305, y: 520..542 with (14, 17, 22)
draw.rectangle([12, 520, 305, 542], fill=(14, 17, 22, 255))
try:
    font_bot = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 8)
except Exception:
    font_bot = ImageFont.load_default()
draw.text((14, 529), 'CHECKED JUST NOW · USING ZETICA API', font=font_bot, fill=(90, 95, 105, 255))

# Load ihRdy image for exact size and alpha channel
ihRdy = Image.open(r'c:\Users\ZETICUZ\Documents\artcraft\branding\ihRdy_view.png')
target_size = ihRdy.size # (2048, 1087)

# Upscale using high-quality Lanczos filter
im_hq = im.resize(target_size, Image.Resampling.LANCZOS)

# Apply original rounded corner mask
if 'A' in ihRdy.getbands():
    ihRdy_alpha = ihRdy.split()[3]
    im_hq.putalpha(ihRdy_alpha)

# Save
out_png = r'c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_launcher_hero.png'
im_hq.save(out_png, 'PNG')
out_avif = r'c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_launcher_hero.avif'
im_hq.save(out_avif, 'AVIF', quality=95)

# Overwrite in output_neuraflas
target_png = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\assets\images\ihRdyAqkJP0yCygC1qHb8txaCo.png'
target_avif = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\assets\images\ihRdyAqkJP0yCygC1qHb8txaCo-e95e5071.avif'
im_hq.save(target_png, 'PNG')
im_hq.save(target_avif, 'AVIF', quality=95)

print('Pixel-perfect ZETICA launcher hero generated successfully!')
