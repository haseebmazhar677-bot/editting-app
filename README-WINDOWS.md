# Video Transformer for Windows (beginner guide)

You do **not** need to install Python, Gradio or PyYAML, and you do **not** need to use a terminal.

## Honest status

| Part | Status |
|---|---|
| Video processing (color, voice) and the AI-service connection code | Tested on Linux with real ffmpeg |
| The `.bat` launcher files | Written, **not yet run on Windows** |
| `VideoTransformer.exe` | **Not built, not tested.** It does not exist yet. See `BUILDING.md`. |

So today you start the app with the `.bat` file below. If a step fails, the black window or a popup
tells you what went wrong, and `Open Logs.bat` shows the details.

## Why your own Python 3.15.2 is not used

Gradio needs helper packages such as PyYAML. For a brand-new Python version, ready-made Windows
installers for those packages may not exist, so pip tries to compile them and fails. The launcher avoids
this by downloading its own Python 3.12 into this folder. Your installed Python is left alone.

## Start the app (graphical steps)

1. Right-click `video-transformer.zip`, choose **Extract All...**, pick a simple location such as
   `C:\VideoTransformer`, and click **Extract**. (Avoid OneDrive and "Program Files". Do not run it from
   inside the zip.)
2. Open the extracted folder in File Explorer.
3. Double-click **Start Video Transformer.bat**.
   - If blue "Windows protected your PC" appears: click **More info**, then **Run anyway**.
4. A black window opens. **First time only**, it downloads its tools (a few minutes, needs internet; about
   150 MB for ffmpeg unless you already have it). Wait until you see "Video Transformer is running".
5. Your web browser opens the app automatically. If it does not, copy the address shown in the black window
   (like `http://127.0.0.1:7860`) into your browser.
6. **To quit:** close the black window.

### Optional: Desktop shortcut

Double-click **Create Desktop Shortcut.bat**. A "Video Transformer" icon appears on your Desktop; double-click it
from then on.

## Using the three tabs

- **1. Color Transformation:** upload a video, pick a preset, click the button, preview, and download with the
  download icon on the result player.
- **3. Voice Transformation:** changes only the voice, to a generic style. It is audio processing (pitch and EQ),
  not AI voice cloning, so it sounds processed. It never imitates a real person.
- **2. Object & Character Transformation:** needs an AI service **you** connect. It will not run, and does not
  pretend to, until you do the next section.

## Connecting an AI service (Object & Character mode)

This mode needs a paid or self-hosted video-to-video AI service. No such service is built in or included.

1. Get a **service URL (https://...)** and an **API key** from the provider. The provider's API must follow the
   request format described at the top of `services\object_transform.py` (a ready-made vendor-specific connector
   does not exist yet; ask for one).
2. In the app, open the **Settings (AI service)** tab.
3. Paste the URL and the key, click **Save**.
4. Your key is encrypted for your Windows user account (Windows DPAPI) and stored in
   `%APPDATA%\VideoTransformer\config.json`. It is never displayed again and never written as plain text.
   Anyone logged in as a different Windows user, or on another PC, cannot read it.
   *(The encryption call itself has only been written, not run on Windows yet.)*
5. For safety the app refuses to send the key over plain `http://` (except to your own PC).
6. To remove it: Settings tab, **Remove saved key and URL**.

Advanced alternative: set the environment variables `VIDEO_EDIT_URL` and `VIDEO_EDIT_API_KEY`
(Start menu, search "environment variables", **Edit environment variables for your account**). These take priority over
the saved values.

Never put your key in a file you share, or send it to anyone, including me.

## If something goes wrong

| What you see | What to do |
|---|---|
| A popup or text saying a download failed | Check internet, VPN/proxy or antivirus, then run the `.bat` again. |
| "ffmpeg not found" | Run **Start Video Transformer.bat** (it downloads ffmpeg), or install ffmpeg yourself. |
| "Gradio could not be loaded" | Use the `.bat` launcher instead of your own Python. |
| Browser did not open | Copy the address from the black window into your browser. |
| Anything else | Double-click **Check Setup.bat**, and **Open Logs.bat** to find `app.log`. |

## Uninstall

Close the app and delete the folder. Also delete `%APPDATA%\VideoTransformer` (saved settings) and
`%LOCALAPPDATA%\VideoTransformer` (logs) if you want everything gone.
