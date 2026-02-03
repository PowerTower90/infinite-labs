# File Verification Script
# Run this on both computers to compare files

Write-Host "`n=== INFINITE LABS FILE VERIFICATION ===" -ForegroundColor Cyan
Write-Host ""

$repoPath = Get-Location

# Get all files (excluding .git and database files)
$files = Get-ChildItem -Recurse -File | Where-Object { 
    $_.FullName -notmatch '\.git' -and 
    $_.Name -notmatch '\.db$' -and 
    $_.Name -notmatch '\.sqlite$'
} | Sort-Object FullName

# Count files
$fileCount = $files.Count
Write-Host "Total Files Found: $fileCount" -ForegroundColor Green
Write-Host ""

# List all files with their sizes
Write-Host "=== FILE LIST ===" -ForegroundColor Yellow
$files | ForEach-Object {
    $relativePath = $_.FullName.Replace($repoPath.Path + '\', '')
    $size = "{0:N2} KB" -f ($_.Length / 1KB)
    Write-Host "  ✓ $relativePath ($size)" -ForegroundColor White
}

Write-Host ""
Write-Host "=== IMPORTANT FILES CHECK ===" -ForegroundColor Yellow

$importantFiles = @(
    'app.py',
    'requirements.txt',
    'Procfile',
    'runtime.txt',
    'auto-sync.ps1',
    'AUTO-SYNC-README.md',
    'README.md',
    'templates\home.html',
    'templates\products.html',
    'templates\cart.html',
    'static\css\style.css'
)

foreach ($file in $importantFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file" -ForegroundColor Green
    } else {
        Write-Host "  ✗ MISSING: $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=== Git Status ===" -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "=== Last 3 Commits ===" -ForegroundColor Yellow
git log -3 --oneline

Write-Host ""
Write-Host "=== VERIFICATION COMPLETE ===" -ForegroundColor Cyan
Write-Host "Copy this output and compare with the other computer!" -ForegroundColor Yellow
Write-Host ""
