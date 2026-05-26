# SESIÓN 1 — Brief Estratégico

**Pack:** Onboarding Estratégico · **Orden:** 1 de 4 · **Dependencias:** ninguna
**Output esperado:** `clients/{{CLIENTE_NOMBRE_KEBAB}}/strategy/brief-estrategico.md`

> **Cómo usar esta plantilla:** reemplaza los `{{PLACEHOLDERS}}` con los datos del cliente y pega el resultado completo en una sesión nueva de Claude Code. Esta sesión NO depende de otras — es la base para todas las siguientes.

---

```markdown
# Misión de esta sesión
Construir el "Brief Estratégico de {{CLIENTE_NOMBRE}}" — el documento fuente
de verdad que va a alimentar todas las decisiones de marketing, producto y
contenido del próximo año. Este documento se va a pegar como contexto en las
próximas 3 sesiones (estudio de mercado, PRD del sistema de virales, plan de
marketing inbound).

# Sobre el cliente
- **Empresa:** {{CLIENTE_NOMBRE}}
- **Web:** {{CLIENTE_WEB}}
- **Vertical principal:** {{CLIENTE_VERTICAL_PRINCIPAL}}
- **Vertical secundario / upsell:** {{CLIENTE_VERTICAL_SECUNDARIO}}
- **Catálogo de productos/servicios:** {{CLIENTE_CATALOGO_URL}}
- **Contacto:** {{CLIENTE_EMAIL}}
- **Mercado geográfico:** {{CLIENTE_GEO}}

# Hipótesis estratégica (si aplica)
{{HIPOTESIS_ESTRATEGICA}}

(Ejemplo Riqueza Digital: "La formación es nuestra 'demo pública de
capacidad'. El cliente que aprende de nosotros entiende qué le podemos
construir como software a medida → cross-sell natural → mayor LTV por
cliente.")

# Lo que necesito que produzcas
Un documento markdown estructurado con estas 10 secciones:

1. **Identidad de marca** — misión, visión, valores, tono de voz
2. **Propuesta de valor** — frase de 1 línea + 3 promesas concretas
3. **ICP (Ideal Customer Profile)**
   - Empresa: sector, tamaño, madurez digital, geografía
   - Decisor: cargo, dolores, motivaciones, objeciones
   - Anti-ICP: a quién explícitamente NO queremos
4. **Catálogo de servicios** — qué vendemos hoy, precios, márgenes
5. **Diferenciadores reales** — qué hacemos que la competencia no
6. **Modelo de adquisición** — funnel completo (canal → contenido → lead → venta → upsell)
7. **Capacidad operativa actual** — equipo, horas/semana para contenido,
   herramientas, presupuesto mensual
8. **Métricas baseline** — followers, engagement, leads/mes, conversiones
   actuales (lo que se sepa hoy)
9. **Restricciones** — legales, éticas, financieras, de tiempo
10. **Definición de éxito** — KPIs a 3, 6 y 12 meses

# Antes de redactar nada, pregúntame UNO POR UNO sobre:
1. ICP exacto (sector, tamaño, decisor concreto)
2. Diferenciador real vs. competencia (qué única perspectiva tenemos)
3. Productos/servicios actuales: cuáles, precios, cuántos vendemos al mes
4. Capacidad de producción de contenido (equipo, herramientas, horas)
5. Métricas actuales de canales orgánicos (followers, engagement, leads)
6. Presupuesto mensual disponible para marketing/herramientas
7. Stack tecnológico interno
8. Definición personal de éxito a 12 meses

NO redactes el documento hasta tener respuestas claras. Si una respuesta es
vaga, repregunta hasta que sea accionable.

# Formato final
Markdown limpio, accionable, sin relleno. Marca asunciones como [ASUNCIÓN]
cuando no haya dato confirmado. Estructura el doc de manera que se pueda
copiar y pegar como contexto a sesiones futuras.
```
