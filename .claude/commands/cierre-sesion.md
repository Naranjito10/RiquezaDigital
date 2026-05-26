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
   | YYYY-MM-DD | [descripción breve de lo trabajado] | [horas estimadas]h |
   ```
3. Si las horas no son evidentes, preguntar al usuario: *"¿Cuántas horas registramos para esta sesión?"*
4. Si el archivo no existe, crearlo con estructura básica (tabla con columnas Fecha / Descripción / Horas).

Si es trabajo de agencia o interno → saltar al Paso 3.

---

## Paso 3 — SOPs y aprendizajes

1. Identificar procesos repetibles ejecutados en la sesión (ejemplos: configurar webhook, rotar API keys, crear campaña Meta, onboarding cliente, resolver error de despliegue).
2. Para cada proceso detectado:
   - Comprobar si existe SOP en `shared/sops/`
   - **No existe** → crear borrador usando `shared/sops/_plantilla-sop.md` como plantilla
   - **Existe** → revisar si hay pasos nuevos, mejoras o correcciones aprendidas hoy; actualizar si procede
3. Si se creó o actualizó algún SOP → añadir/actualizar la entrada en `shared/sops/README.md`
4. Si no se ejecutó ningún proceso repetible → saltar este paso sin mencionar.

---

## Paso 4 — Tareas Notion de seguimiento

1. Identificar todas las tareas que quedaron abiertas, surgieron durante la sesión o necesitan acción futura.
2. Clasificar:
   - **Tareas del usuario (Kevin / Andrés)** → crear en la Notion DB de tareas con estado **"Por hacer"** usando el MCP de Notion. Nunca en archivos locales.
   - **Tareas para Claude (próxima sesión)** → incluir en el archivo de sesión del Paso 5, sección "Siguiente sesión".
3. Crear las tareas del usuario en Notion. Para cada una: título claro + descripción breve si aplica.
4. Confirmar cuántas tareas se crearon antes de continuar.

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
