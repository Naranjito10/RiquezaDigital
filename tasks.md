# 📋 Tablero de Control — Tareas de la Agencia (Agente Claude)

Este archivo es el panel de control exclusivo para el **Agente Claude**. Aquí se registran las tareas pendientes, en proceso y completadas de los distintos clientes y servicios, organizadas por prioridad.

> [!NOTE]
> Las tareas asignadas al **Usuario** se gestionan directamente en su Notion y no se trackean aquí, de acuerdo a las reglas del proyecto en [CLAUDE.md](./CLAUDE.md).

---

## 🔴 ALTA PRIORIDAD (Urgente / Bloqueante)

| Cliente | Servicio | Tarea | Estado | Notas / Enlaces |
| :--- | :--- | :--- | :---: | :--- |
| **Keller** | Desarrollo Web | Mockup Home HTML/CSS/JS completo (Fase 1) | `[ ]` | Plan 100% definido en [plan-web.md](clients/keller-valentina/plan-web.md). Sin bloqueos — listo para ejecutar. |
| **Veganashi + Tecniclima** | Agencia Autónoma | Sprint 0.5: Definir objetivos en números (leads/mes, CPA máx, fecha objetivo) | `[ ]` | ⚠️ **Kevin define (30 min).** Bloqueante para todos los agentes autónomos. Spec: [agencia-autonoma-design.md](docs/superpowers/specs/2026-05-29-agencia-autonoma-design.md) |

---

## 🟡 MEDIA PRIORIDAD (Desarrollo Activo)

| Cliente | Servicio | Tarea | Estado | Notas / Enlaces |
| :--- | :--- | :--- | :---: | :--- |
| **Riqueza Digital** | Marketing | Actualizar página /servicios-google-ads/ (WP ID 6822) con métricas reales Tecniclima y publicar | `[ ]` | Kevin trae leads/mes y CPL. Fuente local: [google-ads-page.html](output/agency/google-ads-page.html). ⚠️ No publicar con benchmarks genéricos actuales. |
| **Riqueza Digital** | Marketing / Legal | Crear página Términos de Servicio en riquezadigital.es | `[ ]` | Requerida para solicitud de developer token Google Ads API. |
| **Veganashi + Tecniclima** | Agencia Autónoma | Sprint 1: Completar profiles + authority-matrix + intelligence/ por cliente | `[ ]` | Bloqueado por Sprint 0.5. Spec completa en [agencia-autonoma-design.md](docs/superpowers/specs/2026-05-29-agencia-autonoma-design.md) |
| **Tecniclima** | Google Ads | Crear `pipelines/marketing-digital/ads/clients/tecniclima/profile.json` con customer_id | `[ ]` | Kevin proporciona customer_id. Prerequisito para ejecutar pipeline Google Ads. |
| **Riqueza Digital** | Desarrollo Software | F-013: Base Python del bucle Generador-Evaluador (checkpoints Git, límites presupuesto, prompts estéticos) | `[ ]` | Plan en [AGENCIA-AGENTICA.md](agencia/AGENCIA-AGENTICA.md). |
| **Keller** | Desarrollo Web | Fase 2: Páginas interiores (Trámites, Consultoría, Marketing, Contacto, Blog) | `[ ]` | Bloqueado por Fase 1 (mockup Home). |

---

## 🟢 BAJA PRIORIDAD (Planificación / Backlog)

