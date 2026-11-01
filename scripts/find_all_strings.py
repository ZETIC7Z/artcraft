import msilib

msi_path = r'c:\Users\ZETICUZ\Documents\artcraft\test_rebrand.msi'
db = msilib.OpenDatabase(msi_path, msilib.MSIDBOPEN_READONLY)

v_tables = db.OpenView("SELECT Name FROM _Tables")
v_tables.Execute(None)
tables = []
while True:
    r = v_tables.Fetch()
    if not r: break
    tables.append(r.GetString(1))
v_tables.Close()

found = []
for t in tables:
    if t.startswith('_'): continue
    try:
        v = db.OpenView(f"SELECT * FROM `{t}`")
        v.Execute(None)
        names = v.GetColumnInfo(msilib.MSICOLINFO_NAMES)
        types = v.GetColumnInfo(msilib.MSICOLINFO_TYPES)
        col_count = names.GetFieldCount()
        while True:
            r = v.Fetch()
            if not r: break
            for i in range(1, col_count + 1):
                try:
                    s = r.GetString(i)
                    for term in ['artcraft', 'learning machines']:
                        if term in s.lower():
                            found.append((t, names.GetString(i), s))
                except:
                    pass
        v.Close()
    except Exception as e:
        pass

for t, col, s in found:
    print(f"[{t}.{col}] -> {s[:80]}")
