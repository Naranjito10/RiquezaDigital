# Arquitectura del Proyecto

> **Para qué sirve este doc:** explicar cómo está organizado el repositorio de Riqueza Digital + Agencia Agéntica, qué va dónde, y por qué. Lo lee: (a) el equipo (fundador + Andrés) para no perderse; (b) un futuro comprador del producto "Agencia Agéntica" para entender lo que adquiere.

---

## Filosofía

El proyecto separa **6 capas** por tipo de cosa, no por cliente o servicio:

| Capa | Carpeta | Tipo de cosa | Pregunta que responde |
|---|---|---|---|
| **Ejecutable** | `.claude/` | Commands, agentes, settings de Claude Code | "¿Qué comandos puedo usar?" |
| **Empresa** | `agencia/` | RD como entidad: marketing interno + producto comercial | "¿Quién es RD y qué vende?" |
| **Clientes** | `clients/` | Datos, outputs, histórico por cliente que paga | "¿Quién es el cliente X?" |
| **Capacidades** | `services/` | Catálogo de servicios que RD ofrece (docs, no ejecutable) | "¿Qué sabe hacer RD?" |
| **Pipelines/Código** | `pipelines/` | Motores ejecutables, scripts de automatización y código base | "¿Dónde se ejecuta el software?" |
| **Cross-cutting** | `shared/` | Plantillas, prompts, SOPs reutilizables | "¿Qué herramientas comunes hay?" |
| **Temporal** | `output/` | Working files efímeros | "¿Dónde están los borradores?" |

---

## Estructura completa

```
RD-TEAM/
├── CLAUDE.md                       ← Orquestador raíz (router de servicios)
├── ARQUITECTURA.md                 ← Este documento
├── .env                            ← Variables sensibles (gitignored)
├── .mcp.json                       ← Configuración de MCPs
│
├── .claude/                        ← CAPA EJECUTABLE
│   ├── settings.local.json         ← Permisos locales
│   ├── commands/                   ← Slash commands (/nuevo-cliente, /reporte-semanal, etc.)
│   └── agents/                     ← Subagentes paralelizables (ads, analyst, content, seo)
│
├── agencia/                        ← RIQUEZA DIGITAL como empresa propia
│   ├── CLAUDE.md                   ← Contexto cuando trabajamos cosas internas de RD
│   ├── AGENCIA-AGENTICA.md         ← Inventario vivo del producto comercial
│   ├── perfil.md                   ← Identidad, misión, KPIs de RD
│   ├── inteligencia-competitiva/   ← Dossiers de competidores (ej: vibiz)
│   ├── marketing/                  ← Marketing INTERNO (captar clientes para RD)
│   │   ├── strategy/               ← Outputs onboarding aplicado a RD
│   │   └── contenido/              ← Pipeline de contenido propio
│   ├── producto/                   ← "Agencia Agéntica" como SKU vendible
│   │   └── ventas/                 ← Pipeline comercial del producto
│   └── reportes-internos/          ← P&L, salud agencia, imputación horas RD interno
│
├── clients/                        ← Clientes que PAGAN a RD
│   ├── _template/                  ← Plantilla para nuevo cliente
│   │   ├── profile.md
│   │   └── imputacion-horas.md     ← Diario de horas del cliente
│   ├── veganashi/
│   │   ├── profile.md
│   │   ├── strategy/               ← Outputs del onboarding estratégico
│   │   ├── reports/                ← Reportes mensuales AL CLIENTE
│   │   ├── proposals/              ← Propuestas comerciales
│   │   └── imputacion-horas.md     ← Registro interno (NO se entrega al cliente)
│   ├── tecniclima/
│   ├── selarom-jordi/
│   ├── federico-sirux/
│   └── keller-valentina/           ← Desarrollo Web (Home y páginas interiores)
│
├── services/                       ← CATÁLOGO de capacidades (definición, no ejecutable)
│   ├── marketing/
│   │   ├── CLAUDE.md               ← Cuándo activar este servicio
│   │   ├── playbooks/              ← Cómo se entrega operativamente
│   │   ├── sops/                   ← Procedimientos estándar
│   │   └── pricing.md              ← Modelo comercial
│   ├── automatizaciones/
│   ├── desarrollo-web/             ← Docs, SOPs y especificaciones de maquetación y diseño web
│   ├── desarrollo-software/        ← Docs, SOPs y especificaciones de software a medida
│   ├── formacion/
│   └── edicion-video/              ← Docs, SOPs y especificaciones del servicio de vídeo
│
├── pipelines/                      ← MOTORES DE SOFTWARE Y SCRIPTS EJECUTABLES
│   ├── edicion-video/              ← Pipeline Python/Node, watcher, helpers y entornos venv
│   ├── marketing-digital/          ← API clients de Google/Meta, scrapers y scripts de ads
│   └── desarrollo/                 ← Utilidades de software a medida (ej: wordpress_client.py)
│
├── shared/                         ← Reutilizables cross-cutting
│   ├── prompts/                    ← Prompts reutilizables (onboarding, etc.)
│   ├── templates/                  ← Plantillas de informes
│   ├── sops/                       ← Procedimientos globales
│   └── assets/                     ← Logos, brand RD
│
└── output/                         ← Working files temporales (no commit)
```

