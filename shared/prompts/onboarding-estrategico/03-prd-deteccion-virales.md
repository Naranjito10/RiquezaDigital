# SESIÓN 3 — PRD: Sistema de Detección y Recreación de Virales

**Pack:** Onboarding Estratégico · **Orden:** 3 de 4 · **Dependencias:** Sesiones 1 y 2
**Output esperado:** `clients/{{CLIENTE_NOMBRE_KEBAB}}/strategy/prd-virales.md`

> **Aplicabilidad:** solo si la estrategia del cliente es inbound vía social media (IG / LinkedIn / TikTok). Para clientes sin estrategia de contenido viral, saltar esta sesión.

> **Cómo usar:** ejecuta primero las sesiones 1 y 2, luego pega ambos outputs donde se indica abajo. Puede correr en paralelo con la sesión 4.

---

```markdown
# Misión de esta sesión
Escribir el PRD completo del sistema interno que va a:
1. Monitorizar a los competidores en {{PLATAFORMAS_OBJETIVO}}
2. Detectar cuándo publican algo viral
3. Analizarlo para entender por qué funcionó
4. Producir una versión adaptada para {{CLIENTE_NOMBRE}}

Este es el sistema que va a alimentar la máquina de contenido del cliente.

# Contexto del cliente
[PEGAR AQUÍ EL OUTPUT COMPLETO DEL BRIEF ESTRATÉGICO — SESIÓN 1]

# Competidores objetivo
[PEGAR AQUÍ EL OUTPUT COMPLETO DEL ESTUDIO DE MERCADO — SESIÓN 2]

# Lo que necesito que produzcas
Un PRD completo con esta estructura:

1. **Problema y oportunidad** — qué duele hoy, qué ganamos
2. **Usuarios y casos de uso** — quién lo usa, en qué momento
3. **Definición operativa de "viral"** — umbrales numéricos por plataforma
   (likes, comentarios, saves, shares, ratio sobre baseline del competidor)
4. **Pipeline funcional**
   - Capa 1: Detección (scraping/API/manual + frecuencia)
   - Capa 2: Análisis (qué señales extraemos del post viral)
   - Capa 3: Adaptación (cómo lo reinterpretamos a nuestra voz)
   - Capa 4: Producción (handoff a creación de contenido)
5. **Stack técnico recomendado** — qué construir vs. qué usar
   (APIs oficiales, scrapers, herramientas SaaS, scripts propios)
6. **Consideraciones legales y éticas** — qué se puede recrear, qué no,
   atribución, plagio vs. inspiración
7. **Métricas de éxito del sistema** — no del contenido, del sistema mismo
8. **Roadmap por fases**
   - MVP (qué corre en 2 semanas, manual+scripts)
   - v1 (qué corre en 2 meses, semi-automatizado)
   - v2 (qué corre en 6 meses, agentico/inteligente)
9. **Riesgos y mitigaciones**
10. **Coste estimado** — desarrollo + operación mensual

# Antes de empezar, pregúntame sobre:
1. ¿Quién va a operar este sistema? (operador único / equipo / agente IA)
2. ¿Preferencia: construir desde cero vs. usar herramientas existentes
   (Notion + Zapier + scripts)?
3. ¿Qué presupuesto razonable para el MVP y para operación mensual?
4. ¿Cuántos posts virales esperas detectar/recrear por semana?
5. ¿Qué tan automatizada quieres la adaptación?
   (full IA / semi-IA con revisión humana / 100% manual con sistema de tracking)
6. ¿Hay líneas éticas que NO quieres cruzar al "recrear" contenido ajeno?
7. Stack actual del cliente (Claude, ChatGPT, Make, n8n, Airtable, Notion).

# Formato final
PRD en markdown, concreto, listo para entregar a un dev o para auto-ejecutar.
No "usar IA" sino "Claude Sonnet 4.6 vía API con prompt X para extraer
atributos del post". No "usar scraper" sino "Apify actor Y con frecuencia Z".
```
