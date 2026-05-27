# F-010 — Fase A: Mapeo Top-Level del Workspace Notion

**Fecha:** 2026-05-27  
**Auditor:** Claude Code (sesión automática)  
**Estado:** ✅ Completado  

---

## Metodología

Exploración vía Notion MCP: se consultaron las páginas raíz, las bases de datos clave y las secciones principales. Sin tocar ni mover nada (Fase A es solo documentar).

---

## Estructura Top-Level

El workspace tiene **dos raíces separadas** — no existe una jerarquía única unificada:

| Raíz | ID | Última actividad | Descripción |
|------|-----|-----------------|-------------|
| `🧠 RIQUEZA DIGITAL` | `9a5bbf82` | 2026-05-26 | Hub principal de operaciones y servicios |
| `📅 PROYECTOS CLIENTES` | `249d2fec` | 2026-05-27 (DB activa) | Hub de gestión de clientes y tareas |

> ⚠️ **Drift arquitectónico #1:** Las dos raíces no están conectadas entre sí. Alguien que entre al workspace sin contexto puede no encontrar las tareas si empieza desde la home.

---

## Árbol 1: `🧠 RIQUEZA DIGITAL`

```
🧠 RIQUEZA DIGITAL (home)
├── CLIENTES [solo botones — sin páginas directas visibles]
├── COLABORADORES → página /6dca7e24
├── SERVICIOS → página /2e7d2fec (link)
│
├── GESTIÓN INTERNA
│   ├── RD Onboarding
│   ├── Accesos Herramientas
│   ├── Contrato Marco
│   ├── Formación - Mejora tu vida
│   ├── Branding RD
│   └── Brief Andrés — Webhooks Notion → n8n  ← ⚠️ ítem operativo en home
│
├── MARKETING
│   ├── 📈 Métricas Semanales [DB]
│   ├── Contenido RD
│   ├── Web Riqueza Digital
│   ├── VENTAS
│   └── Financiación & Programas Estratégicos
│
├── SERVICIOS (catálogo detallado — 11 páginas) ← ⚠️ DUPLICADO con el SERVICIOS de arriba
│   ├── Formación IA
│   ├── Procesos de Experiencia de Usuario
│   ├── N8N
│   ├── ERP/CRM
│   ├── Servicio Web
│   ├── Google Ads
│   ├── SEO
│   ├── Cold email
│   ├── Formación
│   ├── Proceso Marcas Personales / Marketing
│   └── Agencia MKT automatizada
│
├── PROYECTOS RD
│   ├── APP LegioSafe
│   ├── Antigravity Projects  ← ⚠️ proyecto viejo, ¿archivado?
│   └── Otros
│
├── NETWORKING
│   ├── BNI ALTO RENDIMIENTO
│   ├── Networking Mediterráneo
│   ├── Techies Network
│   └── Barcelona Activa
│
├── Otros
│   └── 🗄️ Archivo
│
└── 2026 EVENTOS [DB inline]
```

---

## Árbol 2: `📅 PROYECTOS CLIENTES`

```
📅 PROYECTOS CLIENTES (hub)
├── [botones de acción rápida — sin páginas directas]
├── Transcripciones
├── Horas trabajadas  ← ⚠️ página, no DB — ¿se usa sistemáticamente?
│
├── ✅ Tareas [DB — activa, uso diario]
│   ├── Schema: Tarea, Estado, Categoría, Esfuerzo, Responsable, Fecha, Link, Proyecto
│   ├── Categorías: 1.Servicio / 2.CEO / 3.Dr.MKT / 4.DrOps / 5.Formación / 6.RRHH / 7.Dr.Finanzas / 8.Dr.Producto
│   └── Vistas: Para mí (calendar), Clientes-Activos (board), Riqueza Digital (board), Hecho (calendar)
│
└── 😈 Seguimiento [DB — CRM completo]
    ├── Schema: Cliente, STATUS, Servicios, Viene de, Reunión, Drive, Responsable, Colaboradores, ...
    ├── STATUS pipeline: CLAUDE → DESCUBRIMIENTO → DAR OFERTA → ENVIAR FACTURA → 
    │                   Onboarding → Activación → Implementación → Cierre → Ex Cliente/Cancelado
    ├── Servicios trackados: CRM/ERP, Meta Ads, SEO, Google Ads, Notion, APP, AUTOM, CONSU, Email MKT, WEB, MKT
    └── Vistas: Leads, Cliente, RD, Cierre/Testimonio, EX CLIENTE, Legionella, ALL, Origen (chart)
```

---

