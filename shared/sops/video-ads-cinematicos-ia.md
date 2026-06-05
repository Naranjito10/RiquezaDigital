# SOP: Video Ads Cinemáticos con IA

**Área:** Producción de Contenido / Marketing Digital  
**Estado:** 🌱 Draft  
**Última actualización:** 2026-06-05  
**Clientes donde se aplicó:** —  
**Tiempo estimado:** 30 min (brief) + 10-15 min (generación) + 15 min (revisión/iteración)

---

## Resumen

Proceso para crear un spot publicitario completo (imágenes, animación, voz, música, montaje) a partir de fotos del producto de un cliente. Claude Code orquesta Higgsfield, ElevenLabs y FFmpeg con un solo prompt.

Aplicable a clientes con **producto físico o servicio visual** (alimentación, cosmética, electrodomésticos, moda, etc.).

---

## Pre-requisitos

- [ ] Higgsfield MCP configurado en Claude Code (ver tarea "Configurar stack video ads")
- [ ] `ELEVENLABS_API_KEY` añadida a variables de entorno Windows
- [ ] FFmpeg disponible en PATH
- [ ] 2-3 fotos del producto en ángulos distintos (fondo neutro o natural, buena luz)
- [ ] Brief de dirección creativa completado (ver Paso 2)

---

## Pasos

### 1. Recopilar fotos del producto

Pedir al cliente o buscar en `clients/<cliente>/assets/` al menos:
- 1 foto frontal limpia (fondo neutro)
- 1 foto en contexto de uso real
- 1 foto de detalle o ángulo distintivo

**Resultado esperado:** 2-3 imágenes de referencia que Claude Code puede usar para mantener coherencia visual del producto en todas las escenas.

---

### 2. Completar el brief de dirección creativa

Este paso es el diferenciador de calidad. Rellenar antes de lanzar nada:

**A. Concept board (opcional pero recomendado)**
- Personaje o protagonista: ¿hay persona? ¿qué perfil? ¿cara visible o levemente borrosa para consistencia?
- Setting principal: ¿dónde transcurre el anuncio? (outdoor, cocina, ciudad, naturaleza, etc.)
- Paleta visual / estética: referencias de marcas o estilos (ej. "estilo Patagonia", "minimalista escandinavo")

**B. Money shot**
- ¿Cuál es la toma clave que vende el producto? (ej. botella en mano en cumbre, plato humeante en mesa)
- ¿Qué elemento se quiere exagerar o destacar? (resistencia, frescura, lujo, velocidad)

**C. Brief narrativo**
- Historia en 2-3 frases: ¿qué ocurre? ¿cuál es el arco emocional?
- Tagline o frase final propuesta (puede dejarse a Claude si no hay idea)
- Tono: épico / íntimo / divertido / aspiracional / urgente

**D. Parámetros de producción**

| Parámetro | Opciones | Default recomendado |
|-----------|----------|---------------------|
| Nº de escenas | 5, 8, 10 | 8 |
| Duración por clip | 3s, 5s, 8s, 10s | Mix 5-8s |
| Resolución | 720p / 1080p | 720p (testing), 1080p (final) |
| Estilo de voz | reflexivo, épico-trailer, íntimo, energético | reflexivo/pausado |
| Estilo de música | cinemática, tensión dramática, upbeat, minimal | cinemática con percusión |
| Idioma voz en off | ES / EN | ES |

---

### 3. Lanzar generación con Claude Code

Abrir nueva conversación en Claude Code y enviar:

```
Quiero crear un video ad cinemático para [CLIENTE].

Producto: [descripción + fotos adjuntas]
Historia: [brief narrativo del Paso 2]
Money shot: [descripción]
Personaje/setting: [concept board del Paso 2]
Parámetros: [nº escenas, duración, resolución, voz, música]

Stack: Higgsfield MCP (imágenes con GPT Image 2, animación con Sideens 2.0), 
ElevenLabs (voz + música), FFmpeg (montaje final).
```

Si tienes el skill `claude-ads:video-cinematico` instalado, usarlo directamente.

