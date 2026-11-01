$ddfContent = @"
.OPTION EXPLICIT
.Set CabinetNameTemplate=test_cab.cab
.Set DiskDirectory1=C:\Users\ZETICUZ\Documents\artcraft\extracted_payload
.Set MaxDiskSize=0
.Set CompressionType=MSZIP
.Set Cabinet=ON
.Set Compress=ON
"C:\Users\ZETICUZ\Documents\artcraft\extracted_payload\test_icon_exe.exe" ArtCraftLauncherExe
"@

$ddfPath = "C:\Users\ZETICUZ\Documents\artcraft\extracted_payload\test.ddf"
[System.IO.File]::WriteAllText($ddfPath, $ddfContent)

$res = Start-Process -FilePath "makecab.exe" -ArgumentList @("/F", $ddfPath) -Wait -PassThru
Write-Host "Makecab ExitCode: $($res.ExitCode)"
if (Test-Path "C:\Users\ZETICUZ\Documents\artcraft\extracted_payload\test_cab.cab") {
    $item = Get-Item "C:\Users\ZETICUZ\Documents\artcraft\extracted_payload\test_cab.cab"
    Write-Host "Created test_cab.cab with size $($item.Length)"
}
