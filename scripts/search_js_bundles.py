import os

js_dir = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\assets\js'
terms = [
    'Supercharge Your Business',
    'Get Started for Free',
    'Get This Template',
    'NeuraFlas',
    'NeuraFlow',
    'ihRdyAqkJP0yCygC1qHb8txaCo'
]

for f in os.listdir(js_dir):
    if f.endswith('.js'):
        p = os.path.join(js_dir, f)
        with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
            c = fp.read()
            for t in terms:
                if t in c:
                    print(f'{f}: contains "{t}" (count={c.count(t)})')
