import os

html_path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html'
js_path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\assets\js\FGTOLLMThkoHC2wnismTmroah2VJGUOs0d94yau0hZ8.IJGwxbv3-49d9b659.js'

old_text = "Automate workflows, predict trends, and make smarter decisions with ZETICA's cutting-edge AI platform"
new_text = "Unleash GPU-accelerated VFX, Vector, Photo, Audio, and Publishing tools with ZETICA's lightweight native platform."

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

if old_text in html:
    html = html.replace(old_text, new_text)
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print('Updated subtitle in index.html')

with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# in JS it might still have NeuraFlow or ZETICA
js_old1 = "Automate workflows, predict trends, and make smarter decisions with NeuraFlow's cutting-edge AI platform"
js_old2 = "Automate workflows, predict trends, and make smarter decisions with ZETICA's cutting-edge AI platform"

if js_old1 in js:
    js = js.replace(js_old1, new_text)
    print('Replaced js_old1 in JS')
if js_old2 in js:
    js = js.replace(js_old2, new_text)
    print('Replaced js_old2 in JS')

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print('Updated subtitle in JS bundle')
