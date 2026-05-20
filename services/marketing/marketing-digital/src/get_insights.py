"""
Obtiene reportes de performance de Meta Ads.
Uso: python src/get_insights.py
"""

import os
from utils.api_client import get_ad_account, init_api
from facebook_business.adobjects.adaccount import AdAccount


FIELDS = [
    "campaign_name",
    "adset_name",
    "impressions",
    "reach",
    "clicks",
    "spend",
    "cpc",
    "cpm",
    "ctr",
    "actions",
    "cost_per_action_type",
]


def get_account_insights(date_preset: str = "last_7d", level: str = "campaign") -> list:
    """
    Obtiene insights de la cuenta para el rango de fechas indicado.

    Args:
        date_preset: last_7d, last_14d, last_30d, last_month, this_month
        level: account, campaign, adset, ad

    Returns:
        Lista de dicts con métricas
    """
    init_api()
    account = get_ad_account()

    params = {
        "date_preset": date_preset,
        "level": level,
        "fields": ",".join(FIELDS),
    }

    print(f"\nObteniendo insights: {level} | {date_preset}...")
    insights = account.get_insights(params=params)

    results = []
    for row in insights:
        results.append(dict(row))

    if not results:
        print("Sin datos para el rango seleccionado.")
        return []

    # Mostrar resumen en consola
    print(f"\n{'='*60}")
    print(f"REPORTE: {level.upper()} | {date_preset}")
    print(f"{'='*60}")
    for row in results:
        name = row.get("campaign_name") or row.get("adset_name") or "N/A"
        print(f"\n  {name}")
        print(f"    Spend:      ${float(row.get('spend', 0)):.2f} USD")
        print(f"    Impressions: {row.get('impressions', 0)}")
        print(f"    Clicks:      {row.get('clicks', 0)}")
        print(f"    CTR:         {row.get('ctr', 0)}%")
        print(f"    CPC:         ${float(row.get('cpc', 0)):.2f} USD")
        print(f"    CPM:         ${float(row.get('cpm', 0)):.2f} USD")

    return results


if __name__ == "__main__":
    get_account_insights(date_preset="last_7d", level="campaign")
