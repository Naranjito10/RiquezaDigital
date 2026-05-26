# Vibiz — UX y Onboarding

> Objetivo: reverse engineering paso-a-paso del flujo desde "instalo el plugin" hasta "publico mi primera pieza". Lo que ellos pulieron con miles de usuarios nosotros lo copiamos sin pagar ese coste de iteración.

## Captura del flujo

> **Cómo capturar:** durante tu primer uso, anota cada pantalla / paso. Si puedes, screenshot en `ux-onboarding/screenshots/`. Cualquier detalle aparentemente trivial (orden de preguntas, defaults preseleccionados, mensajes de error) es señal de optimización.

### Paso 1 — Instalación

- **Comando que se ejecutó:** `/plugin marketplace add Vibiz-ai/vibiz-claude-plugin` + `/plugin install vibiz@vibiz`
- **Qué pasó visualmente:** <!-- a rellenar -->
- **Qué pidió:** <!-- a rellenar -->
- **Errores / fricciones:** <!-- a rellenar -->

### Paso 2 — Autenticación (`/mcp`)

- **Plataformas que pidió conectar:** <!-- a rellenar -->
- **Orden de las plataformas:** <!-- importante: ¿qué priorizan? -->
- **¿OAuth limpia?** <!-- ¿abre navegador, vuelve solo, etc.? -->
- **¿Pide tokens / credenciales manualmente para algo?** <!-- a rellenar -->

### Paso 3 — `/vibiz:onboard`

- **Preguntas que hizo y en qué orden:** <!-- captura literal -->
- **Defaults preseleccionados:** <!-- a rellenar -->
- **Datos pedidos sobre la empresa / ICP / oferta:** <!-- a rellenar (cruzar con data-schema.md) -->
- **Tiempo total hasta completar:** <!-- a rellenar -->

### Paso 4 — Primera generación / primer post

- **Cómo se llega al primer output:** <!-- a rellenar -->
- **Calidad del primer output (rating 1-5):** <!-- a rellenar -->
- **¿Pide aprobar antes de publicar?** <!-- a rellenar -->

## Patrones de UX detectados

<!-- Patrones reutilizables. Ejemplos:
- "Pide menos datos al principio que al final" (progresivo)
- "Genera un draft antes de pedir confirmar para anclar al usuario"
- "Defaults son siempre lo más vendible para ellos (probablemente upsell hook)"
-->

## Decisiones para Agencia Agéntica

<!-- Qué de su onboarding queremos replicar tal cual y qué adaptaríamos -->
