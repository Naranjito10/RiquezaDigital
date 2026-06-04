# /cierre-sesion — Cierre Inteligente de Sesión

Ejecuta el cierre completo de la sesión actual: consolida trabajo, documenta estado, crea tareas Notion y deja el contexto listo para la próxima sesión.

---

## Paso 1 — Recopilar contexto

1. Si no es evidente por el historial de conversación, preguntar: **¿Cuál fue el cliente o área principal de esta sesión?** (`keller-valentina` / `veganashi` / `tecniclima` / `agencia` / nombre del cliente)
2. Repasar la conversación completa: tareas completadas, decisiones tomadas, temas tratados, archivos creados o modificados.
3. Anotar internamente: qué se terminó, qué quedó abierto, qué decisiones implican contexto no obvio.

---

## Paso 2 — Imputación de horas (solo clientes de pago)

Si el cliente activo es un cliente facturado (no "agencia" ni trabajo interno):

1. Abrir `clients/<cliente>/imputacion-horas.md`
2. Añadir entrada:
   ```
   | YYYY-MM-DD | [descripción breve de lo trabajado] | [horas humano equivalente]h |
   ```
3. Si el archivo no existe, crearlo con estructura básica (tabla con columnas Fecha / Descripción / Horas).
4. Si el archivo no existe, crearlo con estructura básica (tabla con columnas Fecha / Descripción / Horas).

### Metodología de imputación: tiempo humano equivalente (sin IA)

**Regla crítica:** Las horas se imputan como el tiempo que habría tardado un profesional humano competente en realizar el mismo trabajo **sin ayuda de IA**. No se registra el tiempo real de la sesión con Claude.

**Por qué:** Este dato es el activo de negocio más valioso del sistema. Permite:
- Calcular el ahorro real acumulado por cliente y en total
- Demostrar ROI de la Agencia Agéntica a futuros clientes con datos reales
- Justificar el coste del servicio frente a freelancers o agencias tradicionales

**Cómo estimar:**

| Tipo de trabajo | Multiplicador orientativo (sesión IA → humano) |
|----------------|-----------------------------------------------|
| Auditoría y análisis (ads, SEO, web) | 3–5x |
| Redacción de informes y documentos | 3–4x |
| Desarrollo web / edición WordPress | 2–4x |
| Creación de copy publicitario | 2–3x |
| Configuración técnica (APIs, webhooks) | 2–3x |
| Investigación y recomendaciones estratégicas | 3–5x |

Ejemplo: si una auditoría Google Ads tomó 45 min con IA, un analista humano tardaría ~4-6h → imputar 5h.

Si las horas no son evidentes, estimar conservadoramente y anotar entre paréntesis que es estimación: `5h (est.)`.

Si es trabajo de agencia o interno → saltar al Paso 3.

---

## Paso 3 — SOPs y aprendizajes

1. Preguntar explícitamente al usuario: **"¿Ejecutamos algún proceso repetible hoy?"**
   - Si la respuesta es **"No"** (o no se identifica ninguno): saltar este paso.
   - Si la respuesta es **"Sí"** (o el usuario indica el proceso):
     - Identificar el proceso repetible y su área (ejemplos: configurar webhook, rotar API keys, crear campaña Meta, onboarding cliente, resolver error de despliegue).
     - Comprobar si existe SOP correspondiente en `shared/sops/`.
     - **No existe** → crear borrador usando `shared/sops/_plantilla-sop.md` como plantilla. Rellenar los campos básicos conocidos y presentarlo/abrirlo para que el usuario o tú añadáis los pasos.
     - **Existe** → abrir el archivo existente, revisar qué aprendizajes/cambios de la sesión actual aplican, y proponer la actualización.
2. Si se creó o actualizó algún SOP → añadir/actualizar la entrada en `shared/sops/README.md`.

---

## Paso 4 — Tareas Notion de seguimiento

**Toda tarea — del usuario o del agente — va a Notion. El asignatario indica quién la ejecuta.**

1. Identificar todas las tareas que quedaron abiertas o surgieron en la sesión. Incluir:
   - Tareas directas (algo que no se terminó o quedó pendiente)
   - Cada paso ejecutable de cualquier **plan de implementación** creado en esta sesión (ver protocolo abajo)
   - Decisiones que necesitan validación de Kevin, el cliente, o Andrés

2. Clasificar cada tarea por asignatario:
   - **Tarea de Kevin** → estado **"Por hacer"**, asignada a Kevin. Ejemplos: definir objetivos, aportar datos, validar diseño, tomar decisión estratégica.
   - **Tarea de Claude** → estado **"Por hacer"**, **sin asignatario**. Ejemplos: construir mockup, escribir código, crear página WP, redactar copy.
   - **Tarea de Andrés u otro** → **comentar con Kevin antes de crear**. No crear sin confirmar disponibilidad y contexto.

3. **Protocolo para planes de implementación:**
   Si en la sesión se creó un plan (spec, fases, sprints, pasos numerados):
   - Cada paso **accionable y no bloqueado** del plan → 1 tarea Notion (no crear tareas bloqueadas por otras)
   - Descripción: referencia al plan en el repo + qué se hace exactamente
   - Aplicar lógica de asignatario de arriba
   - Los pasos bloqueados por dependencias se crean cuando el paso previo esté en "Revisar" o "Hecho"

