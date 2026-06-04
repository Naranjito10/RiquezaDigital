# Auditoría Google Ads — Tecniclima
**Periodo analizado:** 8 mayo – 4 junio 2026 (27 días efectivos)
**Analista:** Riqueza Digital
**Estado de la cuenta:** Activa — 1 campaña activa, 2 en pausa

---

## Resumen Ejecutivo

La cuenta presenta rendimiento mixto: CTR excelente (7.49%) y volumen de conversiones razonable, pero con un CPA de **€36.07 que cuadruplica el objetivo de €9**. Sin embargo, este dato es probablemente engañoso — la extensión de llamada recibe 560 clics sin tracking configurado, lo que sugiere que la mayoría de los leads reales no se están contando. **La prioridad #1 antes de cualquier otra optimización es configurar el tracking de llamadas.**

Hay además ~€200 de gasto desperdiciado identificado en keywords sin conversión, dos grupos de anuncios completamente inactivos, y una temporada de AC que empieza sin ningún grupo de anuncios activo para capturarla.

---

## Métricas Globales

| Métrica | Valor | Objetivo | Estado |
|---------|-------|----------|--------|
| Gasto total | €1,659.34 | ~€1,800/mes | ✅ |
| Impresiones | 11,700 | — | — |
| Clics | 876 | — | — |
| CTR | 7.49% | >5% | ✅ Excelente |
| CPC medio | €1.89 | — | ✅ |
| Conversiones (trackeadas) | 46 | — | ⚠️ Incompleto |
| Tasa de conversión | 5.25% | — | ✅ |
| CPA | €36.07 | ≤€9 | 🔴 4x objetivo |
| Valor conversiones | €841.54 | >€1,659 | 🔴 ROAS 0.51x |

> **Nota crítica sobre el CPA:** El perfil indica que las llamadas directas no se cuentan en el tracking. La extensión de llamada tiene 560 clics sobre €1,208 de gasto. Si incluso el 20% de esas llamadas convierte, el CPA real estaría en torno a €14-16 — todavía por encima del objetivo pero muy diferente a €36. Confirmar con Edgar el volumen real de leads (llamadas + formulario + WhatsApp).

---

## Estructura de Campañas

| Campaña | Estado | Presupuesto | Tipo | Gasto | Conv. | CPA |
|---------|--------|-------------|------|-------|-------|-----|
| **M! - Search** | ✅ Activa | €60/día | Search | €1,659 | 46 | €36.07 |
| Campaign #1 | ⏸ Pausa | €21.62/día | PMax | €0 | 0 | — |
| Search - Calderas/Calefacción | ⏸ Pausa | €50/día | Search | €0 | 0 | — |

**Alerta:** M! - Search está marcada como **"Apto (limitado) - elemento limitado por el presupuesto"**. El sistema está gastando los €60/día completos cada día, lo que significa que se pierden impresiones y oportunidades de conversión diariamente. El budget es el cuello de botella — pero no se debe aumentar antes de eliminar el gasto desperdiciado.

---

## Rendimiento por Grupo de Anuncios

| Grupo | Impr. | Clics | CTR | Gasto | Conv. | CPA | Estado |
|-------|-------|-------|-----|-------|-------|-----|--------|
| Calderas | 6,350 | 463 | 7.29% | €877.83 | 22 | €39.90 | ✅ |
| Calentadores | 3,563 | 278 | 7.80% | €562.64 | 18 | €31.26 | ✅ Mejor CPA |
| Termos Eléctricos | 1,787 | 135 | 7.55% | €218.87 | 6 | €36.48 | ✅ |
| **Lavadoras** | **0** | **0** | **—** | **€0** | **0** | **—** | 🔴 Muerto |
| **Neveras/Congeladores** | **0** | **0** | **—** | **€0** | **0** | **—** | 🔴 Muerto |

---

## Análisis de Keywords

### Keywords Estrella (mantener y escalar)

| Keyword | Gasto | Conv. | CPA | Nota |
|---------|-------|-------|-----|------|
| reparación de calderas | €482.08 | 18 | €26.78 | ⭐ Core keyword, mejor volumen |
| instalador gas autorizado | €118.68 | 6 | €19.78 | ⭐ Pese a "baja calidad", convierte bien |
| tecnico calderas | €94.05 | 4.5 | €20.90 | ⭐ Buen CPA pero mal asignada (en Calentadores) |
| arreglo de calentadores a gas | €53.84 | 4 | €13.46 | ⭐ Mejor CPA del grupo Termos |
| tecnico de gas autorizado | €45.69 | 2 | €22.84 | ✅ Eficiente |
| calderas mantenimiento | €1.98 | 2 | €0.99 | ⚠️ CPA sospechosamente bajo — verificar tracking |

