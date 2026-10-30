import base64
import io
import re
from PIL import Image

with open(r'C:\Users\ZETICUZ\Downloads\ZE.svg', 'r', encoding='utf-8') as f:
    text = f.read()

# Extract the base64 image
m = re.findall(r'href="data:image/png;base64,([^"]+)"', text)
if not m:
    m = re.findall(r'xlink:href="data:image/png;base64,([^"]+)"', text)

print(f"Found {len(m)} base64 images.")
for i, b64 in enumerate(m):
    data = base64.b64decode(b64)
    img = Image.open(io.BytesIO(data))
    print(f"Image {i}: size={img.size}, mode={img.mode}")
    bbox = img.getbbox()
    print(f"Image {i} non-empty bbox:", bbox)
    img.save(f"branding/ze_extracted_{i}.png")
