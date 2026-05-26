"""
Pipeline de renderizado: extrae segmentos, concatena y aplica subtítulos.
Basado en browser-use/video-use, adaptado para Windows + OpenAI Whisper.

EDL (edl.json) esperado:
{
  "sources": {"clip1": "input/clip1.mp4"},
  "ranges": [
    {"source": "clip1", "start": 1.5, "end": 8.0, "grade": "warm_cinematic"},
    {"source": "clip1", "start": 12.0, "end": 20.5}
  ],
  "overlays": [
    {"file": "edit/animations/intro/output.mp4", "start_in_output": 0.0, "duration": 5.0}
  ],
  "subtitles": true
}

Uso:
    uv run helpers/render.py edl.json --mode final
    uv run helpers/render.py edl.json --mode draft
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import unicodedata
import tempfile
from pathlib import Path



def generate_pop_sound(out_path: Path):
    import wave
    import numpy as np
    
    sample_rate = 44100
    duration = 0.15
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freq = 600 + (1200 - 600) * (t / duration)
    signal = np.sin(2 * np.pi * freq * t)
    envelope = np.exp(-15 * t)
    signal = signal * envelope
    signal_normalized = np.int16(signal * 32767 * 0.8)
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(signal_normalized.tobytes())


def generate_swoosh_sound(out_path: Path):
    import wave
    import numpy as np
    
    sample_rate = 44100
    duration = 0.4
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    freq = 150 + (850 - 150) * (t / duration)
    signal = np.sin(2 * np.pi * freq * t)
    envelope = np.sin(np.pi * (t / duration))
    signal = signal * envelope
    signal_normalized = np.int16(signal * 32767 * 0.8)
    
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(signal_normalized.tobytes())


def get_image_bg_hex(img_path: Path) -> str:
    try:
        from PIL import Image
        with Image.open(img_path) as img:
            rgb = img.convert("RGB").getpixel((0, 0))
            return f"0x{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
    except Exception:
        return "0x250d3d" # default fallback


GRADES = {
    "warm_cinematic": "curves=red='0/0 0.5/0.55 1/1':green='0/0 0.5/0.5 1/0.95':blue='0/0 0.5/0.45 1/0.85'",
    "cool_modern":    "curves=red='0/0 0.5/0.45 1/0.9':green='0/0 0.5/0.5 1/1':blue='0/0 0.5/0.55 1/1'",
    "bw_contrast":    "hue=s=0,curves=all='0/0 0.3/0.2 0.7/0.85 1/1'",
    "auto":           "",  # sin grade
}

QUALITY = {
    "final":   {"preset": "fast",      "crf": 20},
    "preview": {"preset": "medium",    "crf": 22},
    "draft":   {"preset": "ultrafast", "crf": 28},
}

# Filtros de escala/recorte por formato de salida
ASPECT = {
    "landscape": {"scale": "1920:-2",  "crop": None, "pad": None, "fps": 24},
    "vertical":  {"scale": "-2:1920",  "crop": "1080:1920", "pad": None, "fps": 30},
    "square":    {"scale": "1080:1080:force_original_aspect_ratio=decrease",
                  "crop": None, "pad": "1080:1080:(ow-iw)/2:(oh-ih)/2:black", "fps": 30},
}

SUBTITLE_STYLE = (
    "FontName=Arial,FontSize=18,Bold=1,"
    "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
    "BorderStyle=1,Outline=2,Alignment=2,MarginV=90"
)

FADE_MS = 0.03  # 30 ms fade en cortes


def _extract_title(edl: dict, transcripts_dir: Path, max_words: int = 5) -> str:
    """
    Genera un slug de nombre de fichero a partir de las palabras más
    significativas de la transcripción (elimina stop-words y puntuación).
    """
    STOP = {
        'el','la','los','las','un','una','y','e','o','u','a','de','del','al',
        'en','es','que','por','para','se','su','lo','le','nos','les','me',
        'qué','cómo','si','no','mí','yo','tu','este','esta','estos','estas',
        'son','era','ser','hay','muy','bien','todo','todos','cada','porque',
        'pero','más','con','sin','desde','hasta','sobre','entre','como',
    }
    transcript_files = list(transcripts_dir.glob("*.json"))
    src_names = list(edl.get("sources", {}).keys())
    
    tf_to_use = None
    for tf in transcript_files:
        if any(tf.stem in s or s in tf.stem for s in src_names) or len(transcript_files) == 1:
            tf_to_use = tf
            break
            
    if tf_to_use and tf_to_use.exists():
        text = json.loads(tf_to_use.read_text(encoding="utf-8")).get("text", "")
        if text:
            clean = re.sub(r'[\u00bf\u00a1!?.,;:\(\)\[\]"\u2026]', ' ', text)
            words = [w.strip() for w in clean.split() if w.strip()]
            meaningful = [
                w for w in words
                if w.lower() not in STOP and len(w) > 2
            ][:max_words]
            slug = '-'.join(meaningful).lower()
            # Quitar acentos y caracteres no ASCII
            slug = ''.join(
                c for c in unicodedata.normalize('NFD', slug)
                if unicodedata.category(c) != 'Mn'
            )
            slug = re.sub(r'[^a-z0-9\-]', '', slug)
            if slug:
                return slug
    return "video"


def _ff() -> str:
    from helpers.utils import ffmpeg_bin
    return ffmpeg_bin()


def run(cmd: list[str], **kwargs) -> None:
    result = subprocess.run(cmd, **kwargs)
    if result.returncode != 0:
        sys.exit(f"FFmpeg falló: {' '.join(cmd[:6])}...")


def extract_segment(source: Path, start: float, end: float, out: Path,
                    grade: str, quality: dict, aspect: dict | None = None,
                    crop_x: float = 0.5) -> None:
    if aspect is None:
        aspect = ASPECT["landscape"]
    duration = end - start
    fade_start = max(0.0, duration - FADE_MS)

    vf_parts = [f"scale={aspect['scale']}"]
    if aspect.get("crop"):
        w, h = aspect["crop"].split(":")
        vf_parts.append(f"crop={w}:{h}:(iw-{w})*{crop_x:.2f}:0")
    if aspect.get("pad"):
        vf_parts.append(f"pad={aspect['pad']}")
    grade_filter = GRADES.get(grade, "")
    if grade_filter:
        vf_parts.append(grade_filter)
    vf = ",".join(vf_parts)

    cmd = [
        _ff(), "-y",
        "-ss", str(start), "-i", str(source), "-t", str(duration),
        "-vf", vf,
        "-af", f"afade=t=in:st=0:d={FADE_MS},afade=t=out:st={fade_start}:d={FADE_MS}",
        "-c:v", "libx264", "-preset", quality["preset"], "-crf", str(quality["crf"]),
        "-pix_fmt", "yuv420p", "-r", str(aspect["fps"]),
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart",
        str(out),
    ]
    run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)


def build_srt(ranges: list[dict], sources: dict, transcripts_dir: Path) -> str | None:
    """Genera SRT alineado con la línea de tiempo de salida."""
    lines: list[str] = []
    idx = 1
    output_offset = 0.0

    for rng in ranges:
        src_name = rng["source"]
        seg_start = rng["start"]
        seg_end = rng["end"]
        transcript_file = transcripts_dir / f"{src_name}.json"

        if not transcript_file.exists():
            output_offset += seg_end - seg_start
            continue

        data = json.loads(transcript_file.read_text(encoding="utf-8"))
        words = [w for w in data.get("words", [])
                 if w["start"] >= seg_start and w["end"] <= seg_end]

        chunk: list[str] = []
        chunk_start: float | None = None
        chunk_end: float | None = None

        def flush_chunk() -> None:
            nonlocal idx
            if not chunk or chunk_start is None:
                return
            out_s = chunk_start - seg_start + output_offset
            out_e = (chunk_end or chunk_start) - seg_start + output_offset
            lines.append(str(idx))
            lines.append(f"{_srt_ts(out_s)} --> {_srt_ts(out_e)}")
            lines.append(" ".join(chunk).upper())
            lines.append("")
            idx += 1
            chunk.clear()

        for w in words:
            if chunk_start is None:
                chunk_start = w["start"]
            chunk.append(w["text"])
            chunk_end = w["end"]
            if len(chunk) >= 2:
                flush_chunk()
                chunk_start = None

        flush_chunk()
        output_offset += seg_end - seg_start

    return "\n".join(lines) if lines else None


def _srt_ts(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def render(edl_path: Path, mode: str = "final",
           aspect: str = "landscape", crop_x: float = 0.5) -> Path:
    edl = json.loads(edl_path.read_text(encoding="utf-8"))
    quality = QUALITY[mode]
    asp = ASPECT.get(aspect, ASPECT["landscape"])

    sources = {k: Path(v).resolve() for k, v in edl["sources"].items()}
    ranges = edl["ranges"]
    overlays = edl.get("overlays", [])
    build_subtitles = edl.get("subtitles", False)

    edit_dir = edl_path.parent
    suffix = f"_{aspect}" if aspect != "landscape" else ""
    segments_dir = edit_dir / f"segments{suffix}"
    segments_dir.mkdir(parents=True, exist_ok=True)
    transcripts_dir = edit_dir / "transcripts"

    print(f"[render] modo={mode}, aspecto={aspect}, {len(ranges)} segmentos")

    # 1. Extraer segmentos
    segment_files: list[Path] = []
    for i, rng in enumerate(ranges):
        src = sources[rng["source"]]
        seg_out = segments_dir / f"seg_{i:03d}.mp4"
        grade = rng.get("grade") or edl.get("grade", "auto")
        print(f"  seg {i:03d}: {rng['source']} [{rng['start']:.2f}–{rng['end']:.2f}]  grade={grade}")
        extract_segment(src, rng["start"], rng["end"], seg_out, grade, quality, asp, crop_x)
        segment_files.append(seg_out)

    # 2. Concatenar
    concat_list = edit_dir / "_concat.txt"
    concat_list.write_text(
        "\n".join(f"file '{f}'" for f in segment_files), encoding="utf-8"
    )
    base_mp4 = edit_dir / "base.mp4"
    run([
        _ff(), "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-c", "copy",
        "-movflags", "+faststart", str(base_mp4),
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    print(f"  base.mp4 generado")

    working = base_mp4

    # 3. Overlays de animación
    for ov in overlays:
        ov_file = Path(ov["file"]).resolve()
        t = ov["start_in_output"]
        dur = ov.get("duration", 5.0)
        ov_out = edit_dir / "with_overlay.mp4"
        cmd = [
            _ff(), "-y", "-i", str(working), "-i", str(ov_file),
            "-filter_complex",
            f"[1:v]setpts=PTS-STARTPTS+{t}/TB[a1];"
            f"[0:v][a1]overlay=enable='between(t,{t},{t+dur})'[outv]",
            "-map", "[outv]", "-map", "0:a",
            "-c:v", "libx264", "-preset", quality["preset"], "-crf", str(quality["crf"]),
            "-c:a", "copy", "-movflags", "+faststart", str(ov_out),
        ]
        run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        working = ov_out
        print(f"  overlay aplicado: {ov_file.name} en t={t}s")


    # 3.5. Overlays de imágenes e iconos con efecto de sonido "pop"
    image_overlays = edl.get("image_overlays", [])
    if image_overlays:
        # Construimos el comando de FFmpeg
        cmd = [_ff(), "-y", "-i", str(working)]
        
        # Añadir inputs de imágenes
        for ov in image_overlays:
            img_path = (edit_dir.parent / ov["file"]).resolve()
            cmd += ["-i", str(img_path)]
            
        # Añadir input de sonido pop
        pop_sound = (edit_dir / "pop.wav").resolve()
        if not pop_sound.exists():
            from helpers.sounds import generate_pop_sound
            generate_pop_sound(pop_sound)
        cmd += ["-i", str(pop_sound)]
        
        # El índice de entrada para el pop es len(image_overlays) + 1
        pop_input_idx = len(image_overlays) + 1
        
        filter_complex_parts = []
        vf_chain = "[0:v]"
        
        for idx, ov in enumerate(image_overlays):
            img_idx = idx + 1
            start_t = ov["start"]
            end_t = ov["end"]
            img_path = (edit_dir.parent / ov["file"]).resolve()
            bg_hex = get_image_bg_hex(img_path)
            
            # Filtro para quitar fondo de color e iconizar a 300px
            colorkey_filter = f"colorkey={bg_hex}:0.2:0.1,scale=300:-1"
            v_in_name = f"img{img_idx}"
            cmd_filter = f"[{img_idx}:v]{colorkey_filter}[{v_in_name}]"
            filter_complex_parts.append(cmd_filter)
            
            # Centrado abajo de los subtítulos: y=1200 (para formato vertical) o 700 (cuadrado/horizontal)
            v_out_name = f"v_ov{img_idx}"
            y_pos = "1200" if aspect == "vertical" else "700"
            overlay_filter = f"{vf_chain}[{v_in_name}]overlay=x=(W-w)/2:y={y_pos}:enable='between(t,{start_t},{end_t})'[{v_out_name}]"
            filter_complex_parts.append(overlay_filter)
            
            vf_chain = f"[{v_out_name}]"
            
        # División del sonido para los N eventos de pop
        audio_split = f"[{pop_input_idx}:a]asplit={len(image_overlays)}"
        split_names = [f"pop{i}" for i in range(len(image_overlays))]
        audio_split += "".join(f"[{name}]" for name in split_names)
        filter_complex_parts.append(audio_split)
        
        # Delay de cada pop a su respectivo segundo
        delay_names = []
        for idx, ov in enumerate(image_overlays):
            start_ms = int(ov["start"] * 1000)
            d_name = f"pop_d{idx}"
            delay_names.append(d_name)
            filter_complex_parts.append(f"[{split_names[idx]}]adelay={start_ms}|{start_ms}[{d_name}]")
            
        # Mezclar todos los sonidos
        mix_inputs = "[0:a]" + "".join(f"[{n}]" for n in delay_names)
        filter_complex_parts.append(f"{mix_inputs}amix=inputs={len(image_overlays)+1}:duration=first[outa]")
        
        complex_filter_str = ";".join(filter_complex_parts)
        ov_out = edit_dir / "with_images.mp4"
        
        cmd += [
            "-filter_complex", complex_filter_str,
            "-map", vf_chain, "-map", "[outa]",
            "-c:v", "libx264", "-preset", quality["preset"], "-crf", str(quality["crf"]),
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
            "-movflags", "+faststart", str(ov_out)
        ]
        
        run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        working = ov_out
        print("  Imágenes de conceptos clave y sonidos pop aplicados.")

    # 4. Subtítulos ASS word-by-word (siempre al final, por encima de overlays)
    exportados_dir = edit_dir / "exportados"
    exportados_dir.mkdir(parents=True, exist_ok=True)
    title = _extract_title(edl, transcripts_dir)
    final_mp4 = exportados_dir / f"{title}_{aspect}.mp4"
    if build_subtitles and transcripts_dir.exists():
        from helpers.subtitles import generate_ass, load_highlights

        # Buscar el transcript que corresponde a la primera fuente del EDL
        transcript_files = list(transcripts_dir.glob("*.json"))
        highlights_path = edit_dir / "highlights.json"
        hl_words, em_words = load_highlights(highlights_path)

        ass_path = edit_dir / "subtitles.ass"
        generated = False
        for tf in transcript_files:
            # Usamos el transcript cuyo nombre coincide con alguna fuente
            src_names = list(sources.keys())
            if any(tf.stem in s or s in tf.stem for s in src_names) or len(transcript_files) == 1:
                generate_ass(
                    transcript_path=tf,
                    edl_ranges=ranges,
                    output_path=ass_path,
                    highlight_words=hl_words,
                    emphasis_words=em_words,
                    aspect=aspect,
                    title_header=edl.get("title"),
                )
                generated = True
                break

        if generated and ass_path.exists():
            # FFmpeg en Windows necesita ruta con / y : escapado
            ass_escaped = str(ass_path).replace("\\", "/")
            # En Windows el drive letter (C:) necesita escaparse como C\:
            if len(ass_escaped) > 1 and ass_escaped[1] == ":":
                ass_escaped = ass_escaped[0] + "\\:" + ass_escaped[2:]
            run([
                _ff(), "-y", "-i", str(working),
                "-vf", f"ass='{ass_escaped}'",
                "-c:v", "libx264", "-preset", quality["preset"], "-crf", str(quality["crf"]),
                "-c:a", "copy", "-movflags", "+faststart", str(final_mp4),
            ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            print(f"  subtítulos ASS aplicados ({len(hl_words)} highlights, {len(em_words)} emphasis)")
        else:
            working.replace(final_mp4)
    else:
        working.replace(final_mp4)

    print(f"\nRenderizado completo: {final_mp4}")
    return final_mp4


def main() -> None:
    ap = argparse.ArgumentParser(description="Renderiza un EDL a MP4")
    ap.add_argument("edl", type=Path, help="Ruta al fichero edl.json")
    ap.add_argument("--mode", choices=["final", "preview", "draft"], default="final")
    ap.add_argument("--aspect", choices=["landscape", "vertical", "square"], default="landscape",
                    help="Formato de salida (landscape=16:9, vertical=9:16, square=1:1)")
    ap.add_argument("--crop-x", type=float, default=0.5,
                    help="Posición del crop vertical (0.0=izq, 0.5=centro, 1.0=der)")
    args = ap.parse_args()

    edl_path = args.edl.resolve()
    if not edl_path.exists():
        sys.exit(f"EDL no encontrado: {edl_path}")

    render(edl_path, mode=args.mode, aspect=args.aspect, crop_x=args.crop_x)


if __name__ == "__main__":
    main()
