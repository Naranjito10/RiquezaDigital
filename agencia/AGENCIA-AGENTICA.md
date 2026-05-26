# Agencia Agéntica — Producto Interno de Riqueza Digital

> **Qué es esto:** el inventario vivo de toda la maquinaria que opera Riqueza Digital internamente, diseñada desde el inicio para ser comercializable como servicio empaquetado bajo el nombre **"Agencia Agéntica"**.

> **Doble lente:** cada funcionalidad sirve dos propósitos — (a) operar mejor a la agencia (Riqueza Digital misma) y a sus clientes (Veganashi, Tecniclima, Selarom Jordi, Federico Sirux), (b) construir IP defendible vendible a futuros compradores del producto "Agencia Agéntica".

---

## Visión del Producto

**Una sola línea:** El sistema operativo completo de una agencia de marketing digital empaquetado como producto, no como horas.

**Para quién:** agencias jóvenes o consultores solitarios que quieren escalar sin contratar antes de tiempo.

**Por qué ahora:** la combinación IA + plantillas + automatizaciones permite que un operador único maneje 10x los clientes que podría hace 3 años — y vender ese stack es un negocio en sí mismo.

**Modelo comercial (tentativo):**
- Tier 1 — Templates pack (one-time)
- Tier 2 — Templates + onboarding + consultoría (1-3 meses)
- Tier 3 — Implementación full (templates + automatizaciones + sistema viral + entrenamiento del equipo del comprador)

---

## Inventario de Funcionalidades

Estado: 🌱 PoC · 🔧 Interno-estable · 💰 Vendible

### F-001 — Pack de Onboarding Estratégico
- **Estado:** 🔧 Interno-estable
- **Ubicación:** `shared/prompts/onboarding-estrategico/`
- **Qué hace:** 4 prompts secuenciales (Brief Estratégico → Estudio de Mercado → PRD de Detección de Virales → Plan de Marketing Inbound) que construyen la base estratégica completa de cualquier cliente B2B en 4 sesiones de Claude Code.
- **Clientes aplicables:** todos (universal para B2B), excepto la sesión 3 que es condicional a estrategia social media.
- **Próximos pasos:** ejecutar primer pase con la propia Riqueza Digital → guardar outputs en `agencia/marketing/strategy/`. Después replicar con clientes (`clients/<cliente>/strategy/`).
- **Fecha de creación:** 2026-05-25

### F-002 — Sistema de Detección y Recreación de Virales
- **Estado:** 🌱 PoC (PRD pendiente de redactar)
- **Ubicación prevista:** `services/marketing/agents/viral-detector/`
- **Qué hace (previsto):** monitoriza competidores en Instagram (y opcionalmente LinkedIn/TikTok), detecta posts virales según umbrales configurables, los analiza para extraer la receta del éxito y produce una versión adaptada para el cliente.
- **Clientes aplicables:** todos los que tengan estrategia inbound vía social media (RD, Veganashi, posiblemente Selarom Jordi y Federico Sirux).
- **Próximos pasos:** ejecutar F-001 sesión 3 para tener el PRD definitivo → MVP en 2 semanas.
- **Fecha de creación:** 2026-05-25

### F-010 — Auditoría y Reorganización de Workspace Operativo
- **Estado:** 🌱 PoC (piloto interno con Notion de RD arrancando 2026-05-27)
- **Ubicación prevista:** `agencia/producto/notion-audit/` para los outputs del piloto; futura skill `/audit-workspace` en `.claude/skills/agencia/`.
- **Qué hace:** proceso estructurado en 4 fases (Mapeo top-level → Triage por área → Ejecución → Mantenimiento continuo) para auditar y reorganizar workspaces operativos (Notion, ClickUp, Asana) que han evolucionado caóticamente. Reordena, archiva obsoleto, propone nueva estructura y crea las skills de mantenimiento periódico.
- **Clientes aplicables:** universalmente vendible — casi toda PYME B2B tiene un Notion/equivalente con drift acumulado. Servicio one-shot o como módulo de Tier 2 del producto.
- **Próximos pasos:** Fase A (mapeo top-level del Notion de RD) en sesión dedicada el 2026-05-27. Documentar el método en SOP reutilizable después del piloto.
- **Fecha de creación:** 2026-05-26

