import os
import shutil

def update_index():
    path = 'site/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Canvas
    old_canvas = '<canvas style="display: block;"></canvas>'
    new_canvas = '<canvas id="hero-galaxy-canvas" style="display: block; width: 100%; height: 100%;"></canvas>'
    if old_canvas in html:
        html = html.replace(old_canvas, new_canvas, 1)
        print("Replaced canvas tag.")
    elif 'id="hero-galaxy-canvas"' in html:
        print("Canvas tag already updated.")
    else:
        print("Warning: could not find old canvas tag!")

    # 2. Update Hero Wordmark
    # Find the old wordmark container: role="img" aria-label="ZETICA"
    start_tag = '<div role="img" aria-label="ZETICA"'
    idx_start = html.find(start_tag)
    if idx_start != -1:
        # find closing </div>
        idx_end = html.find('</div>', idx_start) + 6
        old_wm = html[idx_start:idx_end]
        print(f"Found old wordmark ({len(old_wm)} chars):")
        print(old_wm[:150])

        new_wm = '''<div id="hero-wordmark-masthead" role="img" aria-label="ZETICA" class="relative text-ink select-none my-4" style="font-family: var(--font-archivo), 'Space Grotesk', system-ui, sans-serif; font-weight: 850; font-stretch: 125%; font-size: clamp(48px, 9vw, 96px); line-height: 1; letter-spacing: 0.04em; display: flex; align-items: center; justify-content: center; gap: 0.16em;">
  <span id="wm-letter-0" class="wm-letter" style="display:inline-flex; align-items:center; justify-content:center; width: 1.42em; height: 1em; vertical-align: middle;">
    <img src="./assets/images/zetica-monogram.svg" alt="ZETICA" style="width: 100%; height: 100%; object-fit: contain;" />
  </span>
  <span id="wm-letter-1" class="wm-letter" data-char="Z" style="display:inline-block;">Z</span>
  <span id="wm-letter-2" class="wm-letter" data-char="E" style="display:inline-block;">E</span>
  <span id="wm-letter-3" class="wm-letter" data-char="T" style="display:inline-block;">T</span>
  <span id="wm-letter-4" class="wm-letter" data-char="I" style="display:inline-block;">I</span>
  <span id="wm-letter-5" class="wm-letter" data-char="C" style="display:inline-block;">C</span>
  <span id="wm-letter-6" class="wm-letter" data-char="A" style="display:inline-block;">A</span>
</div>'''
        html = html[:idx_start] + new_wm + html[idx_end:]
        print("Updated hero wordmark with clean black monogram and letters.")
    elif 'id="hero-wordmark-masthead"' in html:
        print("Wordmark masthead already updated.")
    else:
        print("Warning: could not locate wordmark start tag.")

    # 3. Add scripts before </body>
    script_bundle = '''
<!-- ZETICA 3D Galaxy & Motion Animation Engine -->
<script src="./assets/js/three.min.js"></script>
<script src="./assets/js/gsap.min.js"></script>
<script src="./assets/js/ScrollTrigger.min.js"></script>
<script src="./assets/js/zetica-hero-galaxy.js"></script>
<script src="./assets/js/zetica-wordmark-scroll.js"></script>
'''
    if 'zetica-hero-galaxy.js' not in html:
        body_idx = html.rfind('</body>')
        if body_idx != -1:
            html = html[:body_idx] + script_bundle + html[body_idx:]
            print("Appended animation scripts before </body>.")
    else:
        print("Animation scripts already present.")

    # Write back
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved site/index.html successfully.")

    # Sync to UNCAGE folder if present
    uncage_index = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\index.html'
    if os.path.exists(uncage_index):
        with open(uncage_index, 'w', encoding='utf-8') as f:
            f.write(html)
        print("Synchronized C:\\Users\\ZETICUZ\\Documents\\UNCAGE\\output\\getartcraft.com\\index.html")

    # Also copy the js scripts to UNCAGE folder
    uncage_js = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js'
    if os.path.exists(uncage_js):
        for js_file in ['three.min.js', 'gsap.min.js', 'ScrollTrigger.min.js', 'zetica-hero-galaxy.js', 'zetica-wordmark-scroll.js']:
            src_f = os.path.join('site', 'assets', 'js', js_file)
            if os.path.exists(src_f):
                shutil.copy(src_f, os.path.join(uncage_js, js_file))
        print("Synchronized JS scripts to UNCAGE folder.")

if __name__ == '__main__':
    update_index()
