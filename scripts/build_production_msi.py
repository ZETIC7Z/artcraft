import os
import shutil
import subprocess
import msilib

ROOT = r"C:\Users\ZETICUZ\Documents\artcraft"
SRC_MSI = r"C:\Users\ZETICUZ\Downloads\artcraft-launcher-0.8.1-windows-x64.msi"
FINAL_MSI = os.path.join(ROOT, "zetica-hub-windows-x64.msi")
PAYLOAD_DIR = os.path.join(ROOT, "build_payload")
DIALOG_BMP = os.path.join(ROOT, r"branding\verification\test_installer_dialog.bmp")
BANNER_BMP = os.path.join(ROOT, r"branding\verification\test_installer_banner.bmp")
ICO_PATH = os.path.join(ROOT, r"repos\craft-launcher\assets\app-icon\artcraft-launcher.ico")
UPDATE_ICON_PS1 = os.path.join(ROOT, r"scripts\update_exe_icon.ps1")

print("1. Preparing payload directory...")
if os.path.exists(PAYLOAD_DIR):
    shutil.rmtree(PAYLOAD_DIR)
os.makedirs(PAYLOAD_DIR, exist_ok=True)

# Extract original binary using msiexec /a
print("2. Extracting original executable from source MSI...")
cmd = [
    "msiexec.exe", "/a", SRC_MSI, "/qn", f"TARGETDIR={PAYLOAD_DIR}"
]
subprocess.run(cmd, check=True)

extracted_exe = os.path.join(PAYLOAD_DIR, r"LocalApp\Programs\ArtCraft Launcher\artcraft-launcher.exe")
branded_exe = os.path.join(PAYLOAD_DIR, "zetica-hub.exe")
shutil.copyfile(extracted_exe, branded_exe)

print("3. Injecting new ZETICA squircle desktop icon into executable...")
ps_cmd = [
    "powershell", "-ExecutionPolicy", "Bypass", "-File", UPDATE_ICON_PS1,
    "-ExePath", branded_exe,
    "-IcoPath", ICO_PATH
]
res = subprocess.run(ps_cmd, capture_output=True, text=True, check=True)
print(res.stdout)

new_exe_size = os.path.getsize(branded_exe)
print(f"Branded executable ready, size = {new_exe_size} bytes")

print("4. Creating compressed cabinet cab1.cab with makecab...")
ddf_content = f"""
.OPTION EXPLICIT
.Set CabinetNameTemplate=cab1.cab
.Set DiskDirectory1={PAYLOAD_DIR}
.Set MaxDiskSize=0
.Set CompressionType=MSZIP
.Set Cabinet=ON
.Set Compress=ON
"{branded_exe}" ArtCraftLauncherExe
"""
ddf_path = os.path.join(PAYLOAD_DIR, "cab.ddf")
with open(ddf_path, "w") as f:
    f.write(ddf_content.strip())

subprocess.run(["makecab.exe", "/F", ddf_path], check=True)
cab_path = os.path.join(PAYLOAD_DIR, "cab1.cab")
print(f"Cabinet cab1.cab generated, size = {os.path.getsize(cab_path)} bytes")

print("5. Initializing new MSI database...")
if os.path.exists(FINAL_MSI):
    os.remove(FINAL_MSI)
shutil.copyfile(SRC_MSI, FINAL_MSI)

db = msilib.OpenDatabase(FINAL_MSI, msilib.MSIDBOPEN_TRANSACT)

print("6. Updating cab1.cab stream...")
v = db.OpenView("UPDATE _Streams SET Data = ? WHERE Name = 'cab1.cab'")
r = msilib.CreateRecord(1)
r.SetStream(1, cab_path)
v.Execute(r)
v.Close()

print("7. Updating Binary bitmaps...")
v = db.OpenView("UPDATE Binary SET Data = ? WHERE Name = 'WixUI_Bmp_Dialog'")
r = msilib.CreateRecord(1)
r.SetStream(1, DIALOG_BMP)
v.Execute(r)
v.Close()

v = db.OpenView("UPDATE Binary SET Data = ? WHERE Name = 'WixUI_Bmp_Banner'")
r = msilib.CreateRecord(1)
r.SetStream(1, BANNER_BMP)
v.Execute(r)
v.Close()

