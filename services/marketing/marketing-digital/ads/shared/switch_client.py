"""
Carga el profile.json de un cliente en ~/.claude-ads/profile.json
para que el plugin Claude Ads apunte a esa cuenta.

Uso:
    python ads/shared/switch_client.py veganashi
    python ads/shared/switch_client.py tecniclima
    python ads/shared/switch_client.py riqueza-digital
"""

import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent  # ads/
CLAUDE_ADS_PROFILE = Path.home() / ".claude-ads" / "profile.json"

# Mapeo de campos entre nuestro profile.json y el formato del plugin
def _build_plugin_profile(profile: dict) -> dict:
    client = profile["client"]
    meta = profile["platforms"].get("meta", {})
    google = profile["platforms"].get("google", {})

    plugin_profile = {
        "client": client,
        "industry": profile.get("industry", ""),
        "monthly_spend": profile.get("monthly_spend_eur", 0),
        "platforms": {
            "meta": {
                "enabled": meta.get("enabled", False),
                "access_token": meta.get("access_token", ""),
                "ad_account_id": meta.get("ad_account_id", ""),
                "app_id": meta.get("app_id", ""),
                "app_secret": meta.get("app_secret", ""),
            },
            "google": {
                "enabled": google.get("enabled", False),
                "developer_token": google.get("developer_token", ""),
                "client_id": google.get("client_id", ""),
                "client_secret": google.get("client_secret", ""),
                "refresh_token": google.get("refresh_token", ""),
                "customer_id": google.get("customer_id", ""),
            },
            "tiktok": {
                "enabled": profile["platforms"].get("tiktok", {}).get("enabled", False),
            },
        },
    }
    return plugin_profile


def switch_to(client_name: str) -> None:
    profile_path = BASE_DIR / "clients" / client_name / "profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"No existe ads/clients/{client_name}/profile.json")

    with open(profile_path) as f:
        profile = json.load(f)

    CLAUDE_ADS_PROFILE.parent.mkdir(parents=True, exist_ok=True)
    plugin_profile = _build_plugin_profile(profile)

    with open(CLAUDE_ADS_PROFILE, "w") as f:
        json.dump(plugin_profile, f, indent=2)

    active_platforms = [
        p for p, cfg in profile["platforms"].items()
        if isinstance(cfg, dict) and cfg.get("enabled")
    ]
    print(f"Cliente activo: {client_name}")
    print(f"Plataformas habilitadas: {', '.join(active_platforms) or 'ninguna'}")
    print(f"Profile cargado en: {CLAUDE_ADS_PROFILE}")
    print("\nPróximos pasos:")
    print("  /ads start  — (primera vez) onboarding wizard")
    print("  /ads audit  — auditoría completa")
    print("  /ads meta   — solo Meta Ads (50 checks)")
    print("  /ads google — solo Google Ads (80 checks)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        clients = sorted(p.parent.name for p in BASE_DIR.glob("clients/*/profile.json"))
        print(f"Uso: python switch_client.py <cliente>")
        print(f"Clientes disponibles: {', '.join(clients)}")
        sys.exit(1)

    switch_to(sys.argv[1])
