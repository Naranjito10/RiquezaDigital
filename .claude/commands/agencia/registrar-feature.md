# /registrar-feature — Registrar nueva funcionalidad en Agencia Agéntica

Registra una nueva feature en el inventario vivo de `agencia/AGENCIA-AGENTICA.md` de forma estandarizada: asigna número F-###, genera el bloque completo, lo muestra para confirmar y lo inserta.

---

## Uso

```
/registrar-feature [descripción libre de la funcionalidad]
```

Si no se pasa descripción, pedir al usuario que la escriba antes de continuar.

---

## Paso 1 — Capturar descripción

Si el usuario ejecutó `/registrar-feature` sin argumentos:
> *"¿Qué funcionalidad quieres registrar? Descríbela en lenguaje natural: qué hace, para qué sirve, dónde vivirá en el repo y qué clientes la usarían."*

Si ya hay descripción en el comando → pasar directamente al Paso 2.

---

## Paso 2 — Leer el inventario y determinar el número

1. Leer `agencia/AGENCIA-AGENTICA.md` completo.
2. Identificar el número F-### más alto ya registrado (tanto en sección activa como en Backlog y sección "Funcionalidades Pendientes").
3. Asignar `F-### = máximo + 1`.
4. Verificar que no haya conflicto de números (dos features con el mismo número).

---

## Paso 3 — Generar el borrador

Con la descripción del usuario y el contexto del inventario, generar el bloque completo siguiendo exactamente este formato Markdown:

```markdown
### F-### — [Nombre descriptivo en español]
- **Estado:** 🌱 PoC  ← (o 🔧 Interno-estable / 💰 Vendible según la madurez que indique el usuario)
- **Ubicación prevista:** `[ruta dentro del repo]`  ← inferir del tipo de funcionalidad
- **Qué hace:** [descripción clara en 2-4 líneas. Explicar el valor, no solo el mecanismo.]
- **Clientes aplicables:** [listar clientes de RD donde aplica, o "universal" si es cross-cutting]
- **Próximos pasos:** [2-4 bullets de acciones concretas para avanzar del estado actual al siguiente]
- **Fecha de creación:** YYYY-MM-DD  ← fecha real de hoy
```

Reglas de inferencia de ubicación:
- Skill de Claude Code → `.claude/commands/nombre-skill.md`
- Pipeline Python/n8n → `pipelines/<área>/nombre/`
- Módulo de servicio → `services/<área>/nombre/`
- Documento o plantilla → `shared/templates/` o `shared/prompts/`
- Agente multi-step → `pipelines/<área>/agents/nombre/`
- Uso interno de agencia → `agencia/<subcarpeta>/`

Reglas de estado inicial:
- Si hay código o skill funcional → `🔧 Interno-estable`
- Si está diseñado pero no implementado → `🌱 PoC`
- Si ya se está cobrando o está listo para vender → `💰 Vendible`

---

## Paso 4 — Mostrar borrador y pedir confirmación

Presentar al usuario el bloque generado en un bloque de código Markdown y preguntar:

> *"Este es el bloque F-### que insertaré en `AGENCIA-AGENTICA.md`. ¿Lo apruebas, o quieres cambiar algo antes de insertarlo?"*

Opciones que el usuario puede pedir:
- Cambiar el nombre
- Cambiar el estado
- Editar la descripción o los próximos pasos
- Cambiar la ubicación
- Confirmar e insertar → pasar al Paso 5

**No insertar nada hasta recibir confirmación explícita.**

---

## Paso 5 — Insertar en el inventario

Una vez confirmado:

1. **Localizar el punto de inserción** en `agencia/AGENCIA-AGENTICA.md`:
   - Insertar el bloque al final de la sección `## Inventario de Funcionalidades`, antes de `## Funcionalidades Pendientes / Backlog`.
   - Si la feature es un backlog item que se está promoviendo a activa, eliminar su línea del backlog.

2. **Actualizar el changelog** al final del documento (sección `## Última actualización`):
   ```
   YYYY-MM-DD (sesión F-###) — Añadida **F-### ([Nombre])** como [estado emoji + texto]. [Una línea explicando qué aporta al producto.]
   ```
   Insertar al inicio del changelog (la entrada más reciente va primero).

3. Usar Edit (no Write) para no sobreescribir el archivo entero.

---

## Paso 6 — Confirmación y propuesta de commit

Tras insertar:

1. Mostrar resumen:
   ```
   ✅ F-### — [Nombre] registrada en AGENCIA-AGENTICA.md

   Estado: [emoji + texto]
   Ubicación prevista: [ruta]
   Clientes: [lista]
   ```

2. Preguntar: *"¿Hacemos commit ahora o esperas a cerrar sesión?"*
   - Si sí → `git add agencia/AGENCIA-AGENTICA.md && git commit -m "feat: F-### registrada — [Nombre] [skip-vibiz]"`
   - Si no → registrar en `tasks.md` como tarea Claude pendiente: "Commit F-###"

---

## Notas de uso

- El usuario puede pasar la descripción directamente en el comando: `/registrar-feature "Sistema de alertas de inactividad de clientes vía Telegram"`
- Si hay duda sobre el estado, preguntar al usuario antes de generar el borrador.
- Si la funcionalidad ya existe en el Backlog como bullet `[ ]`, promover ese item a entrada completa en lugar de duplicar.
- Usar siempre `[skip-vibiz]` en el mensaje de commit (es infraestructura interna, no contenido de marketing).
