# SOP: Construir una Skill de Claude Code

**Área:** Desarrollo / Producto Interno  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-05-26  
**Clientes donde se aplicó:** Agencia interna (RD)  
**Tiempo estimado:** 15–30 minutos

---

## Resumen

Crear un nuevo comando slash (`/nombre-skill`) para Claude Code documentando el comportamiento deseado en un archivo Markdown en `.claude/commands/`. Se usa cada vez que se quiere automatizar un flujo repetible del agente.

---

## Pre-requisitos

- [ ] Tener claro qué problema resuelve la skill (1 línea de descripción)
- [ ] Haber identificado los pasos del proceso que se quiere automatizar
- [ ] Acceso de escritura al repo

---

## Pasos

### 1. Verificar que la skill no existe ya

Comprobar `.claude/commands/` para evitar duplicados:

```bash
ls .claude/commands/
```

**Resultado esperado:** lista de archivos `.md` existentes. Si ya hay una con nombre similar, leer su contenido antes de crear una nueva.

### 2. Revisar una skill existente como referencia de formato

Leer una skill similar (ej. `reporte-semanal.md`, `cierre-sesion.md`) para mantener consistencia de estilo.

### 3. Diseñar la skill en papel (mental o escrito)

Definir antes de escribir:
- **Nombre:** verbo-sustantivo en español, corto (`cierre-sesion`, `registrar-feature`)
- **Pasos secuenciales:** numerados, condicionales claros, sin ambigüedad
- **Entradas que necesita:** ¿pregunta al usuario? ¿lee archivos? ¿usa MCPs?
- **Salidas que produce:** archivos, cambios en Notion, mensajes al usuario

### 4. Crear el archivo

Ubicación: `.claude/commands/<nombre-skill>.md`

Estructura recomendada:
```markdown
# /nombre-skill — Descripción corta

Párrafo de 1-2 líneas explicando qué hace y cuándo se usa.

---

## Paso 1 — [Nombre del paso]
[instrucciones para el agente]

## Paso 2 — [Nombre del paso]
...

## Notas de uso
[disparadores, casos especiales, advertencias]
```

**Resultado esperado:** el archivo aparece automáticamente en la lista de skills disponibles en la próxima sesión (sin reiniciar).

### 5. Registrar en AGENCIA-AGENTICA.md

Si la skill es parte de una F-### del producto:
- Actualizar el estado de la F-### correspondiente (de 🌱 PoC a 🔧 Interno-estable)
- Actualizar ubicación de "prevista" a real
- Añadir entrada en "Última actualización"

### 6. Commit con [skip-vibiz]

```
git add .claude/commands/<nombre-skill>.md agencia/AGENCIA-AGENTICA.md
git commit -m "feat: [F-###] skill /<nombre-skill> implementada [skip-vibiz]"
```

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| La skill no aparece en la lista | Sesión abierta antes de crear el archivo | Verificar con el sistema — suele detectarse sin reiniciar; si no, iniciar nueva sesión |
| El agente no sigue los pasos en orden | Instrucciones ambiguas o sin numeración clara | Usar pasos numerados con condicionales explícitos (`Si X → hacer Y / Si no → saltar`) |
| Skill demasiado larga y el agente la ignora | Demasiados pasos o muy detallada | Dividir en sub-skills o reducir a pasos esenciales |

---

## Decisiones clave

- **Decisión:** Skills en `.claude/commands/` (no en `services/` ni `agents/`)  
  **Razón:** Son comandos ejecutables por el agente, no documentación de servicios  
  **Alternativa descartada:** Carpeta `agencia/skills/` — no la lee el harness automáticamente

- **Decisión:** Markdown puro, sin código ejecutable  
  **Razón:** El "programa" son instrucciones en lenguaje natural; el agente las interpreta  
  **Alternativa descartada:** Scripts Python/bash — más frágiles, más mantenimiento

---

## Notas adicionales

- El nombre del archivo = el slash command: `cierre-sesion.md` → `/cierre-sesion`
- Skills de producto (F-###) deben estar vinculadas a su entrada en `AGENCIA-AGENTICA.md`
- Siempre probar mentalmente la skill antes de commitear: ¿el agente podría seguir estos pasos sin contexto previo?

---

*Última sesión que actualizó este SOP: 2026-05-26 — Creado al construir F-011 (`/cierre-sesion`). Primera skill construida de forma estructurada.*
