import os

html_path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

attribution_snippet = '''
<!-- Start of ZETICUZ Developer Footer Attribution -->
<div id="zeticuz-dev-footer" style="background:#000000;padding:24px 20px 36px 20px;border-top:1px solid rgba(255,255,255,0.08);width:100%;box-sizing:border-box;display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:14px;position:relative;z-index:99999;">
  <img src="./assets/images/zeticuz-logo.svg" alt="ZETICUZ Developer Logo" style="height:28px;width:auto;display:inline-block;vertical-align:middle;" />
  <span style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;font-size:13px;font-weight:600;letter-spacing:0.8px;color:#9ca3af;">
    SITE DEVELOPED BY: <span style="color:#ffffff;">Sam Pangilinan</span> · © 2026
  </span>
  <a href="https://www.zeticuz.xyz/" target="_blank" rel="noopener noreferrer" style="margin-left:8px;padding:6px 16px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.2);border-radius:6px;color:#ffffff;font-size:12px;font-weight:600;letter-spacing:0.5px;text-decoration:none;display:inline-flex;align-items:center;gap:6px;transition:all 0.2s ease;">
    <span>View Developer Portfolio</span>
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17l9.2-9.2M17 17V8H8"/></svg>
  </a>
</div>
<script>
  (function() {
    function injectFooterAttribution() {
      const footer = document.querySelector('footer');
      const devFooter = document.getElementById('zeticuz-dev-footer');
      if (footer && devFooter && devFooter.parentElement !== footer) {
        footer.appendChild(devFooter);
      }
    }
    window.addEventListener('load', injectFooterAttribution);
    setTimeout(injectFooterAttribution, 1000);
    setTimeout(injectFooterAttribution, 2500);
    setTimeout(injectFooterAttribution, 4000);
  })();
</script>
<!-- End of ZETICUZ Developer Footer Attribution -->
'''

if 'id="zeticuz-dev-footer"' not in html:
    html = html.replace('<!-- Start of bodyEnd -->', attribution_snippet + '\n<!-- Start of bodyEnd -->')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Inserted zeticuz-dev-footer into index.html!')
else:
    print('Already present!')
