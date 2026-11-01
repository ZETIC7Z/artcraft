import glob
import os
import re

site_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com"
html_files = glob.glob(os.path.join(site_dir, "**", "*.html"), recursive=True)

print(f"Scanning {len(html_files)} HTML files in {site_dir}...")

msi_target = "/zetica-hub-windows-x64.msi"
github_msi_url = "https://github.com/ZETIC7Z/craft-launcher/releases/download/v0.10.0/zetica-hub-windows-x64.msi"

modified_count = 0

for file_path in html_files:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        orig = f.read()

    content = orig

    # Replace zip release downloads with the msi target
    content = re.sub(
        r'https://github\.com/ZETIC7Z/craft-launcher/releases/download/[^/]+/zetica-hub-windows-x64\.zip',
        github_msi_url,
        content
    )
    content = re.sub(
        r'https://github\.com/storytold/craft-launcher/releases/download/[^/]+/artcraft-launcher-[^/]+-windows-x64\.(?:msi|zip)',
        github_msi_url,
        content
    )
    # Also if there are relative links or button links
    content = re.sub(r'href="[^"]*zetica-hub-windows-x64\.zip"', f'href="{msi_target}"', content)
    content = re.sub(r"href='[^']*zetica-hub-windows-x64\.zip'", f"href='{msi_target}'", content)

    # In hero buttons or download buttons where text says "DOWNLOAD ZETICA HUB" or "DOWNLOAD LAUNCHER"
    # Ensure href points to /zetica-hub-windows-x64.msi
    # Also update any text saying "(ZIP)" to "(MSI)"
    content = re.sub(r'\.zip\b', '.msi', content, flags=re.IGNORECASE)
    content = re.sub(r'\bZIP\b', 'MSI', content)

    if content != orig:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        modified_count += 1
        rel = os.path.relpath(file_path, site_dir)
        print(f"Updated: {rel}")

print(f"Finished! Updated {modified_count} files to use MSI installer downloads.")
