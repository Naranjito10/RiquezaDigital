"""
Reporte de rendimiento Google Ads — entrada unificada.

Modos de uso:
  API directa (requiere profile.json configurado):
    python src/get_google_insights.py --client tecniclima
    python src/get_google_insights.py --client tecniclima --range LAST_7_DAYS --level adgroup
    python src/get_google_insights.py --all

  Fallback Google Sheets (exportación manual desde Google Ads Scripts):
    python src/get_google_insights.py --sheet <url_o_id>
    GOOGLE_SHEET_URL_OR_ID=<id> python src/get_google_insights.py --sheet

Setup inicial por cliente (una sola vez):
    python src/get_google_insights.py --setup <cliente>
"""

import os
import csv
import sys
import argparse
import requests
from pathlib import Path

# Ejecutar desde pipelines/marketing-digital/ para que el paquete ads sea visible
sys.path.insert(0, str(Path(__file__).parent.parent))


DATE_RANGES = [
    "LAST_7_DAYS", "LAST_14_DAYS", "LAST_30_DAYS",
    "THIS_MONTH", "LAST_MONTH", "LAST_90_DAYS",
]


def _run_api_mode(client_name: str, date_range: str, level: str) -> list:
    """Obtiene datos directamente de la Google Ads API."""
    from ads.shared.google_client import load_profile, get_campaign_insights, get_adgroup_insights, print_report

    profile = load_profile(client_name)
    fn = get_adgroup_insights if level == "adgroup" else get_campaign_insights
    insights = fn(profile, date_range)
    print_report(client_name, insights, date_range)
    return insights


def _run_all_api_mode(date_range: str, level: str) -> None:
    """Ejecuta el reporte para todos los clientes con Google habilitado."""
    from ads.shared.google_client import list_google_clients, load_profile, get_campaign_insights, get_adgroup_insights, print_report

    clients = list_google_clients()
    if not clients:
        print("[ERROR] No hay clientes con Google Ads habilitado.")
        print("Crea un profile.json en ads/clients/<cliente>/ siguiendo la plantilla.")
        sys.exit(1)

    for name in clients:
        profile = load_profile(name)
        fn = get_adgroup_insights if level == "adgroup" else get_campaign_insights
        insights = fn(profile, date_range)
        print_report(name, insights, date_range)


def _run_sheets_mode(sheet_url_or_id: str = None) -> list:
    """
    Fallback: lee el CSV exportado por el Google Ads Script a Google Sheets.
    Útil si la API directa no está configurada aún.
    """
    if not sheet_url_or_id:
        sheet_url_or_id = os.getenv("GOOGLE_SHEET_URL_OR_ID")

    if not sheet_url_or_id:
        print("[ERROR] Falta especificar la hoja de Google Sheets.")
        print("Usa: --sheet <url> o define GOOGLE_SHEET_URL_OR_ID en .env")
        sys.exit(1)

    sheet_id = sheet_url_or_id
    if "docs.google.com/spreadsheets" in sheet_url_or_id:
        parts = sheet_url_or_id.split("/d/")
        if len(parts) > 1:
            sheet_id = parts[1].split("/")[0]

    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

    try:
        response = requests.get(csv_url, timeout=15)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] No se pudo descargar la hoja: {e}")
        print("Verifica que la hoja tiene permisos 'Cualquier persona con el enlace puede leer'.")
        return []

    csv_data = response.text.strip()
    if not csv_data:
        print("[INFO] La hoja de cálculo está vacía.")
        return []

    lines = csv_data.splitlines()
    reader = csv.DictReader(lines)
    results = [row for row in reader]

    if not results:
        print("[INFO] Sin registros de campañas en la hoja.")
        return []

    print(f"\n{'='*65}")
    print(f"GOOGLE ADS — Google Sheets export (modo fallback)")
    print(f"{'='*65}")
    for row in results:
        status_icon = "✅" if row.get("Status", "").upper() == "ENABLED" else "⏸"
        print(f"\n  {status_icon} {row.get('CampaignName', 'N/A')} [{row.get('Status', 'N/A')}]")
        print(f"      Gasto:       €{row.get('Cost', '0')}")
        print(f"      Impresiones: {row.get('Impressions', '0')}")
        print(f"      Clicks:      {row.get('Clicks', '0')}")
        print(f"      Conversiones:{row.get('Conversions', '0')}")
        print(f"      CTR:         {row.get('CTR', '0%')}")
        print(f"      CPC Medio:   €{row.get('CPC', '0')}")

    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Ads insights — API o Sheets")
    parser.add_argument("--client", metavar="NOMBRE", help="Cliente concreto (usa API directa)")
    parser.add_argument("--all", action="store_true", help="Todos los clientes con Google habilitado")
    parser.add_argument("--range", default="LAST_30_DAYS", choices=DATE_RANGES, dest="date_range")
    parser.add_argument("--level", default="campaign", choices=["campaign", "adgroup"])
    parser.add_argument("--sheet", metavar="URL_O_ID", nargs="?", const="env",
                        help="Fallback: leer desde Google Sheets (pasa URL o usa GOOGLE_SHEET_URL_OR_ID de .env)")
    parser.add_argument("--setup", metavar="CLIENTE", help="Generar refresh_token OAuth2 para un cliente")

    args = parser.parse_args()

    if args.setup:
        from ads.shared.google_client import setup_oauth_flow
        setup_oauth_flow(args.setup)
        sys.exit(0)

    if args.sheet is not None:
        sheet_param = None if args.sheet == "env" else args.sheet
        _run_sheets_mode(sheet_param)
        sys.exit(0)

    if args.all:
        _run_all_api_mode(args.date_range, args.level)
        sys.exit(0)

    if args.client:
        _run_api_mode(args.client, args.date_range, args.level)
        sys.exit(0)

    parser.print_help()
