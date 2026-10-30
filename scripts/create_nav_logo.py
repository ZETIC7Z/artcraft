import base64
from PIL import Image
import io

# Load cropped powe_rgba.png
im = Image.open(r'c:\Users\ZETICUZ\Documents\artcraft\branding\powe_rgba.png')
# Resize to height 38, keeping aspect ratio
target_h = 36
aspect = im.width / im.height
target_w = int(target_h * aspect)
im_resized = im.resize((target_w, target_h), Image.Resampling.LANCZOS)

buffered = io.BytesIO()
im_resized.save(buffered, format='PNG')
b64_emblem = base64.b64encode(buffered.getvalue()).decode('utf-8')

# The navbar logo width is 175, height 40
# We can position the emblem on the left: x=2, y=2, width=target_w, height=target_h
# And text ZETICA on the right starting at x = target_w + 12
text_x = target_w + 12

svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" width="175" height="40" viewBox="0 0 175 40" fill="none">
  <!-- Official ZETICA 3D Monogram Emblem from Powe.svg -->
  <image x="2" y="2" width="{target_w}" height="{target_h}" href="data:image/png;base64,{b64_emblem}" preserveAspectRatio="xMidYMid meet" />
  <!-- ZETICA Bold Wordmark -->
  <g transform="translate({text_x}, 27)">
    <text font-family="system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif" font-weight="900" font-size="20" letter-spacing="2.5" fill="#FFFFFF">ZETICA</text>
  </g>
</svg>'''

out_path = r'c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_nav_logo.svg'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f'Created zetica_nav_logo.svg: emblem={target_w}x{target_h}, text_x={text_x}')