---

## Decisiones clave (y por qué)

### 1. Commands y Agents van en `.claude/`, NO en `services/<x>/agents/`

**Por qué:**
- Claude Code descubre automáticamente `.claude/commands/` y `.claude/agents/`. Si los ponemos dentro de un servicio, requieren configuración adicional.
- Producto vendible: alguien que compre "Agencia Agéntica" clona el repo y todo funciona out-of-the-box.
- Mantener los agentes centralizados permite escalarlos y utilizarlos en varios servicios si es necesario.

**Excepción:** subagents con `subagent_type` específicos definidos por Claude Code SDK siguen estándares propios.

### 2. `services/<x>/` se queda con DOCUMENTACIÓN, no con ejecutables

Cada `services/<servicio>/` contiene:
- `CLAUDE.md` — instrucciones de cuándo y cómo activar el servicio
- `playbooks/` — cómo se entrega operativamente
- `sops/` — procedimientos estándar
- `pricing.md` — modelo comercial

Esto separa "qué es el servicio" (services/) del código y lógica de software que lo ejecuta (pipelines/). Todo código fuente, scripts de automatización complejos, dependencias y carpetas de trabajo con ficheros pesados se ubican en `pipelines/<servicio>/`.

### 3. Riqueza Digital NO está en `clients/`

RD es la empresa propia, no un cliente. Vive en `agencia/`. Esto evita que el concepto de "cliente" se contamine con el meta-negocio. Ver memoria `project-riqueza-digital-naturaleza`.

### 4. Imputación de horas: documento interno, NO se entrega al cliente

- `clients/<cliente>/imputacion-horas.md` — registro interno de horas + actividad (NO se enseña al cliente)
- `clients/<cliente>/reports/YYYY-MM-DD_mensual.md` — informe al cliente (hitos + ahorros conseguidos, NO horas)

Ver memoria `feedback-imputacion-horas`.

---

## Cómo añadir cosas

### Cliente nuevo
1. Ejecutar skill `/nuevo-cliente` (o copiar `clients/_template/` → `clients/<nuevo>/`)
2. Rellenar `profile.md`
3. Ejecutar pack `shared/prompts/onboarding-estrategico/` → outputs van a `clients/<nuevo>/strategy/`
4. Crear `clients/<nuevo>/imputacion-horas.md` con plantilla

### Servicio nuevo
1. Crear `services/<servicio>/CLAUDE.md` con contexto del servicio
2. Crear `services/<servicio>/playbooks/`, `sops/`, `pricing.md`
3. Si el servicio requiere código/motores ejecutables, crear `pipelines/<servicio>/` con su código, scripts y dependencias.
4. Crear skills relacionadas en `.claude/skills/<servicio>/`
5. Crear agentes relacionados en `.claude/agents/`
6. Actualizar tabla de servicios en `CLAUDE.md` raíz
7. Registrar la capacidad en `agencia/AGENCIA-AGENTICA.md` si es vendible

### Skill nueva
1. Crear `.claude/skills/<dominio>/<nombre>.md` con frontmatter Claude Code
2. Documentar en `agencia/AGENCIA-AGENTICA.md` si es relevante para el producto

### Activo que se generaliza de un cliente
Si construyendo algo para un cliente concreto detectamos que sirve a otros:
1. **Avisar al fundador** (regla `feedback-reusable-assets`)
2. Si aprueba: mover/copiar a `shared/` parametrizado con placeholders
3. Registrar en `agencia/AGENCIA-AGENTICA.md`

---

## Convenciones

| Convención | Detalle |
|---|---|
| **Idioma** | Español por defecto en todos los documentos internos |
| **Fechas** | Formato `YYYY-MM-DD` para archivos con fecha (ej: `2026-05-25_reporte.md`) |
| **Nombres de archivo** | kebab-case (`brief-estrategico.md`) |
| **Placeholders en plantillas** | Estilo Mustache: `{{NOMBRE_VAR}}` |
| **Estado de funcionalidades** | 🌱 PoC · 🔧 Interno-estable · 💰 Vendible |
| **No commitear** | `.env`, `output/`, credenciales, contenido confidencial de cliente |

---

## Última actualización

2026-05-25 — Creación del documento tras refactor (RD movida de `clients/` a `agencia/`).
