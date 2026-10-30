import os
import shutil
from PIL import Image

output_img_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\images"
os.makedirs(output_img_dir, exist_ok=True)

# 1. Copy Sam Pangilinan's developer logo
dev_logo_src = r"C:\Users\ZETICUZ\Downloads\zeticuz-logo.svg"
dev_logo_dest = os.path.join(output_img_dir, "zeticuz-logo.svg")
shutil.copyfile(dev_logo_src, dev_logo_dest)
print(f"Copied dev logo to {dev_logo_dest}")

# 2. Extract base64 from powe_rgba.png to create official SVG icon
import base64
with open(r"c:\Users\ZETICUZ\Documents\artcraft\branding\powe_rgba.png", "rb") as f:
    powe_b64 = base64.b64encode(f.read()).decode("ascii")

# Create official ZETICA SVG icon
zetica_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2121 1260" fill="none">
  <image width="2121" height="1260" href="data:image/png;base64,{powe_b64}" />
</svg>'''

# Overwrite artcraft-icon-1d615f19.svg and artcraft-icon.svg
for fname in ["artcraft-icon-1d615f19.svg", "artcraft-icon.svg", "zetica-icon.svg"]:
    target = os.path.join(output_img_dir, fname)
    with open(target, "w", encoding="utf-8") as f:
        f.write(zetica_svg)
    print(f"Wrote {target}")

# Also copy powe_rgba.png
shutil.copyfile(
    r"c:\Users\ZETICUZ\Documents\artcraft\branding\powe_rgba.png",
    os.path.join(output_img_dir, "zetica-emblem.png")
)
print("Asset generation complete!")
