import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'c:\Users\ZETICUZ\Documents\artcraft\site\index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Check if lenis.min.js is in index.html
if 'lenis.min.js' not in content:
    print("Adding lenis.min.js to site/index.html")
    # Insert lenis.min.js before three.min.js or before zetica-scroll-ruler.js
    needle = '<script src="./assets/js/three.min.js"></script>'
    replacement = '<script src="./assets/js/lenis.min.js"></script>\n<script src="./assets/js/three.min.js"></script>'
    if needle in content:
        content = content.replace(needle, replacement, 1)
        with open(r'c:\Users\ZETICUZ\Documents\artcraft\site\index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        print("Successfully added lenis.min.js!")
    else:
        print("Could not find three.min.js marker")
else:
    print("lenis.min.js already present in index.html")
