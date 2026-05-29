# Agencia Autónoma — Diseño del Sistema
**Fecha**: 2026-05-29  
**Estado**: Aprobado por Kevin Berbel  
**Objetivo**: Construir una agencia de marketing digital capaz de gestionar clientes (campañas Meta + Google Ads) de forma autónoma, con Kevin como validador estratégico, no como ejecutor operativo.

---

## 1. Problema que resuelve

Kevin es actualmente el cuello de botella de toda la operación: revisa cada acción, aprueba cada cambio, cierra cada sesión. El objetivo del sistema es que Claude pueda gestionar los clientes activos de forma autónoma, escalando solo cuando necesite aprobación estratégica o cuando falte contexto específico del cliente.

**Condición de éxito**: Claude puede hacer reportes, análisis, propuestas de optimización y ejecutar cambios aprobados sin que Kevin supervise cada paso. Kevin solo valida resultados y decisiones estratégicas.

---

## 2. Arquitectura en capas

```
CAPA 5: APRENDIZAJE CONTINUO
  Knowledge Updater — busca mejores prácticas, actualiza SOPs, descarta lo obsoleto
  Umbral de estabilidad: solo propone cambio si delta > 15%

CAPA 4: AGENTES OPERATIVOS
  Campaign Monitor     diario 08:07h  — alertas de anomalías
  Daily Briefing       diario 08:15h  — foco del día para Kevin
  Campaign Optimizer   lunes 09:03h   — propuestas de mejora
  Context Validator    al abrir sesión — detecta contexto faltante, pregunta
  Knowledge Updater    domingos       — actualiza SOPs desde fuentes externas

CAPA 3: AUTORIDAD
  Matriz verde / amarillo / rojo por cliente (ver sección 5)

CAPA 2: CONTEXTO
  Notion (CRM, tareas, estado campañas) — fuente de verdad operativa
  Repo local (SOPs, perfiles, autoridad matrix, Campaign Intelligence DB)
  Memory Claude (~/.claude/memory/) — reglas de comportamiento persistentes

CAPA 1: INFRAESTRUCTURA
  Desarrollo:   Claude Code CLI + Antigravity (local, Kevin y Andrés)
  Producción:   VPS Hostinger — OpenClaw + n8n + Panel web
  Comunicación: Telegram (interfaz principal) + panel.riquezadigital.es (interfaz web)
```

---

## 3. Infraestructura (VPS Hostinger)

### Componentes en el VPS

| Componente | Rol | Setup |
|---|---|---|
| **OpenClaw** | Runtime 24/7 + interfaz Telegram bidireccional | One-click Docker Manager Hostinger |
| **n8n** | Orquestación, scheduling, workflows | Ya instalado |
| **Panel web** | Dashboard visual `panel.riquezadigital.es` | Next.js + Tailwind, mismo VPS |
| **Claude API** | Inteligencia y razonamiento | Key en OpenClaw config |

### Patrón de integración OpenClaw ↔ n8n

```
Kevin → Telegram → OpenClaw → razona con Claude API → llama webhook n8n
n8n → ejecuta workflow (Meta API, Notion, Google Ads) → devuelve resultado
OpenClaw → responde a Kevin por Telegram
```

OpenClaw nunca toca credenciales directamente. Toda ejecución sensible pasa por n8n, donde es visualmente auditable por Andrés.

### Canales Telegram (Sprint 4)

| Canal | Audiencia | Uso |
|---|---|---|
| **Operaciones** | Kevin + agentes | Alertas, propuestas, aprobaciones |
| **Equipo** | Kevin + Andrés + colaboradores | Coordinación interna |
| **CEO** | Solo Kevin | Briefing diario personal, métricas clave |

*(Canal comunidad/freemium: fuera de scope, sprint futuro)*

### Seguridad VPS

- `OPENCLAW_GATEWAY_TOKEN` almacenado de forma segura, nunca en repo
- Gateway no expuesto públicamente sin autenticación
- Credenciales de clientes (Meta, Google) solo en n8n, nunca en repo ni logs
- Acceso al panel con autenticación (magic link o password)

