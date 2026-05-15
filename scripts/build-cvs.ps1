# scripts/build-cvs.ps1
# Renders both CV HTML files to PDFs via headless Chrome.
# Run from the project root:  pwsh ./scripts/build-cvs.ps1
# Or from anywhere:            pwsh D:/1.GITHUB/renata-resume/scripts/build-cvs.ps1

$ErrorActionPreference = "Stop"

# Resolve project root (parent of this script's directory)
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Write-Host "Project root: $projectRoot" -ForegroundColor Cyan

# Find Chrome
$chromeCandidates = @(
  "C:\Program Files\Google\Chrome\Application\chrome.exe",
  "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)
$chrome = $chromeCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $chrome) {
  Write-Error "Chrome not found. Install Google Chrome or edit `$chromeCandidates in this script."
  exit 1
}
Write-Host "Chrome:       $chrome" -ForegroundColor Cyan

# Pairs of (source HTML, output PDF) — both relative to project root
$pairs = @(
  @{ Src = "docs/cv-en.html"; Out = "docs/cv-en-pdf/Renata-Baldissara-Kunnela-CV-EN.pdf" },
  @{ Src = "docs/cv-fi.html"; Out = "docs/cv-fi-pdf/Renata-Baldissara-Kunnela-CV-FI.pdf" }
)

foreach ($pair in $pairs) {
  $srcAbs = Join-Path $projectRoot $pair.Src
  $outAbs = Join-Path $projectRoot $pair.Out
  $outDir = Split-Path $outAbs -Parent

  if (-not (Test-Path $srcAbs)) {
    Write-Warning "Skipping: source not found: $srcAbs"
    continue
  }
  if (-not (Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
  }

  $srcUri = "file:///" + ($srcAbs -replace '\\', '/')
  Write-Host ""
  Write-Host "Rendering $($pair.Src) -> $($pair.Out)" -ForegroundColor Green
  & $chrome `
    --headless `
    --disable-gpu `
    --no-sandbox `
    --no-pdf-header-footer `
    "--print-to-pdf=$outAbs" `
    $srcUri | Out-Null

  if (Test-Path $outAbs) {
    $size = (Get-Item $outAbs).Length
    Write-Host ("  OK ({0:N0} bytes)" -f $size) -ForegroundColor Green
  } else {
    Write-Error "Render failed: $outAbs not produced"
    exit 1
  }
}

Write-Host ""
Write-Host "Done. Two PDFs regenerated." -ForegroundColor Cyan
