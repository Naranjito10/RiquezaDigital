"""
Crea un Ad Creative y un Ad en Meta Ads en estado PAUSED.
Uso: python src/create_ad.py
"""

from utils.api_client import get_ad_account, get_page_id
from utils.validators import validate_status
from utils.safety import confirm_write
from utils.logger import log_write, log_error
from facebook_business.adobjects.adcreative import AdCreative
from facebook_business.adobjects.ad import Ad


def create_ad_creative(
    name: str,
    link: str,
    message: str,
    headline: str,
    description: str,
    image_hash: str,
    call_to_action: str = "LEARN_MORE",
) -> str:
    """
    Crea un Ad Creative y retorna su ID.

    Args:
        name: Nombre del creative
        link: URL de destino
        message: Texto principal (hook en primeros 125 chars)
        headline: Titular (máx 40 chars, 27 visible en mobile)
        description: Descripción corta (25-30 chars)
        image_hash: Hash de imagen subida previamente
        call_to_action: LEARN_MORE, SHOP_NOW, SIGN_UP, etc.

    Returns:
        creative_id (string)
    """
    if len(headline) > 40:
        print(f"[ADVERTENCIA] Titular tiene {len(headline)} chars. Máximo recomendado: 40.")

    page_id = get_page_id()
    params = {
        "name": name,
        "object_story_spec": {
            "page_id": page_id,
            "link_data": {
                "link": link,
                "message": message,
                "name": headline,
                "description": description,
                "image_hash": image_hash,
                "call_to_action": {"type": call_to_action},
            },
        },
    }

    summary = {
        "Nombre Creative": name,
        "Link destino": link,
        "Texto principal": message[:80] + "..." if len(message) > 80 else message,
        "Titular": headline,
        "CTA": call_to_action,
    }

    if not confirm_write("CREAR AD CREATIVE", summary):
        return None

    try:
        account = get_ad_account()
        creative = account.create_ad_creative(
            fields=[AdCreative.Field.id],
            params=params,
        )
        log_write("create_ad_creative", params, {"creative_id": creative["id"]})
        print(f"\n[OK] Creative creado: ID {creative['id']}")
        return creative["id"]
    except Exception as e:
        log_error("create_ad_creative", params, str(e))
        print(f"\n[ERROR] No se pudo crear el Creative: {e}")
        raise


def create_ad(adset_id: str, creative_id: str, name: str) -> dict:
    """
    Crea un Ad en PAUSED referenciando un creative y ad set existentes.

    Returns:
        dict con ad_id y nombre
    """
    validate_status("PAUSED")

    params = {
        "name": name,
        "adset_id": adset_id,
        "creative": {"creative_id": creative_id},
        "status": "PAUSED",
    }

    summary = {
        "Nombre Ad": name,
        "Ad Set ID": adset_id,
        "Creative ID": creative_id,
        "Status": "PAUSED",
    }

    if not confirm_write("CREAR AD", summary):
        return {"status": "cancelled"}

    try:
        account = get_ad_account()
        ad = account.create_ad(
            fields=[Ad.Field.id, Ad.Field.name],
            params=params,
        )
        result = {"ad_id": ad["id"], "name": ad["name"], "status": "PAUSED"}
        log_write("create_ad", params, result)
        print(f"\n[OK] Ad creado: ID {ad['id']}")
        return result
    except Exception as e:
        log_error("create_ad", params, str(e))
        print(f"\n[ERROR] No se pudo crear el Ad: {e}")
        raise
