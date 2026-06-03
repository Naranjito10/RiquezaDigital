# /context-validator — Validador de Contexto de Sesión

Revisa el estado del sistema al abrir sesión: perfiles de cliente incompletos, sesiones sin cerrar y tareas Notion bloqueadas. Genera preguntas concretas — no informes genéricos.

---

## Paso 1 — Perfiles de cliente

Para cada cliente en `clients/*/profile.md`, leer el archivo y verificar los campos obligatorios:

| Campo | Dónde buscarlo | Válido si… |
|-------|---------------|------------|
| Budget mensual | Sección "KPIs objetivo" | Tiene valor numérico en € |
| CPA / CPL objetivo | Sección "KPIs objetivo" | Tiene valor numérico (no `null` ni PENDIENTE) |
| Plataforma activa + ID de cuenta | Tabla "Plataformas Activas" | Tiene account_id o customer_id real |
| Objetivo cualitativo | Sección "Objetivo principal" | Texto presente |

Para cada gap detectado, formular **una pregunta concreta**:
- ❌ MAL: "Falta el CPL objetivo de Veganashi"
- ✅ BIEN: "¿Cuál es el CPL máximo aceptable para Veganashi? (actualmente sin configurar por falta de tracking de conversiones)"

Casos especiales que NO cuentan como gap:
- CPL/CPA marcado como `null` con nota explicando el bloqueante → registrar el bloqueante, no el gap
- Campo con "PENDIENTE — preguntar al cliente" → registrar como tarea de Kevin, no preguntar ahora

---

## Paso 2 — Sesiones sin cerrar

1. Leer `.remember/sessions/INDEX.md`
2. Identificar sesiones de las últimas 72h
3. Comprobar si alguna sesión reciente tiene tareas pendientes relevantes para la sesión actual

Si hay sesiones recientes, mostrar al usuario:
> "Hay sesión reciente del [fecha]: [resumen de 1 línea]. ¿Continuamos ese contexto o empezamos nuevo?"

No bloquear — el usuario decide.

---

## Paso 3 — Gaps en intelligence/

Para cada cliente activo, verificar que existe la estructura:
```
clients/<cliente>/intelligence/
  campaign-baseline.json   ← ¿tiene datos reales o solo placeholders?
  feedback-log.json        ← ¿existe?
```

Si `campaign-baseline.json` tiene valores `null` en campos clave → indicar qué falta y por qué importa.

---

## Paso 4 — Reporte de validación

Presentar resultado en formato compacto:

```
🔍 Context Validator — [fecha]

✅ Veganashi
   Budget: €400 Meta / €200 Google ✓
   Objetivo: leads semana + llenar local fds ✓
   ⚠️  CPL objetivo: sin datos (bloqueado por tracking de conversiones — tarea Notion pendiente Kevin)
   ⚠️  Google Ads account_id: sin datos

✅ Tecniclima
   Budget: €60/día ✓
   CPA objetivo: ≤€9 (jun) → ≤€7 (jul-ago) ✓
   customer_id: 500-211-8788 ✓

📋 Sesión reciente: [fecha] — [resumen]

❓ Preguntas pendientes (responde para desbloquear):
   1. [pregunta concreta #1]
   2. [pregunta concreta #2]

▶️  Todo listo para operar / ⚠️ Hay N gaps que limitan la autonomía del sistema
```

Si no hay gaps ni preguntas → mostrar solo:
```
✅ Context Validator — Todo en orden. Sistema listo para operar.
```

---

## Notas de uso

- **Cuándo ejecutar**: al inicio de cualquier sesión donde se vaya a trabajar con campañas o el sistema agéntico
- **No bloquea**: los gaps se reportan pero no impiden trabajar — solo reducen la autonomía del agente
- **Integración futura**: en Sprint 4, este validador se moverá a OpenClaw para ejecutarse automáticamente al abrir sesión Telegram
