"""Desktop entry point: logging, clear start-up errors, local server, opens your default browser.

Used by "Start Video Transformer.bat" and by the packaged VideoTransformer.exe.
  --selftest   check ffmpeg / Gradio and exit (code 0 = OK)
"""
from __future__ import annotations

import logging
import os
import shutil
import socket
import sys
import time
import traceback
import webbrowser
from logging.handlers import RotatingFileHandler
from pathlib import Path

APP_NAME = "VideoTransformer"
HOST = "127.0.0.1"
FIRST_PORT = 7860

log = logging.getLogger(APP_NAME)


def log_dir() -> Path:
    override = os.environ.get("VT_LOG_DIR")
    if override:
        folder = Path(override)
    elif sys.platform == "win32":
        folder = Path(os.environ.get("LOCALAPPDATA") or Path.home()) / APP_NAME / "logs"
    else:
        folder = Path.home() / ".local" / "state" / APP_NAME / "logs"
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def setup_logging() -> Path:
    path = log_dir() / "app.log"
    handlers: list[logging.Handler] = [RotatingFileHandler(path, maxBytes=512_000, backupCount=3, encoding="utf-8")]
    if sys.stdout is not None:
        handlers.append(logging.StreamHandler(sys.stdout))
    logging.basicConfig(level=logging.INFO, handlers=handlers, force=True,
                        format="%(asctime)s %(levelname)s %(message)s")

    def hook(exc_type, exc, tb):
        log.error("Unhandled error:\n%s", "".join(traceback.format_exception(exc_type, exc, tb)))
    sys.excepthook = hook
    return path


def _interactive() -> bool:
    return sys.stdin is not None and sys.stdin.isatty()


def fatal(title: str, message: str, log_file: Path) -> int:
    """Tell the user what went wrong in plain words, then keep the window open if interactive."""
    full = f"{message}\n\nMore detail is in the log file:\n{log_file}"
    log.error("%s: %s", title, message)
    print(f"\n=== {title} ===\n{full}\n")
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.user32.MessageBoxW(0, full, f"Video Transformer - {title}", 0x10)
        except Exception:  # noqa: BLE001 - message box is best effort
            pass
    if _interactive():
        try:
            input("Press Enter to close...")
        except EOFError:
            pass
    return 1


def find_free_port(start: int = FIRST_PORT, tries: int = 50) -> int:
    for port in range(start, start + tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((HOST, port))
                return port
            except OSError:
                continue
    raise OSError(f"No free port found between {start} and {start + tries - 1}")


def selftest() -> int:
    ok = True
    for tool in ("ffmpeg", "ffprobe"):
        path = shutil.which(tool)
        print(f"{tool}: {path or 'MISSING'}")
        ok &= path is not None
    try:
        import gradio
        print("gradio:", gradio.__version__)
    except Exception as e:  # noqa: BLE001 - report any import failure
        print("gradio: FAILED to import:", e)
        ok = False
    print("python:", sys.version.split()[0], "(frozen)" if getattr(sys, "frozen", False) else "")
    print("logs:", log_dir())
    print("SELFTEST", "PASSED" if ok else "FAILED")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    log_file = setup_logging()
    os.environ.setdefault("GRADIO_ANALYTICS_ENABLED", "False")
    log.info("Starting Video Transformer (python %s, frozen=%s)", sys.version.split()[0],
             getattr(sys, "frozen", False))

    if "--selftest" in argv:
        return selftest()

    try:
        import services.common  # noqa: F401  (adds bundled ffmpeg to PATH)
    except Exception:  # noqa: BLE001
        log.exception("Cannot load application files")
        return fatal("Cannot start", "The application files are damaged or incomplete. Re-extract the zip "
                     "or rebuild the application.", log_file)

    if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
        return fatal("ffmpeg not found",
                     "Video Transformer needs ffmpeg and ffprobe, but they were not found.\n"
                     "Run 'Start Video Transformer.bat' (it downloads ffmpeg automatically) or install ffmpeg "
                     "and add it to PATH.", log_file)

    try:
        import gradio  # noqa: F401
    except Exception as e:  # noqa: BLE001
        log.exception("Gradio import failed")
        return fatal("Gradio could not be loaded",
                     f"The Gradio library failed to load:\n{e}\n\nIf you are running from source, use "
                     "'Start Video Transformer.bat', which installs a compatible Python and Gradio for you.",
                     log_file)

    try:
        from app import build_demo
        demo = build_demo()
        port = find_free_port()
        url = f"http://{HOST}:{port}"
        demo.launch(server_name=HOST, server_port=port, inbrowser=False, prevent_thread_lock=True,
                    show_error=True)
    except Exception as e:  # noqa: BLE001
        log.exception("Failed to start the interface")
        return fatal("Could not start the app", f"Starting the local interface failed:\n{e}", log_file)

    log.info("Running at %s", url)
    print(f"\nVideo Transformer is running at {url}\nIf your browser did not open, copy that address into it.\n"
          "Keep this window open. Close it to quit the app.\n")
    try:
        webbrowser.open(url)
    except Exception:  # noqa: BLE001
        log.warning("Could not open the browser automatically")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            demo.close()
        except Exception:  # noqa: BLE001
            pass
        log.info("Stopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
