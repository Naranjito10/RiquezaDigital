# Skill: Video Educativo / Curso

Edita el vídeo como un tutorial estructurado de Riqueza Digital. Sigue el ciclo completo: inventariar → proponer → confirmar → ejecutar → evaluar.

## Archetype Narrativo

```
INTRO (0–15s)      ← gancho + promesa del vídeo
SETUP (15s–2min)   ← contexto, por qué importa
PASOS (2min–Xmin)  ← núcleo: cada paso claramente separado
ERRORES (Xmin–Y)   ← errores comunes a evitar (muy valioso)
RECAP (últimos 60s)← resumen accionable + CTA suave
```

## Configuración

- **Grade:** `warm_cinematic`
- **Subtítulos:** frases de 4–7 palabras, sentence case (no TODO MAYÚSCULAS)
- **FPS:** 24
- **Formato:** 1920×1080 landscape
- **Subtítulos:** sí, siempre
- **Animaciones sugeridas:** lower-third al inicio de cada paso, recap animado al final

## Proceso Paso a Paso

### 1. Inventariar el material

```bash
uv run editar.py transcribir input/$ARGUMENTS --language es
uv run editar.py empaquetar edit/transcripts/
```

Lee `edit/transcripts/takes_packed.md`. Identifica:
- Dónde empieza el contenido real (ignorar preparativos)
- Los momentos de "paso 1", "paso 2", etc.
- Muletillas frecuentes ("eeh", "básicamente", "o sea") a cortar
- Silencios largos (>1s) entre párrafos

### 2. Proponer estrategia (ESPERAR CONFIRMACIÓN)

Describe en 4–6 frases:
- Duración estimada del resultado
- Cómo se distribuyen los bloques INTRO/SETUP/PASOS/ERRORES/RECAP
- Qué fragmentos eliminar y por qué
- Grade y estilo de subtítulos elegido
- Si se añaden lower-thirds numerados

**NO construir el EDL hasta recibir confirmación.**

### 3. Construir el EDL

Formato EDL para educativo:

```json
{
  "version": 1,
  "sources": {"clase": "input/NOMBRE.mp4"},
  "ranges": [
    {"source": "clase", "start": 2.0,  "end": 15.0, "beat": "INTRO",  "reason": "gancho inicial"},
    {"source": "clase", "start": 18.5, "end": 90.0, "beat": "SETUP",  "reason": "contexto del tema"},
    {"source": "clase", "start": 95.0, "end": 210.0,"beat": "PASO_1", "reason": "primer concepto"},
    {"source": "clase", "start": 215.0,"end": 340.0,"beat": "PASO_2", "reason": "segundo concepto"},
    {"source": "clase", "start": 380.0,"end": 440.0,"beat": "ERRORES","reason": "errores comunes"},
    {"source": "clase", "start": 445.0,"end": 495.0,"beat": "RECAP",  "reason": "resumen accionable"}
  ],
  "grade": "warm_cinematic",
  "subtitles": true
}
```

### 4. Renderizar en borrador primero

```bash
uv run editar.py renderizar edit/edl.json --modo borrador
```

Revisar especialmente:
- Los cortes entre bloques (¿hay salto visual raro?)
- Que los subtítulos coincidan con lo que se dice
- Que el RECAP realmente resume

### 5. Añadir lower-thirds (opcional)

Para marcar visualmente cada paso, renderiza una animación HyperFrames y añádela como overlay en el EDL:

```bash
# Edita animations/paso/composition.html con el texto del paso
uv run editar.py animar animations/paso/
# Luego añade al EDL en "overlays"
```

### 6. Render final y evaluación

```bash
uv run editar.py renderizar edit/edl.json
```

Antes de dar por bueno, revisar en el MP4 final:
- Corte de entrada (primer segundo) — ¿arranca limpio?
- Transición SETUP→PASO_1 — ¿fluye?
- Último segundo del RECAP — ¿termina con fuerza?

### 7. Anotar en project.md

Añade: fecha, nombre del vídeo, duración final, EDL guardado en plantillas si fue exitoso.

## Notas

- Si el vídeo tiene secciones marcadas con "punto uno", "punto dos", úsalas como beats
- Los errores son el bloque más visto en replay — dale tiempo suficiente
- El RECAP debe ser tan bueno que alguien que solo lo vea entienda el vídeo entero
