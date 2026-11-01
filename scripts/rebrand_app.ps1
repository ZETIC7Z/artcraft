param (
    [Parameter(Mandatory=$true)] [string]$Repo,
    [Parameter(Mandatory=$true)] [string]$AppName,
    [Parameter(Mandatory=$true)] [string]$Subdir,
    [Parameter(Mandatory=$true)] [string]$Id,
    [Parameter(Mandatory=$true)] [string]$ShortName,
    [Parameter(Mandatory=$true)] [string]$Version,
    [Parameter(Mandatory=$true)] [string]$Description,
    [Parameter(Mandatory=$true)] [string]$MainPath,
    [Parameter(Mandatory=$false)] [string]$LinksPath,
    [Parameter(Mandatory=$true)] [string]$EnvVar
)

$repoDir = "repos/$Repo"
Write-Host "========================================="
Write-Host "Rebranding $Repo to $AppName (v$Version)"
Write-Host "========================================="

# 1. Update check-install-policy.ps1
$policyScript = "$repoDir/packaging/windows/check-install-policy.ps1"
if (Test-Path $policyScript) {
    $c = Get-Content $policyScript -Raw
    # line 91: allow Zetica
    $c = $c.Replace("`$directories['CraftSuiteFolder'][1] -ne 'ArtCraft'", "`$directories['CraftSuiteFolder'][1] -notin @('Zetica', 'ArtCraft')")
    # line 165+: dynamic suiteName and appName
    $oldMachine = '$machineFolder = (Join-Path $machineRoot "ArtCraft\$($policy.name)") + ''\'''
    $newMachine = @'
  $suiteName = if ($directories['CraftSuiteFolder'][1]) { $directories['CraftSuiteFolder'][1] } else { 'Zetica' }
  $appName = if ($directories['INSTALLFOLDER'][1]) { $directories['INSTALLFOLDER'][1] } else { $policy.name }
  $machineFolder = (Join-Path $machineRoot "$suiteName\$appName") + '\'
'@
    $c = $c.Replace($oldMachine, $newMachine)
    $c = $c.Replace('else { (Join-Path $env:LOCALAPPDATA "Programs\ArtCraft\$($policy.name)") + ''\'' }', 'else { (Join-Path $env:LOCALAPPDATA "Programs\$suiteName\$appName") + ''\'' }')
    $c = $c.Replace('Software\Classes\Applications', 'Software\Classes\Applications') # keep
    $c = $c.Replace("if (`$_ -notmatch '^Software\\\\(Classes\\\\|Microsoft\\\\Windows\\\\CurrentVersion\\\\App Paths\\\\)'", "if (`$_ -notmatch '^Software\\\\(ZETICA\\\\|Classes\\\\|Microsoft\\\\Windows\\\\CurrentVersion\\\\App Paths\\\\)'")
    Set-Content -Path $policyScript -Value $c -Encoding utf8
    $errs = $null; $toks = $null
    $ast = [System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $policyScript).Path, [ref]$toks, [ref]$errs)
    if ($errs) {
        throw "Syntax error in $policyScript : $($errs[0].Message)"
    }
    Write-Host "Updated check-install-policy.ps1 (Syntax Verified Valid)"
}

# 2. Update install-policy.json
$policyJson = "$repoDir/packaging/windows/install-policy.json"
if (Test-Path $policyJson) {
    $c = Get-Content $policyJson -Raw
    $c = $c.Replace('ArtCraft\\', 'Zetica\\')
    Set-Content -Path $policyJson -Value $c -Encoding utf8
    Write-Host "Updated install-policy.json"
}

