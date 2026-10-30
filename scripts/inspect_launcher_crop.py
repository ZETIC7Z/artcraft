from PIL import Image

im = Image.open(r'C:\Users\ZETICUZ\.gemini\antigravity\brain\02dc5a0a-4876-48ef-96f0-6876fef960ad\.user_uploaded\media_1793333600568_cbc04aa6.png')
print('Image size:', im.size)

# Crop the top bar (y: 0 to 120, x: 0 to 600)
top_left = im.crop((0, 0, 500, 130))
top_left.save(r'c:\Users\ZETICUZ\Documents\artcraft\branding\launcher_top_left.png')

# Also check bottom status bar
bottom_bar = im.crop((0, im.size[1]-40, im.size[0], im.size[1]))
bottom_bar.save(r'c:\Users\ZETICUZ\Documents\artcraft\branding\launcher_bottom_bar.png')

print('Saved top_left and bottom_bar crops.')
