# SOP: Exportar Datos de Google Ads MCC a Google Sheets

**Área:** Marketing — Google Ads  
**Estado:** 🌱 Draft  
**Última actualización:** 2026-06-04  
**Clientes donde se aplicó:** Tecniclima, Anywr  
**Tiempo estimado:** 30–45 minutos

---

## Resumen

Establece el procedimiento para extraer de forma automatizada las métricas clave de rendimiento de las cuentas gestionadas bajo el Google Ads MCC (Mi Centro de Clientes) de Riqueza Digital y volcarlas a una hoja de cálculo de Google Sheets para reportes en tiempo real.

---

## Pre-requisitos

- [ ] Cuenta Google Ads MCC con ID de administrador (formato XXX-XXX-XXXX)
- [ ] Developer token aprobado (Basic Access en Google Ads API Center) para consultas multi-cuenta
- [ ] Proyecto activo en Google Cloud Console con la API de Google Ads y la API de Google Sheets habilitadas
- [ ] Hoja de cálculo de Google Sheets de destino compartida con acceso de edición

---

## Pasos

### 1. Configurar Credenciales de Google API
Para autorizar a los scripts de Riqueza Digital a leer de Google Ads y escribir en Sheets:
1. En Google Cloud Console → Credenciales:
   - Crear un **ID de cliente OAuth 2.0** tipo "Aplicación de escritorio" para Google Ads API.
   - Crear una **Cuenta de Servicio** (Service Account), descargar su clave JSON y copiar la dirección de correo generada (ej. `mcc-exporter@proyecto.iam.gserviceaccount.com`).
2. Compartir la hoja de Google Sheets de destino con el email de la Cuenta de Servicio dándole permisos de **Editor**.

### 2. Configurar Script de Extracción
En la carpeta de pipelines de la agencia (`pipelines/marketing-digital/ads/`):
1. Crear una subcarpeta `mcc_export/` y el archivo `config.json` con los IDs de las cuentas del cliente, el ID de la hoja de Sheets, y el ID de la hoja (tab) específica:
   ```json
   {
     "mcc_customer_id": "XXX-XXX-XXXX",
     "target_spreadsheet_id": "ID_DE_HOJA_DE_SHEETS",
     "client_accounts": {
       "Tecniclima": "AAA-AAA-AAAA",
       "Anywr": "BBB-BBB-BBBB"
     }
   }
   ```
2. Cargar las credenciales de la API de Google Ads en `profile.json` de cada cliente (o en variables del sistema) según el SOP [google-ads-api-setup.md](../google-ads-api-setup.md).

### 3. Ejecución del Query de Ads (Google Ads Query Language - GAQL)
El script de extracción debe consultar el endpoint de reporte de campañas usando GAQL para obtener los datos de rendimiento agregados. Ejemplo de query básico:
```sql
SELECT
  customer_client.descriptive_name,
  campaign.name,
  metrics.impressions,
  metrics.clicks,
  metrics.cost_micros,
  metrics.conversions,
  segments.date
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
```

*Nota:* El campo `cost_micros` debe dividirse por `1,000,000` para convertirse a la moneda del cliente.

### 4. Escritura en Google Sheets
1. El pipeline lee el JSON devuelto por la API de Google Ads.
2. Inicia conexión con la Sheets API utilizando la clave JSON de la Cuenta de Servicio.
3. Formatea la información en filas (Fecha, Cliente, Campaña, Impresiones, Clics, CTR, Coste, Conversiones, CPA) y limpia las celdas existentes antes de escribir el nuevo set de datos con la llamada `spreadsheets.values.update`.

### 5. Automatización (n8n o Tarea Programada de Windows)
Para mantener los reportes actualizados diariamente:
* **Opción A (n8n):** Crear un workflow con un nodo Cron (Schedule) fijado a las 05:00 AM → ejecutar nodo de ejecución de comando (`Execute Command`) llamando al script de python:
  ```bash
  python pipelines/marketing-digital/ads/mcc_export/run_export.py
  ```
* **Opción B (Windows Task Scheduler):** Crear una tarea básica que lance `powershell.exe` ejecutando el mismo comando diariamente.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Error `API Permission Denied` al consultar Ads | El developer token de la cuenta no está aprobado o no pertenece a la MCC consultada | Verificar en el Centro de la API de Google Ads de la cuenta MCC que el token esté en verde y activo |
| Error `GoogleJsonResponseException: 403 Shared access error` | No se compartió el documento de Sheets con la Cuenta de Servicio | Abrir la hoja de cálculo en el navegador, hacer clic en Compartir y añadir el email de la service account con permisos de editor |
| Desviación en costes de Google Ads | Los costes de la API vienen en "micros" | Asegurarse de dividir la métrica `metrics.cost_micros` entre `1,000,000` en el script procesador |

---

## Decisiones clave

- **Decisión:** Usar una Cuenta de Servicio de Google Cloud para escribir en Sheets en lugar de OAuth de usuario interactivo.  
  **Razón:** Las Cuentas de Servicio no requieren flujos interactivos en navegador para renovar tokens de acceso, lo que las hace 100% fiables para crons y scripts en background desatendidos.  
  **Alternativa descartada:** Flujos OAuth interactivos para Google Sheets (requieren refrescos manuales frecuentes en servidor).

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| Moneda de la cuenta | División de costes | Cuentas en USD vs EUR (se define en la configuración del cliente) |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Creación inicial del SOP de exportación de métricas de Google Ads MCC.*
