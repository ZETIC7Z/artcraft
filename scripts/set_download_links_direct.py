import glob
import os
import re

site_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com"
html_files = glob.glob(os.path.join(site_dir, "**", "*.html"), recursive=True)

modified = 0
for path in html_files:
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    orig = content
    # Replace github release MSI links or any launcher zip links with /zetica-hub-windows-x64.msi
    content = re.sub(
        r'href=["\']https://github\.com/(?:ZETIC7Z|storytold)/craft-launcher/releases/download/[^"\']+["\']',
        'href="/zetica-hub-windows-x64.msi" download="zetica-hub-windows-x64.msi"',
        content
    )
    content = re.sub(
        r'href=["\'][^"\']*zetica-hub-windows-x64\.zip["\']',
        'href="/zetica-hub-windows-x64.msi" download="zetica-hub-windows-x64.msi"',
        content
    )

    if content != orig:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        modified += 1
        print(f"Updated direct download in: {os.path.relpath(path, site_dir)}")

print(f"Direct download link updated across {modified} files.")
