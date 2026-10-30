import os
import shutil

src_dir = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas'
dest_dir = r'c:\Users\ZETICUZ\Documents\artcraft\site'

if os.path.exists(dest_dir):
    shutil.rmtree(dest_dir)

shutil.copytree(src_dir, dest_dir)
print(f'Successfully copied site to {dest_dir}!')

# Count files copied
total_files = sum(len(files) for _, _, files in os.walk(dest_dir))
print(f'Total files in artcraft/site: {total_files}')
