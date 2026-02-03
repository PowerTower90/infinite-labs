@echo off
REM Start auto-sync in background
start /min powershell -WindowStyle Hidden -File "H:\nfinite-labs\infinite-labs\auto-sync.ps1"

REM Wait a moment
timeout /t 2 /nobreak > nul

REM Open VS Code in this folder
code "H:\nfinite-labs\infinite-labs"
