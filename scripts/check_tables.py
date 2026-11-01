import msilib

msi_path = r'C:\Users\ZETICUZ\Downloads\artcraft-launcher-0.8.1-windows-x64.msi'
db = msilib.OpenDatabase(msi_path, msilib.MSIDBOPEN_READONLY)

print("=== Shortcut Table ===")
v = db.OpenView("SELECT Shortcut, Directory_, Name, Component_, Target, Arguments, Description, Hotkey, Icon_, IconIndex, ShowCmd, WkDir FROM Shortcut")
v.Execute(None)
while True:
    r = v.Fetch()
    if not r: break
    fields = [r.GetString(i) for i in range(1, 13)]
    print(fields)
v.Close()

print("\n=== Directory Table ===")
v = db.OpenView("SELECT Directory, Directory_Parent, DefaultDir FROM Directory")
v.Execute(None)
while True:
    r = v.Fetch()
    if not r: break
    print([r.GetString(1), r.GetString(2), r.GetString(3)])
v.Close()
