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
| [wp-edit (skill)](../../.claude/commands/web/wp-edit.md) | Desarrollo Web | 🔧 Verificado | Skill `/web:wp-edit`: flujo completo leer → editar quirúrgico → validar → publicar página WP. Incluye Yoast SEO, Playwright visual y errores comunes. |
| [campaign-monitor-n8n.md](campaign-monitor-n8n.md) | Automatizaciones / Marketing | 🔧 Verificado | Crear workflow n8n de monitoreo diario Meta Ads: schedule → API → detección anomalías → alerta Gmail. Token Meta, umbrales configurables. |
| [campaign-optimizer-n8n.md](campaign-optimizer-n8n.md) | Automatizaciones / Marketing | 🔧 Verificado | Workflow n8n semanal: Meta API (semana + ad sets) → Claude API → propuestas numeradas → Gmail. Incluye Feedback Updater (bucle aprendizaje 7 días). |
| [meta-ads-error-fix-api.md](meta-ads-error-fix-api.md) | Marketing | 🔧 Verificado | Fix de ad sets WITH_ISSUES via Graph API: audiencia eliminada, ad set expirado, extensión end_time. Sin necesidad de Ads Manager UI. |

---

## Estructura de carpetas

```
shared/sops/
├── README.md                          ← Este archivo (índice)
├── _plantilla-sop.md                  ← Plantilla base para nuevos SOPs
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
