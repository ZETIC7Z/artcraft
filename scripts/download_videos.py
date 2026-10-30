import os
import urllib.request

site_dir = r"C:\Users\ZETICUZ\Documents\UNCAGE\output\getartcraft.com"
dest_dir = os.path.join(site_dir, "videos", "features")
os.makedirs(dest_dir, exist_ok=True)

videos = [
    "Background.webm",
    "Character-Pose.webm",
    "Editor.webm",
    "Make_3D.webm",
    "Mixed.webm",
    "Panel.webm",
    "WorldLabs_Demo_2.webm"
]

for v in videos:
    target_path = os.path.join(dest_dir, v)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 1000:
        print(f"Already exists: {v}")
        continue
    url = f"https://getartcraft.com/videos/features/{v}"
    print(f"Downloading {url} ...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as resp, open(target_path, "wb") as out:
            out.write(resp.read())
        print(f"Downloaded {v} ({os.path.getsize(target_path)} bytes)")
    except Exception as e:
        print(f"Failed to download {v}: {e}")

print("Video download complete!")
