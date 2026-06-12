"""
Cliente Google Ads multi-cuenta.
Usa OAuth2 con refresh_token almacenado en profile.json.

Setup inicial por cliente (una sola vez):
    python ads/shared/google_client.py setup <cliente>

Uso normal:
    python ads/shared/google_client.py <cliente>
    python ads/shared/google_client.py <cliente> --range LAST_7_DAYS
    python ads/shared/google_client.py <cliente> --level adgroup
    python ads/shared/google_client.py --all
"""

import json
import sys
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent  # ads/
CLIENTS_DIR = BASE_DIR / "clients"

DATE_RANGES = [
    "LAST_7_DAYS", "LAST_14_DAYS", "LAST_30_DAYS",
    "THIS_MONTH", "LAST_MONTH", "LAST_90_DAYS",
]


def load_profile(client_name: str) -> dict:
    profile_path = CLIENTS_DIR / client_name / "profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(
            f"No existe ads/clients/{client_name}/profile.json\n"
            f"Crea el perfil siguiendo la plantilla en ads/clients/_template/profile.json"
        )
    with open(profile_path) as f:
        return json.load(f)


def list_google_clients() -> list[str]:
    """Devuelve todos los clientes con Google Ads habilitado."""
    clients = []
    for profile_path in sorted(CLIENTS_DIR.glob("*/profile.json")):
        if profile_path.parent.name == "_template":
            continue
        try:
            with open(profile_path) as f:
                p = json.load(f)
            if p.get("platforms", {}).get("google", {}).get("enabled"):
                clients.append(profile_path.parent.name)
        except Exception:
            pass
    return clients


def init_google_client(profile: dict):
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ImportError:
        raise ImportError(
            "Instala el SDK: pip install google-ads\n"
            "O ejecuta: pip install -r requirements.txt"
        )

    google = profile["platforms"]["google"]
    if not google.get("enabled"):
        raise ValueError(f"Google Ads no está habilitado para '{profile['client']}'")

    config = {
        "developer_token": google["developer_token"],
        "client_id": google["client_id"],
        "client_secret": google["client_secret"],
        "refresh_token": google["refresh_token"],
        "login_customer_id": google["customer_id"].replace("-", ""),
        "use_proto_plus": True,
    }
    return GoogleAdsClient.load_from_dict(config)