4. Preguntar explícitamente al usuario: *¿Deseas que creemos estas tareas en Notion o las dejamos registradas solo en `tasks.md` como referencia?* (Si el usuario ya las revisó durante la sesión y no desea añadirlas, saltar la creación en la base de datos).
5. Crear las tareas aprobadas en Notion usando el MCP (si el usuario confirmó).
6. Actualizar `tasks.md` con el estado resultante (snapshot de referencia para Claude entre sesiones).
7. Confirmar el estado resultante de las tareas al usuario.

> **Por qué importa:** Claude no tiene visibilidad de lo que Kevin hace fuera de sesiones. Con las tareas de Kevin en Notion con asignatario, Claude puede consultar el estado al abrir sesión y saber qué cambió. Las tareas de Claude sin asignar permiten ver el trabajo total pendiente en un solo lugar. Omitir la subida si ya se han alineado evita duplicidades y ruido en el tablero de Notion.

---

## Paso 5 — Archivo de sesión

1. Obtener timestamp actual (formato `YYYY-MM-DD_HHMM`, hora local Madrid).
2. Crear el archivo `.remember/sessions/YYYY-MM-DD_HHMM.md` con exactamente estas 3 secciones:

```markdown
## Estado al cerrar
[Qué se completó. Qué decisiones se tomaron. Estado de cada tarea o entregable. Si algo quedó a medias, indicar hasta dónde llegó.]

## Siguiente sesión (prioridad)
[Lista ordenada: qué hacer primero la próxima vez. Incluir tareas Claude pendientes. El primer item es lo más urgente.]

## Contexto no obvio
[Lo que NO está en el código, en Notion ni en el historial de commits: decisiones de diseño con razón implícita, alertas, dependencias entre tareas, acuerdos verbales con el cliente, cosas que se decidieron descartar y por qué.]

## Prompt de arranque
[Prompt listo para pegar al inicio de la próxima sesión. Formato: párrafo corto que sitúa el contexto + lista numerada de tareas por orden de prioridad. Ejemplo:

"Continuamos trabajo en [cliente/área]. En la sesión anterior [1 frase de qué se hizo].

Prioridades para hoy:
1. [tarea más urgente — con suficiente detalle para que Claude retome sin leer el historial]
2. [segunda tarea]
3. [tercera tarea si aplica]

Archivos clave: [rutas relevantes si las hay]"]
```

3. Añadir una línea al final de `.remember/sessions/INDEX.md`:
   ```
   | YYYY-MM-DD HH:MM | YYYY-MM-DD_HHMM.md | [resumen de 1 línea de qué se hizo] |
   ```
   ⚠️ Nunca sobreescribir archivos de sesión existentes. Siempre timestamp nuevo.

---

## Paso 6 — Propuestas de actualización del sistema

Revisar si algo de la sesión debería actualizar alguno de estos archivos:

| Archivo | Cuándo actualizar |
|---|---|
| `memory/*.md` | Nueva regla de comportamiento aprendida, nuevo hecho sobre el fundador o el proyecto |
| `agencia/AGENCIA-AGENTICA.md` | Se construyó algo nuevo, avanzó una F-###, cambió estado de una funcionalidad |
| `CLAUDE.md` | Se descubrió un patrón de flujo nuevo, una regla de delegación o una corrección al orquestador |
| `shared/sops/` | Ya cubierto en Paso 3 |

Para cada propuesta relevante:
- Presentar de forma compacta: *"Propongo actualizar [archivo] porque [razón]. ¿Lo hago?"*
- **Solo ejecutar si el usuario confirma** — nunca aplicar cambios sin aprobación en este paso.
- Si no hay propuestas relevantes, omitir este paso completamente.

---

## Paso 7 — Resumen de cierre

Presentar mensaje final al usuario:

```
✅ Sesión cerrada — [fecha y hora]

Completado hoy:
• [item 1]
• [item 2]

Creado en Notion: [N] tarea(s)
SOPs actualizados: [N o "ninguno"]
Sesión guardada: .remember/sessions/YYYY-MM-DD_HHMM.md

🔜 Próxima sesión: [primera prioridad de la lista]

---
📋 **Prompt de arranque** (copia y pega al inicio de la próxima sesión):

[insertar aquí el prompt de arranque generado en el Paso 5]
```

---

## Notas de uso

- **Disparadores para proponer cierre de forma proactiva** (sin que el usuario lo pida):
  - Fin de la tarea principal de la sesión
  - Salto de tema significativo detectado
  - Estimación ~60% de contexto → sugerir suave: *"¿Cerramos la sesión antes de continuar?"*
  - Estimación ~75% de contexto → recomendar: *"Recomiendo cerrar sesión para no perder contexto"*
  - Estimación ~85% de contexto → cierre inmediato: *"El contexto está casi lleno. Ejecuto cierre ahora."*

- **Commits de cierre**: usar siempre `[skip-vibiz]` en el mensaje de commit (el cierre es infraestructura interna, no contenido de marketing).

- **Sesiones paralelas**: si al escribir en INDEX.md detectas que hay otra sesión del mismo día con timestamp distinto, no hacer nada especial — el sistema de timestamps lo gestiona automáticamente.
