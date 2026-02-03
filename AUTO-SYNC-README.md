# Auto-Sync Setup Instructions

## How to Enable Automatic Synchronization

This script will automatically sync your changes with GitHub every 30 seconds.

### On Your Computer (PowerTower90)

1. Open a NEW PowerShell terminal in VS Code (Terminal → New Terminal)
2. Run this command:
   ```powershell
   cd "d:\infinite labs"
   .\auto-sync.ps1
   ```
3. Keep this terminal running in the background
4. You'll see sync messages every 30 seconds

### On Brother's Computer (Andeer)

1. First, get the latest files:
   ```powershell
   cd H:\nfinite-labs\infinite-labs
   git pull
   ```

2. Create a modified version for his path:
   ```powershell
   # Edit auto-sync.ps1 and change line 9 to:
   $repoPath = "H:\nfinite-labs\infinite-labs"
   ```

3. Run the script:
   ```powershell
   cd H:\nfinite-labs\infinite-labs
   .\auto-sync.ps1
   ```

4. Keep this terminal running in the background

## What Happens Now?

✅ Any file you create/edit is automatically committed and pushed every 30 seconds
✅ Changes from the other person are automatically pulled every 30 seconds
✅ Both computers stay synchronized without manual git commands
✅ You can see sync status in the terminal

## To Stop Auto-Sync

Press `Ctrl + C` in the terminal running auto-sync

## Notes

- Keep the auto-sync terminal open while working
- Both people should run auto-sync for best results
- If you make changes at the exact same time, Git will handle conflicts automatically
- You can still use regular git commands when auto-sync is stopped

## Testing

1. Create a file on one computer
2. Wait 30-60 seconds
3. Check if it appears on the other computer automatically

Enjoy automatic synchronization! 🚀