| Cliente | Servicio | Tarea | Estado | Notas / Enlaces |
| :--- | :--- | :--- | :---: | :--- |
| **Keller** | Desarrollo Web | Fase 3: Migración y montaje en WordPress | `[ ]` | Bloqueado por Fases 1 y 2. |
| **Riqueza Digital** | Estrategia | P2: Revisión integral de pricing (formación + dev a medida) | `[ ]` | Sesión dedicada. Ver [proximos-pasos-brief-v1.md](agencia/marketing/strategy/proximos-pasos-brief-v1.md) |
| **Riqueza Digital** | Infraestructura | P3.1: Setup GA4 + GSC + GTM + UTM tracking en riquezadigital.es | `[ ]` | Habilita medición del plan inbound desde día 1. |
| **Riqueza Digital** | Infraestructura | P3.2: Deploy Postiz self-hosted en servidor | `[ ]` | Para publicación multi-plataforma automatizada sin SaaS. |
| **Riqueza Digital** | Inteligencia Competitiva | P4.1: Dossier referentes IA-automation (Nate Herk, Ben Cord) | `[ ]` | Aplicar protocolo de inteligencia competitiva (igual que Vibiz). |
| **Riqueza Digital** | Estrategia | P4.2: Decidir repurpose o cierre de generaleads.es | `[ ]` | Decisión Kevin. Opciones: landing alternativa RD / subproducto / cierre. |

---

## 📅 Historial de Tareas Completadas

* **Riqueza Digital (Google Ads pipeline):** `pipelines/marketing-digital/ads/` reescrito — multi-cliente, ROAS/CPA, niveles campaign/adgroup, CLI standalone. [2026-05-28]
* **Riqueza Digital (Marketing WP):** Página `/servicios-google-ads/` creada como draft en WP (ID 6822, slug: servicios-google-ads) — Hero + 6 módulos + Proceso + FAQ GEO + schema Service+FAQPage+LocalBusiness. ⚠️ *Pendiente publicar* con datos reales Tecniclima. [2026-05-28]
* **Riqueza Digital (Auditoría Notion — F-010):** Fases A (inventario top-level) y B (triage + archivado + conexión raíces) completadas. Tareas enviadas a Notion. [2026-05-28]
* **F-011 /cierre-sesion:** Skill implementada con 7 pasos integrados (contexto, horas, SOPs, Notion, archivo sesión, propuestas sistema, resumen). Integrada con F-014. [2026-05-26]
* **F-012 /registrar-feature:** Skill implementada — auto-inventario de features en AGENCIA-AGENTICA.md con asignación de número, estado y ubicación. [2026-05-27]
* **F-015 WP REST API:** Patrón Registry + SOP documentado en `shared/sops/wordpress-rest-api-claude.md`. Variables `WP_RD_*` en Windows Registry. Funcional para riquezadigital.es. [2026-05-26]
* **P0.1 Rotación API keys:** 6 claves rotadas (2026-05-26). ⚠️ Meta Veganashi token: tarea Notion creada 2026-05-27 — verificar si fue rotado.
* **Keller (Fase 0):** Perfil completo creado, design system documentado (tokens colores, tipografías, componentes), añadida a CLAUDE.md. Autopilot ejecutado: 2 iteraciones, scores 9/8/9/8. [2026-05-26]
* **Riqueza Digital (Edición Video):** Pipeline optimizado — overlays abajo, Imagen 3 API, fallbacks semánticos, sonidos pop/swoosh. [2026-05-27]
* **F-014 SOP Library:** Estructura `shared/sops/` creada. SOPs activos: `gestion-claves-api-windows.md` ✓, `wordpress-rest-api-claude.md` ✓, `construir-skill-claude-code.md` ✓, `sop-bucle-generador-evaluador.md` (borrador), `seo-onpage-guidelines.md` (borrador), `manychat-n8n-integration.md` (borrador). [2026-05-26]
* **Spec Agencia Autónoma aprobada:** 5 agentes, matriz autoridad verde/amarillo/rojo, dashboard Next.js, 6 sprints definidos. Documento en `docs/superpowers/specs/2026-05-29-agencia-autonoma-design.md`. [2026-05-29]
* **Borrador curso Agencia Agéntica:** Subido a WP como draft (ID 6820). [2026-05-27]
* **Vibiz conectado:** Workspace "riquezadigital-s-workspace-1779734804241496773". Dossier inteligencia competitiva en `agencia/inteligencia-competitiva/vibiz/`. [2026-05-26]

---
*Última actualización: 2026-06-02*
