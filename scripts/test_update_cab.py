import msilib
import os

msi_path = r'c:\Users\ZETICUZ\Documents\artcraft\test_rebrand.msi'
cab_path = r'C:\Users\ZETICUZ\Documents\artcraft\extracted_payload\test_cab.cab'

db = msilib.OpenDatabase(msi_path, msilib.MSIDBOPEN_TRANSACT)
v = db.OpenView("UPDATE _Streams SET Data = ? WHERE Name = 'cab1.cab'")
r = msilib.CreateRecord(1)
r.SetStream(1, cab_path)
v.Execute(r)
v.Close()

# Also update the File table with new file size
new_size = os.path.getsize(r"C:\Users\ZETICUZ\Documents\artcraft\extracted_payload\test_icon_exe.exe")
print(f"Updating File table with FileSize = {new_size} and FileName = wd5qblc6.exe|zetica-hub.exe...")
v = db.OpenView(f"UPDATE File SET FileSize = {new_size}, FileName = 'wd5qblc6.exe|zetica-hub.exe' WHERE File = 'ArtCraftLauncherExe'")
v.Execute(None)
v.Close()

db.Commit()
print("Successfully updated cab1.cab and File table in test_rebrand.msi!")
