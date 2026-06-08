# shared/sops/ — Biblioteca de Procesos de Riqueza Digital

> **Para qué sirve esto:** documentación de procesos repetibles, lista para que cualquier persona del equipo (o Claude Code) pueda ejecutar un proceso por primera vez sin cometer los errores que ya hemos cometido.

---

## Cómo se usa

**Como operador:** antes de empezar un proceso nuevo con un cliente, busca si ya existe un SOP. Si existe, síguelo y anota desviaciones. Si no existe, créalo al terminar.

**Con Claude Code:** pregunta directamente — *"¿Cómo hacemos el setup de WordPress para un cliente nuevo?"* o *"¿Qué errores comunes hay con Meta Ads en la fase de aprendizaje?"* — Claude leerá el SOP correspondiente y te guiará.

**Para nuevas incorporaciones:** este directorio es el punto de entrada. Leer primero `onboarding/` y luego los SOPs de tu área.

---

## SOPs disponibles

| Archivo | Área | Estado | Descripción |
|---------|------|--------|-------------|
| [gestion-claves-api-windows.md](gestion-claves-api-windows.md) | Seguridad / Infra | 🔧 Verificado | Almacenar y rotar claves API con variables de entorno de Windows. Incluye variables WordPress REST API (`WP_RD_*`). |
| [manychat-n8n-integration.md](manychat-n8n-integration.md) | Automatizaciones | 🌱 Draft | Integración entre ManyChat y n8n via webhook |
| [seo-onpage-guidelines.md](seo-onpage-guidelines.md) | Marketing / SEO | 🌱 Draft | Directrices de SEO on-page para webs de clientes |
| [construir-skill-claude-code.md](construir-skill-claude-code.md) | Desarrollo / Producto | 🔧 Verificado | Crear un nuevo slash command (`/nombre`) para Claude Code en `.claude/commands/` |
| [wordpress-rest-api-claude.md](wordpress-rest-api-claude.md) | Desarrollo Web | 🔧 Verificado | Acceso a WordPress REST API desde Claude Code vía Registry de Windows + Python. Patrón sin MCP. |
| [wordpress-setup-nuevo-cliente.md](desarrollo-web/wordpress-setup-nuevo-cliente.md) | Desarrollo Web | 🔧 Verificado | Proceso base para configurar e instalar WordPress en nuevos clientes (DNS, plugins esenciales, APIs). |
| [wp-fix-http500-elementor-db.md](desarrollo-web/wp-fix-http500-elementor-db.md) | Desarrollo Web | 🔧 Verificado | Recuperar WordPress de error HTTP 500 reparando el metadato de Elementor directamente en base de datos. |
| [wp-fix-cors-fonts.md](desarrollo-web/wp-fix-cors-fonts.md) | Desarrollo Web | 🔧 Verificado | Corregir bloqueos CORS en la carga de tipografías externas en Elementor y WordPress. |
| `/web:wp-edit` (skill) | Desarrollo Web | 🔧 Verificado | Skill `/web:wp-edit`: flujo completo leer → editar quirúrgico → validar → publicar página WP. Incluye Yoast SEO, Playwright visual y errores comunes. |
| [campaign-monitor-n8n.md](campaign-monitor-n8n.md) | Automatizaciones / Marketing | 🔧 Verificado | Crear workflow n8n de monitoreo diario Meta Ads: schedule → API → detección anomalías → alerta Gmail. Token Meta, umbrales configurables. |
| [campaign-optimizer-n8n.md](campaign-optimizer-n8n.md) | Automatizaciones / Marketing | 🔧 Verificado | Workflow n8n semanal: Meta API (semana + ad sets) → Claude API → propuestas numeradas → Gmail. Incluye Feedback Updater (bucle aprendizaje 7 días). |
| [n8n-tally-mailerlite-integration.md](automatizaciones/n8n-tally-mailerlite-integration.md) | Automatizaciones | 🔧 Verificado | Integración de formularios Tally con listas de MailerLite usando webhooks de n8n. |
| [meta-ads-error-fix-api.md](meta-ads-error-fix-api.md) | Marketing | 🔧 Verificado | Fix de ad sets WITH_ISSUES via Graph API: audiencia eliminada, ad set expirado, extensión end_time. Sin necesidad de Ads Manager UI. |
| [meta-ads-troubleshooting.md](marketing/meta-ads-troubleshooting.md) | Marketing | 🔧 Verificado | Resolución de incidencias en Meta Ads (píxeles, conjuntos con fallos, aprendizaje limitado, tokens). |
| [alta-nuevo-cliente.md](onboarding-cliente/alta-nuevo-cliente.md) | Onboarding Cliente | 🔧 Verificado | Flujo administrativo y estratégico F-001 de alta para nuevos clientes en el sistema. |
| [google-ads-mcc-sheets-export.md](marketing/google-ads-mcc-sheets-export.md) | Marketing | 🌱 Draft | Extracción y volcado automático de métricas de Google Ads MCC a Google Sheets con Cuenta de Servicio. |
| [guiones-redes-mcp-notion.md](produccion-contenido/guiones-redes-mcp-notion.md) | Producción de Contenido | 🔧 Verificado | Generación automatizada de guiones de video e hilos duales y almacenamiento directo en la base de datos de Notion. |
| [video-ads-cinematicos-ia.md](video-ads-cinematicos-ia.md) | Producción de Contenido | 🌱 Draft | Crear spots publicitarios completos (imágenes, animación, voz, música, montaje) desde fotos de producto vía Claude Code + Higgsfield + ElevenLabs + FFmpeg. Para clientes con producto físico. |
| [prospeccion-cliente-ads.md](prospeccion-cliente-ads.md) | Marketing / Ventas | 🌱 Draft | Investigar web de prospect + cualificación en llamada + propuesta de 3 niveles de presupuesto para servicios de ads (Meta + Google). |