### F-011 — Sistema de Cierre de Sesión Inteligente
- **Estado:** 🔧 Interno-estable
- **Ubicación:** skill `/cierre-sesion` en `.claude/commands/cierre-sesion.md`; regla en memoria `feedback-cierre-sesion-proactivo`; protocol en `CLAUDE.md` sección `GESTIÓN DE SESIONES`; hook `context-monitor` en `.claude/hooks/` (v2 — pendiente).
- **Qué hace:** 4 capas integradas. (1) Skill ejecutable `/cierre-sesion`: 7 pasos — recopilar contexto, imputación de horas, SOPs, tareas Notion, archivo de sesión, propuestas de sistema, resumen. (2) Regla en memoria que detecta cuándo proponer cierre activamente (5 disparadores: fin de tarea, salto de tema, umbrales 60/75/85% de contexto). (3) **Capa SOP (integrada con F-014):** identifica procesos repetibles ejecutados en la sesión y crea/actualiza el SOP correspondiente en `shared/sops/`. (4) Hook futuro que da el % real de contexto en lugar de estimación (pendiente v2).
- **Clientes aplicables:** universal — todo usuario serio de Claude Code se beneficia. Vendible como módulo de Tier 1 o como add-on.
- **Próximos pasos:** (1) Validar con uso real en las próximas sesiones. (2) Hook v2 para % real de contexto.
- **Fecha de creación:** 2026-05-26
- **Fecha de implementación:** 2026-05-26

### F-012 — Skill `/registrar-feature` (auto-inventario)
- **Estado:** 🌱 PoC (construcción en sesión dedicada — fecha por confirmar)
- **Ubicación prevista:** `.claude/skills/agencia/registrar-feature.md`.
- **Qué hace:** toma una idea/funcionalidad nueva y automatiza el registro en `agencia/AGENCIA-AGENTICA.md`: asigna número F-###, sugiere estado (PoC/Interno/Vendible), ubicación, clientes aplicables, próximos pasos. Estandariza el patrón que se ha hecho manual con F-001 a F-011.
- **Clientes aplicables:** uso interno + vendible como herramienta de mantenimiento del producto Agencia Agéntica.
- **Próximos pasos:** sesión dedicada para construir skill, idealmente después o en paralelo con F-011.
- **Fecha de creación:** 2026-05-26

### F-013 — Autopilot Generador-Evaluador (Bucle de Diseño y Calidad)
- **Estado:** 🌱 PoC
- **Ubicación:** `pipelines/desarrollo/generator_evaluator/` (local) y flujos en n8n
- **Qué hace:** Estructura un bucle multi-agente híbrido (n8n + local). El Generador (Gemini Flash / Claude Haiku) diseña copys o maquetas web y el Evaluador (Claude Sonnet / Opus) audita el resultado visualmente y técnicamente (usando Playwright/tests automáticos) hasta superar un umbral de calidad del 80% antes de requerir aprobación humana.
- **Clientes aplicables:** Keller (desarrollo web), campañas de ads y flujos de n8n para cualquier cliente.
- **Próximos pasos:** Crear la base en Python para checkpoints de Git y límites de presupuesto, y definir prompts de evaluación estéticos.
- **Fecha de creación:** 2026-05-26

### F-014 — Sistema de Biblioteca de SOPs
- **Estado:** 🌱 PoC (estructura creada, primeros SOPs documentados)
- **Ubicación:** `shared/sops/` — índice en `shared/sops/README.md`, plantilla en `_plantilla-sop.md`
- **Qué hace:** biblioteca de procesos repetibles accesible por el equipo y por Claude Code. Cada SOP documenta pasos, problemas comunes y decisiones clave de un proceso operativo. Claude lo actualiza al cerrar sesión si se ejecutó un proceso nuevo o se resolvió un problema no documentado.
- **SOPs activos:** `gestion-claves-api-windows.md` (verificado), `manychat-n8n-integration.md` (draft), `seo-onpage-guidelines.md` (draft).
- **Clientes aplicables:** universal — transferible a cualquier agencia o equipo que use Claude Code. Vendible como parte de Tier 2 del producto (onboarding incluye traspaso del SOP inicial).
- **Próximos pasos:** indexar procesos ya ejecutados sin SOP (onboarding cliente, setup WordPress, setup Meta Ads) → construir 3-5 SOPs maduros → integrar en F-011 como capa de cierre automático.
- **Nota de numeración:** tarea Notion creada originalmente como F-013 el 2026-05-26 mañana; renumerada a F-014 al detectar conflicto con F-013 (Autopilot).
- **Fecha de creación:** 2026-05-26

---

## Funcionalidades Pendientes / Backlog

