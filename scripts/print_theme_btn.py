with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('lucide-moon')
print(text[idx-250:idx+200])