---

## Estructura de carpetas

```
shared/sops/
├── README.md                          ← Este archivo (índice)
├── _plantilla-sop.md                  ← Plantilla base para nuevos SOPs
├── desarrollo-web/
│   ├── wordpress-setup-nuevo-cliente.md
│   ├── wp-fix-http500-elementor-db.md
│   └── wp-fix-cors-fonts.md
├── marketing/
│   ├── meta-ads-troubleshooting.md
│   └── google-ads-mcc-sheets-export.md
├── onboarding-cliente/
│   └── alta-nuevo-cliente.md
├── automatizaciones/
│   └── n8n-tally-mailerlite-integration.md
├── produccion-contenido/
│   └── guiones-redes-mcp-notion.md
├── gestion-claves-api-windows.md      ← Seguridad: variables de entorno + rotación de claves
├── manychat-n8n-integration.md        ← Automatizaciones: ManyChat + n8n
└── seo-onpage-guidelines.md           ← Marketing: SEO on-page
```

---

## Cuándo se actualiza un SOP

El SOP se actualiza (o se crea) al **cerrar una sesión de trabajo** si:
- Se ejecutó un proceso que se repetirá con otros clientes
- Se encontró un problema no documentado y se resolvió
- Se tomó una decisión técnica o estratégica relevante para futuros proyectos

**Regla de oro:** si tardaste más de 15 minutos resolviendo algo que debería ser obvio → anótalo.

---

## Convención de nombres de archivo

`<area>/<proceso-en-kebab-case>.md`

Ejemplos:
- `desarrollo-web/wordpress-setup-nuevo-cliente.md`
- `marketing/meta-ads-troubleshooting.md`
- `marketing/google-ads-mcc-export-sheets.md`
- `automatizaciones/n8n-webhook-setup.md`
- `onboarding-cliente/alta-nuevo-cliente.md`

---

## Niveles de madurez

| Nivel | Significado |
|-------|-------------|
| 🌱 Draft | Primeras notas, no verificado |
| 🔧 Verificado | Ejecutado al menos 1 vez con éxito |
| 💰 Maduro | Ejecutado 3+ veces, problemas comunes documentados |
