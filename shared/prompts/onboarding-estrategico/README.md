# Pack de Onboarding Estratégico

Pack de 4 prompts que se ejecutan en sesiones separadas de Claude Code para construir la base estratégica completa de cualquier cliente B2B (nuevo o existente).

**Output esperado:** 4 documentos markdown guardados en `clients/<cliente>/strategy/` (o `agencia/marketing/strategy/` si se aplica a la propia RD) que sirven como fuente de verdad y alimentan toda decisión posterior (creativos, copy, campañas, contenido orgánico, propuestas).

---

## Cuándo usar

- **Cliente nuevo:** ejecutar el pack completo en la primera semana de relación.
- **Cliente existente sin documentación estratégica:** ejecutar para construir la base que faltaba.
- **Pivote estratégico:** rehacer las sesiones 1 y 4 cuando el cliente cambia de modelo o vertical.

---

## Aplicabilidad por sesión

| Sesión | Universal | Notas |
|---|---|---|
| 1 — Brief Estratégico | ✅ Sí | Cualquier cliente B2B necesita esto. |
| 2 — Estudio de Mercado | ✅ Sí | Adaptar profundidad al presupuesto del cliente. |
| 3 — PRD Detección de Virales | ⚠️ Condicional | Solo si la estrategia es inbound vía social media (IG/LinkedIn/TikTok). |
| 4 — Plan de Marketing Inbound | ✅ Sí | Adaptar canales según ICP del cliente. |

---

## Cómo ejecutar el pack

1. **Sesión 1 — sola.** Reemplazar `{{PLACEHOLDERS}}` con datos del cliente. Lanzar en sesión nueva de Claude Code. Output → `clients/<cliente>/strategy/brief-estrategico.md`.
2. **Sesión 2 — después de la 1.** Pegar el output de la sesión 1 donde indica el prompt. Output → `clients/<cliente>/strategy/estudio-mercado.md`.
3. **Sesiones 3 y 4 — en paralelo después de la 2.** Pegar outputs de 1 y 2. Outputs → `clients/<cliente>/strategy/prd-virales.md` y `clients/<cliente>/strategy/plan-inbound.md`.

---

## Placeholders comunes

| Placeholder | Significado | Ejemplo |
|---|---|---|
| `{{CLIENTE_NOMBRE}}` | Nombre comercial | Riqueza Digital |
| `{{CLIENTE_WEB}}` | URL principal | riquezadigital.es |
| `{{CLIENTE_VERTICAL_PRINCIPAL}}` | Servicio core | Formación en IA para equipos B2B |
| `{{CLIENTE_VERTICAL_SECUNDARIO}}` | Upsell (si aplica) | Desarrollo de software personalizado |
| `{{CLIENTE_CATALOGO_URL}}` | URL del catálogo | riquezadigital.es/cursos |
| `{{CLIENTE_EMAIL}}` | Contacto comercial | info@riquezadigital.es |
| `{{CLIENTE_GEO}}` | Mercado geográfico | España + LATAM |

---

## Mantenimiento

Este pack es parte del producto comercial "Agencia Agéntica". Cualquier mejora detectada al ejecutarlo con un cliente debe propagarse aquí (mejora la plantilla, no solo el output del cliente).

Ver `agencia/AGENCIA-AGENTICA.md` para el inventario completo del producto.
