/**
 * Google Ads Script para Riqueza Digital
 * Exporta métricas de rendimiento de campañas a un archivo de Google Sheets.
 * 
 * Instrucciones:
 * 1. Crea una hoja de Google Sheets vacía en tu cuenta.
 * 2. Copia la URL de la hoja y pégala abajo en la variable SPREADSHEET_URL.
 * 3. En el panel de Google Ads, ve a Herramientas -> Scripts.
 * 4. Crea un script nuevo, pega este código completo, autoriza los permisos y haz clic en Ejecutar (Run).
 * 5. Configura una programación diaria o semanal para que se actualice solo.
 */

function main() {
  // Pega la URL completa de tu Google Sheet aquí:
  var SPREADSHEET_URL = "REEMPLAZAR_CON_LA_URL_DE_TU_GOOGLE_SHEETS"; 
  
  if (SPREADSHEET_URL === "REEMPLAZAR_CON_LA_URL_DE_TU_GOOGLE_SHEETS") {
    Logger.log("Por favor, reemplaza la variable SPREADSHEET_URL con una URL válida de Google Sheets.");
    return;
  }

  try {
    var spreadsheet = SpreadsheetApp.openByUrl(SPREADSHEET_URL);
    var sheet = spreadsheet.getActiveSheet();
    sheet.clear();
    
    // Escribir cabecera
    sheet.appendRow(["CampaignName", "Status", "Impressions", "Clicks", "Cost", "Conversions", "CTR", "CPC"]);
    
    // Consultar el reporte utilizando el lenguaje de consultas de Google Ads (GAQL / AWQL)
    var report = AdsApp.report(
      "SELECT CampaignName, CampaignStatus, Impressions, Clicks, Cost, Conversions, ActiveViewCtr, AverageCpc " +
      "FROM CAMPAIGN_PERFORMANCE_REPORT " +
      "DURING LAST_30_DAYS"
    );
    
    var rows = report.rows();
    var count = 0;
    while (rows.hasNext()) {
      var row = rows.next();
      sheet.appendRow([
        row["CampaignName"],
        row["CampaignStatus"],
        row["Impressions"],
        row["Clicks"],
        row["Cost"],
        row["Conversions"],
        row["ActiveViewCtr"],
        row["AverageCpc"]
      ]);
      count++;
    }
    Logger.log("Reporte exportado correctamente. " + count + " campañas añadidas a: " + SPREADSHEET_URL);
  } catch (e) {
    Logger.log("Error al exportar: " + e.toString());
  }
}
