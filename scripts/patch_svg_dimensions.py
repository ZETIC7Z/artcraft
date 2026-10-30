import os
import re

svg_files = [
    r'c:\Users\ZETICUZ\Documents\artcraft\site\assets\images\artcraft-icon-1d615f19.svg',
    r'c:\Users\ZETICUZ\Documents\artcraft\site\assets\images\artcraft-icon.svg',
    r'c:\Users\ZETICUZ\Documents\artcraft\site\assets\images\zetica-icon.svg',
    r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\images\artcraft-icon-1d615f19.svg',
    r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\images\artcraft-icon.svg',
    r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\images\zetica-icon.svg',
]

for svg_path in svg_files:
    if not os.path.exists(svg_path):
        continue
    with open(svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    # Find the <svg ...> opening tag
    m = re.search(r'<svg([^>]*)>', svg_content)
    if m:
        attrs = m.group(1)
        if 'width=' not in attrs:
            new_tag = f'<svg width="48" height="28.5"{attrs}>'
            new_svg = svg_content[:m.start()] + new_tag + svg_content[m.end():]
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(new_svg)
            print(f"Added width/height to <svg> in: {svg_path}")
        else:
            print(f"<svg> tag already has width/height: {svg_path}")

print("Fixed SVG tags successfully.")
