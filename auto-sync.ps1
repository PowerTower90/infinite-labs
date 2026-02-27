# Auto-Sync Script for Infinite Labs Project
# Syncs every 30 seconds - auto-commits local changes and syncs with GitHub.

Write-Host "=== Auto-Sync Started ===" -ForegroundColor Green
Write-Host "Auto-commits local edits and pushes them automatically." -ForegroundColor Yellow
Write-Host "Pull from GitHub happens every cycle. Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

# Auto-detect the repository path (works on both computers)
$repoPath = $PSScriptRoot

while ($true) {
    try {
        Set-Location $repoPath
        $ts = Get-Date -Format 'HH:mm:ss'

        # --- 1. Fetch remote state silently ---
        git fetch origin main 2>&1 | Out-Null

        # --- 2. Auto-commit local changes (tracked + untracked) ---
        $status = git status --porcelain 2>&1
        if ($status) {
            git add -A 2>&1 | Out-Null
            git diff --cached --quiet
            if ($LASTEXITCODE -ne 0) {
                $commitTs = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
                git commit -m "Auto-sync: $commitTs" 2>&1 | Out-Null
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "[$ts] Auto-committed local changes" -ForegroundColor Cyan
                } else {
                    Write-Host "[$ts] Auto-commit failed (will retry next cycle)" -ForegroundColor Yellow
                }
            }
        }

        # --- 3. Pull if remote has new commits ---
        $behind = (git rev-list --count HEAD..origin/main 2>&1).Trim()
        if ($behind -gt 0) {
            $pullOutput = git pull --rebase origin main 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[$ts] Pulled $behind new commit(s) from GitHub" -ForegroundColor Green
            } else {
                Write-Host "[$ts] Pull failed - rebase conflict detected. Run: git rebase --abort" -ForegroundColor Yellow
                Write-Host ($pullOutput.Trim()) -ForegroundColor DarkYellow
            }
        }

        # --- 4. Push local commits ahead of origin ---
        $ahead = (git rev-list --count origin/main..HEAD 2>&1).Trim()
        if ($ahead -gt 0) {
            Write-Host "[$ts] Found $ahead local commit(s) to push..." -ForegroundColor Cyan
            git push origin main 2>&1 | Out-Null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[$ts] Pushed $ahead commit(s) to GitHub" -ForegroundColor Green
            } else {
                # Most common cause: remote moved ahead again between fetch and push
                Write-Host "[$ts] Push skipped --- remote changed since last fetch (will retry next cycle)" -ForegroundColor Yellow
            }
        }

        Write-Host "[$ts] Sync cycle complete" -ForegroundColor Gray

    } catch {
        $ts = Get-Date -Format 'HH:mm:ss'
        Write-Host "[$ts] Unexpected error: $_" -ForegroundColor Red
    }

    # Wait 30 seconds before next sync
    Start-Sleep -Seconds 30
}

