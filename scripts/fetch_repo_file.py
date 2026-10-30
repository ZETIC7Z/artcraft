import sys
import subprocess
import json
import base64
import os

path_in_repo = sys.argv[1]
out_path = sys.argv[2]

cmd = ["gh", "api", f"repos/storytold/artcraft-services/contents/{path_in_repo}"]
result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
if result.returncode != 0:
    print(f"Error: {result.stderr}")
    sys.exit(1)

data = json.loads(result.stdout)
content = base64.b64decode(data['content']).decode('utf-8')

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully saved {path_in_repo} to {out_path}")
