@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Video Transformer

rem ---------------------------------------------------------------
rem  Self-contained launcher. First run downloads (one time only):
rem    - uv      (fetches its own Python 3.12 + Gradio; your own Python is NOT used)
rem    - ffmpeg  (only if not already installed on this PC)
rem  Everything goes into the "tools" folder next to this file.
rem ---------------------------------------------------------------

set "TOOLS=%~dp0tools"
set "SETUP=%~dp0scripts\setup_tools.ps1"
if not exist "%TOOLS%" mkdir "%TOOLS%"

set "UV_PYTHON_PREFERENCE=only-managed"
set "UV_PYTHON_INSTALL_DIR=%TOOLS%\python"
set "UV_CACHE_DIR=%TOOLS%\uv-cache"

if exist "%TOOLS%\uv.exe" goto have_uv
echo [1/3] Downloading uv, one-time setup...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SETUP%" -Tools "%TOOLS%" -Only uv
if errorlevel 1 goto fail_uv
:have_uv

if exist "%TOOLS%\ffmpeg\bin\ffmpeg.exe" goto have_ffmpeg
where ffmpeg >nul 2>nul && where ffprobe >nul 2>nul && goto have_ffmpeg
echo [2/3] Downloading ffmpeg, one-time setup, about 150 MB...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SETUP%" -Tools "%TOOLS%" -Only ffmpeg
if errorlevel 1 goto fail_ffmpeg
:have_ffmpeg

echo [3/3] Starting Video Transformer. The first start installs packages and can take a few minutes.
"%TOOLS%\uv.exe" run desktop_launcher.py
if errorlevel 1 goto fail_run
goto end

:fail_uv
echo.
echo Could not download uv. Check your internet connection, proxy or antivirus, then try again.
goto fail
:fail_ffmpeg
echo.
echo Could not download ffmpeg. Check your internet connection, then try again.
echo Alternative: install ffmpeg yourself and make sure ffmpeg and ffprobe are on PATH.
goto fail
:fail_run
echo.
echo The app stopped with an error. See the message above, or double-click "Open Logs.bat".
:fail
echo.
pause
exit /b 1

:end
endlocal
