import os
import re

core_dir = r"c:\Users\ZETICUZ\Documents\artcraft\repos\craft-launcher"
for root, dirs, files in os.walk(core_dir):
    for f in files:
        if f.endswith((".rs", ".toml", ".json")):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
            urls = re.findall(r'https?://[^\s"\'<>]+', content)
            for u in urls:
                if any(k in u for k in ["getartcraft", "storytold", "api", "release", "download", "json", "raw.github"]):
                    print(f"{os.path.relpath(p, core_dir)}: {u}")