### Keywords con Gasto Desperdiciado (pausar o revisar)

| Keyword | Grupo | Gasto | Conv. | Problema |
|---------|-------|-------|-------|---------|
| **mantenimiento gas** | Calderas | €61.96 | 0 | 🔴 Baja calidad + €62 sin retorno |
| tecnicos en calefaccion | Calentadores | €40.94 | 0 | 🔴 Intención no-transaccional |
| tecnico en calefaccion | Calentadores | €28.81 | 0 | 🔴 Duplicado semántico |
| tecnico de calefaccion | Calderas | €21.31 | 0 | 🔴 Duplicado semántico |
| caldera a gas | Calderas | €22.31 | 0 | ⚠️ Puede ser informacional |
| arreglo de calentadores | Termos | €27.16 | 0 | ⚠️ Mismatch de grupo |
| **Total identificado** | | **€202.49** | **0** | |

> **€202 = 12.2% del gasto total del periodo sin una sola conversión.** Redirigir este gasto a keywords estrella podría generar ~5-7 conversiones adicionales/mes.

### Keywords Mal Asignadas (group mismatch)

Estas keywords activan anuncios del grupo incorrecto, reduciendo relevancia y Quality Score:

| Keyword | Grupo actual | Grupo correcto |
|---------|-------------|----------------|
| tecnico calderas | Calentadores | Calderas |
| reparació calderes | Calentadores | Calderas |
| arreglo de calentadores | Termos Eléctricos | Calentadores |
| arreglar calentador de gas | Termos Eléctricos | Calentadores |
| tecnico calentador de gas | Termos Eléctricos | Calentadores |

### Keywords con Quality Score bajo

Marcadas como "Limitado - baja calidad" o con patrones de baja calidad:

| Keyword | Problema | Acción |
|---------|----------|--------|
| mantenimiento gas | Baja calidad + €62 sin conv. | Pausar |
| instalador gas autorizado | Baja calidad pero convierte (€19.78 CPA) | Mejorar landing page relevancia |
| calefacción de gas | Baja calidad, intención informacional | Revisar/pausar |
| saunier duval barcelona | Baja calidad pero 1 conv (€17.23 CPA) | Mantener, mejorar QS |
| reparación de calderas barcelona | Baja calidad, 0 conv | Revisar landing |

---

## Assets y Extensiones

### Lo que funciona

| Asset | Tipo | Clics | CTR | Nota |
|-------|------|-------|-----|------|
| 931 89 54 38 | Llamada | 560 | 6.45% | ⭐ Máximo engagement, sin tracking |
| Contacto (sitelink) | Sitelink | 423 | 7.91% | ⭐ Mejor CTR de sitelinks |
| WhatsApp +34640641819 | Mensaje | 270 | 5.09% | ✅ Buen canal |
| Nuestros Servicios | Sitelink IA | 333 | 7.21% | ✅ Relevante |
| Reparación De Calefacción | Sitelink IA | 201 | 5.48% | ✅ Relevante |

### Problemas con assets

| Asset | Problema |
|-------|---------|
| **Extracto de sitio** (Reparación calderas, averías...) | 🔴 **RECHAZADO** — falta un asset importante |
| Camaras industriales sitelink | 🔴 **RECHAZADO** — pero generó €79.55 en clics mientras estuvo activo |
| Encimera De Gas (sitelink IA) | ⚠️ Google AI lo creó, puede desviar intención de reparación a instalación |
| Servicios De Aerotermia (sitelink IA) | ⚠️ Idem — servicio diferente |
| Repara Aire Acondicionado (sitelink campaña) | ⚠️ 0 clics — necesita revisión |

---

## Los 5 Problemas Críticos

### 🔴 #1 — Tracking de llamadas no configurado
**Impacto:** El CPA aparente (€36.07) puede estar 3-4x inflado. La extensión de llamada generó 560 clics y €1,208 de gasto. Sin saber cuántas de esas llamadas convierten, es imposible tomar decisiones de optimización correctas. **Todo lo demás depende de resolver esto primero.**

Estimación: Si el 15-20% de los clics en llamada convierte (84-112 leads adicionales), el CPA real estaría en €12-14. Cerca del objetivo de €9 y ajustable.

### 🔴 #2 — Presupuesto limitado con gasto desperdiciado activo
**Impacto:** La cuenta llega al límite de €60/día cada día, pero €202 del periodo (12%) se fue a keywords sin conversión. Si se pausan esas keywords, el mismo presupuesto comprará más conversiones. Aumentar budget antes de limpiar las keywords sería escalar el problema.

### 🔴 #3 — Sin grupo de Aire Acondicionado en temporada alta
**Impacto:** El perfil define junio-agosto como "foco AC". Actualmente no hay ningún grupo activo para capturar búsquedas de reparación/instalación de aire acondicionado. Junio ya empezó. Se está perdiendo la temporada más rentable del año.

