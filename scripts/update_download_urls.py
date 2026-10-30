import os
import glob
import re

directories = [
    r'c:\Users\ZETICUZ\Documents\artcraft\site',
    r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com'
]

OLD_LAUNCHER_MSI = 'https://github.com/ZETIC7Z/craft-launcher/releases/download/v0.8.1/artcraft-launcher-0.8.1-windows-x64.msi'
NEW_HUB_ZIP = 'https://github.com/ZETIC7Z/craft-launcher/releases/download/v0.10.0/zetica-hub-windows-x64.zip'

OLD_SETUP_EXE = 'https://github.com/ZETIC7Z/artcraft/releases/download/artcraft-v0.41.0/Zetica_0.41.0_x64-setup.exe'
# We link to the official Zetica Hub release zip directly for Windows
NEW_SETUP_EXE = 'https://github.com/ZETIC7Z/craft-launcher/releases/download/v0.10.0/zetica-hub-windows-x64.zip'

for base_dir in directories:
    if not os.path.exists(base_dir):
        continue
    html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)
    for fpath in html_files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        changed = False
        if OLD_LAUNCHER_MSI in content:
            content = content.replace(OLD_LAUNCHER_MSI, NEW_HUB_ZIP)
            changed = True
        if OLD_SETUP_EXE in content:
            content = content.replace(OLD_SETUP_EXE, NEW_SETUP_EXE)
            changed = True

        # Also check for any storytold or old artcraft releases
        if 'https://github.com/storytold/craft-launcher/releases' in content:
            content = content.replace('https://github.com/storytold/craft-launcher/releases', 'https://github.com/ZETIC7Z/craft-launcher/releases')
            changed = True

        if changed:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated download URLs in: {fpath}")

print("Download URL update complete!")
