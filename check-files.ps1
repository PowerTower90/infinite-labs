# File Verification Script
Write-Host "=== INFINITE LABS FILE VERIFICATION ===" -ForegroundColor Cyan

$files = Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch '\.git' }
Write-Host "Total Files: $($files.Count)" -ForegroundColor Green

Write-Host "`nFILE LIST:" -ForegroundColor Yellow
$files | Sort-Object FullName | ForEach-Object {
    Write-Host "  $($_.Name)"
}

Write-Host "`nGit Status:" -ForegroundColor Yellow
git status --short

Write-Host "`nLast 3 Commits:" -ForegroundColor Yellow
git log -3 --oneline

Write-Host "`nCOMPARE THIS OUTPUT WITH OTHER COMPUTER!" -ForegroundColor Cyan
