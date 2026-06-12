# SOP: Construir una Skill de Claude Code

**Área:** Desarrollo / Producto Interno  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-05  
**Clientes donde se aplicó:** Agencia interna (RD)  
**Tiempo estimado:** 15–30 minutos

---

## Resumen

Crear un nuevo comando slash (`/namespace:nombre`) para Claude Code documentando el comportamiento deseado en una carpeta autocontenida dentro de `.claude/commands/`. Cada skill es una **unidad independiente** con su propio directorio, lo que permite añadir recursos empaquetados (referencias, scripts, assets) sin contaminar el resto del sistema.

---

## Pre-requisitos

- [ ] Tener claro qué problema resuelve la skill (1 línea de descripción)
- [ ] Haber buscado primero si ya existe una skill oficial o de comunidad que lo cubra
- [ ] Identificar el namespace correcto (ver tabla al final)
- [ ] Acceso de escritura al repo

---

## Pasos

### 1. Verificar que la skill no existe

Comprobar skills disponibles en el sistema antes de construir desde cero:

```bash
ls .claude/commands/<namespace>/
```

Si hay una con nombre similar, leer su `SKILL.md` antes de crear una nueva. También revisar la lista de skills instaladas — muchas funcionalidades ya están cubiertas por skills oficiales o de comunidad.

### 2. Diseñar la skill antes de escribir

Definir:
- **Nombre:** verbo-sustantivo en español, corto (`cierre-sesion`, `integrar-video`)
- **Namespace:** según el servicio al que pertenece (ver tabla de namespaces)
- **Pasos secuenciales:** numerados, con condicionales explícitos
- **Entradas:** ¿pregunta al usuario? ¿lee archivos? ¿usa MCPs?
- **Salidas:** archivos generados, cambios en Notion, mensajes al usuario
- **Recursos necesarios:** ¿necesita plantillas, scripts o docs de referencia?

### 3. Crear la estructura de carpeta

```bash
mkdir -p .claude/commands/<namespace>/<nombre-skill>
```

La estructura mínima es siempre solo `SKILL.md`. Las subcarpetas son opcionales:

```
.claude/commands/
└── namespace/
    └── nombre-skill/
        ├── SKILL.md          ← obligatorio siempre
        ├── references/       ← solo si hay documentación extensa (>200 líneas)
        ├── scripts/          ← solo si hay código ejecutable reutilizable
        └── assets/           ← solo si hay plantillas o ficheros de output fijos
```

**Regla práctica:** si puedes escribirlo todo en un único `SKILL.md` sin que quede pesado, no necesitas subcarpetas.

### 4. Escribir SKILL.md

Ubicación: `.claude/commands/<namespace>/<nombre>/SKILL.md`

Estructura obligatoria (frontmatter + cuerpo):

```markdown
---
name: namespace:nombre-skill
description: >
  Descripción de cuándo usar este skill. Incluir frases trigger concretas:
  "úsalo cuando el usuario diga X", "activa siempre que Y ocurra".
  Ser específico — la descripción es el mecanismo principal de activación.
---

# nombre-skill

[Cuerpo: instrucciones claras, pasos numerados, formato de output esperado]
```

El slash command resultante es automático: `namespace/nombre/SKILL.md` → `/namespace:nombre`

**Resultado esperado:** la skill aparece en la lista de skills disponibles sin reiniciar sesión.

### 5. Registrar en los índices

**Siempre:**
- Añadir línea en `CLAUDE.md` raíz (tabla "SKILLS DISPONIBLES")

**Si el namespace tiene su propio CLAUDE.md de servicio** (`services/<namespace>/CLAUDE.md`):
- Añadir línea en la tabla de skills de ese servicio

**Si la skill forma parte de una F-### del producto:**
- Actualizar estado en `agencia/AGENCIA-AGENTICA.md` (de 🌱 PoC a 🔧 Interno-estable)
- Referenciar por nombre de comando, no por ruta de fichero

### 6. Commit con [skip-vibiz]

```
git add .claude/commands/<namespace>/<nombre>/
git commit -m "feat: skill /<namespace>:<nombre> implementada [skip-vibiz]"
```

---

## Regla crítica: referenciar skills siempre por nombre de comando

Cuando un skill, SOP o documento mencione otra skill, usar **siempre el nombre del comando**. Nunca la ruta interna del fichero.

| Correcto | Incorrecto |
|---|---|
| `invocar /web:wp-edit` | `ver .claude/commands/web/wp-edit/SKILL.md` |
| `antes de continuar, usa /sistema:session-start` | `ejecutar .claude/commands/sistema/session-start.md` |

Las rutas de fichero son detalle de implementación. El nombre del comando es la interfaz pública — estable aunque la estructura interna cambie.

---

## Cuándo añadir subcarpetas

| Subcarpeta | Cuándo crearla | Ejemplo |
|---|---|---|
| `references/` | El skill necesita consultar docs extensos sin cargarlos siempre en contexto | Guía de estructura SEO para `boveda-post` |
| `scripts/` | Hay código Python/JS que se repetiría en cada invocación | Helper REST API para `wp-edit` |
| `assets/` | El skill produce outputs basados en plantillas fijas | Template HTML del informe mensual |

Crear la subcarpeta con un `.gitkeep` para marcar la intención aunque esté vacía.

---