**Resultado esperado:** Claude confirma conexión a Higgsfield y ElevenLabs, propone storyboard de escenas, solicita aprobación antes de generar.

---

### 4. Revisar storyboard propuesto

Claude presenta las escenas antes de generar. Revisar:
- ¿La narrativa tiene arco (inicio → tensión → resolución)?
- ¿El producto aparece en al menos 3-4 escenas?
- ¿El tagline final encaja con la identidad del cliente?
- ¿La voz y música propuestas son coherentes con el tono de marca?

Aprobar o ajustar antes de continuar.

---

### 5. Revisar output y refinar

Tras la generación, evaluar:
- **Coherencia del producto**: ¿se reconoce el producto en todas las escenas?
- **Ritmo**: ¿hay suficiente pausa entre frases de voz en off?
- **Escenas débiles**: identificar 1-2 que no encajan y pedir regeneración específica
- **Audio**: ¿la música no tapa la voz?

Para regenerar una escena concreta:
```
La escena [N] no encaja porque [razón]. Regenera solo esa escena manteniendo 
el mismo personaje y paleta visual.
```

---

### 6. Exportar y entregar

- Claude exporta el vídeo final vía FFmpeg a `output/<cliente>/`
- Mover a `clients/<cliente>/assets/videos/YYYY-MM-DD_video-ad-[descripcion].mp4`
- Anotar coste real de la generación en `clients/<cliente>/imputacion-horas.md`

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Producto cambia de apariencia entre escenas | Pocas fotos de referencia o prompt inconsistente | Añadir más ángulos del producto; usar concept board con personaje fijo |
| Voz se solapa con música | Niveles de audio no ajustados en FFmpeg | Pedir a Claude que baje el volumen de música a 30-40% durante la voz |
| Escenas de 8s consumen muchos créditos | Sideens 2.0 a 1080p es caro | Usar 720p para drafts; solo 1080p para versión final aprobada |
| Cookie consent / bloqueo en Higgsfield web | Problema de interfaz web, no de API | Usar siempre vía MCP, no vía navegador |
| Claude no conecta a Higgsfield MCP | Conector no reiniciado | Reiniciar Claude Code tras añadir conector |

---

## Decisiones clave

- **720p para testing, 1080p para entrega final**: reduce el coste a la mitad durante iteraciones (~$10 vs ~$24 por vídeo completo).
- **Airtable reemplazado por Notion**: el tracking de proyectos de vídeo se gestiona en la DB de tareas Notion estándar de RD, no en Airtable.
- **Skill de buenas prácticas separado del brief**: el brief lo rellena el equipo antes de la sesión; el skill de Claude contiene los parámetros técnicos de generación.

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| Tipo de producto | Escenas posibles, money shot | Comida → close-up textura / Botella → caída y resistencia |
| Tono de marca | Estilo de voz y música | Veganashi: cálido/natural → voz íntima, música orgánica |
| Idioma del mercado | Voz en off y texto en pantalla | ES para España/LATAM, EN si el cliente vende internacionalmente |
| Presupuesto cliente | Resolución y nº de iteraciones | Cliente pequeño → 720p, 1 iteración / Cliente premium → 1080p, 2-3 iteraciones |

**Preguntas a hacer al cliente antes de empezar:**
1. ¿Tienes fotos de producto de calidad o necesitamos generarlas primero?
2. ¿Hay una historia o emoción específica que quieras comunicar?
3. ¿El vídeo es para Meta Ads (9:16 o 1:1) o para YouTube/web (16:9)?

---

## Notas adicionales

- El sistema completo fue documentado a partir de un vídeo de referencia (junio 2026) sobre creación de ads cinemáticos con Claude Code + Higgsfield.
- El piloto de validación es con Veganashi. Hasta completarlo, este SOP es 🌱 Draft.
- Coste de referencia por vídeo: $10 (720p, 8 escenas) — $24 (1080p, 8 escenas). Márgenes de agencia por definir tras el piloto.

---

*Última sesión que actualizó este SOP: 2026-06-05 — creación inicial basada en metodología de video ads cinemáticos con IA*