---

## 4. Capa de contexto — qué necesita saber el sistema

Para que los agentes tomen buenas decisiones sin escalar a Kevin, cada cliente necesita contexto estructurado en su perfil.

### Estructura por cliente: `clients/{cliente}/`

```
profile.md                    perfil del cliente (ya existe, completar)
authority-matrix.md           qué puede hacer el agente sin preguntar
intelligence/
  campaign-baseline.json      métricas históricas de referencia
  feedback-log.json           qué acciones tomó el agente y qué resultado tuvieron
  winning-creatives.md        creativos y ángulos que funcionaron
  seasonal-patterns.md        estacionalidad detectada
reports/                      reportes generados (ya existe)
```

### Campos obligatorios en `profile.md` (completar en Sprint 1)

- Objetivo concreto en números: `X leads/mes a Y€ CPA máximo antes de Z fecha`
- Budget mensual autorizado + delta de ajuste sin preguntar
- ICP definido (cliente ideal del cliente)
- Plataformas activas + IDs de cuenta (customer_id Google, ad_account_id Meta)
- Restricciones: sectores, audiencias o mensajes que no se pueden usar

### Bucle de aprendizaje (Campaign Intelligence)

Después de cada cambio implementado, el Campaign Monitor verifica resultados a 7 días y escribe en `feedback-log.json`:

```json
{
  "fecha": "2026-05-29",
  "accion": "aumentar puja grupo-A 15%",
  "contexto": "CPA subió 20% semana previa, estacionalidad mayo",
  "resultado_7d": { "cpa_delta": -12, "conversiones_delta": +8 },
  "aprendizaje": "ajuste_puja_estacional_efectivo"
}
```

El Optimizer lee este log antes de proponer. Con el tiempo deja de aplicar reglas genéricas y aplica lo que funciona específicamente para cada cliente.

---

## 5. Los 5 agentes

### Agente 1 — Campaign Monitor
**Cuándo**: cada día 08:07h  
**Qué hace**:
1. Lee métricas Meta / Google Ads de cada cliente activo
2. Compara contra baseline de la semana anterior
3. Si detecta anomalía (CPA > umbral, CTR < umbral, gasto parado, campaña en error): alerta Telegram inmediata con contexto específico
4. Si todo normal: silencio total

**Si no tiene datos suficientes**: abre tarea en Notion con pregunta exacta — "Para monitorear Tecniclima necesito customer_id de Google Ads. ¿Me lo das?" — no bloquea, no escala sin contexto.

### Agente 2 — Daily Briefing
**Cuándo**: cada día 08:15h (después del Monitor)  
**Qué hace**:
1. Consolida alertas del Monitor del día
2. Revisa tareas Notion con fecha de hoy o vencidas
3. Detecta sesiones abiertas sin cerrar
4. Calcula recomendación de foco: EJECUTAR (clientes) / SISTEMA (mejoras) / VENDER (prospección)
5. Envía mensaje Telegram a canal CEO con resumen de 5 líneas + recomendación

Kevin responde "ok" o redirige. Si no contesta en 2h, el sistema asume que ejecuta el plan propuesto.

### Agente 3 — Campaign Optimizer
**Cuándo**: cada lunes 09:03h  
**Qué hace**:
1. Analiza la semana completa por cliente (métricas + feedback-log + baseline)
2. Consulta al Knowledge Updater si hay best practices relevantes recientes
3. Genera lista de propuestas concretas por cliente
4. Las envía por Telegram en formato de menú numerado:
   ```
   Veganashi — propuestas semana:
   1. Pausar anuncio ID-123 (CTR 0.4%, por debajo umbral 0.8%)
   2. Probar copy variante B en conjunto de anuncios "Verano"
   3. Aumentar puja 12% en audiencia lookalike (historial: +9% conversiones)
   Responde 1/2/3 para aprobar, "skip" para ignorar, "todo" para aprobar todas.
   ```
