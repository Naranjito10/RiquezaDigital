"""
Cliente Google Ads multi-cuenta.
Usa OAuth2 con refresh_token almacenado en profile.json.

Setup inicial por cliente (una sola vez):
    python ads/shared/google_client.py setup tecniclima
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent  # ads/


def load_profile(client_name: str) -> dict:
    profile_path = BASE_DIR / "clients" / client_name / "profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"No existe profile.json para '{client_name}'")
    with open(profile_path) as f:
        return json.load(f)


def init_google_client(profile: dict):
    """Inicializa el cliente Google Ads con credenciales OAuth2 del profile."""
    try:
        from google.ads.googleads.client import GoogleAdsClient
    except ImportError:
        raise ImportError("Instala el SDK: pip install google-ads")

    google = profile["platforms"]["google"]
    if not google.get("enabled"):
        raise ValueError(f"Google Ads no está habilitado para '{profile['client']}'")

    config = {
        "developer_token": google["developer_token"],
        "client_id": google["client_id"],
        "client_secret": google["client_secret"],
        "refresh_token": google["refresh_token"],
        "login_customer_id": google["customer_id"],
        "use_proto_plus": True,
    }
    return GoogleAdsClient.load_from_dict(config)


def get_campaigns_overview(profile: dict) -> list[dict]:
    """Retorna lista de campañas con estado y presupuesto."""
    client = init_google_client(profile)
    customer_id = profile["platforms"]["google"]["customer_id"].replace("-", "")
    ga_service = client.get_service("GoogleAdsService")
    query = """
        SELECT
          campaign.id,
          campaign.name,
          campaign.status,
          campaign_budget.amount_micros,
          metrics.impressions,
          metrics.clicks,
          metrics.cost_micros
        FROM campaign
        WHERE segments.date DURING LAST_30_DAYS
        ORDER BY metrics.cost_micros DESC
    """
    response = ga_service.search(customer_id=customer_id, query=query)
    results = []
    for row in response:
        results.append({
            "id": row.campaign.id,
            "name": row.campaign.name,
            "status": row.campaign.status.name,
            "budget_eur": row.campaign_budget.amount_micros / 1_000_000,
            "impressions": row.metrics.impressions,
            "clicks": row.metrics.clicks,
            "spend_eur": row.metrics.cost_micros / 1_000_000,
        })
    return results


def setup_oauth_flow(client_name: str) -> None:
    """
    Genera refresh_token para un cliente via OAuth2 interactivo.
    Ejecutar una sola vez por cliente. Guarda el token en profile.json.
    """
    try:
        from google_auth_oauthlib.flow import InstalledAppFlow
    except ImportError:
        raise ImportError("Instala: pip install google-auth-oauthlib")

    profile_path = BASE_DIR / "clients" / client_name / "profile.json"
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
    scopes = ["https://www.googleapis.com/auth/adwords"]
    flow = InstalledAppFlow.from_client_config(client_config, scopes=scopes)
    credentials = flow.run_local_server(port=0)

    profile["platforms"]["google"]["refresh_token"] = credentials.refresh_token
    with open(profile_path, "w") as f:
        json.dump(profile, f, indent=2)

    print(f"refresh_token guardado en {profile_path}")
    print("Ahora pon google.enabled = true en el profile.json y ejecuta el cliente.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python google_client.py <client> | setup <client>")
        sys.exit(1)

    if sys.argv[1] == "setup" and len(sys.argv) == 3:
        setup_oauth_flow(sys.argv[2])
    else:
        profile = load_profile(sys.argv[1])
        campaigns = get_campaigns_overview(profile)
        print(f"{len(campaigns)} campañas para {profile['client']}:")
        for c in campaigns:
            print(f"  [{c['status']}] {c['name']} — €{c['spend_eur']:.2f}")
