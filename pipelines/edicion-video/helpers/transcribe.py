"""
Transcripción de vídeo con OpenAI Whisper (word-level timestamps).
Adaptado de browser-use/video-use para usar OpenAI en lugar de ElevenLabs Scribe.

Uso:
    uv run helpers/transcribe.py input/mi_video.mp4
    uv run helpers/transcribe.py input/mi_video.mp4 --language es
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def load_api_key() -> str:
    for candidate in [Path(__file__).resolve().parent.parent / ".env", Path(".env")]:
        if candidate.exists():
            for line in candidate.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() == "OPENAI_API_KEY":
                    return v.strip().strip('"').strip("'")
    v = os.environ.get("OPENAI_API_KEY", "")
    if not v:
        sys.exit("OPENAI_API_KEY no encontrada en .env ni en variables de entorno")
    return v


def extract_audio(video_path: Path, dest: Path) -> None:
    """Extrae audio mono 16kHz WAV — formato óptimo para Whisper."""
    from helpers.utils import ffmpeg_bin
    cmd = [
        ffmpeg_bin(), "-y", "-i", str(video_path),
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(dest),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def call_whisper(audio_path: Path, api_key: str, language: str | None = None) -> dict:
    """Llama a Whisper API con timestamps a nivel de palabra."""
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    with open(audio_path, "rb") as f:
        kwargs: dict = {
            "model": "whisper-1",
            "file": f,
            "response_format": "verbose_json",
            "timestamp_granularities": ["word"],
        }
        if language:
            kwargs["language"] = language

        response = client.audio.transcriptions.create(**kwargs)

    raw = response.model_dump() if hasattr(response, "model_dump") else dict(response)

    # Normalizar al mismo formato que ElevenLabs Scribe: lista de palabras con start/end
    words = []
    for w in raw.get("words", []):
        words.append({
            "text": w.get("word", "").strip(),
            "start": w.get("start", 0.0),
            "end": w.get("end", 0.0),
            "type": "word",
            "speaker_id": "speaker_0",
        })

    return {
        "text": raw.get("text", ""),
        "language": raw.get("language", language or "auto"),
        "words": words,
        "segments": raw.get("segments", []),
        "_source": "whisper-1",
    }


def transcribe_one(
    video: Path,
    edit_dir: Path,
    api_key: str,
    language: str | None = None,
    verbose: bool = True,
) -> Path:
    """Transcribe un vídeo. Devuelve la ruta al JSON. Resultado cacheado."""
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcripts_dir / f"{video.stem}.json"

    if out_path.exists():
        if verbose:
            print(f"  cached: {out_path.name}")
        return out_path

    if verbose:
        print(f"  extrayendo audio de {video.name}...", flush=True)

    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / f"{video.stem}.wav"
        extract_audio(video, audio)
        size_mb = audio.stat().st_size / (1024 * 1024)
        if verbose:
            print(f"  enviando a Whisper ({size_mb:.1f} MB)...", flush=True)
        payload = call_whisper(audio, api_key, language)

    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    dt = time.time() - t0

    if verbose:
        kb = out_path.stat().st_size / 1024
        nwords = len(payload.get("words", []))
        print(f"  guardado: {out_path.name} ({kb:.1f} KB, {nwords} palabras, {dt:.1f}s)")

    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Transcribe un vídeo con OpenAI Whisper")
    ap.add_argument("video", type=Path, help="Ruta al fichero de vídeo")
    ap.add_argument("--edit-dir", type=Path, default=None,
                    help="Directorio de salida (por defecto: <carpeta_video>/edit)")
    ap.add_argument("--language", type=str, default=None,
                    help="Código ISO del idioma (es, en...). Omitir para autodetectar.")
    args = ap.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"Vídeo no encontrado: {video}")

    edit_dir = (args.edit_dir or (video.parent / "edit")).resolve()
    api_key = load_api_key()
    transcribe_one(video=video, edit_dir=edit_dir, api_key=api_key, language=args.language)


if __name__ == "__main__":
    main()
