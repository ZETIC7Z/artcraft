import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com\assets\js\29wilaqtb26u5.js'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

pos = 81125
start = max(0, pos - 2500)
snippet = text[start:pos]

# find definitions in snippet
import re
defs = re.findall(r'([A-Za-z0-9_$]+)=', snippet)
print("Defs before pos:", [d for d in defs if '_' in d or len(d) <= 2])

# let's look for "_="
u_pos = snippet.rfind('_=')
if u_pos != -1:
    print("Found _= at:", snippet[u_pos-50:u_pos+50])
else:
    print("_= not found in snippet")
