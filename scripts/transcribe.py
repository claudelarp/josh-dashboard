#!/usr/bin/env python3
"""Transcribe a video/audio URL or local file to text.

Usage:
    python3 scripts/transcribe.py <url-or-path> [--model REPO] [--prompt "domain hint"]

Prints one JSON object to stdout: title, source, duration_seconds, language, model, transcript.
All progress/errors go to stderr so stdout stays valid JSON.

Installs its own dependencies (yt-dlp, mlx-whisper, imageio-ffmpeg) on first run.
Prefers mlx-whisper (fast on Apple Silicon); falls back to openai-whisper if that's unavailable.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_MODEL = "mlx-community/whisper-large-v3-turbo"
DEFAULT_PROMPT = "Use proper punctuation and paragraph breaks."


def log(msg):
    print(msg, file=sys.stderr)


def ensure(module_name, pip_name=None):
    pip_name = pip_name or module_name
    try:
        return __import__(module_name)
    except ImportError:
        log(f"Installing {pip_name} (first-time setup)...")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", pip_name], capture_output=True, text=True)
        if r.returncode != 0:
            r = subprocess.run([sys.executable, "-m", "pip", "install", "-q", pip_name, "--break-system-packages"],
                                capture_output=True, text=True)
        if r.returncode != 0:
            log(r.stderr[-2000:])
            raise RuntimeError(f"Could not install {pip_name} automatically. Try manually: "
                                f"{sys.executable} -m pip install {pip_name}")
        return __import__(module_name)


def ensure_ffmpeg_on_path():
    import shutil
    if shutil.which("ffmpeg"):
        return
    # No Homebrew in this environment - imageio-ffmpeg bundles a static binary,
    # which sidesteps needing a system package manager at all.
    imageio_ffmpeg = ensure("imageio_ffmpeg")
    real_ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    shim_dir = Path(tempfile.gettempdir()) / "josh-brain-ffmpeg-shim"
    shim_dir.mkdir(exist_ok=True)
    shim = shim_dir / "ffmpeg"
    if not shim.exists():
        shim.symlink_to(real_ffmpeg)
    os.environ["PATH"] = f"{shim_dir}{os.pathsep}{os.environ.get('PATH', '')}"


def download_audio(url, workdir):
    yt_dlp = ensure("yt_dlp")
    ensure_ffmpeg_on_path()
    opts = {
        "format": "bestaudio/best",
        "outtmpl": str(Path(workdir) / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        audio_path = ydl.prepare_filename(info)
    return audio_path, info.get("title", url), info.get("duration")


def transcribe(audio_path, model, prompt):
    ensure_ffmpeg_on_path()
    try:
        mlx_whisper = ensure("mlx_whisper")
        log(f"Transcribing with mlx-whisper ({model})...")
        result = mlx_whisper.transcribe(audio_path, path_or_hf_repo=model, initial_prompt=prompt)
        return result["text"].strip(), result.get("language"), f"mlx-whisper:{model}"
    except Exception as e:
        log(f"mlx-whisper unavailable or failed ({e}); falling back to openai-whisper (slower, CPU-based)...")
        whisper = ensure("whisper", "openai-whisper")
        fallback_model = "base" if "/" in model else model  # mlx repo IDs aren't valid openai-whisper size names
        w = whisper.load_model(fallback_model)
        result = w.transcribe(audio_path, initial_prompt=prompt)
        return result["text"].strip(), result.get("language"), f"openai-whisper:{fallback_model}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", help="URL (YouTube, etc.) or local audio/video file path")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="mlx-community HF repo id (fallback uses an openai-whisper size instead)")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="domain hint / style prompt for Whisper")
    args = parser.parse_args()

    is_url = args.source.startswith("http://") or args.source.startswith("https://")

    try:
        with tempfile.TemporaryDirectory() as workdir:
            if is_url:
                audio_path, title, duration = download_audio(args.source, workdir)
            else:
                audio_path = args.source
                title = Path(args.source).stem
                duration = None
                if not Path(audio_path).exists():
                    log(f"File not found: {audio_path}")
                    sys.exit(1)

            text, language, model_used = transcribe(audio_path, args.model, args.prompt)
    except Exception as e:
        log(f"Transcription failed: {e}")
        sys.exit(1)

    print(json.dumps({
        "title": title,
        "source": args.source,
        "duration_seconds": duration,
        "language": language,
        "model": model_used,
        "transcript": text,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