print("8. Updating Icon table...")
v = db.OpenView("UPDATE Icon SET Data = ? WHERE Name = 'ArtCraftLauncherIcon.exe'")
r = msilib.CreateRecord(1)
r.SetStream(1, ICO_PATH)
v.Execute(r)
v.Close()

print("9. Updating File table...")
v = db.OpenView(f"UPDATE File SET FileSize = {new_exe_size}, FileName = 'wd5qblc6.exe|zetica-hub.exe' WHERE File = 'ArtCraftLauncherExe'")
v.Execute(None)
v.Close()

print("10. Updating Properties...")
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
    v = db.OpenView(f"UPDATE Property SET Value = '{val}' WHERE Property = '{k}'")
    v.Execute(None)
    v.Close()

print("11. Updating Controls...")
v = db.OpenView("UPDATE Control SET Text = 'Zetica Hub installs, updates and opens the Zetica App Suite: ZETICA PHOTO, ZETICA VECTOR, ZETICA FILM and the rest of the open-source Zetica apps.\r\n\r\nIt installs for you only, so no administrator rights are needed. Click Next to continue.' WHERE Dialog_ = 'WelcomeDlg' AND Control = 'Description'")
v.Execute(None)
v.Close()

v = db.OpenView("UPDATE Control SET Text = 'Zetica Hub installs for you only, without administrator rights, so pick a folder you can write to. Updates install into the same folder.' WHERE Dialog_ = 'ArtCraftInstallDirDlg' AND Control = 'PerUserNote'")
v.Execute(None)
v.Close()

print("12. Updating Shortcuts...")
v = db.OpenView("UPDATE Shortcut SET Name = 'zetica|Zetica Hub', Description = 'Install and update the Zetica App Suite', Icon_ = 'ArtCraftLauncherIcon.exe', IconIndex = 0 WHERE Shortcut = 'DesktopShortcut'")
v.Execute(None)
v.Close()

v = db.OpenView("UPDATE Shortcut SET Name = 'zetica|Zetica Hub', Description = 'Install and update the Zetica App Suite', Icon_ = 'ArtCraftLauncherIcon.exe', IconIndex = 0 WHERE Shortcut = 'StartMenuShortcut'")
v.Execute(None)
v.Close()

print("13. Updating Directory...")
v = db.OpenView("UPDATE Directory SET DefaultDir = 'zetica|Zetica Hub' WHERE Directory = 'INSTALLFOLDER'")
v.Execute(None)
v.Close()

print("14. Updating Registry and RegLocator...")
v = db.OpenView("UPDATE Registry SET `Key` = 'Software\\ZETICA\\Zetica Hub' WHERE `Key` = 'Software\\Learning Machines LLC\\ArtCraft Launcher'")
v.Execute(None)
v.Close()

v = db.OpenView("UPDATE Registry SET `Key` = 'Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\zetica-hub.exe' WHERE `Key` = 'Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\artcraft-launcher.exe'")
v.Execute(None)
v.Close()

v = db.OpenView("UPDATE RegLocator SET `Key` = 'Software\\ZETICA\\Zetica Hub' WHERE `Key` = 'Software\\Learning Machines LLC\\ArtCraft Launcher'")
v.Execute(None)
v.Close()

print("15. Updating LaunchCondition and Feature...")
v = db.OpenView("UPDATE LaunchCondition SET Description = 'A newer version of Zetica Hub is already installed.'")
v.Execute(None)
v.Close()

v = db.OpenView("UPDATE Feature SET Title = 'Zetica Hub' WHERE Feature = 'Main'")
v.Execute(None)
v.Close()

print("16. Updating MsiShortcutProperty...")
v = db.OpenView("UPDATE MsiShortcutProperty SET PropVariantValue = 'xyz.zeticuz.zetica-hub' WHERE PropVariantValue = 'ai.storyteller.artcraft-launcher'")
v.Execute(None)
v.Close()

print("17. Updating SummaryInformation...")
si = db.GetSummaryInformation(20)
si.SetProperty(msilib.PID_SUBJECT, 'Zetica Hub: install and update the Zetica App Suite')
si.SetProperty(msilib.PID_AUTHOR, 'ZETICA / Sam Pangilinan')
si.SetProperty(msilib.PID_COMMENTS, 'This installer database contains the logic and data required to install Zetica Hub.')
si.Persist()

db.Commit()
print(f"Successfully built production MSI: {FINAL_MSI} ({os.path.getsize(FINAL_MSI)} bytes)")
