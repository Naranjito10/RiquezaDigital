# Riqueza Digital — Registro de Sesiones de Edición

Este fichero mantiene continuidad entre sesiones. Añade una entrada al final después de cada sesión.

---

## 2026-05-14 — Setup inicial del estudio

**Completado:**
- Instalado FFmpeg v8.1.1, uv 0.11.14, Node.js v22.14.0
- HyperFrames v0.6.6 instalado (npm)
- Pipeline Python adaptado de browser-use/video-use con OpenAI Whisper
- Animación de intro creada: `animations/intro/composition.html`
- 3 skills creados: `/video-educativo`, `/video-social`, `/video-marketing`
- Multi-format export implementado: `uv run editar.py exportar edit/edl.json`

**Pendiente:**
- Configurar `.env` con OPENAI_API_KEY
- Primer vídeo real de prueba
- Ajustar colores de la animación intro si es necesario

**Notas:**
- Usar `--modo borrador` siempre en primera pasada (10x más rápido)
- Los EDLs buenos se guardan en `edit/plantillas/` para reutilizar
- El grade `warm_cinematic` funciona bien para talking heads en interior

---

## 2026-05-14 — Primer vídeo real: claude_agentico.MOV

**Completado:**
- Transcripción con Whisper: `edit/transcripts/clip.json` (word-level timestamps)
- EDL construido: 4 beats (GANCHO → PROBLEMA_SOLUCIÓN → EJEMPLOS → CTA), 56s total
- Sistema de subtítulos ASS word-by-word implementado (`helpers/subtitles.py`)
  - Colores de marca: blanco por defecto, morado #8000FC para highlights, rosa #E300FF para énfasis
  - Fix de substring matching: solo coincidencia exacta + palabras >4 caracteres
- Grade aplicado: `cool_modern`
- Highlights configurados en `edit/highlights.json`
- Render final: `edit/final_vertical.mp4` — 26.5 MB — formato 1080×1920
- Fix Unicode Windows: stdout forzado a UTF-8, ✓ reemplazado por [OK] en `editar.py`

**Notas:**
- El vídeo fuente era MOV 1080p — el pipeline lo maneja sin conversión previa
- Grade `cool_modern` funciona bien para vídeos sobre tecnología/IA
- El highlight matching evita falsos positivos en palabras cortas (≤4 chars)
- Para el siguiente vídeo: revisar si falta ajuste de `crop-x` (sujeto centrado/descentrado)

---

<!-- Añade tus propias entradas abajo -->
