---
name: sistema:integrar-video
description: >
  Absorbe el conocimiento de una transcripción de vídeo de YouTube e integra las ideas
  al sistema Riqueza Digital con un plan accionable. Úsalo siempre que el usuario pegue
  una transcripción, diga "he visto un vídeo sobre X y quiero aplicarlo", "saca las ideas
  de esta transcripción", "¿cómo implementamos esto en RD?" o "el youtuber explica un
  método que me interesa". También activa cuando el usuario comparte un texto largo de
  un vídeo sin pedir explícitamente análisis — si huele a transcripción, usa este skill.
---

# sistema:integrar-video

Objetivo: convertir el conocimiento de un vídeo en acciones concretas dentro del sistema
Riqueza Digital, sin perder ni diluir la esencia de lo que enseña el creador.

## Paso 1 — Leer y clasificar la transcripción

Antes de extraer nada, identifica:

- **Dominio**: marketing, ventas, automatización, SEO, operaciones, producto, mindset, etc.
- **Destino principal**: ¿Aplica a RD como agencia? ¿A un cliente concreto? ¿Al producto Agencia Agéntica? ¿A múltiples clientes?
- **Tipo de contenido**: framework/metodología, táctica concreta, herramienta, caso de estudio, mentalidad/principio.

Si el destino no está claro tras leer la transcripción, **pregunta antes de continuar** (ver Paso 4).

## Paso 2 — Extraer ideas accionables

Para cada idea relevante que encuentres, captura:

1. **La idea en una frase** — qué propone el youtuber
2. **Por qué importa** — el razonamiento o problema que resuelve
3. **Aplicabilidad en RD** — puntuación subjetiva: Alta / Media / Baja
4. **Tipo de acción** — elige uno:
   - `SOP` → proceso repetible que debería documentarse
   - `Estrategia` → cambio en cómo operamos o servimos a clientes
   - `Herramienta` → software/plataforma a evaluar o adoptar
   - `Skill` → proceso suficientemente complejo para convertirse en skill de Claude
   - `Tarea` → acción puntual ejecutable en la sesión actual o en Notion
   - `Referencia` → saber que existe, no actuar ahora

No filtres demasiado — incluye todo lo que tenga aplicabilidad Media o Alta.

## Paso 3 — Mapear al sistema RD

Para cada idea, indica dónde viviría dentro del repositorio o del sistema:

| Destino | Cuándo usarlo |
|---------|--------------|
| `shared/sops/` | Procesos repetibles que cualquier miembro del equipo puede ejecutar |
| `clients/<cliente>/` | Estrategias o cambios específicos a un cliente |
| `services/<servicio>/CLAUDE.md` | Mejoras al catálogo de capacidades de un servicio |
| `AGENCIA-AGENTICA.md` | Nuevas capacidades vendibles del producto agencia |
| Notion tasks | Acciones ejecutables con owner y fecha |
| Nueva skill | Si la secuencia de pasos es compleja y repetible varias veces al mes |
| Solo contexto | Ideas a tener en cuenta sin acción inmediata |

## Paso 4 — Preguntas de clarificación (si aplica)

Pregunta **únicamente si** alguna de estas condiciones se cumple:

- No está claro si la implementación es para RD o para un cliente
- Hay 2+ clientes donde aplicaría y necesitas priorizar
- La idea requiere inversión económica o cambio de herramienta de pago
- Existe posible conflicto con una práctica actual documentada en un SOP
- El youtuber menciona algo que ya hacemos — necesitas saber si queremos cambiarlo

Formula las preguntas de forma concreta: "¿Esto lo implementamos primero para Veganashi o para todos los clientes?" en vez de "¿A quién va dirigido?"

Si no hay dudas bloqueantes, **procede directamente al plan**.

## Paso 5 — Crear el plan

Presenta el plan con este formato:

---
### Plan de integración: [Título del vídeo o tema]

**Dominio:** [marketing / automatización / etc.]
**Destino principal:** [RD / cliente X / producto]
**Ideas extraídas:** [N total] | **Accionables ahora:** [N] | **Para referencia:** [N]

---

#### Ideas a implementar

**[1] [Nombre corto de la idea]**
- Qué propone: ...
- Aplicación en RD: ...
- Destino: `shared/sops/nombre-sop.md` / Notion / etc.
- Prioridad: Alta / Media / Baja
- Esfuerzo estimado: [< 1h / 1-3h / sesión completa / proyecto]
- Ejecuta: Claude / Kevin / Andrés

*(repetir para cada idea accionable)*

---

#### Ideas para referencia (sin acción inmediata)
- [Idea]: [por qué la guardamos para después]

---

#### Propuesta de próximos pasos
1. [Primera acción concreta]
2. [Segunda acción]
3. ...

¿Arrancamos con el paso 1 ahora o prefieres revisar primero el plan completo?

---

## Aviso sobre activos reutilizables

Si durante el análisis detectas que alguna idea podría aplicarse a varios clientes (no solo al que se mencionó), comunícalo con el formato estándar antes de continuar:

> "Esto que estamos viendo en [vídeo] podría aplicarse también a [clientes]. ¿Lo integramos de forma genérica o solo para [cliente actual]?"
