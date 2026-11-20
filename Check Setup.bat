@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Video Transformer - Check Setup
set "TOOLS=%~dp0tools"
set "UV_PYTHON_PREFERENCE=only-managed"
set "UV_PYTHON_INSTALL_DIR=%TOOLS%\python"
set "UV_CACHE_DIR=%TOOLS%\uv-cache"
if not exist "%TOOLS%\uv.exe" (
  echo Run "Start Video Transformer.bat" once first so it can download its tools.
  pause
  exit /b 1
)
if exist "%TOOLS%\ffmpeg\bin" set "PATH=%TOOLS%\ffmpeg\bin;%PATH%"
"%TOOLS%\uv.exe" run desktop_launcher.py --selftest
echo.
pause
endlocal
