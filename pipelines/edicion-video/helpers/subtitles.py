"""
Generador de subtítulos ASS — Riqueza Digital.

Modos:
  • Palabra sola  (default): una palabra a la vez, desaparece antes de la siguiente.
  • Frase progresiva (highlight): cuando la frase contiene una palabra clave,
    se muestra toda la frase construyéndose palabra a palabra. Las palabras
    clave aparecen en color; el resto en blanco.

Uso:
    from helpers.subtitles import generate_ass, load_highlights
    ass_path = generate_ass(transcript_json, edl_ranges, output_path, hl_words, em_words)
"""
from __future__ import annotations

import json
import re
from pathlib import Path


# ── Colores de marca (ASS: &HAABBGGRR&) ──────────────────────────────────────
ASS_WHITE   = "&H00FFFFFF&"   # blanco
ASS_PURPLE  = "&H00FC0080&"   # #8000FC morado principal
ASS_PINK    = "&H00FF00E3&"   # #E300FF rosa neon
ASS_BLACK   = "&H00000000&"   # outline
ASS_SHADOW  = "&H80000000&"   # sombra semitransparente

# Mismas referencias sin & final para usar en override tags inline
_C_PURPLE = "&H00FC0080&"
_C_PINK   = "&H00FF00E3&"
_C_WHITE  = "&H00FFFFFF&"

# ── Parámetros ────────────────────────────────────────────────────────────────
FONT_NAME      = "Inter Tight"
FONT_SIZE      = 82       # palabra sola — grande
PHRASE_SIZE    = 62       # frase progresiva — más pequeño para encajar varias palabras
FONT_BOLD      = -1
OUTLINE_PX     = 4
SHADOW_PX      = 2
MARGIN_V       = 900      # Alignment 2 = bottom-center, MarginV=900 -> centers the baseline exactly
MARGIN_H       = 80
MIN_WORD_DUR   = 0.20     # duración mínima visible (evita palabras con start==end)

# ── Agrupación de frases ──────────────────────────────────────────────────────
PAUSE_THRESHOLD = 0.40    # segundos de silencio para cortar frase
MAX_PHRASE_WORDS = 7      # máximo de palabras por frase


def _ass_ts(seconds: float) -> str:
    """Segundos → formato ASS H:MM:SS.cc"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    cs = round((s - int(s)) * 100)
    return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"


def _normalize(word: str) -> str:
    """Quita puntuación y pone en minúsculas para comparar con highlight_set."""
    return re.sub(r"[¿?¡!,.:;\"'()\[\]…]", "", word).lower().strip()


def _is_highlight(word: str, highlight_set: set[str]) -> bool:
    norm = _normalize(word)
    if not norm:
        return False
    if norm in highlight_set:
        return True
    for h in highlight_set:
        if len(h) > 4 and h == norm:           # coincidencia exacta ya cubierta
            return True
        if len(norm) > 4 and norm == h:
            return True
        # raíz: "agente" → "agentes", "sistema" → "sistemas"
        if len(norm) > 4 and len(h) > 4 and (norm in h or h in norm):
            return True
    return False


def _ass_header(play_res_x: int = 1080, play_res_y: int = 1920) -> str:
    return f"""[Script Info]
ScriptType: v4.00+
WrapStyle: 1
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: {play_res_x}
PlayResY: {play_res_y}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{FONT_NAME},{FONT_SIZE},{ASS_WHITE},{ASS_WHITE},{ASS_BLACK},{ASS_SHADOW},{FONT_BOLD},0,0,0,100,100,2,0,1,{OUTLINE_PX},{SHADOW_PX},2,{MARGIN_H},{MARGIN_H},{MARGIN_V},1
Style: Highlight,{FONT_NAME},{FONT_SIZE},{ASS_PURPLE},{ASS_WHITE},{ASS_BLACK},{ASS_SHADOW},{FONT_BOLD},0,0,0,100,100,2,0,1,{OUTLINE_PX},{SHADOW_PX},2,{MARGIN_H},{MARGIN_H},{MARGIN_V},1
Style: Emphasis,{FONT_NAME},{FONT_SIZE},{ASS_PINK},{ASS_WHITE},{ASS_BLACK},{ASS_SHADOW},{FONT_BOLD},0,0,0,100,100,2,0,1,{OUTLINE_PX},{SHADOW_PX},2,{MARGIN_H},{MARGIN_H},{MARGIN_V},1
Style: Phrase,{FONT_NAME},{PHRASE_SIZE},{ASS_WHITE},{ASS_WHITE},{ASS_BLACK},{ASS_SHADOW},{FONT_BOLD},0,0,0,100,100,2,0,1,{OUTLINE_PX},{SHADOW_PX},2,{MARGIN_H},{MARGIN_H},{MARGIN_V},1
Style: TitleHeader,{FONT_NAME},64,&H00000000&,&H00FFFFFF&,&H00FFFFFF&,&H00000000&,-1,0,0,0,100,100,2,0,1,6,0,8,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""


