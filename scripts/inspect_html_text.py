import shutil
import re

# 1. Replace nav logo SVGs
src_logo = r'c:\Users\ZETICUZ\Documents\artcraft\branding\zetica_nav_logo.svg'
dest_logo1 = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\assets\images\SSqo2xpb8BFyqexlL0GXm9AUGw-8ce4293f.svg'
dest_logo2 = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\assets\images\SSqo2xpb8BFyqexlL0GXm9AUGw.svg'

shutil.copyfile(src_logo, dest_logo1)
shutil.copyfile(src_logo, dest_logo2)
print('Copied zetica_nav_logo.svg to SSqo2xpb8BFyqexlL0GXm9AUGw files')

# 2. Inspect index.html
html_path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Let's check occurrences of key phrases
phrases = [
    'Supercharge Your Business',
    'AI-Powered',
    'Intelligence',
    'Get Started for Free',
    'Get This Template',
    'NeuraFlow',
    'NeuraFlas',
    'Automate workflows',
    'About Us',
    'Integration'
]

for p in phrases:
    print(f'Count of "{p}": {html.count(p)}')
