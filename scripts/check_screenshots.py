import os
import glob

files = glob.glob('branding/verification/*.png')
for f in files:
    print(f, os.path.getsize(f), "bytes", os.path.getmtime(f))
