# Emergency Stop and Fix Script
# Run this in a NEW PowerShell window (NOT in VS Code terminal)

Write-Host "=== Stopping Auto-Sync ===" -ForegroundColor Red
Get-Process powershell | Where-Object { $_.CommandLine -like "*auto-sync*" } | Stop-Process -Force

Write-Host "`n=== Removing Git Lock File ===" -ForegroundColor Yellow
Remove-Item "G:\infinite labs\.git\index.lock" -Force -ErrorAction SilentlyContinue

Write-Host "`n=== Resetting Staged Files ===" -ForegroundColor Cyan
Set-Location "G:\infinite labs"
git reset HEAD .

Write-Host "`n=== Creating Clean Commit ===" -ForegroundColor Green
git add .
git commit -m "Auto-sync improvements: detailed file logging and exit-code validation"

Write-Host "`n=== Syncing with GitHub ===" -ForegroundColor Green
git pull --rebase origin main
git push origin main

Write-Host "`n=== Done! ===" -ForegroundColor Green
Write-Host "You can now restart the Auto-Sync task in VS Code." -ForegroundColor Cyan
