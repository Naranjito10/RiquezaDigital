"""
Exporta un EDL en tres formatos simultáneos: landscape (16:9), vertical (9:16), square (1:1).

Uso:
    uv run helpers/multi_format.py edit/edl.json
    uv run helpers/multi_format.py edit/edl.json --crop-x 0.3   # ajustar crop horizontal
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import subprocess
import sys
from pathlib import Path


FORMATS = {
    "landscape": {
        "scale": "1920:-2",
        "crop": None,
        "fps": 24,
        "suffix": "landscape",
        "label": "16:9  1920×1080",
    },
    "vertical": {
        "scale": "-2:1920",
        "crop": "1080:1920",      # crop x se ajusta con --crop-x
        "fps": 30,
        "suffix": "vertical",
        "label": "9:16  1080×1920",
    },
    "square": {
        "scale": "1080:1080:force_original_aspect_ratio=decrease",
        "crop": None,
        "pad": "1080:1080:(ow-iw)/2:(oh-ih)/2:black",
        "fps": 30,
        "suffix": "square",
        "label": "1:1   1080×1080",
    },
}

GRADES = {
    "warm_cinematic": "curves=red='0/0 0.5/0.55 1/1':green='0/0 0.5/0.5 1/0.95':blue='0/0 0.5/0.45 1/0.85'",
    "cool_modern":    "curves=red='0/0 0.5/0.45 1/0.9':green='0/0 0.5/0.5 1/1':blue='0/0 0.5/0.55 1/1'",
    "bw_contrast":    "hue=s=0,curves=all='0/0 0.3/0.2 0.7/0.85 1/1'",
    "auto":           "",
}

FADE_MS = 0.03
QUALITY_CRF = 20
QUALITY_PRESET = "fast"

SUBTITLE_STYLE = (
    "FontName=Arial,FontSize=18,Bold=1,"
    "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
    "BorderStyle=1,Outline=2,Alignment=2,MarginV=90"
)


def build_vf(fmt: dict, grade_filter: str, crop_x: float = 0.5) -> str:
    parts: list[str] = []

    if fmt.get("crop"):
        w, h = fmt["crop"].split(":")
        # crop_x=0.5 centra, 0.0=izquierda, 1.0=derecha
        x_expr = f"(iw-{w})*{crop_x:.2f}"
        parts.append(f"scale={fmt['scale']}")
        parts.append(f"crop={w}:{h}:{x_expr}:0")
    elif fmt.get("pad"):
        parts.append(f"scale={fmt['scale']}")
        parts.append(f"pad={fmt['pad']}")
    else:
        parts.append(f"scale={fmt['scale']}")

    if grade_filter:
        parts.append(grade_filter)

    return ",".join(parts)


def _ff() -> str:
    from helpers.utils import ffmpeg_bin
    return ffmpeg_bin()


def extract_segment(source: Path, start: float, end: float, out: Path,
                    vf: str, fps: int) -> None:
    duration = end - start
    fade_start = max(0.0, duration - FADE_MS)
    cmd = [
        _ff(), "-y",
        "-ss", str(start), "-i", str(source), "-t", str(duration),
        "-vf", vf,
        "-af", f"afade=t=in:st=0:d={FADE_MS},afade=t=out:st={fade_start}:d={FADE_MS}",
        "-c:v", "libx264", "-preset", QUALITY_PRESET, "-crf", str(QUALITY_CRF),
        "-pix_fmt", "yuv420p", "-r", str(fps),
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000",
        "-movflags", "+faststart", str(out),
    ]
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg falló en {out.name}: {result.stderr.decode()[-300:]}")


def render_format(edl: dict, fmt_name: str, fmt: dict, edit_dir: Path,
                  crop_x: float) -> Path:
    sources = {k: Path(v).resolve() for k, v in edl["sources"].items()}
    ranges = edl["ranges"]
    grade_key = edl.get("grade", "auto")
    grade_filter = GRADES.get(grade_key, "")

    vf = build_vf(fmt, grade_filter, crop_x)

    segments_dir = edit_dir / "segments" / fmt_name
    segments_dir.mkdir(parents=True, exist_ok=True)

    segment_files: list[Path] = []
    for i, rng in enumerate(ranges):
        src = sources[rng["source"]]
        seg_out = segments_dir / f"seg_{i:03d}.mp4"
        extract_segment(src, rng["start"], rng["end"], seg_out, vf, fmt["fps"])
        segment_files.append(seg_out)

    concat_list = segments_dir / "_concat.txt"
    concat_list.write_text("\n".join(f"file '{f}'" for f in segment_files), encoding="utf-8")

    out_path = edit_dir / "exportados" / f"{fmt['suffix']}.mp4"
    result = subprocess.run([
        _ff(), "-y", "-f", "concat", "-safe", "0",
        "-i", str(concat_list), "-c", "copy",
        "-movflags", "+faststart", str(out_path),
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"Concat falló ({fmt_name}): {result.stderr.decode()[-300:]}")

    return out_path


def export_all(edl_path: Path, crop_x: float = 0.5) -> dict[str, Path]:
    edl = json.loads(edl_path.read_text(encoding="utf-8"))
    edit_dir = edl_path.parent

    print(f"[exportar] EDL: {edl_path.name} | {len(edl['ranges'])} segmentos | crop_x={crop_x}")
    print(f"           Formatos: {', '.join(f['label'] for f in FORMATS.values())}\n")

    (edit_dir / "exportados").mkdir(parents=True, exist_ok=True)

    results: dict[str, Path] = {}
    errors: list[str] = []

    def render_one(fmt_name: str) -> tuple[str, Path | None]:
        fmt = FORMATS[fmt_name]
        print(f"  ► {fmt['label']}...", flush=True)
        try:
            out = render_format(edl, fmt_name, fmt, edit_dir, crop_x)
            size_mb = out.stat().st_size / (1024 * 1024)
            print(f"  ✓ {fmt['label']} → {out.name} ({size_mb:.1f} MB)")
            return fmt_name, out
        except Exception as e:
            print(f"  ✗ {fmt['label']} — ERROR: {e}")
            return fmt_name, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {executor.submit(render_one, name): name for name in FORMATS}
        for future in concurrent.futures.as_completed(futures):
            name, path = future.result()
            if path:
                results[name] = path
            else:
                errors.append(name)

    print(f"\n{'─'*50}")
    print(f"Exportados: {len(results)}/3 formatos")
    for name, path in results.items():
        print(f"  {FORMATS[name]['label']} → {path}")
    if errors:
        print(f"  Errores: {', '.join(errors)}")

    return results


def main() -> None:
    ap = argparse.ArgumentParser(description="Exporta un EDL en 3 formatos simultáneos")
    ap.add_argument("edl", type=Path, help="Ruta al edl.json")
    ap.add_argument("--crop-x", type=float, default=0.5,
                    help="Posición horizontal del crop vertical (0.0=izq, 0.5=centro, 1.0=der)")
    args = ap.parse_args()

    edl_path = args.edl.resolve()
    if not edl_path.exists():
        sys.exit(f"EDL no encontrado: {edl_path}")

    export_all(edl_path, crop_x=args.crop_x)


if __name__ == "__main__":
    main()
