@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\create_shortcut.ps1" -Root "%~dp0."
if errorlevel 1 (
  echo Could not create the shortcut.
) else (
  echo Done. Look for "Video Transformer" on your Desktop.
)
pause
endlocal
