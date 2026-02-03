# File Verification Script - Run on both computers to compare files
Write-Host "`n=== INFINITE LABS FILE VERIFICATION ===" -ForegroundColor Cyan
Write-Host ""

# Get all files excluding git and database files
$files = Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch '\.git' -and $_.Name -notmatch '\.db$' }
$fileCount = $files.Count

Write-Host "Total Files: $fileCount" -ForegroundColor Green
Write-Host "`n=== FILE LIST ===" -ForegroundColor Yellow

$files | Sort-Object FullName | ForEach-Object {
    $rel = $_.FullName.Replace((Get-Location).Path + '\', '')
    $size = [math]::Round($_.Length / 1KB, 2)
    Write-Host "  $rel - $size KB"
}

Write-Host "`n=== IMPORTANT FILES ===" -ForegroundColor Yellow
$important = @('app.py', 'requirements.txt', 'Procfile', 'auto-sync.ps1', 'README.md', 'templates\home.html', 'static\css\style.css')

foreach ($f in $important) {
    if (Test-Path $f) {
        Write-Host "  ✓ $f" -ForegroundColor Green
    } else {
        Write-Host "  ✗ MISSING: $f" -ForegroundColor Red
    }
}

Write-Host "`n=== Git Status ===" -ForegroundColor Yellow
git status --short

Write-Host "`n=== Last 3 Commits ===" -ForegroundColor Yellow
git log -3 --oneline

Write-Host "`n=== DONE - Compare with other computer! ===" -ForegroundColor Cyan
