# Próximos pasos — tras Brief Estratégico v1

> **Generado:** 2026-05-26 al cierre de la sesión del Brief
> **Para:** Kevin (auto-ejecutable con Claude Code en próximas sesiones)
> **Brief de referencia:** `agencia/marketing/strategy/brief-estrategico.md`

Agenda priorizada en 5 niveles. Hacer en orden — no saltar P0 antes que el resto.

---

## 🔴 P0 — CRÍTICO (hacer YA, antes de cualquier otra sesión técnica)

### P0.1 — Rotar 6 API keys vistas en chat de la sesión 2026-05-26

Las 6 claves quedaron en el contexto de un chat de Claude. Aunque `.mcp.json` está protegido por gitignore, la mejor higiene es rotarlas. Acción manual desde cada consola web:

- [x] **ANTHROPIC_API_KEY** → console.anthropic.com → Settings → API Keys → revoke + generate new
- [x] **META_ACCESS_TOKEN** → developers.facebook.com → Graph API Explorer / Business Settings → regenerar *(⚠️ Token Veganashi expuesto en git 2026-05-27 — verificar rotación, tarea Notion creada)*
- [x] **META_APP_SECRET** → developers.facebook.com → App Settings → Basic → Reset secret
- [x] **GEMINI_API_KEY** → aistudio.google.com → API Keys → revoke + create new
- [x] **NOTION_API_KEY** → notion.so/my-integrations → revoke + create new integration
- [x] **N8N_API_KEY** → tu instancia n8n hstgr.cloud → Settings → API → regenerate

**Tiempo total estimado:** 30-45 min.

**Importante:** NO actualizar `.mcp.json` con las nuevas claves todavía — eso se hace en P1 directamente como variables de entorno. Hasta entonces, tus MCPs no funcionarán. Si necesitas que sigan funcionando MIENTRAS migras, haz P0 + P1 en la misma sesión.

> ✅ **Completado 2026-05-26.** (Ref: INDEX sesión tarde + sesión 2026-05-27_2118)

---

## 🟠 P1 — Sesión técnica inmediata con Claude Code (~2h)

> ⚠️ **Parcialmente completado.** Variables WP en Registry ✅. MCPs funcionando ✅. Pendiente verificar migración `.mcp.json` a `${env:VAR}` (no se puede leer sin avisar) y auditoría completa de secretos. (Ref: sesiones 2026-05-26_1958, 2026-05-27_2118)

Abre nueva sesión y dile: *"Sesión técnica de migración de secretos a variables de entorno + auditoría repo"*.

### P1.1 — Setup variables de entorno Windows con las 6 nuevas claves

Crear variables de usuario en Windows (PowerShell o GUI):
- `META_ACCESS_TOKEN`, `META_APP_SECRET`, `META_AD_ACCOUNT_ID`
- `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`
- `NOTION_API_KEY`
- `N8N_API_URL`, `N8N_API_KEY`

Reiniciar PowerShell/Claude Code después de setear.

### P1.2 — Migrar `.mcp.json` para usar `${env:VAR}` en vez de claves hardcoded

Reescribir el fichero para que NINGUNA clave aparezca en texto plano. Solo referencias `${env:NOMBRE_VAR}`.

### P1.3 — Auditoría completa del repo: buscar otros secretos

Grep recursivo del repo en busca de:
- Tokens (`sk-`, `EAA`, `AIza`, `ntn_`, `eyJ`)
- Strings tipo "secret", "password", "api_key", "token"
- `.env` files no listados en `.gitignore`
- Scripts con credenciales hardcoded

### P1.4 — Limpiar MCP de Klaviyo (ya estamos en `.mcp.json`)

Eliminar la entrada de Klaviyo si existe — no se usa.

### P1.5 — Test final: verificar que todos los MCPs siguen funcionando con variables de entorno

Probar Notion, Meta Ads, n8n, Gemini en orden.

---

## 🟡 P2 — Bloqueante estratégico (sesión dedicada, ~2-3h)

### P2.1 — Revisión integral de pricing: formación + desarrollo a medida

> **CRÍTICO para Q1.** Sin esto, todo el plan inbound atrae leads a precios obsoletos. Lo confesaste tú mismo durante el brief.

Inputs para la sesión:
- Catálogo actual web (4 formaciones + Promptathon)
- Ventas reales últimos 3 meses (1h €90-120, 3h €400, dev €1.500)
- Benchmark de la competencia (referente: Promptathon ya está en €12k)
- Posicionamiento del brief (P5 — in-house, no curso enlatado)

Output esperado: tabla nueva de precios para cada línea (formación 1h, 3h, in-company corta, in-company larga, Promptathon, desarrollo a medida según tier), publicada o no en web.

---

## 🟢 P3 — Setup técnico que habilita el plan inbound (Andrés NO necesario, contigo basta)

### P3.1 — Setup GA4 + GSC + UTM tracking + GTM en riquezadigital.es

Para tener medición desde día 1 del plan inbound (sesión 4). Sin esto, todo el reporting es opaco.

### P3.2 — Deploy Postiz self-hosted en tu servidor disponible

Para automatizar programación de publicaciones IG/LinkedIn/etc desde tu sistema agéntico, sin SaaS.

---

## 🔵 P4 — Inteligencia y exploración estratégica

### P4.1 — Dossier referentes IA-automation: Nate Herk + Ben Cord

Aplicar protocolo de inteligencia competitiva (igual que hicimos con Vibiz). Sesión dedicada.

### P4.2 — Decidir repurpose o cierre de `generaleads.es`

Tienes el dominio dormante. ¿Lo enchufas como landing alternativa de RD, como subproducto, o lo dejas morir?

---

## ⚪ P5 — Físico (cuando llegue el momento, no urgente)

### P5.1 — Comprar panel de iluminación (~€40-80)

Para batch de grabación de reels.

### P5.2 — Esperar iPhone nuevo antes de batch grande de grabación

La calidad de cámara compensa por sí sola.

---

## Resumen ejecutivo de la cola

| Bloque | Tareas | Tiempo estimado | Cuándo |
|--------|--------|-----------------|--------|
| P0 — Rotar claves | 6 | 30-45 min | YA, manual |
| P1 — Migrar a env vars + auditoría | 5 | 2h | Próxima sesión técnica |
| P2 — Pricing review | 1 | 2-3h | Sesión dedicada Q1 |
| P3 — Setup técnico inbound | 2 | 4-6h total | Tras P1 |
| P4 — Inteligencia + ops | 2 | 1-2h c/u | Cuando haya hueco |
| P5 — Físico | 2 | flexible | Flexible |

**Foco máximo:** P0 → P1 → P2 son la ruta crítica antes de poder ejecutar las sesiones 2-4 del Pack de Onboarding Estratégico con calidad.
