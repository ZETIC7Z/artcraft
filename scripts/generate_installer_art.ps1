Add-Type -AssemblyName System.Drawing
$Root = 'c:\Users\ZETICUZ\Documents\artcraft\repos\craft-launcher'
$BannerOut = 'c:\Users\ZETICUZ\Documents\artcraft\branding\verification\test_installer_banner.bmp'
$DialogOut = 'c:\Users\ZETICUZ\Documents\artcraft\branding\verification\test_installer_dialog.bmp'

$ink = [System.Drawing.ColorTranslator]::FromHtml('#121316')
$accent = [System.Drawing.ColorTranslator]::FromHtml('#e0368f')
$muted = [System.Drawing.Color]::FromArgb(153, 242, 241, 238)
$line = [System.Drawing.Color]::FromArgb(38, 242, 241, 238)

$apps = 'photocraft', 'vectorcraft', 'filmcraft', 'lightcraft', 'pdfcraft', 'effectcraft', 'designcraft', 'figcraft', 'wordcraft', 'soundcraft', 'deckcraft', 'cadcraft', 'gridcraft'
$mark = [System.Drawing.Image]::FromFile((Join-Path $Root 'assets\app-icon\hicolor\256x256\apps\ai.storyteller.artcraft-launcher.png'))
$wordmark = [System.Drawing.Image]::FromFile((Join-Path $Root 'docs\brand\zetica-logo-white.png'))
$icons = $apps | ForEach-Object { [System.Drawing.Image]::FromFile((Join-Path $Root "assets\app-icons\$_.png")) }

$fonts = New-Object System.Drawing.Text.PrivateFontCollection
$fonts.AddFontFile((Join-Path $Root 'assets\fonts\GeistMono-Variable.ttf'))
$labelFont = New-Object System.Drawing.Font $fonts.Families[0], 9, ([System.Drawing.FontStyle]::Regular), ([System.Drawing.GraphicsUnit]::Pixel)

foreach ($spec in @(@($BannerOut, 493, 58), @($DialogOut, 493, 312))) {
  $bmp = New-Object System.Drawing.Bitmap $spec[1], $spec[2], ([System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
  $g = [System.Drawing.Graphics]::FromImage($bmp)
  $panel = New-Object System.Drawing.SolidBrush $ink
  $stripe = New-Object System.Drawing.SolidBrush $accent
  try {
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
    $g.Clear([System.Drawing.Color]::White)
    if ($spec[2] -eq 58) {
      $g.FillRectangle($panel, 405, 0, 88, 58)
      $g.FillRectangle($stripe, 405, 0, 2, 58)
      $g.DrawImage($mark, 431, 11, 36, 36)
    } else {
      $g.FillRectangle($panel, 0, 0, 164, 312)
      $g.FillRectangle($stripe, 162, 0, 2, 312)
      $g.DrawImage($mark, 20, 16, 44, 44)
      $wm_h = [int](120 * $wordmark.Height / $wordmark.Width)
      $g.DrawImage($wordmark, 22, 68, 120, $wm_h)
      $brush = New-Object System.Drawing.SolidBrush $muted
      $x = 22.0
      foreach ($ch in 'HUB'.ToCharArray()) {
        $g.DrawString([string]$ch, $labelFont, $brush, $x, 96, [System.Drawing.StringFormat]::GenericTypographic)
        $x += $g.MeasureString([string]$ch, $labelFont, 100, [System.Drawing.StringFormat]::GenericTypographic).Width + 2.0
      }
      $brush.Dispose()
      $pen = New-Object System.Drawing.Pen $line, 1
      $left = 22; $top = 118; $cell = 36
      for ($i = 0; $i -lt $icons.Count; $i++) {
        $cx = $left + ($i % 3) * $cell
        $cy = $top + [math]::Floor($i / 3) * $cell
        $g.DrawRectangle($pen, $cx, $cy, $cell, $cell)
        $g.DrawImage($icons[$i], $cx + 5, $cy + 5, $cell - 10, $cell - 10)
      }
      $pen.Dispose()
    }
  } finally { $panel.Dispose(); $stripe.Dispose(); $g.Dispose() }
  $bmp.Save($spec[0], [System.Drawing.Imaging.ImageFormat]::Bmp)
  $bmp.Dispose()
}
$labelFont.Dispose(); $fonts.Dispose(); $mark.Dispose(); $wordmark.Dispose()
$icons | ForEach-Object { $_.Dispose() }
Write-Host 'Generated installer art!'
