import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js\29wilaqtb26u5.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('!e.isHero&&e.label.split("")')
if idx != -1:
    # search backwards for the start of the component or render function
    start = max(0, idx - 6000)
    end = min(len(text), idx + 1000)
    print("CODE BEFORE AND AROUND LETTERS:")
    with open('scripts/extracted_flow_logic.js', 'w', encoding='utf-8') as out:
        out.write(text[start:end])
    print(f"Wrote {end - start} bytes to scripts/extracted_flow_logic.js")
