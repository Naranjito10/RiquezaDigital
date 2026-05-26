"""
Convierte transcripciones JSON (word-level) en takes_packed.md:
un índice compacto con rangos de tiempo por frase, optimizado para edición.

Uso:
    uv run helpers/pack_transcripts.py edit/transcripts/
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


SILENCE_BREAK = 0.5  # segundos de silencio para cortar frase


def pack_words(words: list[dict], source_name: str) -> list[str]:
    """Agrupa palabras en frases según silencios. Devuelve líneas markdown."""
    if not words:
        return []

    lines = []
    phrase: list[dict] = []

    def flush(p: list[dict]) -> None:
        if not p:
            return
        start = p[0]["start"]
        end = p[-1]["end"]
        text = " ".join(w["text"] for w in p).strip()
        lines.append(f"[{start:.2f}-{end:.2f}] {text}")

    for i, w in enumerate(words):
        if phrase and w["start"] - phrase[-1]["end"] >= SILENCE_BREAK:
            flush(phrase)
            phrase = []
        phrase.append(w)

    flush(phrase)
    return lines


def main() -> None:
    ap = argparse.ArgumentParser(description="Empaqueta transcripciones en takes_packed.md")
    ap.add_argument("transcripts_dir", type=Path, help="Carpeta con ficheros .json")
    ap.add_argument("--output", type=Path, default=None,
                    help="Ruta de salida (por defecto: transcripts_dir/takes_packed.md)")
    args = ap.parse_args()

    t_dir = args.transcripts_dir.resolve()
    out_path = args.output or (t_dir / "takes_packed.md")

    json_files = sorted(t_dir.glob("*.json"))
    if not json_files:
        print(f"No se encontraron ficheros .json en {t_dir}")
        return

    sections: list[str] = []
    for jf in json_files:
        data = json.loads(jf.read_text(encoding="utf-8"))
        words = data.get("words", [])
        lines = pack_words(words, jf.stem)
        sections.append(f"## {jf.stem}\n\n" + "\n".join(lines))
        print(f"  {jf.stem}: {len(lines)} frases")

    out_path.write_text("\n\n".join(sections), encoding="utf-8")
    print(f"\nGuardado: {out_path}")


if __name__ == "__main__":
    main()
