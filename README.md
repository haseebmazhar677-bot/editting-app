# Video Transformer

Three separate modes, each with its own service module (`services/`) and UI tab (`app.py`), plus a Settings tab.

| Mode | Module | Status |
|---|---|---|
| Color Transformation | `services/color.py` | Working. ffmpeg filter chains, 8 presets. |
| Voice Transformation | `services/voice.py` | Working with built-in DSP (pitch/EQ). Neural provider optional via `VoiceProvider`. |
| Object & Character Transformation | `services/object_transform.py` | **Needs an AI service you connect.** Unavailable (and says so) until configured. |

**Windows beginners: read `README-WINDOWS.md`.** Building an exe: `BUILDING.md`.

## Run from source (developers)

Requires Python 3.10 to 3.13 and ffmpeg/ffprobe on PATH. The only third-party dependency is Gradio.

    pip install -r requirements.txt
    python desktop_launcher.py          # or: python app.py
    python desktop_launcher.py --selftest

## AI service configuration

Object & Character mode needs a generative video-to-video service. Configure with the Settings tab, or the
`VIDEO_EDIT_URL` / `VIDEO_EDIT_API_KEY` environment variables. The service must accept the multipart contract at the
top of `services/object_transform.py`. For a vendor with a different API, add an `ObjectEditProvider` subclass.
API keys are stored encrypted with Windows DPAPI only; on other systems use the environment variable.

## Tests

    python tests/test_services.py     # color + voice with real ffmpeg
    python tests/test_desktop.py      # settings, HTTP adapter against a local server, launcher failure path
