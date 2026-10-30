import base64
from io import BytesIO
from PIL import Image

def generate_assets():
    img = Image.open('branding/ze_cropped.png')
    buf = BytesIO()
    img.save(buf, format='PNG', optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode('ascii')
    w, h = img.size

    # SVG with currentColor
    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <defs>
    <mask id="ze-monogram-mask">
      <image width="{w}" height="{h}" href="data:image/png;base64,{b64}"/>
    </mask>
  </defs>
  <rect width="{w}" height="{h}" fill="currentColor" mask="url(#ze-monogram-mask)"/>
</svg>'''

    with open('branding/zetica-monogram.svg', 'w', encoding='utf-8') as f:
        f.write(svg_content)

    # Pure black RGBA
    rgba_black = Image.new('RGBA', img.size, (0, 0, 0, 0))
    # Fill with black RGB and alpha from mask
    black_layer = Image.new('RGB', img.size, (0, 0, 0))
    rgba_black = Image.merge('RGBA', (*black_layer.split(), img))
    rgba_black.save('branding/zetica-monogram-black.png', optimize=True)

    # Pure white RGBA
    white_layer = Image.new('RGB', img.size, (255, 255, 255))
    rgba_white = Image.merge('RGBA', (*white_layer.split(), img))
    rgba_white.save('branding/zetica-monogram-white.png', optimize=True)

    # Also generate a standalone solid black SVG for direct <img> or background usage
    svg_black = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">
  <defs>
    <mask id="ze-monogram-mask-black">
      <image width="{w}" height="{h}" href="data:image/png;base64,{b64}"/>
    </mask>
  </defs>
  <rect width="{w}" height="{h}" fill="#000000" mask="url(#ze-monogram-mask-black)"/>
</svg>'''
    with open('branding/zetica-monogram-black.svg', 'w', encoding='utf-8') as f:
        f.write(svg_black)

    print(f"Generated assets for monogram size {w}x{h}:")
    print("- branding/zetica-monogram.svg")
    print("- branding/zetica-monogram-black.svg")
    print("- branding/zetica-monogram-black.png")
    print("- branding/zetica-monogram-white.png")

if __name__ == '__main__':
    generate_assets()