5. Las aprobadas crean tareas en Notion o (cuando haya acceso de escritura) se ejecutan directamente

### Agente 4 — Context Validator
**Cuándo**: al abrir sesión Claude Code  
**Qué hace**:
1. Revisa perfiles de cliente: ¿campos obligatorios completos?
2. Detecta sesiones `.remember/` sin cerrar
3. Detecta tareas Notion sin respuesta > 3 días
4. Para cada gap: hace la pregunta exacta que falta, no un informe genérico

**Principio**: si un agente no puede completar una tarea, es porque falta contexto. El Validator convierte ese gap en una pregunta accionable para Kevin.

### Agente 5 — Knowledge Updater
**Cuándo**: cada domingo  
**Qué hace**:
1. Busca: "Google Ads best practices 2026", "Meta Ads algorithm updates", "Anthropic Claude API changelog", referentes de la industria
2. Compara hallazgos contra SOPs existentes en `shared/sops/`
3. Filtra con umbral de estabilidad: solo propone cambio si el delta de mejora estimado > 15%
4. Si pasa el umbral: propone edición con diff claro — "SOP-003 dice X, la práctica actual es Y, propongo actualizar porque Z"
5. Kevin aprueba → se actualiza y commitea en git
6. Versioning en git: cualquier update es reversible

**Principio**: "si funciona, no lo rompas". El agente tiene bias hacia la estabilidad, no hacia la novedad.

---

## 6. Matriz de autoridad

Se define por cliente en `clients/{cliente}/authority-matrix.md`. Esta es la plantilla base:

| Acción | Verde — actúa solo | Amarillo — propone, 1-tap | Rojo — siempre escala |
|---|---|---|---|
| Analizar métricas | ✓ siempre | — | — |
| Detectar anomalía + alertar | ✓ siempre | — | — |
| Generar reporte cliente | ✓ siempre | — | — |
| Actualizar SOP interno | ✓ siempre | — | — |
| Proponer cambio de copy | — | ✓ | — |
| Proponer ajuste de puja | — | ✓ si delta < 20% | delta > 20% |
| Pausar anuncio underperforming | — | ✓ | — |
| Implementar cambio aprobado | — | — | ✓ con confirmación |
| Cambiar presupuesto campaña | — | — | ✓ siempre |
| Lanzar campaña nueva | — | — | ✓ siempre |

---

## 7. Dashboard — `panel.riquezadigital.es`

### Stack técnico
- **Framework**: Next.js 15 (App Router)
- **UI**: Tailwind CSS + Shadcn/ui
- **Hosting**: VPS Hostinger (mismo servidor que n8n y OpenClaw)
- **Auth**: Magic link por email (simple, sin contraseñas que gestionar)
- **API routes**: conectan directamente a Notion API, Meta API, Google Ads API

### Las 5 secciones del panel

**1. Overview (home)**
- Semáforo por cliente: verde / amarillo / rojo según estado de campañas
- Conteo de aprobaciones pendientes (badge con número)
- Recomendación de foco del día (viene del Daily Briefing)
- Últimas 3 alertas del Campaign Monitor

**2. Clientes**
- Vista por cliente: métricas clave de la semana (gasto, leads, CPA, ROAS)
- Evolución temporal (gráfico sparkline)
- Acciones rápidas: ver propuestas pendientes, ver historial de cambios
- Estado de completitud del perfil (avisa si faltan campos)

**3. Aprobaciones**
- Cola de propuestas amarillas del Optimizer pendientes de aprobar
- Tarjeta por propuesta: qué es, por qué el agente lo sugiere, impacto estimado
- Botones: Aprobar / Rechazar / Pedir más contexto
- Las rechazadas van al feedback-log con razón (eso entrena al agente)

**4. Agentes**
- Estado de cada agente: último run, próximo run, resultado
- Log de las últimas 24h de acciones
- Si un agente falló: mensaje de error legible y acción sugerida

