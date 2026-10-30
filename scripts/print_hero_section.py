with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('<section id="hero"')
idx2 = text.find('</section>', idx1)
print("Hero length:", idx2 - idx1)
print(text[idx1:idx1+1800])
