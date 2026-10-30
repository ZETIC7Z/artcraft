from PIL import Image

im = Image.open(r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png')
crop = im.crop((0, 40, 500, 110))
crop.save(r'c:\Users\ZETICUZ\Documents\artcraft\branding\banner_crop.png')
print('Saved banner_crop.png')
