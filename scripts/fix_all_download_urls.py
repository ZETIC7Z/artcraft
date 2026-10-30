import glob
import os
import re

directories = [
    r'c:\Users\ZETICUZ\Documents\artcraft\site',
    r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com'
]

OLD_PATTERNS = [
    r'https://github.com/[^/]+/craft-launcher/releases/download/v0\.8\.1/artcraft-launcher-0\.8\.1-windows-x64\.msi',
    r'https://github.com/[^/]+/craft-launcher/releases/download/v0\.8\.1/artcraft-launcher-0\.8\.1-windows-x64-portable\.zip',
    r'https://github.com/storytold/craft-launcher/releases/download/v0\.8\.1/artcraft-launcher-0\.8\.1-windows-x64\.msi',
    r'https://github.com/storytold/craft-launcher/releases/download/v0\.8\.1/artcraft-launcher-0\.8\.1-windows-x64-portable\.zip',
]

REPLACEMENT = 'https://github.com/ZETIC7Z/craft-launcher/releases/download/v0.10.0/zetica-hub-windows-x64.zip'

updated_count = 0

for base in directories:
    if not os.path.exists(base):
        continue
    for f in glob.glob(os.path.join(base, '**', '*.html'), recursive=True):
        with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
        
        orig_content = content
        for pat in OLD_PATTERNS:
            content = re.sub(pat, REPLACEMENT, content)
            
        # Also replace any remaining artcraft-launcher-0.8.1-windows-x64.msi references
        content = content.replace('artcraft-launcher-0.8.1-windows-x64.msi', 'zetica-hub-windows-x64.zip')
        content = content.replace('v0.8.1/artcraft-launcher-0.8.1', 'v0.10.0/zetica-hub')
        
        if content != orig_content:
            with open(f, 'w', encoding='utf-8') as fp:
                fp.write(content)
            updated_count += 1
            print(f"Updated: {f}")

print(f"Successfully updated {updated_count} files.")
