# SOP: Campaign Optimizer en n8n (Meta Ads)

**Área:** Automatizaciones / Marketing Digital  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-03  
**Clientes donde se aplicó:** Veganashi  
**Tiempo estimado:** 45–60 minutos (setup inicial) / 5 minutos (mantenimiento semanal)

---

## Resumen

Crea dos workflows n8n coordinados que forman el bucle de optimización semanal:
1. **Campaign Optimizer** (lunes 09:03) — analiza la semana con Claude API y envía propuestas numeradas por email
2. **Feedback Updater** (diario 08:05) — detecta acciones de 7+ días pendientes de evaluación y avisa a Kevin

El bucle completo: Meta API → Claude analiza → Kevin aprueba propuesta → se toma acción → 7 días después Feedback Updater recuerda evaluar → Kevin registra resultado → Claude aprende para la semana siguiente.

---

## Pre-requisitos

- [ ] Campaign Monitor activo y verificado (F-016) — el Optimizer usa el mismo token Meta
- [ ] `clients/<cliente>/intelligence/campaign-baseline.json` con datos reales
- [ ] `clients/<cliente>/intelligence/feedback-log.json` inicializado
- [ ] API key de Anthropic (console.anthropic.com → API Keys → Create)
- [ ] Gmail OAuth configurado en n8n (se reutiliza del Campaign Monitor)

---

## IDs de Workflows (Veganashi)

| Workflow | ID n8n | Schedule | Estado |
|---------|--------|----------|--------|
| Campaign Optimizer | `HOI5Qkfu2FCTSv5j` | Lunes 09:03h Madrid | Inactivo (falta API key) |
| Feedback Updater | `9wbJOSrBIAoYwaO8` | Diario 08:05h Madrid | Inactivo |

---

## Paso 1 — Añadir API key Anthropic al Optimizer

1. Abrir n8n → workflow `Campaign Optimizer — Veganashi (lunes 09:03)`
2. Nodo **Set Config** → campo `CLAUDE_API_KEY`
3. Reemplazar `PEGA_CLAVE_ANTHROPIC_AQUI` con tu API key real
4. Guardar

**Dónde obtener la clave:** [console.anthropic.com](https://console.anthropic.com) → Settings → API Keys

> ⚠️ El token Meta (`META_ACCESS_TOKEN`) ya está copiado del Campaign Monitor. No hace falta modificarlo.

---

## Paso 2 — Verificar flujo del Optimizer

Antes de activar, ejecutar test manual:

1. En el workflow, hacer clic en el nodo `⏰ Schedule lunes 09:03`
2. Pinchar "Test step" o usar el botón "Execute workflow" desde el inicio

**Si falla en `Claude API - Generar Propuestas`:** verificar que la API key sea válida y que la cuenta Anthropic tenga crédito.

**Si falla en `Meta API - Week Account`:** el token Meta puede haber expirado (vida útil ~60 días). Ver SOP de Campaign Monitor para renovación.

**Si el email llega pero sin propuestas:** el CTR y CPC están dentro del rango normal — esto es el comportamiento correcto.

---

## Paso 3 — Activar ambos workflows

1. Optimizer: toggle "Active" → ON
2. Feedback Updater: toggle "Active" → ON

El Optimizer correrá automáticamente el próximo lunes a las 09:03h (Madrid).  
El Feedback Updater correrá mañana a las 08:05h (y todos los días siguientes).

---

## Mantenimiento semanal — Ciclo de operación

### Cada lunes ~09:05h

Kevin recibe email con propuestas. Responde por email (o dice a Claude Code):
- `"Aprobar propuestas 1 y 3"` — Claude Code actualiza el FEEDBACK_LOG
- `"Skip"` — no hacer nada esta semana
- `"Todo"` — aprobar todas

### 7 días después de una acción aprobada

Kevin recibe recordatorio del Feedback Updater. Revisa Meta Ads Manager y dice a Claude Code:
```
"Actualiza el feedback-log de Veganashi: la acción 'pausar conjunto X' 
resultó en CTR +15% y CPC -10%. Aprendizaje: pausar ad sets con CTR < 0.5% funciona."
```

Claude Code usa el n8n MCP para actualizar el campo `FEEDBACK_LOG` en el Set Config del Optimizer.

---

## Cómo actualizar el FEEDBACK_LOG desde Claude Code

Cuando Kevin aprueba una acción o registra un resultado:

```
# Claude Code lee el FEEDBACK_LOG actual del Optimizer
# Añade/actualiza la entrada
# Usa mcp__n8n-mcp__n8n_update_partial_workflow para actualizar el nodo Set Config
# También actualiza el mismo campo en el Feedback Updater
```

**Patrón de entrada en el log:**
```json
{
  "fecha": "2026-06-10",
  "accion": "Pausar conjunto X con CTR 0.3%",
  "contexto": "CTR muy bajo vs baseline 3.24%",
  "resultado_7d": {
    "cpa_delta": -12,
    "leads_delta": 8
  },
  "aprendizaje": "pausar_ad_set_ctr_bajo_0.5_efectivo",
  "aprobado_por": "kevin"
}
```

---

## Renovación del token Meta (~cada 60 días)

El token Meta en el Set Config del Optimizer debe renovarse junto con el del Campaign Monitor.  
Ver `shared/sops/campaign-monitor-n8n.md` sección "Renovación del Token Meta".

> Al renovar en Campaign Monitor, copiar el mismo token al Set Config del Optimizer.

---

## Problemas comunes

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Email no llega los lunes | Workflow inactivo o token caducado | Verificar estado en n8n, revisar ejecuciones fallidas |
| Propuestas sin sentido o incoherentes | API key Anthropic inválida o sin crédito | Verificar en console.anthropic.com |
| "Sin propuestas" semana tras semana | Métricas normales (comportamiento correcto) | Si dura > 3 semanas, revisar si los umbrales baseline son correctos |
| Feedback Updater envía recordatorio demasiado pronto | Fechas en FEEDBACK_LOG incorrectas | Verificar formato YYYY-MM-DD en las entradas |
| Error `JSON.parse` en Preparar Request Claude | FEEDBACK_LOG malformado en Set Config | Validar el JSON en jsonlint.com antes de pegar |

---

## Sprint 4 — Mejoras previstas

- Reemplazar Gmail por **Telegram** (Kevin responde en el móvil con un número)
- **Auto-evaluación**: Feedback Updater consulta Meta API para el período post-acción y calcula deltas automáticamente (sin que Kevin revise manualmente)
- Extender a **Tecniclima Google Ads** cuando haya developer token
