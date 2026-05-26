# Skill: Video Marketing — Promo / Testimonio / Demo de Producto

Produce un vídeo de marketing profesional y lo exporta automáticamente en tres formatos (landscape, vertical, square) para distribución multicanal. Un solo EDL → tres plataformas.

## Archetype Narrativo

```
PROBLEMA (0–20s)        ← el dolor específico que tu audiencia siente HOY
SOLUCIÓN (20–50s)       ← Riqueza Digital como la respuesta
BENEFICIOS (50s–1:30)   ← 3 beneficios concretos y medibles
PRUEBA SOCIAL (1:30–2m) ← resultado real, testimonio, número
CTA (últimos 20s)       ← una sola acción, sin ambigüedad
```

## Configuración

- **Grade:** `warm_cinematic`
- **Subtítulos:** branded — blanco sobre fondo dorado semi-transparente
- **FPS:** 24 (landscape/square), 30 (vertical)
- **Formato:** multi-output (los tres a la vez)
- **Duración:** 90s–3min landscape; ≤60s vertical
- **Animaciones:** intro de marca obligatoria, lower-thirds de datos, outro con CTA

## Proceso Paso a Paso

### 1. Inventariar el material

```bash
uv run editar.py transcribir input/$ARGUMENTS --language es
uv run editar.py empaquetar edit/transcripts/
```

Buscar en `takes_packed.md`:
- La frase que mejor describe el PROBLEMA del cliente
- Los 3 beneficios más concretos mencionados
- Cualquier número o resultado real ("aumenté mis ingresos X%")
- El CTA más claro y directo

### 2. Proponer estrategia (ESPERAR CONFIRMACIÓN)

Incluir:
- Estructura PROBLEMA→SOLUCIÓN→BENEFICIOS→PRUEBA→CTA con timestamps
- Grade elegido y justificación
- Animaciones a usar (intro marca, lower-thirds, outro)
- Duración estimada por formato
- Si el material permite los 3 formatos o solo algunos

### 3. Construir el EDL

```json
{
  "version": 1,
  "sources": {"promo": "input/NOMBRE.mp4"},
  "ranges": [
    {"source": "promo", "start": 5.0,  "end": 25.0, "beat": "PROBLEMA",     "reason": "dolor del cliente"},
    {"source": "promo", "start": 30.0, "end": 55.0, "beat": "SOLUCION",     "reason": "RD como respuesta"},
    {"source": "promo", "start": 60.0, "end": 115.0,"beat": "BENEFICIOS",   "reason": "3 beneficios clave"},
    {"source": "promo", "start": 120.0,"end": 145.0,"beat": "PRUEBA",       "reason": "resultado real"},
    {"source": "promo", "start": 148.0,"end": 165.0,"beat": "CTA",          "reason": "llamada a la acción"}
  ],
  "overlays": [
    {"file": "animations/intro/output.mp4",  "start_in_output": 0.0,  "duration": 4.0},
    {"file": "animations/outro/output.mp4",  "start_in_output": 145.0,"duration": 8.0}
  ],
  "grade": "warm_cinematic",
  "subtitles": true
}
```

### 4. Render borrador landscape

```bash
uv run editar.py renderizar edit/edl.json --modo borrador
```

### 5. Exportar los 3 formatos de una vez

Una vez aprobado el borrador:

```bash
uv run editar.py exportar edit/edl.json
```

Esto genera:
- `edit/final_landscape.mp4` → YouTube, web, LinkedIn (1920×1080)
- `edit/final_vertical.mp4`  → Instagram Reels, TikTok, Shorts (1080×1920)
- `edit/final_square.mp4`    → Feed Instagram, Twitter/X (1080×1080)

### 6. Revisión por formato

**Landscape:** ¿Funciona el encuadre original? ¿CTA se ve bien?  
**Vertical:** ¿El smart crop centra bien la cara? ¿Subtítulos visibles?  
**Square:** ¿El contenido cabe? ¿No se cortan datos o textos importantes?

Si el vertical o square no funcionan con el crop automático, ajusta manualmente:

```bash
uv run editar.py renderizar edit/edl.json --aspecto vertical --crop-x 0.5
```

### 7. Copiar a output/ y anotar

```bash
cp edit/final_landscape.mp4 output/NOMBRE_landscape.mp4
cp edit/final_vertical.mp4  output/NOMBRE_vertical.mp4
cp edit/final_square.mp4    output/NOMBRE_square.mp4
```

Añadir entrada a `project.md` con resultados y qué formato funcionó mejor.

## Animaciones de Marca para Marketing

Estas animaciones deben existir antes de renderizar:
- `animations/intro/` — ya creada (intro dorada Riqueza Digital)
- `animations/outro/` — CTA final con "Enlace en bio" o URL
- `animations/lower-third-dato/` — overlay para mostrar un número/estadística
- `animations/testimonio/` — marco para cita de cliente

Para crear una nueva:
```bash
# Crea animations/NOMBRE/composition.html
# Edita el HTML con GSAP
uv run editar.py animar animations/NOMBRE/
```

## Reglas de Marketing

1. **El PROBLEMA debe doler** — si no genera empatía en 20s, reescribe
2. **Un solo CTA** — múltiples CTAs = cero conversiones
3. **Los números son prueba social** — "el 73% de mis alumnos..." > "muchos alumnos..."
4. **Vertical primero en mente** — si el encuadre no funciona en 9:16, reconsidera la grabación
5. **Guarda el EDL** — los EDLs de marketing exitosos son plantillas de oro para futuras campañas