- [ ] **F-003 — Pipeline de creación de contenido** (de viral detectado → adaptación → producción → publicación) — _prioridad alta, alimentado por análisis Vibiz_
- [ ] **F-004 — Sistema de captación de leads orgánico** (lead magnets, funnel, nurturing automatizado) — _alimentado por análisis Vibiz_
- [ ] **F-005 — Sistema de reportes de cliente** (extensión del `/reporte-semanal` actual)
- [ ] **F-006 — Sistema de upsell detectado por señales** (lead madura → señales de compra → trigger comercial)
- [ ] **F-007 — Sistema de propuestas auto-generadas** (cliente entra → brief en 1 sesión → propuesta lista)
- [ ] **F-008 — Publicación multi-plataforma orgánica** (LinkedIn prioritario, después TikTok orgánico si Vibiz lo gestiona bien) — _candidato derivado de Vibiz_
- [ ] **F-009 — Motor de contenido orgánico** (carruseles, hooks, posts con prompts curados) — _candidato derivado de Vibiz_

---

## Activos Reutilizables Ya Existentes

| Activo | Ubicación | Uso |
|---|---|---|
| CLAUDE.md orquestador | `/CLAUDE.md` | Enrutador de tareas por servicio |
| Plantilla de perfil de cliente | `clients/_template/profile.md` | Onboarding administrativo |
| Skills (slash commands) | `/reporte-semanal`, `/auditar-cuenta`, `/crear-campaña`, `/generar-copy`, `/nuevo-cliente` | Operación diaria |
| MCPs integrados | Meta, Ahrefs, Canva, n8n, Notion, Google Drive | Acceso a datos y producción |

---

## Inteligencia Competitiva

> Carpeta viva donde capturamos aprendizajes sistemáticos de competidores de Agencia Agéntica. Cada dossier tiene su propio protocolo de captura.

| Competidor | Estado | Carpeta | Foco principal |
|---|---|---|---|
| **Vibiz.ai** | Activo (cuenta pagada 2026-05-25) | `agencia/inteligencia-competitiva/vibiz/` | Plataforma de marketing autónomo con plugin Claude Code — ~40 MCP tools, ~10K clientes |

**Regla de oro:** Vibiz se usa para contenido de RD misma, no para datos de clientes. Toda decisión derivada del análisis va a `agencia/inteligencia-competitiva/vibiz/decisiones-roadmap.md` y, una vez priorizada, sube a este inventario como F-### activa.

---

## Reglas de Mantenimiento de Este Documento

1. **Toda funcionalidad nueva** (prompt, script, plantilla, pipeline, integración) se registra aquí con: nombre, estado, ubicación, qué hace, clientes aplicables, próximos pasos.
2. **Cambios sustanciales** en funcionalidades existentes → actualizar la entrada.
3. **Si un activo de un cliente se generaliza** → mover a `shared/` y registrar aquí como funcionalidad reutilizable.
4. **Cada entrada con `Fecha de creación`** para tracking histórico.

---

## Última actualización

2026-05-26 (sesión F-011) — **F-011 implementada** como 🔧 Interno-estable. Skill `/cierre-sesion` construida en `.claude/commands/cierre-sesion.md` con 7 pasos: contexto, imputación de horas, SOPs, tareas Notion, archivo de sesión, propuestas de sistema y resumen. Integrada con F-014 (SOPs) y protocolos de `CLAUDE.md`.

2026-05-26 (cierre tarde) — Añadida **F-014 (Sistema de Biblioteca de SOPs)**. Renumerada desde F-013 por conflicto con Autopilot. Primer SOP verificado: `gestion-claves-api-windows.md`. CLAUDE.md actualizado con regla 3 (secretos) y regla 13 (`[skip-vibiz]`).

2026-05-26 — Añadida **F-013 (Autopilot Generador-Evaluador de Diseño y Calidad)** como funcionalidad en PoC tras la aprobación del plan híbrido (n8n + scripts Python).

2026-05-26 (cierre) — Añadidas **F-011 (Sistema de Cierre de Sesión Inteligente)** y **F-012 (Skill /registrar-feature)** como PoCs. Ambas surgen de patrones repetidos en sesiones anteriores que ahora se automatizan. Creadas tareas Notion para sesiones dedicadas de construcción.

2026-05-26 — Añadida **F-010 (Auditoría y Reorganización de Workspace Operativo)** como funcionalidad activa en PoC. Piloto interno con Notion de RD arranca 2026-05-27. Confirmada como vendible (ver memoria `project-arquitectura-info` para política de info repo vs Notion que justifica este servicio).

2026-05-25 (tarde) — Añadida sección **Inteligencia Competitiva** con dossier Vibiz. F-008 y F-009 añadidas al backlog como candidatos derivados del análisis Vibiz. F-003 y F-004 marcadas como alimentadas por el mismo análisis.

2026-05-25 — Creación del documento. F-001 (Pack de Onboarding Estratégico) creado. F-002 (Sistema de Detección de Virales) en estado de PRD pendiente.
