import glob
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_files = glob.glob('site/**/*.html', recursive=True)
print(f"Scanning {len(html_files)} HTML files for prebaked dead scrollbar...")

cleaned_count = 0
for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    start_marker = '<div role="scrollbar"'
    start = html.find(start_marker)
    if start != -1:
        # The block ends right before our custom comment or script
        # Let's find the closing of that fixed container
        # In our inspection, it ends right before '<!-- ZETICA' or '<script' or '</body>'
        end_markers = ['<!-- ZETICA', '<script src="./assets/js/', '<script src="../assets/js/', '<script src="../../assets/js/', '</body>']
        end = -1
        for em in end_markers:
            idx = html.find(em, start)
            if idx != -1 and (end == -1 or idx < end):
                end = idx

        if end != -1:
            print(f"Cleaning {path}: removed {end - start} bytes of dead prebaked scrollbar")
            html = html[:start] + html[end:]
            with open(path, 'w', encoding='utf-8') as f:
                f.write(html)
            cleaned_count += 1
        else:
            print(f"Could not determine end marker for {path}")

print(f"Cleaned {cleaned_count} files successfully!")
