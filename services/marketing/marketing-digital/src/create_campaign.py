"""
Crea una campaña en Meta Ads en estado PAUSED.
Uso: python src/create_campaign.py
"""

from utils.api_client import get_ad_account
from utils.validators import validate_budget, validate_objective, validate_status
from utils.safety import confirm_write
from utils.logger import log_write, log_error
from facebook_business.adobjects.campaign import Campaign


def create_campaign(
    name: str,
    objective: str,
    daily_budget_cents: int = None,
    spend_cap_cents: int = None,
    special_ad_categories: list = None,
) -> dict:
    """
    Crea una campaña en PAUSED.

    Args:
        name: Nombre descriptivo de la campaña
        objective: Ej: OUTCOME_TRAFFIC, OUTCOME_LEADS
        daily_budget_cents: Presupuesto diario en centavos (ej: 5000 = $50)
        spend_cap_cents: Límite de gasto total en centavos
        special_ad_categories: Lista de categorías especiales si aplica

    Returns:
        dict con campaign_id y nombre
    """
    # Validaciones
    validate_objective(objective)
    validate_status("PAUSED")
    if daily_budget_cents:
        validate_budget(daily_budget_cents, "daily_budget")
    if spend_cap_cents:
        validate_budget(spend_cap_cents, "spend_cap")

    params = {
        "name": name,
        "objective": objective,
        "status": "PAUSED",
        "special_ad_categories": special_ad_categories or [],
    }
    if daily_budget_cents:
        params["daily_budget"] = daily_budget_cents
    if spend_cap_cents:
        params["spend_cap"] = spend_cap_cents

    # Confirmación humana
    summary = {
        "Nombre": name,
        "Objetivo": objective,
        "Status": "PAUSED",
        "Presupuesto diario": f"${daily_budget_cents / 100:.2f} USD" if daily_budget_cents else "No definido",
        "Spend cap": f"${spend_cap_cents / 100:.2f} USD" if spend_cap_cents else "No definido",
        "Special Ad Categories": special_ad_categories or "Ninguna",
    }

    if not confirm_write("CREAR CAMPAÑA", summary):
        return {"status": "cancelled"}

    # Ejecución
    try:
        account = get_ad_account()
        campaign = account.create_campaign(fields=[Campaign.Field.id, Campaign.Field.name], params=params)
        result = {"campaign_id": campaign["id"], "name": campaign["name"], "status": "PAUSED"}
        log_write("create_campaign", params, result)
        print(f"\n[OK] Campaña creada: ID {campaign['id']}")
        return result
    except Exception as e:
        log_error("create_campaign", params, str(e))
        print(f"\n[ERROR] No se pudo crear la campaña: {e}")
        raise


if __name__ == "__main__":
    create_campaign(
        name="Test Campaign - PAUSED",
        objective="OUTCOME_TRAFFIC",
        daily_budget_cents=1000,  # $10.00 USD
    )
