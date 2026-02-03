# Auto-Sync Script for Infinite Labs Project
# This script automatically syncs your changes with GitHub every 30 seconds

Write-Host "=== Auto-Sync Started ===" -ForegroundColor Green
Write-Host "This will sync your changes every 30 seconds" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

$repoPath = "d:\infinite labs"

while ($true) {
    try {
        cd $repoPath
        
        # Fetch latest changes
        git fetch origin main 2>&1 | Out-Null
        
        # Check if there are local changes
        $status = git status --porcelain
        
        if ($status) {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Changes detected, committing..." -ForegroundColor Cyan
            git add .
            git commit -m "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" 2>&1 | Out-Null
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Committed changes" -ForegroundColor Green
        }
        
        # Pull latest changes from GitHub
        $pullOutput = git pull --rebase origin main 2>&1
        
        if ($pullOutput -notmatch "Already up to date") {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Pulled new changes from GitHub" -ForegroundColor Green
        }
        
        # Push local changes to GitHub
        $pushOutput = git push origin main 2>&1
        
        if ($pushOutput -notmatch "Everything up-to-date") {
            Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Pushed changes to GitHub" -ForegroundColor Green
        }
        
        # Show sync status
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Sync cycle complete ✓" -ForegroundColor Gray
        
    } catch {
        Write-Host "[$(Get-Date -Format 'HH:mm:ss')] Error: $_" -ForegroundColor Red
    }
    
    # Wait 30 seconds before next sync
    Start-Sleep -Seconds 30
}