# 3. Update install-policy.wxi
$policyWxi = "$repoDir/packaging/windows/install-policy.wxi"
if (Test-Path $policyWxi) {
    $c = Get-Content $policyWxi -Raw
    $c = $c.Replace("ArtCraft\$Subdir", "Zetica\$Subdir")
    $c = $c.Replace("ArtCraft\$($policy.name)", "Zetica\$Subdir")
    $c = $c.Replace("ArtCraft\$Id", "Zetica\$Subdir")
    # Also generic ArtCraft\ in paths
    $c = $c.Replace(']\ArtCraft\', ']\Zetica\')
    $c = $c.Replace('Programs\ArtCraft\', 'Programs\Zetica\')
    $c = $c.Replace('ArtCraft folder under Programs', 'Zetica folder under Programs')
    Set-Content -Path $policyWxi -Value $c -Encoding utf8
    Write-Host "Updated install-policy.wxi"
}

# 4. Update .wxs file
$wxsFile = "$repoDir/packaging/windows/$Id.wxs"
if (Test-Path $wxsFile) {
    $c = Get-Content $wxsFile -Raw
    # Package Name and Manufacturer
    $c = [regex]::Replace($c, '<Package Name="[^"]+" Manufacturer="[^"]+"', "<Package Name=`"$AppName`" Manufacturer=`"ZETICA / Sam Pangilinan`"")
    $c = [regex]::Replace($c, '<SummaryInformation Description="[^"]+" Manufacturer="[^"]+"', "<SummaryInformation Description=`"$Description`" Manufacturer=`"ZETICA / Sam Pangilinan`"")
    $c = [regex]::Replace($c, 'DowngradeErrorMessage="A newer version of [^"]+ is already installed\."', "DowngradeErrorMessage=`"A newer version of $AppName is already installed.`"")
    
    # URLs
    $c = [regex]::Replace($c, '<Property Id="ARPURLINFOABOUT" Value="[^"]+" />', '<Property Id="ARPURLINFOABOUT" Value="https://www.zeticuz.xyz/" />')
    $c = [regex]::Replace($c, '<Property Id="ARPURLUPDATEINFO" Value="[^"]+" />', "<Property Id=`"ARPURLUPDATEINFO`" Value=`"https://github.com/ZETIC7Z/$Repo/releases`" />")
    $c = [regex]::Replace($c, '<Property Id="ARPHELPLINK" Value="[^"]+" />', '<Property Id="ARPHELPLINK" Value="https://www.zeticuz.xyz/" />')

    # Directory Structure
    $c = $c.Replace('<Directory Id="CraftSuiteFolder" Name="ArtCraft">', '<Directory Id="CraftSuiteFolder" Name="Zetica">')
    $c = [regex]::Replace($c, '<Directory Id="INSTALLFOLDER" Name="[^"]+" />', "<Directory Id=`"INSTALLFOLDER`" Name=`"$Subdir`" />")

    # Add DesktopFolder if missing
    if ($c -notmatch '<StandardDirectory Id="DesktopFolder"') {
        $c = $c.Replace('<StandardDirectory Id="ProgramMenuFolder" />', "<StandardDirectory Id=`"ProgramMenuFolder`" />`n    <StandardDirectory Id=`"DesktopFolder`" />")
    }

    # Feature title
    $c = [regex]::Replace($c, '<Feature Id="Main" Title="[^"]+"', "<Feature Id=`"Main`" Title=`"$AppName`"")

    # ExitDialog properties
    $c = [regex]::Replace($c, '<Property Id="WIXUI_EXITDIALOGOPTIONALTEXT" Value="[^"]+" />', "<Property Id=`"WIXUI_EXITDIALOGOPTIONALTEXT`" Value=`"$AppName has been installed. You can start it at any time from the Start menu or desktop.`" />")
    $c = [regex]::Replace($c, '<Property Id="WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT" Value="[^"]+" />', "<Property Id=`"WIXUI_EXITDIALOGOPTIONALCHECKBOXTEXT`" Value=`"Launch $AppName`" />")

    # Shortcuts in main component
    $c = [regex]::Replace($c, '<Shortcut Id="StartMenuShortcut" Directory="ProgramMenuFolder" Name="[^"]+" Description="[^"]+" WorkingDirectory="INSTALLFOLDER" Advertise="yes"[^>]*/>', "<Shortcut Id=`"StartMenuShortcut`" Directory=`"ProgramMenuFolder`" Name=`"$AppName`" Description=`"$Description`" WorkingDirectory=`"INSTALLFOLDER`" Advertise=`"no`" />`n          <Shortcut Id=`"DesktopShortcut`" Directory=`"DesktopFolder`" Name=`"$AppName`" Description=`"$Description`" WorkingDirectory=`"INSTALLFOLDER`" Advertise=`"no`" />")
    
    # Registry paths: add zetica binary & Software\ZETICA\<Subdir>
    $oldReg = "<RegistryValue Root=`"HKMU`" Key=`"Software\Microsoft\Windows\CurrentVersion\App Paths\$Id.exe`""
    $newReg = "<RegistryValue Root=`"HKMU`" Key=`"Software\Microsoft\Windows\CurrentVersion\App Paths\$Id.exe`""
    if ($c -notmatch "zetica-$ShortName\.exe") {
        $c = $c.Replace($oldReg, "<RegistryValue Root=`"HKMU`" Key=`"Software\Microsoft\Windows\CurrentVersion\App Paths\zetica-$ShortName.exe`" Value=`"[#$($Id)Exe]`" Type=`"string`" />`n        $oldReg")
    }
    if ($c -notmatch "Software\\ZETICA\\$Subdir") {
        $installDirReg = "<RegistryValue Root=`"HKMU`" Key=`"Software\$Id`" Name=`"InstallDir`" Value=`"[INSTALLFOLDER]`" Type=`"string`" />"
        if ($c -contains $installDirReg) {
            $c = $c.Replace($installDirReg, "$installDirReg`n        <RegistryValue Root=`"HKMU`" Key=`"Software\ZETICA\$Subdir`" Name=`"InstallDir`" Value=`"[INSTALLFOLDER]`" Type=`"string`" />")
        } else {
            # try after lightcraft InstallFolder
            $c = [regex]::Replace($c, "(<RegistryValue Root=`"HKMU`" Key=`"Software\\[^`"]+`" Name=`"Install(?:Folder|Dir)`" Value=`"\[INSTALLFOLDER\]`" Type=`"string`" />)", "`$1`n        <RegistryValue Root=`"HKMU`" Key=`"Software\ZETICA\$Subdir`" Name=`"InstallDir`" Value=`"[INSTALLFOLDER]`" Type=`"string`" />")
        }
    }

    Set-Content -Path $wxsFile -Value $c -Encoding utf8
    Write-Host "Updated $Id.wxs"
}

# 5. Update main.rs
$fullMainPath = "$repoDir/$MainPath"
if (Test-Path $fullMainPath) {
    $c = Get-Content $fullMainPath -Raw
    # with_title
    $c = [regex]::Replace($c, '\.with_title\("[^"]+"\)', ".with_title(`"$AppName`")")
    # run_native
    $c = [regex]::Replace($c, 'eframe::run_native\(\s*"[^"]+"', "eframe::run_native(`"$AppName`"")
    Set-Content -Path $fullMainPath -Value $c -Encoding utf8
    Write-Host "Updated $MainPath"
}

# 6. Update links.rs if specified
if ($LinksPath) {
    $fullLinksPath = "$repoDir/$LinksPath"
    if (Test-Path $fullLinksPath) {
        $c = Get-Content $fullLinksPath -Raw
        $c = [regex]::Replace($c, 'pub const WEBSITE:\s*&str\s*=\s*"[^"]+";', 'pub const WEBSITE: &str = "https://www.zeticuz.xyz";')
        $c = [regex]::Replace($c, 'pub const APP_PAGE:\s*&str\s*=\s*"[^"]+";', 'pub const APP_PAGE: &str = "https://www.zeticuz.xyz";')
        $c = [regex]::Replace($c, 'pub const GITHUB:\s*&str\s*=\s*"https://github\.com/[^"]+";', "pub const GITHUB: &str = `"https://github.com/ZETIC7Z/$Repo`";")
        $c = [regex]::Replace($c, 'pub const ISSUES:\s*&str\s*=\s*"https://github\.com/[^"]+";', "pub const ISSUES: &str = `"https://github.com/ZETIC7Z/$Repo/issues`";")
        $c = [regex]::Replace($c, 'pub const FEEDBACK:\s*&str\s*=\s*"https://github\.com/[^"]+";', "pub const FEEDBACK: &str = `"https://github.com/ZETIC7Z/$Repo/issues/new`";")
        Set-Content -Path $fullLinksPath -Value $c -Encoding utf8
        Write-Host "Updated $LinksPath"
    }
}

# 7. Create .github/workflows/release-zetica.yml
$workflowDir = "$repoDir/.github/workflows"
if (-not (Test-Path $workflowDir)) { New-Item -ItemType Directory -Path $workflowDir -Force | Out-Null }
$releaseYml = @"
name: Build & Release $AppName

on:
  push:
    tags:
      - 'v*'
  workflow_dispatch:
    inputs:
      tag_name:
        description: 'Release tag (e.g. v$Version)'
        required: true
        default: 'v$Version'

permissions:
  contents: write

jobs:
  build-windows:
    name: Build Windows x64 (MSI & Portable)
    runs-on: windows-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Install Rust Toolchain
        uses: dtolnay/rust-toolchain@stable
        with:
          targets: x86_64-pc-windows-msvc

      - name: Rust Cache
        uses: Swatinem/rust-cache@v2

      - name: Install WiX Toolset v5
        shell: pwsh
        run: |
          dotnet tool install --global wix --version 5.0.2
          wix extension add -g WixToolset.UI.wixext/5.0.2

      - name: Build & Package Windows Artifacts
        shell: pwsh
        run: |
          `$ver = if ("`${{ github.event.inputs.tag_name }}") { "`${{ github.event.inputs.tag_name }}".TrimStart('v') } else { "$Version" }
          `$env:$EnvVar = `$ver
          pwsh packaging/windows/package.ps1 -Arch x64

      - name: Prepare Release Assets
        shell: pwsh
        run: |
          `$ver = if ("`${{ github.event.inputs.tag_name }}") { "`${{ github.event.inputs.tag_name }}".TrimStart('v') } else { "$Version" }
          `$dist = "dist/release"
          mkdir -Force release_assets

          # Copy files from dist/release
          Copy-Item `$dist/*-windows-x64.msi release_assets/ -Force
          Copy-Item `$dist/*-windows-x64-portable.zip release_assets/ -Force

          # Copy canonical zetica naming
          Copy-Item `$dist/*-windows-x64.msi "release_assets/zetica-$ShortName-`$ver-windows-x64.msi" -Force
          Copy-Item `$dist/*-windows-x64-portable.zip "release_assets/zetica-$ShortName-`$ver-windows-x64-portable.zip" -Force

          # Generate SHA256SUMS.txt
          Get-ChildItem release_assets/* -File | ForEach-Object {
            `$h = (Get-FileHash `$_.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            "`$h  `$(`$_.Name)"
          } | Set-Content release_assets/SHA256SUMS.txt -Encoding ascii

      - name: Upload Windows Artifacts
        uses: actions/upload-artifact@v4
        with:
          name: zetica-$ShortName-windows-x64
          path: release_assets/*

  create-release:
    name: Create GitHub Release
    needs: [build-windows]
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Download Windows Artifacts
        uses: actions/download-artifact@v4
        with:
          name: zetica-$ShortName-windows-x64
          path: release_assets

      - name: Publish Release to GitHub
        uses: softprops/action-gh-release@v2
        with:
          tag_name: `${{ github.event.inputs.tag_name || github.ref_name }}
          name: $AppName `${{ github.event.inputs.tag_name || github.ref_name }}
          body: |
            ## $AppName Release `${{ github.event.inputs.tag_name || github.ref_name }}

            Official $Description for the **Zetica Creative Suite**. Rebuilt from scratch in pure Rust.

            ### Included Packages:
            - `zetica-$ShortName-`${{ github.event.inputs.tag_name || github.ref_name }}-windows-x64.msi`: Native Windows Installer
            - `zetica-$ShortName-`${{ github.event.inputs.tag_name || github.ref_name }}-windows-x64-portable.zip`: Portable standalone zip
            - `$Id-`${{ github.event.inputs.tag_name || github.ref_name }}-windows-x64.msi`: Upstream compatible package

            Developed by **Sam Pangilinan** ([zeticuz.xyz](https://www.zeticuz.xyz/)).
          files: release_assets/*
          draft: false
          prerelease: false
"@
Set-Content -Path "$workflowDir/release-zetica.yml" -Value $releaseYml -Encoding utf8
Write-Host "Created release-zetica.yml"

# 8. Create .github/workflows/sync-upstream.yml
$syncYml = @"
name: Sync Upstream

on:
  schedule:
    # Run daily at 00:00 UTC
    - cron: '0 0 * * *'
  workflow_dispatch:

jobs:
  sync:
    name: Sync with upstream storytold/$Repo
    runs-on: ubuntu-latest
    permissions:
      contents: write

    steps:
      - name: Checkout Fork
        uses: actions/checkout@v4
        with:
          token: `${{ secrets.GITHUB_TOKEN }}
          fetch-depth: 0

      - name: Configure Git
        run: |
          git config user.name "ZeticuzBot"
          git config user.email "bot@zeticuz.xyz"

      - name: Add Upstream Remote
        run: |
          git remote add upstream https://github.com/storytold/$Repo.git || true
          git fetch upstream main

      - name: Merge Upstream Changes
        run: |
          git checkout main
          git merge upstream/main -m "chore(sync): automated merge from upstream storytold/$Repo [skip ci]" || git merge --abort
          git push origin main || echo "No changes or push failed"
"@
Set-Content -Path "$workflowDir/sync-upstream.yml" -Value $syncYml -Encoding utf8
Write-Host "Created sync-upstream.yml"
