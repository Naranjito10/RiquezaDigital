"""
Crea un Ad Set en Meta Ads en estado PAUSED.
Uso: python src/create_adset.py
"""

from utils.api_client import get_ad_account
from utils.validators import validate_budget, validate_status, validate_date
from utils.safety import confirm_write
from utils.logger import log_write, log_error
from facebook_business.adobjects.adset import AdSet


def create_adset(
    campaign_id: str,
    name: str,
    daily_budget_cents: int,
    optimization_goal: str,
    targeting: dict,
    start_time: str,
    end_time: str = None,
    bid_amount_cents: int = None,
) -> dict:
    """
    Crea un Ad Set en PAUSED.

    Args:
        campaign_id: ID de la campaña padre
        name: Nombre descriptivo del ad set
        daily_budget_cents: Presupuesto diario en centavos
        optimization_goal: LINK_CLICKS, IMPRESSIONS, REACH, LEAD_GENERATION, etc.
        targeting: Dict con geo_locations, age_min, age_max, interests, etc.
        start_time: ISO 8601 ej: "2025-01-01T00:00:00+0000"
        end_time: ISO 8601 (opcional)
        bid_amount_cents: Monto de puja en centavos (opcional, default: lowest cost)

    Returns:
        dict con adset_id y nombre
    """
    validate_budget(daily_budget_cents, "daily_budget")
    validate_status("PAUSED")
    validate_date(start_time, "start_time")
    if end_time:
        validate_date(end_time, "end_time")

    if "geo_locations" not in targeting:
        raise ValueError("targeting debe incluir geo_locations (ej: {'countries': ['US']})")

    params = {
        "campaign_id": campaign_id,
        "name": name,
        "daily_budget": daily_budget_cents,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": optimization_goal,
        "targeting": targeting,
        "start_time": start_time,
        "status": "PAUSED",
    }
    if end_time:
        params["end_time"] = end_time
    if bid_amount_cents:
        params["bid_amount"] = bid_amount_cents

    geo = targeting.get("geo_locations", {})
    summary = {
        "Campaña ID": campaign_id,
        "Nombre Ad Set": name,
        "Presupuesto diario": f"${daily_budget_cents / 100:.2f} USD",
        "Objetivo de optimización": optimization_goal,
        "Países/Geo": geo,
        "Edad": f"{targeting.get('age_min', 18)}-{targeting.get('age_max', 65)}",
        "Start time": start_time,
        "Status": "PAUSED",
    }

    if not confirm_write("CREAR AD SET", summary):
        return {"status": "cancelled"}

    try:
        account = get_ad_account()
        adset = account.create_ad_set(
            fields=[AdSet.Field.id, AdSet.Field.name],
            params=params,
        )
        result = {"adset_id": adset["id"], "name": adset["name"], "status": "PAUSED"}
        log_write("create_adset", params, result)
        print(f"\n[OK] Ad Set creado: ID {adset['id']}")
        return result
    except Exception as e:
        log_error("create_adset", params, str(e))
        print(f"\n[ERROR] No se pudo crear el Ad Set: {e}")
        raise
