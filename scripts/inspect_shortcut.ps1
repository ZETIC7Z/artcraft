$sh = New-Object -ComObject WScript.Shell
$desktopLnk = Join-Path $env:USERPROFILE 'Desktop\Zetica Hub.lnk'
$sc = $sh.CreateShortcut($desktopLnk)
Write-Host "Target: $($sc.TargetPath)"
Write-Host "IconLocation: $($sc.IconLocation)"
Write-Host "Description: $($sc.Description)"
Write-Host "WorkingDirectory: $($sc.WorkingDirectory)"
