with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('zetica-icon.svg')
if idx != -1:
    print(text[idx - 200:idx + 600])
