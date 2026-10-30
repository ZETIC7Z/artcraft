import os
import re

ui_dir = r"c:\Users\ZETICUZ\Documents\artcraft\repos\craft-launcher\crates\ui-egui"
for root, dirs, files in os.walk(ui_dir):
    for f in files:
        if f.endswith(".rs"):
            p = os.path.join(root, f)
            with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
            if "artcraft" in content.lower():
                matches = re.findall(r'.{0,40}artcraft.{0,40}', content, flags=re.IGNORECASE)
                print(f"=== {f} ===")
                for m in matches[:5]:
                    print("  ", m.strip())
