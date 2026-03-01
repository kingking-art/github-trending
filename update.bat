@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo Updating GitHub Trending...
node update-trending.js
if %ERRORLEVEL% EQU 0 (
    echo Done! Check Obsidian.
) else (
    echo Failed. Check network.
)
pause
