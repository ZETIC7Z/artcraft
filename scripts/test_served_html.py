import urllib.request

url = 'http://localhost:8791/index.html'
req = urllib.request.Request(url, headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
with urllib.request.urlopen(req) as resp:
    data = resp.read().decode('utf-8')
    print('Length of served index.html:', len(data))
    print('zeticuz-dev-footer in served index.html:', 'zeticuz-dev-footer' in data)
