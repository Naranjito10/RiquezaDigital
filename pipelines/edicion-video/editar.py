"""
Estudio de Edición de Vídeo — Riqueza Digital
==============================================
Punto de entrada principal. Orquesta: transcripción → análisis → corte → animación → renderizado.

Comandos:
    uv run editar.py transcribir input/mi_video.mp4
    uv run editar.py empaquetar edit/transcripts/
    uv run editar.py renderizar edit/edl.json
    uv run editar.py renderizar edit/edl.json --modo borrador
    uv run editar.py recortar input/video.mp4 --inicio 1.5 --fin 8.0 --salida output/clip.mp4
    uv run editar.py exportar edit/edl.json
    uv run editar.py exportar edit/edl.json --crop-x 0.3
    uv run editar.py animar animations/intro/
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
from pathlib import Path

# Forzar UTF-8 en stdout/stderr para que ✓ y otros símbolos no crasheen en Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

OK = "[OK]"  # Símbolo seguro para consolas sin UTF-8

# Cargar .env si existe
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


def cmd_transcribir(args: argparse.Namespace) -> None:
    from helpers.transcribe import transcribe_one, load_api_key
    video = Path(args.video).resolve()
    if not video.exists():
        sys.exit(f"Vídeo no encontrado: {video}")
    # Por defecto: edit/ en la raíz del proyecto (junto a editar.py), no junto al vídeo
    project_root = Path(__file__).parent
    edit_dir = Path(args.edit_dir).resolve() if args.edit_dir else (project_root / "edit")
    api_key = load_api_key()
    print(f"Transcribiendo {video.name}...")
    out = transcribe_one(video=video, edit_dir=edit_dir, api_key=api_key, language=args.language)
    print(f"Transcripción guardada en: {out}")


def cmd_empaquetar(args: argparse.Namespace) -> None:
    from helpers.pack_transcripts import main as pack_main
    sys.argv = ["pack_transcripts.py", args.transcripts_dir]
    if args.output:
        sys.argv += ["--output", args.output]
    pack_main()


def cmd_renderizar(args: argparse.Namespace) -> None:
    from helpers.render import render
    edl_path = Path(args.edl).resolve()
    modo_map = {"final": "final", "borrador": "draft", "previo": "preview"}
    modo = modo_map.get(args.modo, "final")
    aspecto = getattr(args, "aspecto", "landscape") or "landscape"
    crop_x = getattr(args, "crop_x", 0.5) or 0.5
    render(edl_path, mode=modo, aspect=aspecto, crop_x=crop_x)


def cmd_exportar(args: argparse.Namespace) -> None:
    from helpers.multi_format import export_all
    edl_path = Path(args.edl).resolve()
    if not edl_path.exists():
        sys.exit(f"EDL no encontrado: {edl_path}")
    export_all(edl_path, crop_x=args.crop_x)


def cmd_recortar(args: argparse.Namespace) -> None:
    """Recorte rápido sin transcripción ni EDL."""
    video = Path(args.video).resolve()
    salida = Path(args.salida).resolve()
    salida.parent.mkdir(parents=True, exist_ok=True)

    inicio = args.inicio
    fin = args.fin
    duracion = fin - inicio if fin else None

    cmd = ["ffmpeg", "-y", "-ss", str(inicio), "-i", str(video)]
    if duracion:
        cmd += ["-t", str(duracion)]
    cmd += ["-c", "copy", str(salida)]

    print(f"Recortando {video.name} [{inicio}s → {fin}s] → {salida.name}")
    result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if result.returncode != 0:
        sys.exit(f"Error en recorte: {result.stderr.decode()[-500:]}")
    print(f"{OK} Guardado: {salida}")


def cmd_animar(args: argparse.Namespace) -> None:
    """Renderiza una composición HyperFrames a MP4."""
    comp_dir = Path(args.directorio).resolve()
    if not comp_dir.exists():
        sys.exit(f"Directorio no encontrado: {comp_dir}")

    html_file = comp_dir / "composition.html"
    if not html_file.exists():
        sys.exit(f"No se encontró composition.html en {comp_dir}")

    print(f"Renderizando animación: {comp_dir.name}...")
    result = subprocess.run(
        ["npx", "hyperframes", "render", str(comp_dir)],
        cwd=str(Path(__file__).parent),
    )
    if result.returncode != 0:
        sys.exit("Error al renderizar animación con HyperFrames")
    print(f"{OK} Animación renderizada en {comp_dir}/output.mp4")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Estudio de edición de vídeo — Riqueza Digital",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="comando", required=True)

    # transcribir
    p_tr = sub.add_parser("transcribir", help="Transcribe un vídeo con Whisper")
    p_tr.add_argument("video", help="Ruta al vídeo")
    p_tr.add_argument("--language", default=None, help="Código idioma (es, en...)")
    p_tr.add_argument("--edit-dir", default=None, help="Carpeta de trabajo")
    p_tr.set_defaults(func=cmd_transcribir)

    # empaquetar
    p_pk = sub.add_parser("empaquetar", help="Genera takes_packed.md desde transcripciones")
    p_pk.add_argument("transcripts_dir", help="Carpeta con ficheros JSON")
    p_pk.add_argument("--output", default=None, help="Fichero de salida")
    p_pk.set_defaults(func=cmd_empaquetar)

    # renderizar
    p_rn = sub.add_parser("renderizar", help="Renderiza un EDL a MP4 final")
    p_rn.add_argument("edl", help="Ruta al edl.json")
    p_rn.add_argument("--modo", choices=["final", "borrador", "previo"], default="final")
    p_rn.add_argument("--aspecto", choices=["landscape", "vertical", "square"], default="landscape",
                      help="Formato de salida (landscape=16:9, vertical=9:16, square=1:1)")
    p_rn.add_argument("--crop-x", type=float, default=0.5, dest="crop_x",
                      help="Posición del crop vertical (0.0=izq, 0.5=centro, 1.0=der)")
    p_rn.set_defaults(func=cmd_renderizar)

    # exportar (un EDL, tres formatos)
    p_ex = sub.add_parser("exportar", help="Exporta un EDL en 3 formatos: landscape, vertical, square")
    p_ex.add_argument("edl", help="Ruta al edl.json")
    p_ex.add_argument("--crop-x", type=float, default=0.5, dest="crop_x",
                      help="Posición del crop vertical (0.0=izq, 0.5=centro, 1.0=der)")
    p_ex.set_defaults(func=cmd_exportar)

    # recortar
    p_rc = sub.add_parser("recortar", help="Recorte rápido de vídeo por tiempos")
    p_rc.add_argument("video", help="Vídeo de entrada")
    p_rc.add_argument("--inicio", type=float, required=True, help="Segundo de inicio")
    p_rc.add_argument("--fin", type=float, required=True, help="Segundo de fin")
    p_rc.add_argument("--salida", required=True, help="Fichero de salida")
    p_rc.set_defaults(func=cmd_recortar)

    # animar
    p_an = sub.add_parser("animar", help="Renderiza una composición HyperFrames")
    p_an.add_argument("directorio", help="Carpeta con composition.html")
    p_an.set_defaults(func=cmd_animar)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
