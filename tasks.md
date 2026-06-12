# 📋 Tablero de Control — Tareas de la Agencia (Agente Claude)

Este archivo es el panel de control exclusivo para el **Agente Claude**. Aquí se registran las tareas pendientes, en proceso y completadas de los distintos clientes y servicios, organizadas por prioridad.

> [!NOTE]
> Las tareas asignadas al **Usuario** se gestionan directamente en su Notion y no se trackean aquí, de acuerdo a las reglas del proyecto en [CLAUDE.md](./CLAUDE.md).

---

## 🔴 ALTA PRIORIDAD (Urgente / Bloqueante)

| Cliente | Servicio | Tarea | Estado | Notas / Enlaces |
| :--- | :--- | :--- | :---: | :--- |
| **Keller** | Desarrollo Web | Mockup Home HTML/CSS/JS completo (Fase 1) | `[ ]` | Plan en [plan-web.md](clients/keller-valentina/plan-web.md). Programado para el fin de semana (2026-06-06). |

---

## 🟡 MEDIA PRIORIDAD (Desarrollo Activo)

| Cliente | Servicio | Tarea | Estado | Notas / Enlaces |
| :--- | :--- | :--- | :---: | :--- |
| **Riqueza Digital** | Marketing | Actualizar página /servicios-google-ads/ (WP ID 6822) con métricas reales Tecniclima y publicar | `[ ]` | Kevin trae leads/mes y CPL. Fuente local: [google-ads-page.html](output/agency/google-ads-page.html). ⚠️ No publicar con benchmarks genéricos actuales. |
| **Veganashi + Tecniclima** | Agencia Autónoma | Sprint 1: Completar profiles + authority-matrix + intelligence/ por cliente | `[ ]` | Bloqueado por Sprint 0.5. Spec completa en [agencia-autonoma-design.md](docs/superpowers/specs/2026-05-29-agencia-autonoma-design.md) |
| **Tecniclima** | Google Ads | Ejecutar setup de OAuth y obtener refresh_token con el developer token activo | `[ ]` | Requisito: que el developer token esté verificado en Google. Ejecutar `python pipelines/marketing-digital/ads/shared/google_client.py --setup tecniclima`. |
| **Keller** | Desarrollo Web | Fase 2: Páginas interiores (Trámites, Consultoría, Marketing, Contacto, Blog) | `[ ]` | Bloqueado por Fase 1 (mockup Home). |

---

## 🟢 BAJA PRIORIDAD (Planificación / Backlog)

| Cliente | Servicio | Tarea | Estado | Notas / Enlaces |
| :--- | :--- | :--- | :---: | :--- |
| **Riqueza Digital** | Contenido | Crear 2º guión IG/LinkedIn con `/contenido:guion-instagram` (pilar: caso real o tutorial) | `[ ]` | Skill lista. Primer guión fue "agobia IA". Siguiente debe ser pilar distinto. |
| **Riqueza Digital** | Contenido | Integrar skill `/contenido:boveda-post` con `/contenido:guion-instagram` para generación multicanal | `[ ]` | Para derivar automáticamente guiones de redes (IG/LinkedIn) a partir de un post de la Bóveda de golpe. |
| **Riqueza Digital** | Marketing | Automatizar envío lead magnet por DM al comentar AGENCIA/SISTEMA/INFORME (n8n) | `[ ]` | Bloqueado: primero publicar artículo WP 6868. Luego sprint con Andrés. |

