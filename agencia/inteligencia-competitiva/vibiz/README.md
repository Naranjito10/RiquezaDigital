# Inteligencia Competitiva — Vibiz.ai

> **Propósito:** capturar de forma sistemática lo que Vibiz nos enseña sobre cómo construir Agencia Agéntica. No es una carpeta de notas sueltas: es un dossier vivo con protocolo de captura.

## Por qué Vibiz, por qué ahora

Vibiz.ai es el competidor más directo de "Agencia Agéntica" que conocemos: plataforma de marketing autónomo con plugin para Claude Code, ~40 herramientas MCP y ~10K clientes alcanzados sin presencia social grande. RD ha pagado por la cuenta con el objetivo doble de:

1. **Usar la plataforma** para generar contenido orgánico de la propia RD (inbound).
2. **Aprender de su producto** para construir nuestra versión con nuestro stack.

## Plataformas en foco

Vibiz integra Meta, IG, FB, TikTok, LinkedIn, X y Threads. Por decisión del fundador (2026-05-25), capturamos aprendizajes solo de:

- **Meta** (Facebook + Instagram + Meta Ads)
- **LinkedIn**
- **TikTok** — solo si Vibiz lo gestiona de forma autónoma

X y Threads se ignoran en el análisis (no son canales prioritarios de RD).

## Protocolo de captura — cada sesión con Vibiz

Cuando uses Vibiz, dedica 30 segundos al final a registrar:

1. **¿Qué prompt o comando usaste?** → `prompts-capturados/YYYY-MM-DD_<comando>.md`
2. **¿Qué output devolvió?** → `outputs-evaluados/YYYY-MM-DD_<tipo>.md` con rating 1-5 (ver rúbrica abajo)
3. **¿Qué te sorprendió** (UX, taxonomía, datos que pidió, secuencia)? → nota en `decisiones-roadmap.md`
4. **¿Esto va al roadmap de Agencia Agéntica?** → si la respuesta es sí, marcar en `decisiones-roadmap.md`

## Rúbrica de evaluación de outputs (1-5)

- **5** — listo para publicar sin retoques
- **4** — usable con retoque ligero (< 5 min)
- **3** — sirve de borrador, requiere reescritura
- **2** — pierde más tiempo arreglarlo que crearlo desde cero
- **1** — output incorrecto, fuera de tono, o irrelevante

## Ejes de aprendizaje (qué buscamos extraer)

| Archivo | Qué captura |
|---|---|
| `arquitectura-producto.md` | Taxonomía de sus 40 MCP tools — blueprint de organización de features |
| `pricing-y-packaging.md` | Tiers, qué entra en cada uno, cómo justifican precio |
| `growth-playbook.md` | Cómo llegaron a 10K clientes sin presencia social — su frase, su realidad |
| `ux-onboarding.md` | Su flujo de signup → primer publish, paso a paso |
| `data-schema.md` | Su modelo de ICP/Offer — qué campos consideran imprescindibles |
| `decisiones-roadmap.md` | Qué de Vibiz queremos llevar a Agencia Agéntica (y qué no) |
| `prompts-capturados/` | Prompts visibles en cada interacción |
| `outputs-evaluados/` | Samples + rating + por qué |

## Avisos operativos

### Hook post-commit de Vibiz

Vibiz instala un comportamiento que **propone borrador de post social tras cada commit de git** (salvo merge commits, fixes de seguridad, o commits etiquetados `[skip-vibiz]` / `[no-post]`).

> En este repo commiteamos a diario cosas internas que NUNCA deben acabar en redes. **Política RD:** por defecto, todo commit lleva `[skip-vibiz]` salvo que decidas explícitamente publicarlo.

### Datos que salen del entorno RD

Vibiz es SaaS — todo lo que generes se procesa en sus servidores. Mientras usemos Vibiz para RD-marketing (no para datos de cliente), el riesgo es bajo. **No usar Vibiz con datos de Veganashi, Tecniclima, Selarom Jordi ni Federico Sirux** hasta tener clara su política de datos.

### Convivencia con `claude-ads` y MCPs existentes

RD ya tiene `claude-ads`, Meta MCP, Canva MCP, Gemini MCP. **No reemplazan a Vibiz, ni viceversa** — durante esta fase de evaluación, Vibiz cubre orgánico y publicación multi-plataforma; el stack existente cubre ads pagados. Si Vibiz duplica una capacidad, anotar en `decisiones-roadmap.md` cuál preferimos y por qué.

## Estado

| Hito | Estado | Fecha |
|---|---|---|
| Cuenta Vibiz pagada | ✅ | 2026-05-25 |
| Plugin instalado en Claude Code | ⏳ | — |
| Primera sesión documentada | ⏳ | — |
| Decisión 2 semanas: "tool útil" vs "construirlo nosotros" | ⏳ | — |
