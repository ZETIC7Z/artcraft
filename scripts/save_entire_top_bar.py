from PIL import Image

im = Image.open(r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png')
bar = im.crop((0, 0, 1024, 45))
bar.save(r'c:\Users\ZETICUZ\Documents\artcraft\branding\entire_top_bar.png')
print('Saved entire_top_bar.png')
