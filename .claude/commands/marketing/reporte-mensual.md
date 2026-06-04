Genera el informe mensual premium de rendimiento y saneamiento para el cliente activo.

1. Pregunta qué cliente si no está definido en el contexto actual.
2. Solicita el mes a reportar en formato YYYY-MM (por defecto el mes anterior).
3. Carga y verifica la existencia de `report_config.json` y `monthly_metrics_<mes>.json` del cliente en su directorio.
4. Ejecuta el backend Python de compilación:
   ```powershell
   python pipelines/marketing-digital/reports/monthly_report_generator.py --client <cliente> --month <mes>
   ```
5. Muestra un resumen ejecutivo del reporte y los KPIs consolidados (Inversión, Leads, CPL medio) formateados en Markdown en el chat.
6. Entrega el enlace directo al archivo HTML generado en `clients/<cliente>/reports/` para su apertura e impresión a PDF.
