"""Utilidades compartidas — detección de FFmpeg en Windows/Unix."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

# Rutas de fallback donde winget suele instalar FFmpeg en Windows
_WINGET_FFMPEG_PATTERNS = [
    Path.home() / "AppData/Local/Microsoft/WinGet/Packages",
]


def find_ffmpeg() -> str:
    """Devuelve la ruta al ejecutable ffmpeg. Busca en PATH y en rutas conocidas de winget."""
    # 1. Intentar desde PATH (funciona tras reiniciar terminal o en Linux/Mac)
    found = shutil.which("ffmpeg")
    if found:
        return found

    # 2. Buscar en rutas de winget (Windows)
    for base in _WINGET_FFMPEG_PATTERNS:
        if not base.exists():
            continue
        for candidate in sorted(base.glob("Gyan.FFmpeg*/**/bin/ffmpeg.exe"), reverse=True):
            if candidate.exists():
                return str(candidate)

    # 3. CapCut instala ffmpeg — usarlo como último recurso
    capcut_base = Path.home() / "AppData/Local/CapCut/Apps"
    if capcut_base.exists():
        for candidate in sorted(capcut_base.glob("*/ffmpeg.exe"), reverse=True):
            if candidate.exists():
                return str(candidate)

    raise FileNotFoundError(
        "FFmpeg no encontrado. Opciones:\n"
        "  1. Reinicia la terminal (el PATH de winget se aplica en sesiones nuevas)\n"
        "  2. Añade FFmpeg al PATH manualmente\n"
        "  3. winget install --id Gyan.FFmpeg"
    )


def ffmpeg_bin() -> str:
    return find_ffmpeg()


def ffprobe_bin() -> str:
    """Devuelve la ruta a ffprobe (siempre junto a ffmpeg)."""
    ff = find_ffmpeg()
    probe = str(Path(ff).parent / ("ffprobe.exe" if os.name == "nt" else "ffprobe"))
    return probe if Path(probe).exists() else shutil.which("ffprobe") or "ffprobe"