# ── Agrupación de frases ──────────────────────────────────────────────────────

def _group_phrases(words: list[dict]) -> list[list[dict]]:
    """
    Agrupa palabras en frases basándose en pausas y puntuación.
    Una frase = secuencia de palabras sin pausa larga entre ellas.
    """
    phrases: list[list[dict]] = []
    current: list[dict] = []

    for i, w in enumerate(words):
        current.append(w)
        is_last = i == len(words) - 1
        text = w.get("text", "")

        # Cortar por puntuación de fin de frase
        has_end_punct = bool(re.search(r"[.!?]", text))

        # Cortar por pausa larga al siguiente
        has_long_pause = False
        if not is_last:
            gap = words[i + 1].get("start", 0) - w.get("end", 0)
            has_long_pause = gap > PAUSE_THRESHOLD

        if is_last or len(current) >= MAX_PHRASE_WORDS or has_end_punct or has_long_pause:
            if current:
                phrases.append(current[:])
                current = []

    return phrases


# ── Renderizado ───────────────────────────────────────────────────────────────

def _build_phrase_ass(words_so_far: list[dict], hl_set: set[str], em_set: set[str]) -> str:
    """
    Construye el texto ASS de una frase parcial con colores inline.
    Las palabras clave aparecen en su color; el resto en blanco.
    """
    parts: list[str] = []
    for w in words_so_far:
        text = w.get("text", "").strip()
        if not text:
            continue
        if _is_highlight(text, em_set):
            parts.append(f"{{\\c{_C_PINK}}}{text}{{\\c{_C_WHITE}}}")
        elif _is_highlight(text, hl_set):
            parts.append(f"{{\\c{_C_PURPLE}}}{text}{{\\c{_C_WHITE}}}")
        else:
            parts.append(text)
    return " ".join(parts)


def _render_single_words(
    phrase: list[dict],
    hl_set: set[str],
    em_set: set[str],
    seg_start: float,
    output_offset: float,
    events: list[dict],
) -> None:
    """Modo default: una palabra a la vez, aparece y desaparece."""
    for idx, w in enumerate(phrase):
        word_text = w["text"].strip()
        if not word_text:
            continue

        t_start = max(w["start"] - seg_start + output_offset, 0.001)
        
        # Determinar el fin de la palabra evitando solapamientos con la siguiente
        if idx + 1 < len(phrase):
            next_t = max(phrase[idx + 1]["start"] - seg_start + output_offset, 0.001)
            # Evitar huecos muy cortos si la pausa es menor a 0.4s
            gap = phrase[idx + 1]["start"] - w["end"]
            if gap > 0.4:
                t_end = max(w["end"] - seg_start + output_offset, t_start + 0.1)
            else:
                t_end = next_t
            t_end = min(t_end, next_t)
        else:
            t_end = max(w["end"] - seg_start + output_offset, t_start + MIN_WORD_DUR)

        # Evitar frames de duración negativa o demasiado corta
        if t_end - t_start < 0.05:
            continue

        if _is_highlight(word_text, em_set):
            style = "Emphasis"
        elif _is_highlight(word_text, hl_set):
            style = "Highlight"
        else:
            style = "Default"

        events.append({
            "start": t_start,
            "end": t_end,
            "style": style,
            "text": word_text
        })


def _render_phrase_progressive(
    phrase: list[dict],
    hl_set: set[str],
    em_set: set[str],
    seg_start: float,
    output_offset: float,
    events: list[dict],
) -> None:
    """
    Modo frase progresiva: la frase se construye palabra a palabra.
    Las palabras clave aparecen en color; el resto en blanco.
    Cada línea de diálogo muestra el texto acumulado hasta la palabra actual.
    """
    phrase_end = max(w["end"] for w in phrase) - seg_start + output_offset

    for i, w in enumerate(phrase):
        word_text = w["text"].strip()
        if not word_text:
            continue

        t_start = max(w["start"] - seg_start + output_offset, 0.001)

        # Fin de este segmento = inicio del siguiente
        if i + 1 < len(phrase):
            next_t = max(phrase[i + 1]["start"] - seg_start + output_offset, 0.001)
            t_end = next_t
        else:
            t_end = phrase_end

        # Si el inicio y el fin coinciden o son extremadamente cercanos, se salta para evitar parpadeos
        if t_end - t_start < 0.05:
            continue

        phrase_text = _build_phrase_ass(phrase[: i + 1], hl_set, em_set)
        events.append({
            "start": t_start,
            "end": t_end,
            "style": "Phrase",
            "text": phrase_text
        })