## Tabla de namespaces

| Namespace | Servicio | Skills actuales |
|---|---|---|
| `marketing` | Marketing Digital | `reporte-semanal`, `reporte-mensual`, `auditar-cuenta`, `crear-campaña`, `generar-copy` |
| `web` | Desarrollo Web | `generar-prompt-web`, `autopilot-diseno`, `wp-edit`, `wp-page-rd` |
| `contenido` | Producción de Contenido | `boveda-post`, `guion-instagram` |
| `clientes` | Gestión de Clientes | `nuevo-cliente` |
| `agencia` | Gestión Interna RD | `registrar-feature` |
| `sistema` | Orquestación / Sistema | `session-start`, `cierre-sesion`, `context-validator`, `buscar-sop`, `integrar-video`, `Claudia` |

Para skills en un servicio existente: usar el namespace correspondiente.  
Para una capacidad completamente nueva sin namespace: crear namespace nuevo y documentarlo en `ARQUITECTURA.md`.

---

## Variante B: Importar y adaptar una skill externa

Proceso verificado el 2026-06-12 al integrar 16 skills externas (export propio + plugins Anthropic) como capa de conocimiento (F-020).

### B1. Decidir la capa correcta

- **¿Workflow con pasos y efectos** (preguntar cliente, guardar archivos, ejecutar pipeline)? → `.claude/commands/<ns>/<nombre>/` (slash command)
- **¿Conocimiento experto que debe activarse solo por contexto** (frameworks, límites, benchmarks)? → `.claude/skills/<nombre>/` (skill auto-activable)
- Pueden coexistir: el command orquesta y referencia a la skill como capa de conocimiento (ej: `/marketing:generar-copy` usa la skill `ad-copy` para límites y fórmulas).

### B2. Evaluar solapamiento antes de copiar

- Comparar con commands y skills existentes — si el contenido mejora algo existente, cross-referenciar en lugar de duplicar
- Verificar que no esté ya cubierto por un plugin instalado (document-skills, superpowers, claude-ads...)

### B3. Checklist de adaptación RD (obligatorio antes del commit)

- [ ] Rutas de guardado según reglas 4-6 del orquestador (`clients/<nombre>/reports|proposals|contracts/`, `output/agency/`)
- [ ] Política repo-vs-Notion respetada (source of truth por tipo, ver `ARQUITECTURA.md`)
- [ ] Stack real de RD (WordPress REST/Vercel, Notion como CRM, Ahrefs MCP, MailerLite/Klaviyo) en lugar de herramientas genéricas
- [ ] Contexto España/UE si aplica (RGPD, LSSI, jurisdicción, DPA)
- [ ] Checkpoints humanos preservados (precios → Kevin, legal → abogado, envíos → nunca automáticos)
- [ ] Sección final "Contexto RD" / "Agency Context" con todo lo anterior
- [ ] Escanear que no traiga secretos, rutas de otros entornos (`/mnt/...`) ni conectores no disponibles

### B4. Registrar

- Entrada o ampliación de F-### en `agencia/AGENCIA-AGENTICA.md`
- Slash command nuevo → tabla "SKILLS DISPONIBLES" de `CLAUDE.md`; skill de conocimiento → tabla "SKILLS DE CONOCIMIENTO"

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|---|---|---|
| La skill no aparece en la lista | El `SKILL.md` está en la carpeta equivocada | Verificar que la ruta es `commands/<ns>/<nombre>/SKILL.md`, no `commands/<ns>/<nombre>.md` |
| El agente no sigue los pasos en orden | Instrucciones ambiguas o sin numeración | Usar pasos numerados con condicionales explícitos (`Si X → hacer Y / Si no → saltar`) |
| Skill demasiado larga (>500 líneas) | Demasiados pasos o documentación incrustada | Mover docs extensos a `references/` y referenciarlos desde el `SKILL.md` |
| Conflicto de nombre con skill existente | Mismo nombre en mismo namespace | Revisar tabla de namespaces; si el concepto es distinto, elegir nombre más específico |

---

## Decisiones de diseño

- **Decisión:** Carpeta por skill en lugar de fichero plano  
  **Razón:** Cada skill es una unidad distribuible e independiente; permite bundlear recursos sin contaminar el repo; alineado con el sistema de plugins oficial  
  **Alternativa descartada:** `<nombre>.md` plano — no permite recursos empaquetados y dificulta la distribución del producto

- **Decisión:** Skills en `.claude/commands/` con namespaces  
  **Razón:** Son comandos ejecutables por el agente; el namespace organiza por servicio y evita colisiones de nombres  
  **Alternativa descartada:** `services/<servicio>/skills/` — no lo descubre el harness automáticamente

- **Decisión:** Referenciar skills por nombre de comando, nunca por ruta  
  **Razón:** Las rutas internas pueden cambiar en refactors; el nombre del comando es la interfaz estable  
  **Aprendido:** en el refactor de 2026-06-05 se encontraron 8 rutas hardcodeadas que hubo que corregir manualmente

---

*Última sesión que actualizó este SOP: 2026-06-12 — Añadida Variante B (importar y adaptar skills externas) tras integrar las 16 skills de conocimiento de F-020. Anterior: 2026-06-05 reescritura completa tras migración a carpeta+SKILL.md. Creado originalmente 2026-05-26 al construir F-011.*
