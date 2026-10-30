import os
import re

core_dir = r"c:\Users\ZETICUZ\Documents\artcraft\repos\craft-launcher"
for root, dirs, files in os.walk(core_dir):
    for f in files:
        if f.endswith(".rs"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
            if "effectcraft" in content.lower() and "storytold" in content.lower():
                matches = re.findall(r'.{0,50}storytold.{0,50}', content)
                print(f"=== {os.path.relpath(p, core_dir)} ===")
                for m in matches[:5]:
                    print("  ", m.strip())
