param(
    [string]$ExePath = "C:\Users\ZETICUZ\Documents\artcraft\extracted_payload\LocalApp\Programs\ArtCraft Launcher\artcraft-launcher.exe",
    [string]$IcoPath = "C:\Users\ZETICUZ\Documents\artcraft\repos\craft-launcher\assets\app-icon\artcraft-launcher.ico"
)

$code = @"
using System;
using System.IO;
using System.Runtime.InteropServices;

public class ExeIconUpdater {
    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    private static extern IntPtr BeginUpdateResource(string pFileName, bool bDeleteExistingResources);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool UpdateResource(IntPtr hUpdate, IntPtr lpType, IntPtr lpName, ushort wLanguage, byte[] lpData, uint cbData);

    [DllImport("kernel32.dll", SetLastError = true)]
    private static extern bool EndUpdateResource(IntPtr hUpdate, bool fDiscard);

    private static readonly IntPtr RT_ICON = (IntPtr)3;
    private static readonly IntPtr RT_GROUP_ICON = (IntPtr)14;

    public static bool InjectIcon(string exePath, string icoPath) {
        byte[] icoBytes = File.ReadAllBytes(icoPath);
        if (icoBytes.Length < 6) return false;

        ushort idReserved = BitConverter.ToUInt16(icoBytes, 0);
        ushort idType = BitConverter.ToUInt16(icoBytes, 2);
        ushort idCount = BitConverter.ToUInt16(icoBytes, 4);

        if (idType != 1 || idCount == 0) return false;

        IntPtr hUpdate = BeginUpdateResource(exePath, false);
        if (hUpdate == IntPtr.Zero) {
            Console.WriteLine("BeginUpdateResource failed: " + Marshal.GetLastWin32Error());
            return false;
        }

        try {
            // Build GRPICONDIR: 6 bytes header + 14 bytes per entry
            int grpSize = 6 + idCount * 14;
            byte[] grpData = new byte[grpSize];
            Array.Copy(icoBytes, 0, grpData, 0, 6);

            for (int i = 0; i < idCount; i++) {
                int entryOffset = 6 + i * 16;
                byte bWidth = icoBytes[entryOffset];
                byte bHeight = icoBytes[entryOffset + 1];
                byte bColorCount = icoBytes[entryOffset + 2];
                byte bReserved = icoBytes[entryOffset + 3];
                ushort wPlanes = BitConverter.ToUInt16(icoBytes, entryOffset + 4);
                ushort wBitCount = BitConverter.ToUInt16(icoBytes, entryOffset + 6);
                uint dwBytesInRes = BitConverter.ToUInt32(icoBytes, entryOffset + 8);
                uint dwImageOffset = BitConverter.ToUInt32(icoBytes, entryOffset + 12);

                ushort nId = (ushort)(i + 1);

                // Write GRPICONDIRENTRY
                int grpEntryOffset = 6 + i * 14;
                grpData[grpEntryOffset] = bWidth;
                grpData[grpEntryOffset + 1] = bHeight;
                grpData[grpEntryOffset + 2] = bColorCount;
                grpData[grpEntryOffset + 3] = bReserved;
                Array.Copy(BitConverter.GetBytes(wPlanes), 0, grpData, grpEntryOffset + 4, 2);
                Array.Copy(BitConverter.GetBytes(wBitCount), 0, grpData, grpEntryOffset + 6, 2);
                Array.Copy(BitConverter.GetBytes(dwBytesInRes), 0, grpData, grpEntryOffset + 8, 4);
                Array.Copy(BitConverter.GetBytes(nId), 0, grpData, grpEntryOffset + 12, 2);

                // Extract image bytes
                byte[] imgBytes = new byte[dwBytesInRes];
                Array.Copy(icoBytes, (int)dwImageOffset, imgBytes, 0, (int)dwBytesInRes);

                // Update RT_ICON
                if (!UpdateResource(hUpdate, RT_ICON, (IntPtr)nId, 0, imgBytes, (uint)dwBytesInRes)) {
                    Console.WriteLine("UpdateResource RT_ICON " + nId + " failed: " + Marshal.GetLastWin32Error());
                    EndUpdateResource(hUpdate, true);
                    return false;
                }
            }

            // Update RT_GROUP_ICON with ID = 1 (main app icon)
            // WiX / Windows PE uses group icon 1 or MAINICON
            if (!UpdateResource(hUpdate, RT_GROUP_ICON, (IntPtr)1, 0, grpData, (uint)grpSize)) {
                // Try ID 32512 (IDI_APPLICATION) as well just in case
                Console.WriteLine("UpdateResource RT_GROUP_ICON failed: " + Marshal.GetLastWin32Error());
                EndUpdateResource(hUpdate, true);
                return false;
            }

            if (!EndUpdateResource(hUpdate, false)) {
                Console.WriteLine("EndUpdateResource failed: " + Marshal.GetLastWin32Error());
                return false;
            }

            return true;
        } catch (Exception ex) {
            Console.WriteLine("Exception: " + ex.Message);
            EndUpdateResource(hUpdate, true);
            return false;
        }
    }
}
"@

Add-Type -TypeDefinition $code
$res = [ExeIconUpdater]::InjectIcon($ExePath, $IcoPath)
Write-Host "InjectIcon result: $res"
