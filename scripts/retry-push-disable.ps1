$ErrorActionPreference = 'Continue'
$root = 'c:\Users\ZETICUZ\Documents\artcraft\repos'
function Retry($label, [scriptblock]$sb, $max = 40) {
  for ($i = 1; $i -le $max; $i++) {
    $out = & $sb 2>&1 | Out-String
    if ($LASTEXITCODE -eq 0) { Write-Host "OK  $label"; return $out }
    Start-Sleep 15
  }
  Write-Host "FAIL $label"; return $null
}
foreach ($r in 'lightcraft', 'pdfcraft') {
  Retry "push $r" { git -C "$root\$r" push origin main } | Out-Null
}
$repos = 'craft-launcher','deckcraft','effectcraft','soundcraft','gridcraft','cadcraft','pdfcraft','designcraft','filmcraft','photocraft','vectorcraft','figcraft','lightcraft','wordcraft'
foreach ($r in $repos) {
  $json = Retry "list $r" { gh workflow list --repo "ZETIC7Z/$r" --json id,name,state }
  if (-not $json) { continue }
  foreach ($w in ($json | ConvertFrom-Json)) {
    if ($w.name -like 'Build & Release*' -or $w.name -like 'Sync*') { Write-Host "$r KEEP $($w.name)"; continue }
    if ($w.state -eq 'active') {
      Retry "disable $r/$($w.name)" { gh workflow disable $w.id --repo "ZETIC7Z/$r" } | Out-Null
    }
  }
}
Write-Host "DONE"
