param(
  [string]$OutputFile = "c:\Users\ZETICUZ\Documents\artcraft\site\api\v1\release_info.json"
)

$ErrorActionPreference = 'Continue'

$apps = @(
  @{ id = "photocraft"; repo = "ZETIC7Z/photocraft" },
  @{ id = "vectorcraft"; repo = "ZETIC7Z/vectorcraft" },
  @{ id = "filmcraft"; repo = "ZETIC7Z/filmcraft" },
  @{ id = "lightcraft"; repo = "ZETIC7Z/lightcraft" },
  @{ id = "pdfcraft"; repo = "ZETIC7Z/pdfcraft" },
  @{ id = "effectcraft"; repo = "ZETIC7Z/effectcraft" },
  @{ id = "designcraft"; repo = "ZETIC7Z/designcraft" },
  @{ id = "figcraft"; repo = "ZETIC7Z/figcraft" },
  @{ id = "wordcraft"; repo = "ZETIC7Z/wordcraft" },
  @{ id = "soundcraft"; repo = "ZETIC7Z/soundcraft" },
  @{ id = "deckcraft"; repo = "ZETIC7Z/deckcraft" },
  @{ id = "cadcraft"; repo = "ZETIC7Z/cadcraft" },
  @{ id = "gridcraft"; repo = "ZETIC7Z/gridcraft" },
  @{ id = "craft-launcher"; repo = "ZETIC7Z/craft-launcher" }
)

$nowIso = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$appsMap = [ordered]@{}

foreach ($app in $apps) {
  Write-Host "Querying release for $($app.id) ($($app.repo))..."
  $appObj = [ordered]@{
    repo = $app.repo
    latest_release = $null
    app_last_fetched = $nowIso
  }

  try {
    $raw = gh api "repos/$($app.repo)/releases/latest" 2>$null
    if ($raw) {
      $rel = $raw | ConvertFrom-Json
      $assets = @()
      foreach ($a in $rel.assets) {
        $assets += [ordered]@{
          name = $a.name
          size_bytes = [uint64]$a.size
          download_url = $a.browser_download_url
          sha256 = $null
        }
      }

      $appObj.latest_release = [ordered]@{
        tag = $rel.tag_name
        name = $rel.name
        published_at = $rel.published_at
        html_url = $rel.html_url
        prerelease = [bool]$rel.prerelease
        notes_markdown = $rel.body
        assets = $assets
      }
      Write-Host "  -> Found tag $($rel.tag_name) with $($assets.Count) assets"
    } else {
      Write-Host "  -> No published release found yet."
    }
  } catch {
    Write-Host "  -> Error querying release: $_"
  }

  $appsMap[$app.id] = $appObj
}

$feed = [ordered]@{
  release_info = [ordered]@{
    apps = $appsMap
    last_fetched = $nowIso
  }
  app_renames = @()
  repo_renames = @()
  important_notices = [ordered]@{
    announcements = @()
    alerts = @()
  }
}

$parent = Split-Path -Parent $OutputFile
if (-not (Test-Path $parent)) {
  New-Item -ItemType Directory -Path $parent -Force
}

$json = $feed | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($OutputFile, $json, [System.Text.Encoding]::UTF8)

# Also create the extensionless copy so Vercel can serve both
$extLess = Join-Path $parent "release_info"
[System.IO.File]::WriteAllText($extLess, $json, [System.Text.Encoding]::UTF8)

Write-Host "Successfully generated release feed at: $OutputFile and $extLess"
