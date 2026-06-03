# SOP: Campaign Monitor en n8n (Meta Ads)

**Área:** Automatizaciones / Marketing Digital  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-03  
**Clientes donde se aplicó:** Veganashi  
**Tiempo estimado:** 30–45 minutos

---

## Resumen

Crea un workflow n8n que monitoriza métricas de Meta Ads diariamente a las 08:07h y envía alerta por email (o Telegram en Sprint 4) solo cuando detecta anomalías. Silencio = todo OK.

---

## Pre-requisitos

- [ ] Perfil del cliente con `clients/<cliente>/intelligence/campaign-baseline.json` creado
- [ ] Meta Access Token válido disponible (en `.env` local)
- [ ] `account_id` de Meta Ads del cliente
- [ ] Credencial Gmail configurada en n8n (`gmailOAuth2`)
- [ ] n8n activo y accesible

---

## Pasos

### 1. Verificar baseline

Abrir `clients/<cliente>/intelligence/campaign-baseline.json`. Confirmar que tiene:
- `account_id` real (no placeholder)
- Al menos las métricas de referencia: `ctr_real_pct`, `cpc_real_eur`, `gasto_diario_eur`
- Umbrales definidos: `umbral_monitor_ctr_floor_pct`, `umbral_monitor_cpc_ceil_eur`, `umbral_monitor_spend_min_eur`

Si faltan → completar antes de crear el workflow (los umbrales alimentan la lógica de detección).

### 2. Crear workflow via MCP n8n

Estructura de nodos en orden:

```
[Schedule 08:07] → [Set Config] → [Meta API Insights] → [Detectar Anomalías] → [¿Hay Anomalía?] → [Gmail Alert]
```

**Nodo Set Config** — variables configurables:
```
META_ACCESS_TOKEN  → pegar desde .env (⚠️ caduca ~60 días)
ACCOUNT_ID         → act_XXXXXXXXX (sin prefijo "act_" en la URL del API)
CTR_FLOOR_PCT      → del baseline (ej: 0.60)
CPC_CEIL_EUR       → del baseline (ej: 1.80)
SPEND_MIN_DAILY_EUR → 5.0 (alerta si gasto < €5, posible campaña pausada)
ALERT_EMAIL        → info@riquezadigital.es
```

**Nodo Meta API Insights** — endpoint:
```
GET https://graph.facebook.com/v21.0/act_{{ACCOUNT_ID}}/insights
  ?fields=spend,impressions,clicks,ctr,cpc,reach
  &date_preset=yesterday
  &access_token={{META_ACCESS_TOKEN}}
```
⚠️ Activar `continueOnFail: true` — si el token expira, el workflow debe continuar y reportar el error.

**Nodo Detectar Anomalías** — lógica en Code (JavaScript):
```javascript
// 1. Si API falló → alerta con el error
// 2. Parsear: spend, ctr, cpc, impressions, reach, date
// 3. Comprobar vs umbrales de Set Config
// 4. Retornar: { hasAnomaly, alerts[], alertsText, métricas... }
```

**Nodo IF** — condición: `alerts.length > 0`
- Rama true → Gmail Alert
- Rama false → no hacer nada (silencio)

### 3. Configurar token en Set Config

En n8n UI: abrir workflow → nodo "Set Config" → reemplazar `PEGA_TOKEN_META_AQUI` con el valor de `META_ACCESS_TOKEN` del `.env`.

### 4. Activar y testar manualmente

1. Activar el workflow (toggle en n8n)
2. Desde la UI de n8n: botón "Test workflow" (lanza ejecución manual)
3. Verificar nodo "Detectar Anomalías": debe tener `hasAnomaly`, métricas reales del día anterior

**Resultado esperado:** ejecución en <2s, `status: success`, métricas de la cuenta visibles.

### 5. Actualizar baseline con métricas reales

Si las métricas del test son significativamente distintas al baseline estimado → actualizar `campaign-baseline.json` con los valores reales obtenidos de la API.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| `is_ads_mcp_enabled: false` en Meta MCP | Rollout gradual de Meta | No bloquea: usar HTTP Request directo a Meta API (no MCP) |
| Error 190 en Meta API | Token expirado | Renovar token en Meta Business → actualizar Set Config |
| `data: []` en respuesta Meta | Cuenta sin actividad ayer | Normal si la campaña estuvo pausada; revisar manualmente |
| Workflow no se puede testear con `n8n_test_workflow` MCP | Schedule trigger (no webhook) | Testear desde UI de n8n → botón "Test workflow" |

---

## Decisiones clave

- **Decisión:** Gmail como canal de alerta (no Telegram)  
  **Razón:** Telegram bot no configurado hasta Sprint 4 (requiere VPS + OpenClaw + Andrés)  
  **Alternativa descartada:** Telegram directo — bloqueado por falta de bot token y canal configurado

- **Decisión:** `continueOnFail: true` en nodo Meta API  
  **Razón:** Si el token expira, queremos recibir alerta del error — no silencio

- **Decisión:** Principio "silencio = OK"  
  **Razón:** Un monitor que envía email todos los días se ignora. Solo alertar cuando hay algo que hacer.

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| `ACCOUNT_ID` | Set Config | Veganashi: `928041200992402` |
| `CTR_FLOOR_PCT` | Umbral alerta | 0.6% Meta / ajustar por sector |
| `CPC_CEIL_EUR` | Umbral alerta | €1.80 ecommerce / €3.00 servicios B2B |
| `SPEND_MIN_DAILY_EUR` | Detecta campañas pausadas | 5% del budget diario esperado |
| Canal de alerta | Nodo final | Gmail ahora / Telegram en Sprint 4 |

**Preguntas a hacer antes de crear el monitor:**
1. ¿Cuál es el account_id de Meta Ads?
2. ¿Cuál es el CTR y CPC histórico de referencia (baseline)?
3. ¿A qué email deben llegar las alertas?

---

## Notas adicionales

- El token Meta caduca aproximadamente cada 60 días. Crear tarea de recordatorio en Notion.
- En Sprint 4: sustituir el nodo Gmail por HTTP Request al bot de Telegram (canal Operaciones).
- El workflow actual monitoriza solo Meta. Para Google Ads: crear workflow paralelo usando Google Ads API cuando esté disponible el developer token.

---

*Última sesión que actualizó este SOP: 2026-06-03 — creación inicial tras implementar Campaign Monitor Veganashi*
