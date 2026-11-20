@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Build Video Transformer executable
rem Builds dist\VideoTransformer\VideoTransformer.exe. Needs internet. See BUILDING.md.
rem The result is NOT considered working until you have tested it (BUILDING.md, step 6).

set "TOOLS=%~dp0tools"
set "SETUP=%~dp0scripts\setup_tools.ps1"
if not exist "%TOOLS%" mkdir "%TOOLS%"
set "UV_PYTHON_PREFERENCE=only-managed"
set "UV_PYTHON_INSTALL_DIR=%TOOLS%\python"
set "UV_CACHE_DIR=%TOOLS%\uv-cache"

if exist "%TOOLS%\uv.exe" goto have_uv
echo [1/3] Downloading uv...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SETUP%" -Tools "%TOOLS%" -Only uv
if errorlevel 1 goto fail
:have_uv

rem The exe must carry its own ffmpeg, so always use tools\ffmpeg (even if ffmpeg is installed on this PC).
if exist "%TOOLS%\ffmpeg\bin\ffmpeg.exe" goto have_ffmpeg
echo [2/3] Downloading ffmpeg to bundle into the app, about 150 MB...
powershell -NoProfile -ExecutionPolicy Bypass -File "%SETUP%" -Tools "%TOOLS%" -Only ffmpeg
if errorlevel 1 goto fail
:have_ffmpeg

echo [3/3] Building. This can take 5 to 15 minutes...
"%TOOLS%\uv.exe" run --with pyinstaller pyinstaller --noconfirm --clean video-transformer.spec
if errorlevel 1 goto fail

copy /Y "README-WINDOWS.md" "dist\VideoTransformer\README-WINDOWS.md" >nul
echo.
echo Build finished: dist\VideoTransformer\VideoTransformer.exe
echo Now follow BUILDING.md step 6 to test it. Do not share it before testing.
pause
exit /b 0

:fail
echo.
echo Build failed. Scroll up for the first error message, then see BUILDING.md "If the build fails".
pause
exit /b 1
