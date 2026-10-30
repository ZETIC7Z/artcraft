import os
import shutil
import base64
from PIL import Image

launcher_dir = r"c:\Users\ZETICUZ\Documents\artcraft\repos\craft-launcher"
powe_png_path = r"c:\Users\ZETICUZ\Documents\artcraft\branding\powe_rgba.png"

# Load source high-res 3D monogram
src_img = Image.open(powe_png_path)
print(f"Loaded source image: {src_img.size}, mode: {src_img.mode}")

# 1. Update docs/brand/
brand_dir = os.path.join(launcher_dir, "docs", "brand")
os.makedirs(brand_dir, exist_ok=True)

# Generate square mark with padding (1024x1024)
mark_1024 = Image.new("RGBA", (1024, 1024), (0, 0, 0, 0))
# compute scaling to fit inside 960x960
aspect = src_img.width / src_img.height
target_w = 960
target_h = int(target_w / aspect)
resized_powe = src_img.resize((target_w, target_h), Image.Resampling.LANCZOS)
offset_x = (1024 - target_w) // 2
offset_y = (1024 - target_h) // 2
mark_1024.paste(resized_powe, (offset_x, offset_y), resized_powe)

# Save marks
mark_1024.save(os.path.join(brand_dir, "artcraft-mark.png"))
mark_1024.save(os.path.join(brand_dir, "artcraft-mark-black.png"))
mark_1024.resize((64, 64), Image.Resampling.LANCZOS).save(os.path.join(brand_dir, "artcraft-mark-64.png"))
mark_1024.resize((44, 44), Image.Resampling.LANCZOS).save(os.path.join(brand_dir, "artcraft-mark-black-44.png"))

# Generate base64 string for SVGs
with open(os.path.join(brand_dir, "artcraft-mark.png"), "rb") as f:
    mark_b64 = base64.b64encode(f.read()).decode("ascii")

mark_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" fill="none">
  <image width="1024" height="1024" href="data:image/png;base64,{mark_b64}" />
</svg>'''

with open(os.path.join(brand_dir, "artcraft-mark.svg"), "w", encoding="utf-8") as f:
    f.write(mark_svg)
with open(os.path.join(brand_dir, "artcraft-mark-black.svg"), "w", encoding="utf-8") as f:
    f.write(mark_svg)

# Full wordmark SVG (1038 x 108 aspect matching original ARTCRAFT_LOGO_ASPECT)
logo_svg_white = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1038 108" fill="none">
  <image x="10" y="4" width="160" height="100" href="data:image/png;base64,{mark_b64}" preserveAspectRatio="xMidYMid meet" />
  <text x="190" y="80" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="76" letter-spacing="6" fill="#FFFFFF">ZETICA</text>
</svg>'''

logo_svg_dark = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1038 108" fill="none">
  <image x="10" y="4" width="160" height="100" href="data:image/png;base64,{mark_b64}" preserveAspectRatio="xMidYMid meet" />
  <text x="190" y="80" font-family="system-ui, -apple-system, sans-serif" font-weight="900" font-size="76" letter-spacing="6" fill="#0B0B0C">ZETICA</text>
</svg>'''

with open(os.path.join(brand_dir, "artcraft-logo-white.svg"), "w", encoding="utf-8") as f:
    f.write(logo_svg_white)
with open(os.path.join(brand_dir, "artcraft-logo.svg"), "w", encoding="utf-8") as f:
    f.write(logo_svg_dark)

# 2. Update assets/app-icon/
app_icon_dir = os.path.join(launcher_dir, "assets", "app-icon")
os.makedirs(app_icon_dir, exist_ok=True)
mark_1024.save(os.path.join(app_icon_dir, "artcraft-launcher-1024.png"))
with open(os.path.join(app_icon_dir, "artcraft-launcher.svg"), "w", encoding="utf-8") as f:
    f.write(mark_svg)

# Generate multi-size .ico file
ico_sizes = [(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
mark_1024.save(os.path.join(app_icon_dir, "artcraft-launcher.ico"), format="ICO", sizes=ico_sizes)

# Update hicolor png icons
hicolor_dir = os.path.join(app_icon_dir, "hicolor")
for sz in [16, 32, 48, 64, 128, 256, 512]:
    sz_dir = os.path.join(hicolor_dir, f"{sz}x{sz}", "apps")
    if os.path.exists(sz_dir):
        for f in os.listdir(sz_dir):
            if f.endswith(".png"):
                mark_1024.resize((sz, sz), Image.Resampling.LANCZOS).save(os.path.join(sz_dir, f))

print("Updated all launcher brand icons and assets successfully!")
