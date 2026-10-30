import os
import shutil

src_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com"
dst_dir = r"c:\Users\ZETICUZ\Documents\artcraft\site"

# Clean destination or copy over
if os.path.exists(dst_dir):
    shutil.rmtree(dst_dir)

print(f"Copying {src_dir} to {dst_dir} ...")
shutil.copytree(src_dir, dst_dir)
print(f"Copied {len(os.listdir(dst_dir))} entries to {dst_dir}!")
