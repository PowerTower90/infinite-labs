# Auto-Sync Script for Infinite Labs Project
# Syncs every 30 seconds — pushes ONLY when you have manually committed changes.
# No auto-commits. No surprise "Auto-sync:" clutter in your history.

Write-Host "=== Auto-Sync Started ===" -ForegroundColor Green
Write-Host "Watches for YOUR commits and pushes them automatically." -ForegroundColor Yellow
Write-Host "Pull from GitHub happens every cycle. Press Ctrl+C to stop." -ForegroundColor Yellow
Write-Host ""

# Auto-detect the repository path (works on both computers)
$repoPath = $PSScriptRoot

while ($true) {
    try {
        Set-Location $repoPath
        $ts = Get-Date -Format 'HH:mm:ss'

        # ── 1. Fetch remote state silently ──────────────────────────────────
        git fetch origin main 2>&1 | Out-Null

        # ── 2. Pull if remote has new commits ───────────────────────────────
        $behind = (git rev-list --count HEAD..origin/main 2>&1).Trim()
        if ($behind -gt 0) {
            # Abort if there are staged or unstaged changes that could conflict
            $dirty = git status --porcelain 2>&1
            if ($dirty) {
                Write-Host "[$ts] Remote has $behind new commit(s). Skipping pull — you have uncommitted changes. Commit or stash them first." -ForegroundColor Yellow
            } else {
                $pullOutput = git pull --rebase origin main 2>&1 | Out-String
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "[$ts] Pulled $behind new commit(s) from GitHub" -ForegroundColor Green
                } else {
                    Write-Host "[$ts] Pull failed — rebase conflict detected. Run: git rebase --abort" -ForegroundColor Yellow
                    Write-Host ($pullOutput.Trim()) -ForegroundColor DarkYellow
                }
            }
        }

        # ── 3. Push only if YOU have committed changes ahead of origin ──────
        $ahead = (git rev-list --count origin/main..HEAD 2>&1).Trim()
        if ($ahead -gt 0) {
            Write-Host "[$ts] Found $ahead local commit(s) to push..." -ForegroundColor Cyan
            $pushOutput = git push origin main 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[$ts] Pushed $ahead commit(s) to GitHub" -ForegroundColor Green
            } else {
                # Most common cause: remote moved ahead again between fetch and push
                Write-Host "[$ts] Push skipped — remote changed since last fetch (will retry next cycle)" -ForegroundColor Yellow
            }
        }

        # ── 4. Inform about uncommitted local changes (no auto-commit) ──────
        $status = git status --porcelain 2>&1
        if ($status) {
            $fileCount = ($status | Measure-Object).Count
            Write-Host "[$ts] $fileCount file(s) changed locally — commit them to push to GitHub" -ForegroundColor DarkCyan
        }

        Write-Host "[$ts] Sync cycle complete" -ForegroundColor Gray

    } catch {
        $ts = Get-Date -Format 'HH:mm:ss'
        Write-Host "[$ts] Unexpected error: $_" -ForegroundColor Red
    }

    # Wait 30 seconds before next sync
    Start-Sleep -Seconds 30
}
