# Sesión 1 — Brief Estratégico de Riqueza Digital (input)

> **Cómo usar este archivo:**
> 1. Abre una sesión nueva de Claude Code en este mismo proyecto.
> 2. Copia el bloque entre `===PROMPT START===` y `===PROMPT END===`.
> 3. Pégalo como primer mensaje. La sesión hará preguntas una por una antes de redactar.
> 4. Output esperado: `agencia/marketing/strategy/brief-estrategico.md` (Claude lo escribirá al final).

---

===PROMPT START===

# Misión de esta sesión

Construir el "Brief Estratégico de Riqueza Digital" — el documento fuente de verdad para todo el marketing INTERNO de la agencia (la captación propia de RD, NO la operación de campañas de clientes). Este documento alimentará las próximas 3 sesiones del pack de onboarding estratégico (estudio de mercado, PRD del sistema de virales, plan de marketing inbound).

Output final esperado: `agencia/marketing/strategy/brief-estrategico.md`

# Sobre Riqueza Digital

- **Empresa:** Riqueza Digital
- **Tipo:** Agencia de transformación digital — empresa propia, NO cliente. Importante: en este repo, RD vive en `agencia/`, no en `clients/`. Ver `ARQUITECTURA.md` y la memoria `project-riqueza-digital-naturaleza`.
- **Web:** riquezadigital.es
- **Catálogo de cursos:** riquezadigital.es/cursos
- **Email:** info@riquezadigital.es
- **Operador único de estrategia:** el fundador
- **Equipo:** Fundador + Andrés (automatizaciones, desarrollo)
- **Mercado geográfico inicial:** España (asunción — confirmar si extender a LATAM)

# Servicios actuales de Riqueza Digital

- **Marketing Digital** (Meta Ads, Google Ads, SEO) — ✅ Activo
- **Automatizaciones** (n8n, integraciones, bots) — ✅ Activo (Andrés)
- **Consultoría / Desarrollo** (CRM, webs, software a medida) — ✅ Activo (Andrés)
- **Edición de Video** — ⚠️ Existe en estructura, estado a confirmar
- **Formación en IA para equipos B2B** — 🔜 Próximo lanzamiento (foco estratégico actual)

# Producto en desarrollo (paralelo)

**"Agencia Agéntica"** — el sistema operativo interno de RD empaquetado como producto vendible (templates, prompts, pipelines, automatizaciones). Ver `agencia/AGENCIA-AGENTICA.md` para inventario actual.

# Hipótesis estratégica central a validar

La formación en IA es nuestra "demo pública de capacidad". El cliente que aprende de nosotros sobre IA entiende qué le podemos construir como software a medida → cross-sell natural → mayor LTV por cliente. La Formación NO es el negocio final, es el imán que lleva leads hacia los servicios premium (Desarrollo a medida + Agencia Agéntica).

# Funnel de adquisición previsto

1. Contenido viral en IG + LinkedIn (inbound orgánico — gratis)
2. Lead magnet (manual descargable, taller gratuito) → captura de email
3. Nurturing por email + más contenido
4. Conversión a curso pagado
5. Cross-sell a Desarrollo a medida / Agencia Agéntica
6. Upsell continuo

# Lo que necesito que produzcas

Un documento markdown estructurado guardado en `agencia/marketing/strategy/brief-estrategico.md` con estas 10 secciones:

1. **Identidad de marca** — misión, visión, valores, tono de voz
2. **Propuesta de valor** — frase de 1 línea + 3 promesas concretas
3. **ICP (Ideal Customer Profile) para la línea de Formación IA B2B**
   - Empresa: sector, tamaño, madurez digital, geografía
   - Decisor: cargo, dolores, motivaciones, objeciones
   - Anti-ICP: a quién explícitamente NO queremos
4. **Catálogo de servicios** — cuáles, prioridad estratégica, precios, márgenes
5. **Diferenciadores reales** — qué decimos nosotros sobre IA que nadie más dice
6. **Modelo de adquisición detallado** — funnel completo con conversiones esperadas
7. **Capacidad operativa actual** — equipo, horas/semana para contenido, herramientas, presupuesto mensual
8. **Métricas baseline** — followers IG/LinkedIn, engagement, leads/mes, clientes activos
9. **Restricciones** — equipo pequeño, presupuesto, tiempo compartido con operación
10. **Definición de éxito a 3 / 6 / 12 meses** — cuantitativo

# Antes de redactar nada, pregúntame UNO POR UNO sobre

1. **ICP exacto** — ¿qué tipo de empresa B2B compra formación en IA? (sector, tamaño, cargo del comprador)
2. **Diferenciador único** — ¿qué decimos nosotros sobre IA que nadie más dice? (perspectiva, metodología, lenguaje)
3. **Cursos actuales** — los que están en riquezadigital.es/cursos: nombres, precios, ventas al mes
4. **Tiempo real para contenido** — horas/semana realistas que el fundador puede dedicar a producir contenido propio
5. **Métricas actuales** — followers IG y LinkedIn, engagement medio, leads/mes orgánicos hoy
6. **Presupuesto mensual** — para herramientas, automatizaciones del sistema viral
7. **Stack actual** — qué herramientas pagas, qué APIs accesibles
8. **Éxito a 12 meses** — ¿qué número exacto (€, clientes, vistas) sería "lo logramos"?

NO redactes el documento hasta tener respuestas claras. Si una respuesta es vaga, repregunta hasta que sea accionable. Marca asunciones como [ASUNCIÓN] cuando uses datos no confirmados.

# Formato final

Markdown limpio, accionable, sin relleno. Estructurado para pegarse como contexto en las sesiones 2, 3 y 4 — no incluir información que solo sirva a la sesión 1 misma. Al terminar, escribe el archivo a `agencia/marketing/strategy/brief-estrategico.md`.

===PROMPT END===
