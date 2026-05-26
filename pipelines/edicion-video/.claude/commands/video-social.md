# Skill: Video Social — Reels / TikTok / YouTube Shorts

Edita el clip para formato vertical 9:16, máximo 60 segundos, optimizado para retención en los primeros 3 segundos. Ritmo rápido, impacto inmediato.

## Archetype Narrativo

```
GANCHO (0–3s)      ← la frase más impactante del vídeo, sin contexto previo
PROBLEMA (3–15s)   ← el dolor que el espectador reconoce
SOLUCIÓN (15–45s)  ← la respuesta concreta, sin rodeos
CTA (45–60s)       ← qué hacer ahora (seguir, guardar, comentar)
```

**Regla de oro:** Si en los primeros 3 segundos no hay un gancho, el vídeo no funciona en social. Busca primero el gancho en toda la grabación, aunque esté en el minuto 8.

## Configuración

- **Grade:** `cool_modern`
- **Subtítulos:** 2 palabras por línea, TODO EN MAYÚSCULAS, negrita
- **FPS:** 30
- **Formato:** 1080×1920 (vertical 9:16)
- **Duración máxima:** 60 segundos (idealmente 30–45s)
- **Subtítulos:** siempre — el 80% se ve sin audio

## Proceso Paso a Paso

### 1. Buscar el gancho primero (al revés del orden normal)

```bash
uv run editar.py transcribir input/$ARGUMENTS --language es
uv run editar.py empaquetar edit/transcripts/
```

Lee `takes_packed.md` buscando:
- La frase más sorprendente, contraintuitiva o provocadora
- Números llamativos ("gané 3.000€ en...", "el 90% de la gente no sabe...")
- Preguntas que generan curiosidad ("¿por qué los ricos...?")

**Esta frase se convierte en el segundo 0–3 del vídeo**, sin importar cuándo aparece en la grabación original.

### 2. Proponer estructura (ESPERAR CONFIRMACIÓN)

Describe:
- La frase exacta del gancho (con su timestamp original)
- Los rangos del PROBLEMA, SOLUCIÓN y CTA
- Duración total estimada (¿cabe en 60s?)
- Si hay que acelerar algún tramo o cortar más agresivamente

### 3. Construir el EDL vertical

```json
{
  "version": 1,
  "sources": {"src": "input/NOMBRE.mp4"},
  "ranges": [
    {"source": "src", "start": 245.3, "end": 248.1, "beat": "GANCHO",   "reason": "frase más impactante"},
    {"source": "src", "start": 12.0,  "end": 28.5,  "beat": "PROBLEMA", "reason": "plantea el dolor"},
    {"source": "src", "start": 30.0,  "end": 52.0,  "beat": "SOLUCION", "reason": "respuesta concreta"},
    {"source": "src", "start": 55.0,  "end": 62.0,  "beat": "CTA",      "reason": "llamada a la acción"}
  ],
  "grade": "cool_modern",
  "subtitles": true,
  "aspect": "vertical"
}
```

Nota: el GANCHO puede venir de cualquier momento del vídeo original.

### 4. Renderizar en vertical

```bash
uv run editar.py renderizar edit/edl.json --modo borrador --aspecto vertical
```

Revisar:
- ¿El encuadre vertical corta la cara? (ajustar crop si es necesario)
- ¿Los subtítulos se ven grandes y claros?
- ¿El gancho engancha de verdad en los primeros 3 segundos?

### 5. Render final

```bash
uv run editar.py renderizar edit/edl.json --aspecto vertical
```

### 6. Variantes (mismo contenido, diferentes ganchos)

Si tienes varias frases gancho candidatas, crea múltiples EDLs:

```
edit/edl_social_v1.json  ← gancho A
edit/edl_social_v2.json  ← gancho B
```

Renderiza ambos y prueba cuál tiene mejor retención. El que funcione mejor, consérvalo como plantilla.

## Animaciones Típicas para Social

Crea estas en `animations/`:
- `animations/texto-impacto/` — texto grande que entra de golpe (para el gancho)
- `animations/countdown/` — contador 3-2-1 para CTA
- `animations/porcentaje/` — número que sube animado

## Reglas de Oro para Social

1. **Nunca empieces con "Hola, soy..."** — ese es el gancho más débil posible
2. **El primer corte en los primeros 2 segundos** — el salto de corte retiene atención
3. **Subtítulos siempre** — plataformas penalizan si no los tienen
4. **Termina con pregunta** — genera comentarios, el algoritmo lo premia
5. **Guarda el gancho al final** — si el vídeo tiene un momento viral, úsalo al inicio