Keywords obvias sin cobertura: "reparación aire acondicionado barcelona", "técnico AC", "avería aire acondicionado urgente", etc.

### 🟠 #4 — Grupos Lavadoras y Neveras completamente muertos
**Impacto:** 0 impresiones, 0 clics en 27 días. Dos servicios del catálogo de Tecniclima sin ninguna visibilidad. Posibles causas: las keywords tienen bajo volumen de búsqueda, el presupuesto lo absorben completamente Calderas y Calentadores, o hay un problema de configuración. Necesitan diagnóstico y decisión: reestructurar o pausar y redirigir budget.

### 🟠 #5 — Keywords mal asignadas y duplicadas degradan Quality Score
**Impacto:** 5 keywords en grupos incorrectos (ej. "tecnico calderas" en Calentadores) hacen que Google muestre el anuncio equivocado. Además hay 3 keywords casi idénticas sin conversión: "tecnico de calefaccion", "tecnico en calefaccion", "tecnicos en calefaccion" — €90 gastados en duplicados semánticos.

---

## Plan de Acción Priorizado

### Semana 1 — Urgente (impacto inmediato)

| Prioridad | Acción | Impacto estimado |
|-----------|--------|-----------------|
| 🔴 1 | **Configurar tracking de llamadas** en Google Ads (Google Tag Manager o llamadas directas) | Mide el CPA real, desbloquea todas las decisiones siguientes |
| 🔴 2 | **Exportar Informe de Términos de Búsqueda** (últimos 90 días) y añadir negativas | Descubre gasto oculto en búsquedas irrelevantes |
| 🔴 3 | **Pausar "mantenimiento gas"** — €62, 0 conv, baja calidad | Recupera €62/mes |
| 🟠 4 | **Pausar triada sin conversión**: "tecnicos en calefaccion" + "tecnico en calefaccion" + "tecnico de calefaccion" | Recupera ~€90/mes |
| 🟠 5 | **Mover keywords mal asignadas** a sus grupos correctos | Mejora QS y relevancia de anuncios |

### Semana 2 — Alta prioridad

| Acción | Detalle |
|--------|---------|
| **Crear grupo Aire Acondicionado** | Urgente para temporada. Keywords: reparación AC, técnico aire acondicionado, avería AC barcelona, mantenimiento climatización |
| **Revisar landing page de "instalador gas autorizado"** | Convierte bien (CPA €19.78) pese a baja calidad — mejorar relevancia para subir QS y bajar CPC |
| **Reparar extracto de sitio rechazado** | Asset importante sin mostrar — reescribir para cumplir políticas |
| **Diagnosticar Lavadoras y Neveras** | ¿Keywords con volumen suficiente? ¿Presupuesto llegando? → Decisión: reestructurar o pausar |

### Mes 1 — Optimización sostenida

| Acción | Detalle |
|--------|---------|
| Aumentar budget a €80-90/día | Solo después de limpiar keywords y confirmar CPA real con llamadas trackeadas |
| Revisar sitelinks IA (Encimera Gas, Aerotermia) | Evaluar si desvían intención de reparación → excluir si el CTR no justifica |
| Escalar keywords estrella | "reparación de calderas" tiene margen de escala — añadir variantes exactas |
| Activar/revisar PMax (Campaign #1) | En pausa con €21/día asignado — puede capturar intenciones que Search no alcanza |

---

## Datos que Faltan para Análisis Completo

| Dato | Por qué importa |
|------|----------------|
| **Informe de Términos de Búsqueda** | Crítico: revela búsquedas reales activando keywords de concordancia amplia |
| **Informe de Anuncios** | Sin él no podemos evaluar qué copy convierte mejor |
| **Volumen real de leads (Edgar)** | Llamadas + WhatsApp + formulario — confirmar con el cliente |
| **Configuración de conversiones** | ¿Qué trackea exactamente? ¿Click en WhatsApp? ¿Formulario enviado? ¿Llamada? |
| **Quality Score por keyword** | El export no incluía QS — necesario para diagnóstico completo de keywords |

---

## Conclusión

La cuenta tiene una base sólida: CTR del 7.49% es excelente para el sector, el CPC de €1.89 es competitivo, y hay keywords con CPA muy eficiente. El problema principal no es la estructura, sino la **falta de visibilidad real sobre los leads** (tracking de llamadas) y **un 12% del presupuesto desperdiciado** en keywords sin retorno.

Si se resuelve el tracking y se redirige el gasto desperdiciado a keywords estrella, el CPA real podría estar en €10-14 — cerca del objetivo. Añadir el grupo de AC para la temporada alta es la mayor oportunidad de crecimiento en los próximos 60 días.
