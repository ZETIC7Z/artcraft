import os
import glob
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

def update_all_pages():
    html_files = glob.glob('site/**/*.html', recursive=True)
    print(f'Updating {len(html_files)} HTML pages with theme, ruler, and Lenis assets...')

    for path in html_files:
        with open(path, 'r', encoding='utf-8') as f:
            html = f.read()

        rel_depth = os.path.relpath('site', os.path.dirname(path)).replace('\\', '/')
        css_prefix = '.' if rel_depth == '.' else rel_depth

        # 1. Link zetica-enhancements.css
        enhancement_link = f'<link rel="stylesheet" href="{css_prefix}/assets/css/zetica-enhancements.css">'
        if 'zetica-enhancements.css' not in html:
            head_idx = html.find('</head>')
            if head_idx != -1:
                html = html[:head_idx] + '  ' + enhancement_link + '\n' + html[head_idx:]

        # 2. Add lenis.min.js
        lenis_script = f'<script src="{css_prefix}/assets/js/lenis.min.js"></script>'
        if 'lenis.min.js' not in html:
            body_idx = html.rfind('</body>')
            if body_idx != -1:
                html = html[:body_idx] + lenis_script + '\n' + html[body_idx:]

        # 3. Add zetica-theme.js
        theme_script = f'<script src="{css_prefix}/assets/js/zetica-theme.js"></script>'
        if 'zetica-theme.js' not in html:
            body_idx = html.rfind('</body>')
            if body_idx != -1:
                html = html[:body_idx] + theme_script + '\n' + html[body_idx:]

        # 4. On index.html ensure zetica-scroll-ruler.js is present
        if os.path.basename(path) == 'index.html':
            ruler_script = f'<script src="{css_prefix}/assets/js/zetica-scroll-ruler.js"></script>'
            if 'zetica-scroll-ruler.js' not in html:
                body_idx = html.rfind('</body>')
                if body_idx != -1:
                    html = html[:body_idx] + ruler_script + '\n' + html[body_idx:]

        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)

    print('Updated all HTML files successfully.')

    # Sync to UNCAGE folder
    uncage_root = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com'
    if os.path.exists(uncage_root):
        os.makedirs(os.path.join(uncage_root, 'assets', 'css'), exist_ok=True)
        os.makedirs(os.path.join(uncage_root, 'assets', 'js'), exist_ok=True)
        shutil.copy('site/assets/css/zetica-enhancements.css', os.path.join(uncage_root, 'assets', 'css', 'zetica-enhancements.css'))
        shutil.copy('site/assets/js/lenis.min.js', os.path.join(uncage_root, 'assets', 'js', 'lenis.min.js'))
        shutil.copy('site/assets/js/zetica-theme.js', os.path.join(uncage_root, 'assets', 'js', 'zetica-theme.js'))
        shutil.copy('site/assets/js/zetica-hero-galaxy.js', os.path.join(uncage_root, 'assets', 'js', 'zetica-hero-galaxy.js'))
        shutil.copy('site/assets/js/zetica-scroll-ruler.js', os.path.join(uncage_root, 'assets', 'js', 'zetica-scroll-ruler.js'))
        shutil.copy('site/assets/js/zetica-wordmark-scroll.js', os.path.join(uncage_root, 'assets', 'js', 'zetica-wordmark-scroll.js'))
        shutil.copy('site/index.html', os.path.join(uncage_root, 'index.html'))
        print('Synchronized to UNCAGE output folder successfully.')

if __name__ == '__main__':
    update_all_pages()
