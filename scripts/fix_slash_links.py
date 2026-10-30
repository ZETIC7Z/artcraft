import glob
import re

html_files = sorted(glob.glob('site/*.html')) + sorted(glob.glob('site/**/*.html', recursive=True))

replacements = {
    'href="/tutorials"': 'href="./tutorials.html"',
    'href="/news"': 'href="./news.html"',
    'href="/faq"': 'href="./faq.html"',
    'href="/press-kit"': 'href="./press-kit.html"',
    'href="/download"': 'href="./download.html"',
    'href="/apps"': 'href="./apps.html"',
    'href="/pricing"': 'href="./pricing.html"',
    'href="/support"': 'href="./support.html"',
    'href="/beta"': 'href="./beta.html"',
    'href="/minimax-h3"': 'href="./minimax-h3.html"',
    'href="/seedance-2"': 'href="./seedance-2.html"',
    'href="/seedance2-5"': 'href="./seedance2-5.html"',
}

count = 0
for f in html_files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    modified = False
    for k, v in replacements.items():
        if k in content:
            # Handle deep files if in subfolder like site/apps/ or site/tutorials/
            target = v
            if '/apps/' in f.replace('\\', '/') or '/tutorials/' in f.replace('\\', '/') or '/news/' in f.replace('\\', '/') or '/faq/' in f.replace('\\', '/'):
                target = v.replace('./', '../')
            content = content.replace(k, target)
            modified = True
            count += 1
            
    if modified:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(content)
        print(f"Updated links in: {f}")

print(f"Total link replacements made: {count}")
