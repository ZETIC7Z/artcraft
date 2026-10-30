import shutil

# Copy zeticuz-logo.svg to output_neuraflas/assets/images
src_zlogo = r'C:\Users\ZETICUZ\Downloads\zeticuz-logo.svg'
dest_zlogo = r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\assets\images\zeticuz-logo.svg'
shutil.copyfile(src_zlogo, dest_zlogo)
print('Copied zeticuz-logo.svg to assets/images')

with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find footer tag or copyright
pos = html.rfind('footer')
if pos != -1:
    print('Found <footer> at pos:', pos)
    print(html[pos-100:pos+1500])
else:
    # check for 2024 or copyright
    pos2 = html.rfind('2024')
    print('Found 2024 at pos:', pos2)
    print(html[pos2-200:pos2+400])
