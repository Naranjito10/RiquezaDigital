# SOP: Generación de Guiones Duales Redes y Carga en Notion

**Área:** Producción de Contenido  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-04  
**Clientes donde se aplicó:** Riqueza Digital  
**Tiempo estimado:** 20–30 minutos

---

## Resumen

Procedimiento para que el agente autónomo tome ideas o posts virales de referencia de competidores y los transforme en guiones estructurados duales (Instagram y LinkedIn) listos para producción y los cargue automáticamente en la base de datos de Notion.

---

## Pre-requisitos

- [ ] Skill `/contenido:guion-instagram` registrada en el repositorio
- [ ] Notion MCP configurado con acceso de escritura a la base de datos de contenidos
- [ ] ID de la base de datos de ideas de contenido en Notion (`d70d9fb0b3614d96b2c6919dc513b8e3`)
- [ ] Perfil de cliente (o Riqueza Digital) con ICP y propuesta de valor definidos

---

## Pasos

### 1. Recopilar y Analizar Referencias
1. Seleccionar la idea o el post de referencia de competidores (ej. un carrusel técnico de Vibiz).
2. Definir el **pilar de contenido** (ej. Caso Real, Tutorial Técnico, Filosofía Agéntica, Contraintuitivo).
3. Determinar el ICP al que se dirige y el gancho (Hook) inicial.

### 2. Generación del Guion Dual con la Skill
1. Invocar el comando `/contenido:guion-instagram` en Claude Code.
2. Proporcionar la idea y el enlace/texto del post de referencia.
3. El agente generará el entregable con:
   - **Versión Vídeo Corto (Instagram Reels):** Ganchos alternativos (3x), estructura de 3 pasos y llamada a la acción (CTA) (ej: "Comenta SISTEMA").
   - **Versión Texto Largo (LinkedIn):** Estructura en primera persona con hooks limpios y espaciado optimizado para el feed.
   - **Cápsulas de Copy:** Textos listos para pegar en la descripción del vídeo.

### 3. Conexión a la Base de Datos de Notion
Una vez que el guion esté aprobado en la sesión:
1. El agente invocará el Notion MCP para registrar la entrada.
2. Endpoint: `notion-create-pages` o `create-database-row`.
3. Mapeo de propiedades obligatorio:
   - **Título / Name:** `[Pilar] Titulo Corto del Post`
   - **Estado:** `Sin Estado` (dejado en `null` para que caiga en la primera columna del Kanban en Notion).
   - **Plataformas:** Multiselect con `Instagram` y `LinkedIn`.
   - **Fecha de creación:** Fecha actual en formato YYYY-MM-DD.
   - **Cuerpo / Content:** Incluir el contenido completo formateado de ambos guiones dentro de los bloques del cuerpo de la página en Notion.

### 4. Confirmación
El agente devolverá el enlace de la página de Notion recién creada para que el usuario pueda validarlo desde el móvil o desktop.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Error al crear la página en Notion | El esquema de propiedades no coincide con el tipo de datos en Notion | Revisar que las propiedades select/multiselect coincidan exactamente en mayúsculas/minúsculas y que el ID de la base de datos sea correcto |
| Guiones demasiado genéricos o robóticos | Falta de la voz del fundador en el prompt | Usar ejemplos reales del estilo del fundador guardados en `memory/user_kevin_berbel.md` para dar tono conversacional directo |

---

## Decisiones clave

- **Decisión:** Dejar el campo "Estado" como `null` al crear la página en Notion.  
  **Razón:** Al no asignar un estado por defecto, la tarea aparece en la sección "Sin Estado" del Kanban de Notion. Esto obliga a una clasificación y priorización manual de la idea por parte del fundador, evitando que se pierda en el fondo del backlog.  
  **Alternativa descartada:** Asignar "Idea" o "Borrador" automáticamente (tiende a saturar la columna y diluye el triage diario).

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| Voz de marca | Tono del guion de video | Informativo-serio vs Dinámico-agresivo |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Creación del SOP tras implementar la skill de guiones de Instagram.*
