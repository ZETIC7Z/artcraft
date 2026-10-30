with open('site/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('<h1')
# Print 1000 characters before <h1
start = max(0, idx - 1500)
print(text[start:idx])
