import msilib

msi_path = r'C:\Users\ZETICUZ\Downloads\artcraft-launcher-0.8.1-windows-x64.msi'
db = msilib.OpenDatabase(msi_path, msilib.MSIDBOPEN_READONLY)

print("--- _Streams ---")
view = db.OpenView('SELECT Name FROM _Streams')
view.Execute(None)
while True:
    rec = view.Fetch()
    if not rec: break
    print(rec.GetString(1))
view.Close()

print("\n--- File Table ---")
view = db.OpenView('SELECT File, Component_, FileName, FileSize FROM File')
view.Execute(None)
while True:
    rec = view.Fetch()
    if not rec: break
    print([rec.GetString(i) for i in range(1, 5)])
view.Close()

print("\n--- Media Table ---")
view = db.OpenView('SELECT DiskId, LastSequence, Cabinet FROM Media')
view.Execute(None)
while True:
    rec = view.Fetch()
    if not rec: break
    print([rec.GetString(i) for i in range(1, 4)])
view.Close()
