Genera el reporte semanal de rendimiento para el cliente activo.

1. Pregunta qué cliente si no está en contexto
2. Activa el agente Analista (`.claude/agents/analyst/CLAUDE.md`)
3. Pull de métricas últimos 7 días vs 7 días anteriores en todas las plataformas activas del cliente
4. Identifica variaciones >20%, anomalías, y alertas de presupuesto
5. Top 3 insights + 3 recomendaciones priorizadas
6. Guarda el reporte en `clients/<cliente>/reports/YYYY-MM-DD_semanal.md`
7. Resume en 5 bullets para el usuario
