# PyInstaller spec for the standalone Windows build (folder build, not a single file).
# STATUS: written but NOT built or run by the author. Use build_exe.bat or the GitHub Actions
# workflow, then follow BUILDING.md step 6 to test before relying on it.
from pathlib import Path

from PyInstaller.utils.hooks import collect_all, collect_submodules

datas, binaries, hiddenimports = [], [], []

# Gradio loads templates, assets and many modules dynamically, so collect them fully.
for pkg in ("gradio", "gradio_client", "safehttpx", "groovy", "brotli", "yaml"):
    try:
        d, b, h = collect_all(pkg)
        datas += d
        binaries += b
        hiddenimports += h
    except Exception as exc:  # package not installed in this environment
        print(f"spec: skipping {pkg}: {exc}")

# The web server picks its implementation by string name at run time.
for pkg in ("uvicorn", "anyio"):
    try:
        hiddenimports += collect_submodules(pkg)
    except Exception as exc:
        print(f"spec: skipping {pkg}: {exc}")

# Our own modules (app is imported by name inside desktop_launcher).
hiddenimports += ["app", "services.common", "services.color", "services.voice",
                  "services.object_transform", "services.settings"]

# Bundle ffmpeg + ffprobe (placed in tools/ffmpeg/bin by build_exe.bat or CI).
ffbin = Path("tools") / "ffmpeg" / "bin"
for exe_name in ("ffmpeg.exe", "ffprobe.exe"):
    if (ffbin / exe_name).exists():
        binaries.append((str(ffbin / exe_name), "ffmpeg_bin"))
    else:
        print(f"spec: WARNING {exe_name} not found in {ffbin}; the exe will need ffmpeg on PATH")

a = Analysis(
    ["desktop_launcher.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
)
pyz = PYZ(a.pure)
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="VideoTransformer",
    console=True,  # the console window is the app's status window; closing it quits the app
)
coll = COLLECT(exe, a.binaries, a.datas, name="VideoTransformer")