def get_campaign_insights(profile: dict, date_range: str = "LAST_30_DAYS") -> list[dict]:
    """Métricas completas a nivel campaña: spend, clicks, impresiones, conversiones, ROAS."""
    client = init_google_client(profile)
    customer_id = profile["platforms"]["google"]["customer_id"].replace("-", "")
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          campaign_budget.amount_micros,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros,
          metrics.ctr,
          metrics.average_cpc,
          metrics.average_cpm,
          metrics.conversions,
          metrics.conversions_value,
          metrics.cost_per_conversion
        FROM campaign
        WHERE segments.date DURING {date_range}
          AND campaign.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
    """

    response = ga_service.search(customer_id=customer_id, query=query)
    results = []
    for row in response:
        cost_eur = row.metrics.cost_micros / 1_000_000
        conv_value = row.metrics.conversions_value
        roas = (conv_value / cost_eur) if cost_eur > 0 else 0

        results.append({
            "level": "campaign",
            "id": row.campaign.id,
            "name": row.campaign.name,
            "status": row.campaign.status.name,
            "budget_eur": row.campaign_budget.amount_micros / 1_000_000,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost_eur": cost_eur,
            "ctr_pct": row.metrics.ctr * 100,
            "avg_cpc_eur": row.metrics.average_cpc / 1_000_000,
            "avg_cpm_eur": row.metrics.average_cpm / 1_000_000,
            "conversions": row.metrics.conversions,
            "conv_value_eur": conv_value,
            "cost_per_conv_eur": row.metrics.cost_per_conversion / 1_000_000,
            "roas": roas,
        })
    return results


def get_adgroup_insights(profile: dict, date_range: str = "LAST_30_DAYS") -> list[dict]:
    """Métricas a nivel ad group para diagnóstico de rendimiento interno."""
    client = init_google_client(profile)
    customer_id = profile["platforms"]["google"]["customer_id"].replace("-", "")
    ga_service = client.get_service("GoogleAdsService")

    query = f"""
        SELECT
          campaign.name,
          ad_group.id,
          ad_group.name,
          ad_group.status,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros,
          metrics.ctr,
          metrics.average_cpc,
          metrics.conversions,
          metrics.conversions_value,
          metrics.cost_per_conversion
        FROM ad_group
        WHERE segments.date DURING {date_range}
          AND ad_group.status != 'REMOVED'
        ORDER BY metrics.cost_micros DESC
        LIMIT 50
    """

    response = ga_service.search(customer_id=customer_id, query=query)
    results = []
    for row in response:
        cost_eur = row.metrics.cost_micros / 1_000_000
        conv_value = row.metrics.conversions_value
        roas = (conv_value / cost_eur) if cost_eur > 0 else 0

        results.append({
            "level": "adgroup",
            "campaign": row.campaign.name,
            "id": row.ad_group.id,
            "name": row.ad_group.name,
            "status": row.ad_group.status.name,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "cost_eur": cost_eur,
            "ctr_pct": row.metrics.ctr * 100,
            "avg_cpc_eur": row.metrics.average_cpc / 1_000_000,
            "conversions": row.metrics.conversions,
            "conv_value_eur": conv_value,
            "cost_per_conv_eur": row.metrics.cost_per_conversion / 1_000_000,
            "roas": roas,
        })
    return results


def print_report(client_name: str, insights: list[dict], date_range: str) -> None:
    """Imprime el reporte formateado en consola."""
    if not insights:
        print(f"\n[INFO] Sin datos para {client_name} en {date_range}.")
        return

    level = insights[0]["level"]
    print(f"\n{'='*65}")
    print(f"GOOGLE ADS — {client_name.upper()} | {date_range} | nivel {level.upper()}")
    print(f"{'='*65}")

    total_cost = sum(r["cost_eur"] for r in insights)
    total_clicks = sum(r["clicks"] for r in insights)
    total_impressions = sum(r["impressions"] for r in insights)
    total_conv = sum(r["conversions"] for r in insights)
    total_conv_value = sum(r["conv_value_eur"] for r in insights)
    avg_roas = (total_conv_value / total_cost) if total_cost > 0 else 0

    print(f"\n  RESUMEN CUENTA")
    print(f"    Gasto total:   €{total_cost:.2f}")
    print(f"    Impresiones:   {total_impressions:,}")
    print(f"    Clicks:        {total_clicks:,}")
    print(f"    Conversiones:  {total_conv:.1f}")
    print(f"    Valor conv.:   €{total_conv_value:.2f}")
    print(f"    ROAS:          {avg_roas:.2f}x")

    print(f"\n  DETALLE POR {'CAMPAÑA' if level == 'campaign' else 'AD GROUP'}")
    print(f"  {'-'*60}")

    for row in insights:
        label = row["name"]
        if level == "adgroup":
            label = f"{row['campaign']} › {row['name']}"

        status_icon = "✅" if row["status"] == "ENABLED" else "⏸"
        print(f"\n  {status_icon} {label}")
        print(f"      Gasto:    €{row['cost_eur']:.2f}  |  Clicks: {row['clicks']:,}  |  CTR: {row['ctr_pct']:.2f}%")
        print(f"      CPC med:  €{row['avg_cpc_eur']:.2f}  |  Conv: {row['conversions']:.1f}  |  ROAS: {row['roas']:.2f}x")
        if row["conversions"] > 0:
            print(f"      CPA:      €{row['cost_per_conv_eur']:.2f}  |  Val.conv: €{row['conv_value_eur']:.2f}")


# Mantener compatibilidad con el código anterior
def get_campaigns_overview(profile: dict) -> list[dict]:
    return get_campaign_insights(profile)


def setup_oauth_flow(client_name: str) -> None:
    """Genera refresh_token para un cliente via OAuth2 interactivo. Ejecutar una sola vez."""
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        raise ImportError("Instala: pip install google-auth-oauthlib")

    profile_path = CLIENTS_DIR / client_name / "profile.json"
    with open(profile_path) as f:
        profile = json.load(f)

    google = profile["platforms"]["google"]
    client_config = {
        "installed": {
            "client_id": google["client_id"],
            "client_secret": google["client_secret"],
            "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    flow = InstalledAppFlow.from_client_config(
        client_config, scopes=["https://www.googleapis.com/auth/adwords"]
    )
    credentials = flow.run_local_server(port=0)

    profile["platforms"]["google"]["refresh_token"] = credentials.refresh_token
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)

    print(f"refresh_token guardado en {profile_path}")
    print("Pon google.enabled = true en profile.json y ejecuta el cliente.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Ads insights multi-cliente")
    parser.add_argument("client", nargs="?", help="Nombre del cliente (o 'setup <cliente>')")
    parser.add_argument("--all", action="store_true", help="Ejecutar para todos los clientes con Google habilitado")
    parser.add_argument("--range", default="LAST_30_DAYS", choices=DATE_RANGES, dest="date_range")
    parser.add_argument("--level", default="campaign", choices=["campaign", "adgroup"])
    parser.add_argument("--setup", metavar="CLIENTE", help="Generar refresh_token OAuth2 para un cliente")

    args = parser.parse_args()

    if args.setup:
        setup_oauth_flow(args.setup)
        sys.exit(0)

    if args.all:
        clients = list_google_clients()
        if not clients:
            print("No hay clientes con Google Ads habilitado. Crea un profile.json en ads/clients/<cliente>/")
            sys.exit(1)
        for name in clients:
            profile = load_profile(name)
            fn = get_adgroup_insights if args.level == "adgroup" else get_campaign_insights
            insights = fn(profile, args.date_range)
            print_report(name, insights, args.date_range)
        sys.exit(0)

    if not args.client:
        parser.print_help()
        clients = list_google_clients()
        if clients:
            print(f"\nClientes con Google habilitado: {', '.join(clients)}")
        sys.exit(1)

    profile = load_profile(args.client)
    fn = get_adgroup_insights if args.level == "adgroup" else get_campaign_insights
    insights = fn(profile, args.date_range)
    print_report(args.client, insights, args.date_range)
