with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Remove the script that moves it into footer
pos_start = html.find('<!-- Start of ZETICUZ Developer Footer Attribution -->')
pos_end = html.find('<!-- End of ZETICUZ Developer Footer Attribution -->') + len('<!-- End of ZETICUZ Developer Footer Attribution -->')

clean_snippet = '''<!-- Start of ZETICUZ Developer Footer Attribution -->
<div id="zeticuz-dev-footer" style="display:flex !important;flex-wrap:wrap !important;align-items:center !important;justify-content:center !important;gap:16px !important;background:#050508 !important;padding:32px 20px 48px 20px !important;border-top:1px solid rgba(255,255,255,0.1) !important;width:100% !important;box-sizing:border-box !important;position:relative !important;z-index:999999 !important;text-align:center !important;">
  <img src="./assets/images/zeticuz-logo.svg" alt="ZETICUZ Developer Logo" style="height:28px !important;width:auto !important;display:inline-block !important;vertical-align:middle !important;" />
  <span style="font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;font-size:14px !important;font-weight:600 !important;letter-spacing:0.8px !important;color:#9ca3af !important;">
    SITE DEVELOPED BY: <span style="color:#ffffff !important;">Sam Pangilinan</span> · © 2026
  </span>
  <a href="https://www.zeticuz.xyz/" target="_blank" rel="noopener noreferrer" style="margin-left:8px !important;padding:7px 16px !important;background:rgba(255,255,255,0.08) !important;border:1px solid rgba(255,255,255,0.2) !important;border-radius:6px !important;color:#ffffff !important;font-size:12px !important;font-weight:600 !important;letter-spacing:0.5px !important;text-decoration:none !important;display:inline-flex !important;align-items:center !important;gap:6px !important;">
    <span>View Developer Portfolio</span>
    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17l9.2-9.2M17 17V8H8"/></svg>
  </a>
</div>
<!-- End of ZETICUZ Developer Footer Attribution -->'''

html = html[:pos_start] + clean_snippet + html[pos_end:]

with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Updated clean attribution without moving script!')
