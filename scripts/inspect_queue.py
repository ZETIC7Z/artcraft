import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('src_ref/scroll-ruler.tsx', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('queue')
if idx == -1:
    idx = text.find('queued')
print('Found at', idx)
print(text[idx-50:idx+1500])
