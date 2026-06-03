# Matriz de Autoridad — Veganashi

Esta matriz define el nivel de autonomía que tiene la Agencia Autónoma para ejecutar cambios en la cuenta de anuncios de Veganashi sin requerir confirmación explícita de Kevin.

| Acción | Verde — Actúa solo | Amarillo — Propone (1-tap) | Rojo — Escala siempre |
| :--- | :---: | :---: | :---: |
| **Analizar métricas** | ✓ Siempre | — | — |
| **Alertar anomalías** | ✓ Siempre | — | — |
| **Pausar anuncio CTR < 0.6%** | — | ✓ | — |
| **Pausar conjunto CPA > 20€** | — | ✓ | — |
| **Modificar puja conjunto** | — | ✓ Si delta < 15% | Delta > 15% |
| **Aumentar presupuesto diario** | — | ✓ Si delta < 10% | Delta > 10% |
| **Crear campaña de Retargeting** | — | ✓ (PAUSED) | — |
| **Lanzar campaña fría nueva** | — | — | ✓ Siempre |
| **Cambiar presupuesto mensual** | — | — | ✓ Siempre |
