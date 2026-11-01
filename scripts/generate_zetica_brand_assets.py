import base64
import os
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\Users\ZETICUZ\Documents\artcraft"
BRAND_DIR = os.path.join(ROOT, r"repos\craft-launcher\docs\brand")
ICON_DIR = os.path.join(ROOT, r"repos\craft-launcher\assets\app-icon")

mono_w_path = os.path.join(ROOT, r"branding\zetica-monogram-white.png")
mono_b_path = os.path.join(ROOT, r"branding\zetica-monogram-black.png")

mono_w = Image.open(mono_w_path)
mono_b = Image.open(mono_b_path)

# --- 1. Generate artcraft-logo-white (510 x 108) and artcraft-logo (510 x 108) ---
h = 80
w = int(mono_w.width * (h / mono_w.height))
mono_w_resized = mono_w.resize((w, h), Image.Resampling.LANCZOS)
mono_b_resized = mono_b.resize((w, h), Image.Resampling.LANCZOS)

CANVAS_W = 510
CANVAS_H = 108

# White on transparent for dark background
img_w = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
img_w.paste(mono_w_resized, (15, (CANVAS_H - h) // 2), mono_w_resized)
draw_w = ImageDraw.Draw(img_w)
font = ImageFont.truetype("arialbd.ttf", 68)
draw_w.text((15 + w + 24, 18), "Z E T I C A", fill=(255, 255, 255, 255), font=font)
png_w_path = os.path.join(BRAND_DIR, "artcraft-logo-white.png")
img_w.save(png_w_path)

# Dark on transparent for light background
img_b = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
img_b.paste(mono_b_resized, (15, (CANVAS_H - h) // 2), mono_b_resized)
draw_b = ImageDraw.Draw(img_b)
draw_b.text((15 + w + 24, 18), "Z E T I C A", fill=(12, 13, 17, 255), font=font)
png_b_path = os.path.join(BRAND_DIR, "artcraft-logo.png")
img_b.save(png_b_path)

with open(png_w_path, "rb") as f:
    b64_w = base64.b64encode(f.read()).decode("ascii")

with open(png_b_path, "rb") as f:
    b64_b = base64.b64encode(f.read()).decode("ascii")

svg_w = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" fill="none">
  <image x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" href="data:image/png;base64,{b64_w}" />
</svg>
"""
with open(os.path.join(BRAND_DIR, "artcraft-logo-white.svg"), "w", encoding="utf-8") as f:
    f.write(svg_w)

svg_b = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" fill="none">
  <image x="0" y="0" width="{CANVAS_W}" height="{CANVAS_H}" href="data:image/png;base64,{b64_b}" />
</svg>
"""
with open(os.path.join(BRAND_DIR, "artcraft-logo.svg"), "w", encoding="utf-8") as f:
    f.write(svg_b)

# --- 2. Generate artcraft-mark (1024 x 1024) and artcraft-mark-black (1024 x 1024) ---
mark_size = 1024
mark_img = Image.new("RGBA", (mark_size, mark_size), (0, 0, 0, 0))
draw_mark = ImageDraw.Draw(mark_img)

# White rounded square
radius = 210
draw_mark.rounded_rectangle([20, 20, 1004, 1004], radius=radius, fill=(255, 255, 255, 255), outline=(210, 214, 222, 255), width=10)

# Center black monogram inside squircle
mono_target_w = 680
mono_target_h = int(mono_b.height * (mono_target_w / mono_b.width))
mono_mark = mono_b.resize((mono_target_w, mono_target_h), Image.Resampling.LANCZOS)
mark_img.paste(mono_mark, ((mark_size - mono_target_w) // 2, (mark_size - mono_target_h) // 2), mono_mark)

mark_png_path = os.path.join(BRAND_DIR, "artcraft-mark.png")
mark_img.save(mark_png_path)
mark_img.save(os.path.join(BRAND_DIR, "artcraft-mark-black.png"))
mark_img.save(os.path.join(ICON_DIR, "artcraft-launcher-1024.png"))

# 64x64 and 44x44
mark_img.resize((64, 64), Image.Resampling.LANCZOS).save(os.path.join(BRAND_DIR, "artcraft-mark-64.png"))
mark_img.resize((44, 44), Image.Resampling.LANCZOS).save(os.path.join(BRAND_DIR, "artcraft-mark-black-44.png"))

# Update hicolor app icon sizes
hicolor_dir = os.path.join(ICON_DIR, "hicolor")
for sz in [16, 24, 32, 48, 64, 128, 256, 512]:
    sz_dir = os.path.join(hicolor_dir, f"{sz}x{sz}", "apps")
    if os.path.exists(sz_dir):
        mark_img.resize((sz, sz), Image.Resampling.LANCZOS).save(os.path.join(sz_dir, "artcraft-launcher.png"))

with open(mark_png_path, "rb") as f:
    b64_mark = base64.b64encode(f.read()).decode("ascii")

svg_mark = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" fill="none">
  <image x="0" y="0" width="1024" height="1024" href="data:image/png;base64,{b64_mark}" />
</svg>
"""
with open(os.path.join(BRAND_DIR, "artcraft-mark.svg"), "w", encoding="utf-8") as f:
    f.write(svg_mark)
with open(os.path.join(BRAND_DIR, "artcraft-mark-black.svg"), "w", encoding="utf-8") as f:
    f.write(svg_mark)
with open(os.path.join(ICON_DIR, "artcraft-launcher.svg"), "w", encoding="utf-8") as f:
    f.write(svg_mark)

print("Brand assets generated with exact 510x108 dimensions successfully!")
