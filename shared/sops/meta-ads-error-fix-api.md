# SOP: Fix de Errores en Meta Ads via Graph API

**Área:** Marketing  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-03  
**Clientes donde se aplicó:** Veganashi  
**Tiempo estimado:** 20–40 minutos

---

## Resumen

Diagnóstico y corrección de errores en ad sets (`effective_status: WITH_ISSUES`) usando la Meta Graph API directamente desde Claude Code, sin necesidad de acceder a la interfaz de Ads Manager.

Útil cuando: el Ads Manager no carga en el navegador, o cuando los errores requieren modificar campos que la UI no permite editar fácilmente.

---

## Pre-requisitos

- [ ] Variable de entorno `META_ACCESS_TOKEN` configurada en Windows (ver `shared/sops/gestion-claves-api-windows.md`)
- [ ] ID de la cuenta de anuncios (`act_XXXXXXXXX`) — en `clients/<cliente>/profile.md`
- [ ] ID del ad set con error (visible en la URL de Ads Manager o en el mensaje de error)

---

## Pasos

### 1. Diagnosticar el ad set con error

```powershell
$token = $env:META_ACCESS_TOKEN
$result = Invoke-RestMethod -Uri "https://graph.facebook.com/v21.0/<ADSET_ID>?fields=id,name,status,effective_status,targeting,issues_info,start_time,end_time,campaign_id&access_token=$token" -Method GET
$result | ConvertTo-Json -Depth 8
```

**Resultado esperado:** JSON con `issues_info` describiendo el error.

Errores comunes en `issues_info[].error_code`:
- `2446446` — audiencia personalizada o lookalike eliminada
- `2446149` — presupuesto insuficiente para el período configurado

### 2. Listar audiencias disponibles en la cuenta

```powershell
$token = $env:META_ACCESS_TOKEN
$result = Invoke-RestMethod -Uri "https://graph.facebook.com/v21.0/act_<ACCOUNT_ID>/customaudiences?fields=id,name,subtype,delivery_status,operation_status&limit=50&access_token=$token" -Method GET
$result.data | Format-Table -AutoSize
```

**Qué buscar:** audiencias con `delivery_status.code = 200` y `operation_status.code = 200` (ambos = sin problemas).

### 3. Identificar si el ad set tiene fecha de fin expirada

Si `end_time` ya pasó, Meta no permite editar el ad set. Se detecta porque el error dice:
> "No puedes editar este anuncio porque forma parte de un conjunto de anuncios programado que ya ha finalizado."

Solución: extender `end_time` a 30 días vista (no extender demasiado — ver nota sobre presupuesto).

### 4. Aplicar el fix en una sola llamada

Combinar la extensión de fecha + corrección de targeting en un único POST:

```powershell
$token = $env:META_ACCESS_TOKEN
$adsetId = "<ADSET_ID>"

$targetingJson = '<JSON de targeting con custom_audiences corregidas>'

# end_time: 30 días desde hoy (más tiempo puede requerir mayor budget lifetime)
$body = "end_time=2026-07-03T23%3A59%3A59%2B0000&targeting=$([System.Uri]::EscapeDataString($targetingJson))&access_token=$token"

$result = Invoke-RestMethod -Uri "https://graph.facebook.com/v21.0/$adsetId" -Method POST -Body $body -ContentType "application/x-www-form-urlencoded"
$result | ConvertTo-Json
```

**Resultado esperado:** `{ "success": true }`

### 5. Verificar y ajustar status

Tras el fix, el ad set puede quedar en ACTIVE automáticamente (Meta lo reactiva al corregir el error). Si el cliente quiere mantenerlo en PAUSA:

```powershell
$token = $env:META_ACCESS_TOKEN
Invoke-RestMethod -Uri "https://graph.facebook.com/v21.0/<ADSET_ID>" -Method POST -Body "status=PAUSED&access_token=$token" -ContentType "application/x-www-form-urlencoded"
```

### 6. Confirmar estado final

```powershell
$token = $env:META_ACCESS_TOKEN
$result = Invoke-RestMethod -Uri "https://graph.facebook.com/v21.0/<ADSET_ID>?fields=id,status,effective_status,issues_info&access_token=$token" -Method GET
$result | ConvertTo-Json -Depth 5
```

**Resultado esperado:** `effective_status: "PAUSED"`, sin campo `issues_info`.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Error 2446149 "presupuesto demasiado bajo" | `end_time` extendida demasiado lejos — lifetime budget insuficiente | Usar end_time de solo 30 días en vez de años |
| "No puedes editar este anuncio" (error_subcode 1487007) | Ad set tiene fecha de fin ya pasada | Extender `end_time` primero (Paso 3–4) |
| MCP de Meta no funciona para la cuenta | El MCP de Ads está en rollout gradual — no todas las cuentas tienen acceso | Usar PowerShell con Graph API directa (este SOP) |
| `approximate_count` campo no existe | Campo retirado de la API — usar `delivery_status` + `operation_status` en su lugar | Quitar `approximate_count` de la query |

---

## Decisiones clave

- **Decisión:** Usar Lookalike 3% existente en vez de crear nuevo 1%.  
  **Razón:** El 3% ya estaba disponible y sano — fix inmediato sin esperar 24–48h de población. A presupuestos <€1.000/mes en mercados locales la diferencia es mínima.  
  **Alternativa descartada:** Crear nuevo Lookalike 1% — válido a largo plazo pero bloquea el fix inmediato.

- **Decisión:** Extender `end_time` solo 30 días (no años).  
  **Razón:** Extensiones largas en campañas con lifetime budget disparan el presupuesto mínimo requerido por Meta. 30 días está dentro del margen del budget existente.

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| `META_ACCESS_TOKEN` | Autenticación | Variable de entorno Windows — distinta por cuenta |
| `act_XXXXXXXXX` | ID de cuenta | Ver `clients/<cliente>/profile.md` |
| Audiencia de reemplazo | Targeting del ad set | Elegir lookalike/custom con delivery=200 y operation=200 |
| Extensión de `end_time` | Compatibilidad con lifetime budget | 30 días = seguro; más tiempo = verificar budget mínimo |

---

## Notas adicionales

- Si Meta Ads Manager no carga en el navegador (pantalla en blanco) y el problema es igual en todas las cuentas → es problema del navegador, no de las cuentas. Verificar vía API que `account_status: 1` y `disable_reason: 0`. Solución: limpiar cookies de `facebook.com` en Chrome o probar en incógnito.
- Verificar siempre el `effective_status` de la cuenta (no solo del ad set) antes de hacer cambios.

---

*Última sesión que actualizó este SOP: 2026-06-03 — Fix ad set Veganashi WITH_ISSUES (audiencia Lookalike eliminada + ad set expirado 2021)*
