with open(r'C:\Users\ZETICUZ\Documents\UNCAGE\output\output_neuraflas\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos_main = html.find('id="main"')
print('Main starts at:', pos_main)

# Find where </main> or </div> ends before </body>
pos_body_end = html.rfind('</body>')
print('Body ends at:', pos_body_end)
print('Snippet before </body>:', html[pos_body_end-500:pos_body_end])
