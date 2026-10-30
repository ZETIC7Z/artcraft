import os
from PIL import Image, ImageDraw, ImageFont

# Load original screenshot
src_path = r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png'
im = Image.open(src_path).convert('RGBA')

# 1. Top left logo replacement
# Top left background color is (11, 14, 20)
draw = ImageDraw.Draw(im)

# Wipe out ARTCRAFT (x: 10 to 230, y: 10 to 45)
draw.rectangle([10, 10, 230, 48], fill=(11, 14, 20, 255))

# Load powe_rgba emblem
powe = Image.open(r'c:\Users\ZETICUZ\Documents\artcraft\branding\powe_rgba.png')
# Aspect ratio of powe
powe_h = 30
powe_w = int(powe_h * (powe.width / powe.height))
powe_scaled = powe.resize((powe_w, powe_h), Image.Resampling.LANCZOS)
im.paste(powe_scaled, (14, 14), powe_scaled)

# Draw ZETICA text
try:
    font_logo = ImageFont.truetype('C:/Windows/Fonts/bahnschrift.ttf', 20)
except Exception:
    font_logo = ImageFont.load_default()

draw.text((14 + powe_w + 10, 18), 'ZETICA', font=font_logo, fill=(255, 255, 255, 255))

# Wipe CRAFT APP SUITE and replace with CREATIVE SUITE
# x: 375 to 550, y: 16 to 45
draw.rectangle([375, 16, 560, 45], fill=(11, 14, 20, 255))
try:
    font_mono = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 12)
except Exception:
    font_mono = ImageFont.load_default()
draw.text((385, 22), 'CREATIVE SUITE', font=font_mono, fill=(120, 125, 135, 255))

# 2. Update notification banner text
# Wipe out "ArtCraft Launcher 0.10.0 is available." (x: 145 to 480, y: 80 to 110)
# Background color of banner is approx (19, 29, 48)
draw.rectangle([145, 80, 500, 108], fill=(19, 29, 48, 255))
try:
    font_banner = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 13)
except Exception:
    font_banner = ImageFont.load_default()
draw.text((150, 85), 'Zetica Hub 0.10.0 is available.', font=font_banner, fill=(255, 255, 255, 255))

# 3. Bottom status bar
# Wipe "CHECKED JUST NOW - USING ARTCRAFT API" (x: 10 to 300, y: 520 to 542)
draw.rectangle([10, 520, 320, 542], fill=(14, 17, 22, 255))
draw.text((16, 524), 'CHECKED JUST NOW · USING ZETICA API', font=font_mono, fill=(110, 115, 125, 255))

# Load original ihRdy image to get exact target size and alpha mask
ihRdy = Image.open(r'c:\Users\ZETICUZ\Documents\artcraft\branding\ihRdy_view.png')
target_size = ihRdy.size # (2048, 1087)
print('Target size:', target_size)

# Resize im to target_size
im_hq = im.resize(target_size, Image.Resampling.LANCZOS)

# Apply ihRdy's alpha channel (rounded corner mask)
if 'A' in ihRdy.getbands():
    ihRdy_alpha = ihRdy.split()[3]
    im_hq.putalpha(ihRdy_alpha)

# Save high-res PNG and AVIF
out_png = r'c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_launcher_hero.png'
im_hq.save(out_png, 'PNG')
print('Saved zetica_launcher_hero.png')

out_avif = r'c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_launcher_hero.avif'
im_hq.save(out_avif, 'AVIF', quality=90)
print('Saved zetica_launcher_hero.avif')

# Overwrite in output_neuraflas
target_png = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\assets\images\ihRdyAqkJP0yCygC1qHb8txaCo.png'
target_avif = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\assets\images\ihRdyAqkJP0yCygC1qHb8txaCo-e95e5071.avif'
im_hq.save(target_png, 'PNG')
im_hq.save(target_avif, 'AVIF', quality=90)
print('Overwritten ihRdy in output_neuraflas')
