"""
Obtiene reportes de performance de Google Ads leyendo la hoja de Google Sheets exportada.
Uso: python src/get_google_insights.py
"""

import os
import csv
import sys
import requests
from dotenv import load_dotenv

load_dotenv()


def get_google_ads_insights(sheet_url_or_id: str = None) -> list:
    """
    Descarga el CSV del Google Sheet que contiene la exportación de Google Ads.
    
    Args:
        sheet_url_or_id: URL completa o ID de la hoja de Google Sheets.
    """
    if not sheet_url_or_id:
        sheet_url_or_id = os.getenv("GOOGLE_SHEET_URL_OR_ID")
    
    if not sheet_url_or_id:
        print("\n[ERROR] Falta especificar GOOGLE_SHEET_URL_OR_ID en tu archivo .env")
        print("Pega la variable en el archivo .env de la raíz con tu URL de Google Sheets:")
        print("GOOGLE_SHEET_URL_OR_ID=https://docs.google.com/spreadsheets/d/tu_hoja_id/edit")
        return []
    
    # Extraer el ID de la hoja de cálculo
    sheet_id = sheet_url_or_id
    if "docs.google.com/spreadsheets" in sheet_url_or_id:
        parts = sheet_url_or_id.split("/d/")
        if len(parts) > 1:
            sheet_id = parts[1].split("/")[0]

    # URL pública de exportación en formato CSV
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    
    try:
        response = requests.get(csv_url)
        response.raise_for_status()
        
        # Parsear contenido del CSV
        csv_data = response.text.strip()
        if not csv_data:
            print("[INFO] La hoja de cálculo está vacía.")
            return []
            
        lines = csv_data.splitlines()
        reader = csv.DictReader(lines)
        results = [row for row in reader]
        
        if not results:
            print("[INFO] No se encontraron registros de campañas en la hoja de cálculo.")
            return []
            
        print(f"\n{'='*60}")
        print(f"REPORTE DE RENDIMIENTO: GOOGLE ADS (ÚLTIMOS 30 DÍAS)")
        print(f"{'='*60}")
        for row in results:
            campaign = row.get("CampaignName", "N/A")
            status = row.get("Status", "N/A")
            cost = row.get("Cost", "0")
            impr = row.get("Impressions", "0")
            clicks = row.get("Clicks", "0")
            conv = row.get("Conversions", "0")
            ctr = row.get("CTR", "0%")
            cpc = row.get("CPC", "0")
            
            print(f"\n  Campaña: {campaign} [{status}]")
            print(f"    Inversión:   {cost} EUR")
            print(f"    Impresiones: {impr}")
            print(f"    Clicks:      {clicks}")
            print(f"    Conversiones:{conv}")
            print(f"    CTR:         {ctr}")
            print(f"    CPC Medio:   {cpc} EUR")
            
        return results
    except Exception as e:
        print(f"\n[ERROR] No se pudo leer la hoja de cálculo: {e}")
        print("Asegúrate de que la hoja de cálculo tiene permisos para 'Cualquier persona con el enlace puede leer (Lector)'.")
        return []


if __name__ == "__main__":
    sheet_param = sys.argv[1] if len(sys.argv) > 1 else None
    get_google_ads_insights(sheet_param)
