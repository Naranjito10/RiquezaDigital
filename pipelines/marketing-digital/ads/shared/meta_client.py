"""
Cliente Meta Ads multi-cuenta.
Lee credenciales desde ads/clients/{client}/profile.json — nunca desde .env.
"""

import json
import os
from pathlib import Path

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount


BASE_DIR = Path(__file__).parent.parent  # ads/


def load_profile(client_name: str) -> dict:
    profile_path = BASE_DIR / "clients" / client_name / "profile.json"
    if not profile_path.exists():
        raise FileNotFoundError(f"No existe profile.json para '{client_name}': {profile_path}")
    with open(profile_path) as f:
        profile = json.load(f)
    meta = profile.get("platforms", {}).get("meta", {})
    if not meta.get("enabled"):
        raise ValueError(f"Meta Ads no está habilitado para '{client_name}'. Edita profile.json.")
    missing = [k for k in ("app_id", "app_secret", "access_token", "ad_account_id") if not meta.get(k)]
    if missing:
        raise ValueError(f"Faltan credenciales Meta en profile.json de '{client_name}': {missing}")
    if not meta["ad_account_id"].startswith("act_"):
        raise ValueError(f"ad_account_id debe empezar con 'act_'. Valor: {meta['ad_account_id']}")
    return profile


def init_meta_api(profile: dict) -> None:
    meta = profile["platforms"]["meta"]
    FacebookAdsApi.init(meta["app_id"], meta["app_secret"], meta["access_token"])


def get_ad_account(profile: dict) -> AdAccount:
    init_meta_api(profile)
    return AdAccount(profile["platforms"]["meta"]["ad_account_id"])


def get_account_insights(
    profile: dict,
    date_preset: str = "last_30d",
    level: str = "campaign",
) -> list[dict]:
    account = get_ad_account(profile)
    fields = [
        "campaign_name", "adset_name", "impressions", "reach",
        "clicks", "spend", "cpc", "cpm", "ctr",
        "actions", "cost_per_action_type",
    ]
    params = {"date_preset": date_preset, "level": level, "fields": ",".join(fields)}
    raw = account.get_insights(params=params)
    return [dict(row) for row in raw]


if __name__ == "__main__":
    import sys
    client = sys.argv[1] if len(sys.argv) > 1 else "veganashi"
    profile = load_profile(client)
    print(f"Conexión OK para {profile['client']} — cuenta {profile['platforms']['meta']['ad_account_id']}")
    insights = get_account_insights(profile)
    print(f"{len(insights)} registros obtenidos.")