# ── API pública ───────────────────────────────────────────────────────────────

def generate_ass(
    transcript_path: Path,
    edl_ranges: list[dict],
    output_path: Path,
    highlight_words: list[str] | None = None,
    emphasis_words: list[str] | None = None,
    aspect: str = "vertical",
    title_header: str | None = None,
) -> Path:
    """
    Genera .ass con subtítulos duales:
      - Frases sin highlight → cada palabra sola (flash).
      - Frases con highlight → frase progresiva con colores.
    """
    data = json.loads(transcript_path.read_text(encoding="utf-8"))
    all_words: list[dict] = data.get("words", [])

    hl_set = {w.lower().strip() for w in (highlight_words or [])}
    em_set = {w.lower().strip() for w in (emphasis_words or [])}

    res_x, res_y = (1080, 1920) if aspect == "vertical" else (1920, 1080)
    lines = [_ass_header(res_x, res_y)]
    events: list[dict] = []

    output_offset = 0.0
    for rng in edl_ranges:
        seg_start = rng["start"]
        seg_end   = rng["end"]

        seg_words = [
            w for w in all_words
            if w.get("start", 0) >= seg_start and w.get("end", 0) <= seg_end + 0.05
        ]

        # En lugar de usar siempre frase completa si hay un highlight,
        # alternamos estilos dinámicamente palabra por palabra para no aburrir
        phrases = _group_phrases(seg_words)

        for phrase_idx, phrase in enumerate(phrases):
            # Alternancia dinámica: cada 2 frases usamos palabra individual,
            # y en las intermedias usamos progresivo para mantener el dinamismo.
            has_hl = any(
                _is_highlight(w["text"], hl_set) or _is_highlight(w["text"], em_set)
                for w in phrase
            )
            if has_hl and (phrase_idx % 2 == 0):
                _render_phrase_progressive(phrase, hl_set, em_set, seg_start, output_offset, events)
            else:
                _render_single_words(phrase, hl_set, em_set, seg_start, output_offset, events)

        output_offset += seg_end - seg_start

    # Ordenar eventos cronológicamente
    events.sort(key=lambda x: x["start"])

    # Resolver solapamientos entre frases o palabras
    for i in range(len(events) - 1):
        if events[i]["end"] > events[i + 1]["start"]:
            events[i]["end"] = events[i + 1]["start"]

    # Añadir eventos válidos (que tengan una duración mínima útil)
    for e in events:
        if e["end"] - e["start"] >= 0.03:
            lines.append(
                f"Dialogue: 0,{_ass_ts(e['start'])},{_ass_ts(e['end'])},{e['style']},,0,0,0,,{e['text']}"
            )

    # Título persistente de Enrique Rocha en la parte superior durante los primeros 5 segundos
    # Estilo ASS con fondo blanco y letras negras redondeadas arriba en el centro (Alignment 8)
    if title_header:
        lines.append(
            f"Dialogue: 0,0:00:00.00,0:00:05.00,TitleHeader,,0,0,0,,{{\\fnInter Tight}}{{\\fs64}}{{\\b1}}{{\\c&H00000000&}}{{\\3c&H00FFFFFF&}}{{\\4c&H00000000&}}{{\\bord6}}{{\\shad0}}{{\\an8}}{{\\pos(540,150)}}{title_header}"
        )

    content = "\n".join(lines)
    output_path.write_text(content, encoding="utf-8-sig")
    print(f"  ASS generado: {output_path.name} ({len(lines) - 1} eventos)")
    return output_path


def load_highlights(highlights_path: Path) -> tuple[list[str], list[str]]:
    """Lee highlights.json → (highlight_words, emphasis_words)."""
    if not highlights_path.exists():
        return [], []
    data = json.loads(highlights_path.read_text(encoding="utf-8"))
    return data.get("highlight", []), data.get("emphasis", [])