| Cliente | Servicio | Tarea | Estado | Notas / Enlaces |
| :--- | :--- | :--- | :---: | :--- |
| **Riqueza Digital** | SEO | Plan de SEO de Riqueza Digital: Configuración de Medición y Contenido Pilar | `[ ]` | Plan unificado para experto SEO. Incluye: (1) Setup GA4+GSC+GTM+UTM tracking en riquezadigital.es, (2) Redactar primer artículo pilar "Gobernanza de IA y Claude Team para Agencias", (3) Verificar marcado Schema LocalBusiness inyectado en WPCode. Todo alineado con [seo-onpage-guidelines.md](shared/sops/seo-onpage-guidelines.md). |
| **Riqueza Digital** | Infraestructura | Plan de Mejoras del Sistema Progresivo de SOPs y Automatizaciones (F-011/F-014) | `[ ]` | Incluye: (1) Hook de porcentaje real de contexto en skill `/cierre-sesion` (v2), (2) Integración del buscador de SOPs en UI del Dashboard (Tier 3), (3) Migración de notificaciones email a Telegram en workflows n8n (F-016/F-017). |
| **Riqueza Digital** | Agencia Autónoma | Planificar e implementar infraestructura híbrida OpenClaw + Hermes (Sprint 4/5) | `[ ]` | Configurar OpenClaw (gateway) + Hermes (sandbox/Capa 5) guiado por [hermes_openclaw_guide.md](file:///C:/Users/kein-/.gemini/antigravity-ide/brain/ff26b3d0-3d03-49b0-8183-c64fbf6ab27c/hermes_openclaw_guide.md). |
| **Riqueza Digital** | Infraestructura | P3.2: Deploy Postiz self-hosted en servidor | `[ ]` | Para publicación multi-plataforma automatizada sin SaaS. |
| **Riqueza Digital** | Automatización | Outbound: Crear flujo n8n para conectar exportación de Ampleleads (Apollo) with API de Instantly | `[ ]` | Automatización de carga de prospectos. |
| **Riqueza Digital** | Marketing | Outbound: Configurar secuencia de 3 correos "CEO Forward" en Instantly | `[ ]` | Plantillas definidas en [ejecucion-inbound-y-outbound.md](agencia/marketing/strategy/ejecucion-inbound-y-outbound.md). |
| **Riqueza Digital** | Contenido | Grabar el primer vídeo del "Caso Meta" (hablando a cámara) | `[ ]` | Guion estructurado en [ejecucion-inbound-y-outbound.md](agencia/marketing/strategy/ejecucion-inbound-y-outbound.md). |
| **Riqueza Digital** | Estrategia | P4.2: Decidir repurpose o cierre de generaleads.es | `[ ]` | Decisión Kevin. Opciones: landing alternativa RD / subproducto / cierre. |
| **Riqueza Digital** | Inteligencia Competitiva | P4.1: Dossier referentes IA-automation (Nate Herk, Ben Cord) | `[ ]` | Aplicar protocolo de inteligencia competitiva (igual que Vibiz). |
| **Keller** | Desarrollo Web | Fase 3: Migración y montaje en WordPress | `[ ]` | Bloqueado por Fases 1 y 2. |

---

## 📅 Historial de Tareas Completadas

* **F-014 Biblioteca de SOPs:** Consolidación de biblioteca de SOPs, skill `/sistema:buscar-sop` implementada, y creación de 8 SOPs base (setup WP, Meta troubleshoot, Google Ads MCC, onboarding, fix Elementor 500, Tally+MailerLite n8n, guiones Notion y CORS Font Fix). [2026-06-04]
* **Agencia (WIP=1):** Activada política WIP=1 en inventario `AGENCIA-AGENTICA.md`. F-010 y F-012 pausados formalmente para priorizar la consolidación de F-011 como guardrail. [2026-06-04]
* **F-013 Autopilot (Base Python):** Base del bucle Generador-Evaluador con checkpoints Git, límites de presupuesto, orquestador runner y prompts estéticos completada e integrada con Playwright (100% de evals exitosos). [2026-06-04]
* **Riqueza Digital (Bóveda):** Página restaurada de HTTP 500 — `_elementor_data` corrompido reparado via WPCode con `$wpdb->update` directo a DB (bypass hooks Elementor/Yoast). [2026-06-03]
* **Riqueza Digital (Bóveda):** Form Tally (ID: PdkJZ5) embebido. Workflow n8n "Bóveda — Suscripción Newsletter" (ID: wxMxwdVcwV3YoQdD) activo — Tally→MailerLite testado y funcionando. [2026-06-03]
* **Riqueza Digital (SEO):** Schema LocalBusiness añadido via WPCode HTML snippet (pendiente Kevin verificar Header). [2026-06-03]
* **Riqueza Digital (Google Ads pipeline):** `pipelines/marketing-digital/ads/` reescrito — multi-cliente, ROAS/CPA, niveles campaign/adgroup, CLI standalone. [2026-05-28]
* **Riqueza Digital (Marketing WP):** Página `/servicios-google-ads/` creada como draft en WP (ID 6822, slug: servicios-google-ads) — Hero + 6 módulos + Proceso + FAQ GEO + schema Service+FAQPage+LocalBusiness. ⚠️ *Pendiente publicar* con datos reales Tecniclima. [2026-05-28]
* **Riqueza Digital (Auditoría Notion — F-010):** Fases A (inventario top-level) y B (triage + archivado + conexión raíces) completadas. Tareas enviadas a Notion. [2026-05-28]
* **F-011 /cierre-sesion:** Skill implementada con 7 pasos integrados. [2026-05-26]
* **F-012 /registrar-feature:** Skill implementada — auto-inventario AGENCIA-AGENTICA.md. [2026-05-27]
* **F-015 WP REST API:** Patrón Registry + SOP documentado. Variables `WP_RD_*` en Windows Registry. [2026-05-26]
* **P0.1 Rotación API keys:** 6 claves rotadas (2026-05-26).
* **Keller (Fase 0):** Perfil completo creado, design system documentado. [2026-05-26]
* **Riqueza Digital (Edición Video):** Pipeline optimizado — overlays abajo, Imagen 3 API, fallbacks semánticos. [2026-05-27]
* **Spec Agencia Autónoma aprobada:** 5 agentes, matriz autoridad, dashboard Next.js, 6 sprints definidos. [2026-05-29]
* **Riqueza Digital (Web):** Bóveda (ID 6835) + Web IA (ID 6836) + Posicionamiento IA (ID 6837) creadas con RD design system. Menú Servicios+Bóveda actualizado. Fix CSS 71 instancias doble-brace. [2026-06-03]
* **Riqueza Digital (Notion Logs):** Creada base de datos de "Log de Acciones Agenticas" (ID `374d2fec-4b82-8148-bad1-c996c8b5f65e`), subpágina bajo "Gestión Interna" y enlaces en las fichas de los clientes. Integrados agentes Python para registrar logs automáticamente. [2026-06-03]
* **Riqueza Digital (CORS Fix):** Resuelto error CORS de fuentes Poppins/Heebo en la Home mediante reescritura de URLs de Elementor y purga de caché de WP Fastest Cache, validado con Playwright. [2026-06-03]
* **Veganashi (Reporting):** Creada skill genérica y escalable de generación de informes mensuales (`/marketing:reporte-mensual`) y generado el informe de rendimiento y saneamiento de Mayo 2026. [2026-06-04]
* **Tecniclima (Google Ads):** Creado y configurado `profile.json` de Google Ads con el `customer_id` y claves OAuth iniciales. [2026-06-04]

---
*Última actualización: 2026-06-04*
