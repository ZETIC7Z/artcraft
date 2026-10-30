import glob

for f in glob.glob('site/**/*.html', recursive=True):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    if '0.8.1' in c:
        print("Contains 0.8.1:", f)
