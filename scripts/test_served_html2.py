import urllib.request

url = 'http://localhost:8791/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = resp.read().decode('utf-8')
    print('Length of served index.html:', len(data))
    print('zeticuz-dev-footer in served index.html:', 'zeticuz-dev-footer' in data)
