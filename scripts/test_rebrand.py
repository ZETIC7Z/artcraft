import shutil
import msilib
import os

src_msi = r'C:\Users\ZETICUZ\Downloads\artcraft-launcher-0.8.1-windows-x64.msi'
dst_msi = r'C:\Users\ZETICUZ\Documents\artcraft\test_rebrand.msi'
dialog_bmp = r'C:\Users\ZETICUZ\Documents\artcraft\branding\verification\test_installer_dialog.bmp'
banner_bmp = r'C:\Users\ZETICUZ\Documents\artcraft\branding\verification\test_installer_banner.bmp'
icon_ico = r'C:\Users\ZETICUZ\Documents\artcraft\repos\craft-launcher\assets\app-icon\artcraft-launcher.ico'

if os.path.exists(dst_msi):
    os.remove(dst_msi)

shutil.copyfile(src_msi, dst_msi)

db = msilib.OpenDatabase(dst_msi, msilib.MSIDBOPEN_TRANSACT)

# 1. Update Binary table streams
print("Updating WixUI_Bmp_Dialog...")
v = db.OpenView("UPDATE Binary SET Data = ? WHERE Name = 'WixUI_Bmp_Dialog'")
r = msilib.CreateRecord(1)
r.SetStream(1, dialog_bmp)
v.Execute(r)
v.Close()

print("Updating WixUI_Bmp_Banner...")
v = db.OpenView("UPDATE Binary SET Data = ? WHERE Name = 'WixUI_Bmp_Banner'")
r = msilib.CreateRecord(1)
r.SetStream(1, banner_bmp)
v.Execute(r)
v.Close()

# 2. Update Icon table stream
print("Updating ArtCraftLauncherIcon.exe in Icon table...")
v = db.OpenView("UPDATE Icon SET Data = ? WHERE Name = 'ArtCraftLauncherIcon.exe'")
r = msilib.CreateRecord(1)
r.SetStream(1, icon_ico)
v.Execute(r)
v.Close()

# 3. Update Properties
props = {
    'ProductName': 'Zetica Hub',
    'Manufacturer': 'ZETICA / Sam Pangilinan',
    'ProductVersion': '0.10.0',
    'ArtCraftLauncherVersion': '0.10.0',
    'ARPURLINFOABOUT': 'https://www.zeticuz.xyz/',
    'ARPURLUPDATEINFO': 'https://github.com/ZETIC7Z/craft-launcher/releases',
    'ARPHELPLINK': 'https://www.zeticuz.xyz/',
    'WIXUI_EXITDIALOGOPTIONALTEXT': 'Zetica Hub 0.10.0 is installed. Start it any time from the Start menu or desktop to install and update the Zetica App Suite.',
    'WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT': 'Launch Zetica Hub',
}

for k, val in props.items():
    print(f"Updating Property {k} -> {val}...")
    v = db.OpenView(f"UPDATE Property SET Value = '{val}' WHERE Property = '{k}'")
    v.Execute(None)
    v.Close()

# 4. Update Dialog Controls
print("Updating WelcomeDlg text...")
v = db.OpenView("UPDATE Control SET Text = 'Zetica Hub installs, updates and opens the Zetica App Suite: ZETICA PHOTO, ZETICA VECTOR, ZETICA FILM and the rest of the open-source Zetica apps.\r\n\r\nIt installs for you only, so no administrator rights are needed. Click Next to continue.' WHERE Dialog_ = 'WelcomeDlg' AND Control = 'Description'")
v.Execute(None)
v.Close()

v = db.OpenView("UPDATE Control SET Text = 'Zetica Hub installs for you only, without administrator rights, so pick a folder you can write to. Updates install into the same folder.' WHERE Dialog_ = 'ArtCraftInstallDirDlg' AND Control = 'PerUserNote'")
v.Execute(None)
v.Close()

# 5. Update Shortcuts
print("Updating Shortcuts...")
v = db.OpenView("UPDATE Shortcut SET Name = 'zetica|Zetica Hub', Description = 'Install and update the Zetica App Suite', Icon_ = 'ArtCraftLauncherIcon.exe', IconIndex = 0 WHERE Shortcut = 'DesktopShortcut'")
v.Execute(None)
v.Close()

v = db.OpenView("UPDATE Shortcut SET Name = 'zetica|Zetica Hub', Description = 'Install and update the Zetica App Suite', Icon_ = 'ArtCraftLauncherIcon.exe', IconIndex = 0 WHERE Shortcut = 'StartMenuShortcut'")
v.Execute(None)
v.Close()

# 6. Update Directory
print("Updating Directory INSTALLFOLDER...")
v = db.OpenView("UPDATE Directory SET DefaultDir = 'zetica|Zetica Hub' WHERE Directory = 'INSTALLFOLDER'")
v.Execute(None)
v.Close()

db.Commit()
print("Success! Committed changes to test_rebrand.msi")
