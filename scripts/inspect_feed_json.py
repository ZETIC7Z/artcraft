import json

path = r"C:\Users\ZETICUZ\AppData\Local\ArtCraft Launcher\feed.json"
try:
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print("Success loading feed.json")
    if "release_info" in data and "apps" in data["release_info"]:
        print("Apps in feed.json:", list(data["release_info"]["apps"].keys()))
except Exception as e:
    print("Error:", e)
