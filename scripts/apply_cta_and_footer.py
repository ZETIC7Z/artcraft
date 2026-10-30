import os

root_dir = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas'
html_path = os.path.join(root_dir, 'index.html')
js_dir = os.path.join(root_dir, 'assets', 'js')

# 1. Update index.html
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# CTA Title & Subtitle replacements
html = html.replace('Ready to Automate Your ', 'Ready to Supercharge Your ')
html = html.replace('with AI ?', 'with ZETICA ?')
html = html.replace('Business </span></h2></div><div class="framer-1kimzcu" data-framer-name="Title" data-framer-component-type="RichTextContainer" style="justify-content: center; --framer-paragraph-spacing: 0px; transform: none; opacity: 1;"><h2 class="framer-text framer-styles-preset-1px0flj" data-styles-preset="D3zDSiLe5" style="--framer-text-alignment:center">with AI ?',
                    'Creativity </span></h2></div><div class="framer-1kimzcu" data-framer-name="Title" data-framer-component-type="RichTextContainer" style="justify-content: center; --framer-paragraph-spacing: 0px; transform: none; opacity: 1;"><h2 class="framer-text framer-styles-preset-1px0flj" data-styles-preset="D3zDSiLe5" style="--framer-text-alignment:center">with ZETICA ?')

html = html.replace('Start leveraging the power of AI today and unlock new levels of efficiency and growth.',
                    'Download ZETICA Studio today and unlock native GPU-accelerated creative performance.')

# Copyright text replacement
html = html.replace('href="https://designmonks.co" target="_blank" rel="noopener">Design Monks</a><!--/$-->. All rights reserved.',
                    'href="https://www.zeticuz.xyz/" target="_blank" rel="noopener">ZETICA Studio</a><!--/$-->. All rights reserved.')
html = html.replace('2025 © <!--$--><a class="framer-text framer-styles-preset-20cgap" data-styles-preset="dOIWJRzgi" href="https://designmonks.co"',
                    '2026 © <!--$--><a class="framer-text framer-styles-preset-20cgap" data-styles-preset="dOIWJRzgi" href="https://www.zeticuz.xyz/"')

# Attribution snippet
attribution_box = '''
<div style="display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:14px;margin-top:28px;padding:20px 24px;border-top:1px solid rgba(255,255,255,0.08);width:100%;text-align:center;box-sizing:border-box;">
  <img src="./assets/images/zeticuz-logo.svg" alt="ZETICUZ Developer Logo" style="height:28px;width:auto;display:inline-block;vertical-align:middle;" />
  <span style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;font-size:13px;font-weight:600;letter-spacing:0.8px;color:#9ca3af;">
    SITE DEVELOPED BY: <span style="color:#ffffff;">Sam Pangilinan</span> · © 2026
  </span>
  <a href="https://www.zeticuz.xyz/" target="_blank" rel="noopener noreferrer" style="margin-left:8px;padding:6px 14px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.18);border-radius:6px;color:#ffffff;font-size:12px;font-weight:600;letter-spacing:0.5px;text-decoration:none;display:inline-flex;align-items:center;gap:6px;">
    <span>View Developer Portfolio</span>
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17l9.2-9.2M17 17V8H8"/></svg>
  </a>
</div>
'''

if 'SITE DEVELOPED BY: <span style="color:#ffffff;">Sam Pangilinan</span>' not in html:
    # insert inside the copyright text block or right before </footer>
    pos_footer_end = html.rfind('</footer>')
    if pos_footer_end != -1:
        html = html[:pos_footer_end] + attribution_box + html[pos_footer_end:]
        print('Inserted attribution_box before </footer>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print('Updated index.html CTA and footer')

# 2. Update JS bundles
js_replacements = [
    ('Ready to Automate Your ', 'Ready to Supercharge Your '),
    ('with AI ?', 'with ZETICA ?'),
    ('Start leveraging the power of AI today and unlock new levels of efficiency and growth.',
     'Download ZETICA Studio today and unlock native GPU-accelerated creative performance.'),
    ('Design Monks', 'ZETICA Studio'),
    ('https://designmonks.co', 'https://www.zeticuz.xyz/'),
    ('2025 ©', '2026 ©')
]

for f in os.listdir(js_dir):
    if f.endswith('.js'):
        p = os.path.join(js_dir, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
        
        modified = False
        for old, new in js_replacements:
            if old in c:
                c = c.replace(old, new)
                modified = True
        
        if modified:
            with open(p, 'w', encoding='utf-8') as fp:
                fp.write(c)
            print(f'Updated JS bundle: {f}')

print('All CTA and Footer updates completed successfully!')
