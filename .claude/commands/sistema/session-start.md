# /session-start — Arranque Inteligente de Sesión

Inicia la sesión actual reconstruyendo el contexto, repasando prioridades, tareas en Notion y memorias del sistema.

---

## Paso 1 — Leer el último archivo de sesión

1. Abrir `.remember/sessions/INDEX.md` para identificar el archivo de sesión `.md` más reciente (última fila de la tabla).
2. Leer dicho archivo de sesión de la carpeta `.remember/sessions/`.
3. Imprimir el resumen del contexto en el chat:
   - **Estado al cerrar:** Qué quedó pendiente o completado.
   - **Siguiente sesión (prioridad):** Qué era lo primero en la lista.
   - **Contexto no obvio:** Alertas o decisiones críticas.

---

## Paso 2 — Repasar tareas del repositorio local

1. Abrir `tasks.md` en la raíz del proyecto.
2. Imprimir en el chat de forma resumida las tareas que figuren bajo:
   - `🔴 ALTA PRIORIDAD`
   - `🟡 MEDIA PRIORIDAD`

---

## Paso 3 — Sincronizar con Notion

1. Si la API de Notion está disponible (usando credenciales locales), consultar las tareas pendientes de la base de datos `b5c6d3aa-d462-4989-962e-8fc7034de3a9`.
2. Listar aquellas tareas en estado `"En proceso"` o `"Por hacer"` asignadas a Kevin o sin asignar (tareas del agente) que tengan fecha de hoy o estén retrasadas.

---

## Paso 4 — Pregunta de alineación

1. Presentar el resumen unificado en el chat.
2. Formular al usuario una pregunta de alineación para arrancar:
   *"¿Continuamos con la prioridad [Prioridad 1] de la sesión anterior o prefieres que nos enfoquemos en otra tarea?"*