## Observaciones de Drift

### 🔴 Crítico — Requiere decisión del fundador

| # | Drift | Impacto | Propuesta |
|---|-------|---------|-----------|
| D-01 | **Legionella en el CRM de marketing digital** — STATUS options "LEGIONELLA LEAD" y "LEGIONELLA CLIENTE" en la DB de Seguimiento. Si es un segundo negocio de RD, mezcla el pipeline de dos negocios distintos en un solo objeto. | Alto — contamina métricas, confunde a nuevos colaboradores | Decidir: ¿es un negocio separado? Si sí → filtro permanente o DB separada |
| D-02 | **Dos raíces desconectadas** — `RIQUEZA DIGITAL` y `PROYECTOS CLIENTES` son independientes; no hay link entre ellas | Medio — onboarding de nuevos miembros confuso | Añadir link de `RIQUEZA DIGITAL` → `PROYECTOS CLIENTES` en sección visible |

### 🟡 Medio — Limpiar en Fase B

| # | Drift | Descripción |
|---|-------|-------------|
| D-03 | `Brief Andrés — Webhooks Notion → n8n` en la home | Ítem operativo puntual anclado en la página principal. Debería estar bajo PROYECTOS o eliminado si ya está hecho. |
| D-04 | SERVICIOS duplicado en la home | Aparece como sección con link a `/2e7d2fec` Y como lista detallada de 11 páginas. Confusión de qué es el catálogo y qué es la operativa. |
| D-05 | `Antigravity Projects` en PROYECTOS RD | Proyecto viejo (visible desde contexto de sesiones antiguas). Probablemente archivable. |
| D-06 | STATUS "CLAUDE" en el CRM | Hay un estado "CLAUDE" en el pipeline de Seguimiento — ¿es un estado activo o legacy? Verificar y documentar o eliminar. |

### 🟢 Bajo — Notar para mantenimiento

| # | Drift | Descripción |
|---|-------|-------------|
| D-07 | `Horas trabajadas` como página suelta | Tracking de horas en página no estructurada. Si se usa, migrar a DB o al menos verificar formato. |
| D-08 | `CLAUDE.md — Guía para IA` en Notion | Existe una página con ese título en el workspace (ID `337d2fec`). Puede estar obsoleta respecto al `CLAUDE.md` del repo. Verificar y sincronizar o eliminar. |
| D-09 | Páginas en GESTIÓN INTERNA muy antiguas | "Formación - Mejora tu vida", "Contrato Marco" — sin actividad reciente. Verificar si siguen siendo relevantes. |

---

## Bases de Datos Identificadas

| DB | Ubicación | Estado | Uso real |
|----|-----------|--------|---------|
| ✅ Tareas | PROYECTOS CLIENTES | 🟢 Activa | Uso diario — Claude crea entradas al cerrar sesión |
| 😈 Seguimiento | PROYECTOS CLIENTES | 🟢 Activa | CRM principal — mezcla clientes activos, leads y legionella |
| 📈 Métricas Semanales | RIQUEZA DIGITAL › MARKETING | ❓ No verificada | Tracking de KPIs semanales por cliente |
| Colaboradores | RIQUEZA DIGITAL › COLABORADORES | ❓ No verificada | Directorio de colaboradores externos |
| Eventos 2026 | RIQUEZA DIGITAL (inline) | ❓ No verificada | Calendario de eventos de networking |

---

## Recomendaciones para Fase B (Triage por Área)

Orden de prioridad para la siguiente fase:

1. **Decidir sobre Legionella (D-01)** — bloquea el correcto entendimiento del CRM
2. **Conectar las dos raíces (D-02)** — mínimo esfuerzo, máximo impacto en usabilidad
3. **Limpiar la home de RIQUEZA DIGITAL** — D-03, D-04: sacar Brief Andrés, unificar SERVICIOS
4. **Verificar `CLAUDE.md — Guía para IA` (D-08)** — puede generar confusión si hay dos versiones del documento de instrucciones
5. **Archivar Antigravity Projects (D-05)** — quick win

---

## Próximos pasos (Fase B)

- [ ] Fundador decide sobre D-01 (Legionella — negocio separado o filtro)
- [ ] Claude ejecuta D-02, D-03, D-04 con confirmación del fundador
- [ ] Verificar y sincronizar CLAUDE.md de Notion vs repo (D-08)
- [ ] Revisar páginas inactivas en GESTIÓN INTERNA (D-09)

---

*Output de F-010 Fase A. Ningún cambio realizado en el workspace. Solo mapeo y observaciones.*
