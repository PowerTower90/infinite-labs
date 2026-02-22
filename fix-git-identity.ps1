# Fix Git Identity Configuration
Write-Host "Setting Git user identity..." -ForegroundColor Cyan

git config --global user.name "PowerTower90"
git config --global user.email "PowerTower90@users.noreply.github.com"

Write-Host "`nVerifying configuration:" -ForegroundColor Green
git config --list | Select-String "user"

Write-Host "`nCommitting pending changes..." -ForegroundColor Cyan
git add .
git commit -m "Auto-sync improvements: detailed file logging and exit-code validation"

Write-Host "`nCurrent status:" -ForegroundColor Green
git status --short

Write-Host "`nDone! Auto-sync should now work correctly." -ForegroundColor Green
