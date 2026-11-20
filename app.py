"""Gradio UI: three transformation modes (each with its own service) plus Settings.

Normal use on Windows: double-click "Start Video Transformer.bat" or VideoTransformer.exe.
Both go through desktop_launcher.py, which adds logging, error messages and opens the browser.

Developer use:  python app.py   (same as python desktop_launcher.py)
"""
import gradio as gr

from services import color, object_transform, settings, voice
from services.common import NotConfiguredError, ProcessingError


def _guard(fn, *args):
    try:
        return fn(*args), "Done. Preview above; use the download icon on the player to export."
    except NotConfiguredError as e:
        return None, f"Unavailable: {e}"
    except ProcessingError as e:
        return None, f"Error: {e}"


def run_color(video, preset):
    if not video:
        return None, "Upload a video first."
    return _guard(color.apply_color_preset, video, preset)


def run_voice(video, style):
    if not video:
        return None, "Upload a video first."
    return _guard(voice.transform_voice, video, style)


def run_object(video, target, transformation, extra):
    if not video:
        return None, "Upload a video first."
    req = object_transform.ObjectEditRequest(target, transformation, extra or "")
    return _guard(object_transform.transform_object, video, req)


def _settings_status() -> str:
    source = settings.secret_source()
    key = {"environment": "set (from an environment variable)",
           "saved": "set (saved, encrypted for your Windows account)",
           "none": "not set"}[source]
    url = settings.get_value(settings.URL_KEY) or "not set"
    return f"**Service URL:** {url}  \n**API key:** {key}  \n**Object mode:** {object_transform.status_message()}"


def save_settings(url, key):
    try:
        if url is not None and url.strip():
            settings.set_value(settings.URL_KEY, url)
        if key and key.strip():
            settings.set_secret(key)
    except settings.SecureStorageUnavailable as e:
        return _settings_status() + f"\n\n**Not saved:** {e}", ""
    except Exception as e:  # noqa: BLE001 - show any storage error to the user
        return _settings_status() + f"\n\n**Not saved:** {e}", ""
    return _settings_status() + "\n\nSaved.", ""   # clears the key box


def clear_settings():
    settings.clear_secret()
    settings.set_value(settings.URL_KEY, "")
    return _settings_status() + "\n\nSaved key and URL removed.", "", ""


def build_demo() -> "gr.Blocks":
    with gr.Blocks(title="Video Transformer") as demo:
        gr.Markdown("# Video Transformer\nThree independent modes. Each has its own processing service.")

        with gr.Tab("1. Color Transformation"):
            gr.Markdown("Global color grading of the whole video (ffmpeg). Does not target individual objects.")
            with gr.Row():
                c_in = gr.Video(label="Original video")
                c_out = gr.Video(label="Result")
            c_preset = gr.Dropdown(color.available_presets(), value="Cinematic", label="Preset")
            c_btn = gr.Button("Apply color preset", variant="primary")
            c_msg = gr.Markdown()
            c_btn.click(run_color, [c_in, c_preset], [c_out, c_msg])

        with gr.Tab("2. Object & Character Transformation"):
            gr.Markdown("Prompt-driven edits of specific objects, characters or clothing using an AI "
                        "video-to-video service that **you** connect in the Settings tab. "
                        "Without one, this mode is unavailable and produces nothing.")
            with gr.Row():
                o_in = gr.Video(label="Original video")
                o_out = gr.Video(label="Result")
            o_target = gr.Textbox(label="Object / element to change", placeholder="the blue pen")
            o_change = gr.Textbox(label="Desired transformation", placeholder="a white pen")
            o_extra = gr.Textbox(label="Extra instructions (optional)",
                                 placeholder="keep the hand, background and movement unchanged")
            o_btn = gr.Button("Transform object", variant="primary")
            o_msg = gr.Markdown()
            o_btn.click(run_object, [o_in, o_target, o_change, o_extra], [o_out, o_msg])

        with gr.Tab("3. Voice Transformation"):
            gr.Markdown("Changes the audio voice only, to a generic style. Built-in processing is DSP "
                        "(pitch/EQ), not neural voice conversion. No real person's voice is imitated.")
            with gr.Row():
                v_in = gr.Video(label="Original video")
                v_out = gr.Video(label="Result")
            v_style = gr.Dropdown(voice.available_styles(), value="Narrator", label="Voice style")
            v_btn = gr.Button("Transform voice", variant="primary")
            v_msg = gr.Markdown()
            v_btn.click(run_voice, [v_in, v_style], [v_out, v_msg])

        with gr.Tab("Settings (AI service)"):
            gr.Markdown("Only needed for **Object & Character Transformation**. You need an account with an "
                        "AI video-editing service that follows the contract in the README. The API key is "
                        "encrypted for your Windows user account and is never shown again.")
            s_status = gr.Markdown(_settings_status())
            s_url = gr.Textbox(label="Service URL (https://...)", value=settings.get_value(settings.URL_KEY))
            s_key = gr.Textbox(label="API key (paste, then Save)", type="password")
            with gr.Row():
                s_save = gr.Button("Save", variant="primary")
                s_clear = gr.Button("Remove saved key and URL")
            s_save.click(save_settings, [s_url, s_key], [s_status, s_key])
            s_clear.click(clear_settings, None, [s_status, s_url, s_key])

    return demo


if __name__ == "__main__":
    from desktop_launcher import main
    raise SystemExit(main())
