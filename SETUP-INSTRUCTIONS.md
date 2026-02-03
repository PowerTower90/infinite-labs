# INFINITE LABS PROJECT - SETUP INSTRUCTIONS FOR YOUR COMPUTER

Your project location: `H:\nfinite-labs\infinite-labs`

## STEP-BY-STEP SETUP:

### 1. Open PowerShell and navigate to your project folder:
```powershell
cd H:\nfinite-labs\infinite-labs
```

### 2. Pull all latest changes from GitHub:
```powershell
git pull
```

This downloads:
- Dark theme CSS (blue/gold/green colors)
- Auto-sync script (fixed for your H: drive)
- VS Code auto-start configuration
- All templates and files

### 3. Close VS Code completely if it's currently open

### 4. Reopen VS Code in the project folder:
```powershell
cd H:\nfinite-labs\infinite-labs
code .
```

### 5. IMPORTANT - When VS Code opens, you'll see a notification popup:
> "This folder contains tasks that run automatically. Do you allow automatic tasks to run?"

**Click "Allow" button**

This is required for auto-sync to start automatically.

### 6. Verify auto-sync is working:
- Look for a terminal tab called "Start Auto-Sync"
- You should see: `[23:XX:XX] Working in: H:\nfinite-labs\infinite-labs`
- Messages will appear every 30 seconds showing sync activity

---

## WHAT HAPPENS NOW:
✅ Your computer syncs with PowerTower90's computer every 30 seconds  
✅ All file changes sync automatically through GitHub  
✅ SHARED-ACTIVITY-LOG.md stays in sync between both computers  
✅ Flask website runs on http://127.0.0.1:5500 with dark theme  
✅ Every time you open VS Code, auto-sync starts automatically  

---

**YOU'RE ALL SET!** Both computers now work as one unified workspace.