**5. Equipo**
- Tareas Notion abiertas de Kevin y Andrés
- Últimos commits al repo
- Sesiones Claude activas o sin cerrar

### Principio de diseño
El panel es el complemento al Telegram, no su reemplazo. Telegram = tiempo real en el móvil. Panel = revisión profunda en escritorio. Todo lo que se puede hacer en el panel también se puede hacer por Telegram.

---

## 8. Plan de sprints

### Sprint 0.5 — Objetivos en números (1-2h, solo Kevin)
- Para Veganashi: X leads/mes, Y€ CPA máximo, fecha objetivo
- Para Tecniclima: X leads/mes, Y€ CPA máximo, fecha objetivo
- Sin esto los agentes no pueden evaluar si están ganando o perdiendo

### Sprint 1 — Context Foundation (1-2 sesiones)
- Completar `clients/veganashi/profile.md` con todos los campos obligatorios
- Completar `clients/tecniclima/profile.md`
- Crear `authority-matrix.md` para cada cliente
- Crear estructura `intelligence/` por cliente
- Rellenar `campaign-baseline.json` con métricas actuales (punto de partida)
- Registrar en Notion tarea para resolver developer token Google Ads (Tecniclima)

### Sprint 2 — Primer loop funcional (2-3 sesiones)
- Implementar Campaign Monitor para Veganashi / Meta (MCP ya conectado)
- Implementar Daily Briefing con salida a Telegram
- CronCreate durable en local para testear scheduling
- Implementar Context Validator básico
- Quality Reviewer: paso de validación dentro del Optimizer (no es un agente separado) — antes de enviar cualquier propuesta a Kevin, una segunda pasada verifica coherencia con el perfil del cliente, cumplimiento de políticas de plataforma y alineación con la authority matrix

### Sprint 3 — Optimizer + Feedback Loop (2-3 sesiones)
- Implementar Campaign Optimizer con propuestas vía Telegram
- Implementar feedback-log (registro de resultados a 7 días)
- Conectar Google Ads Tecniclima (cuando esté el developer token)
- Extender Monitor a Google Ads

### Sprint 4 — VPS + OpenClaw + Panel (1-2 sesiones con Andrés)
- Instalar OpenClaw vía Docker Manager en Hostinger (one-click)
- Conectar Claude API key + Telegram bot
- Configurar seguridad del Gateway
- Migrar agentes de local a n8n → OpenClaw
- Configurar 3 canales Telegram (Operaciones / Equipo / CEO)
- Desplegar panel Next.js en `panel.riquezadigital.es`

### Sprint 5 — Knowledge Updater + autonomía creciente (sesiones iterativas)
- Implementar Knowledge Updater semanal
- Calibrar umbral de estabilidad con datos reales
- Escritura directa en Meta/Google Ads (cuando haya confianza en los agentes)
- Kevin pasa de aprobar propuestas a validar resultados

---

## 9. Prerequisitos bloqueantes

Estos no son código — son decisiones o accesos que solo Kevin puede resolver:

| Prerequisito | Quién | Cuándo necesario |
|---|---|---|
| Objetivos en números por cliente | Kevin (Sprint 0.5) | Antes de Sprint 1 |
| Developer token Google Ads | Kevin (solicitud a Google) | Antes de Sprint 3 |
| `customer_id` Tecniclima en perfil | Kevin | Antes de Sprint 3 |
| Acceso VPS con Andrés | Kevin + Andrés | Sprint 4 |
| Bot Telegram creado en BotFather | Kevin | Sprint 2 (o 4 si prefiere) |

---

## 10. Fuera de scope (por ahora)

- Canal Telegram comunidad / modelo freemium para captación
- Escritura autónoma en Meta/Google sin aprobación previa
- Integración con nuevos clientes (onboarding automatizado — Sprint futuro)
- Sistema de facturación o propuestas comerciales automáticas
- Gestión de redes sociales orgánicas
