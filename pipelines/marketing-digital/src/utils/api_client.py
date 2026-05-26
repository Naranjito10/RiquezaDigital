"""
Cliente base para Meta Marketing API.
Lee credenciales desde .env — nunca hardcodear tokens.
"""

import os
from dotenv import load_dotenv
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

load_dotenv()


def init_api():
    """Inicializa la conexión con Meta Marketing API."""
    app_id = os.getenv("META_APP_ID")
    app_secret = os.getenv("META_APP_SECRET")
    access_token = os.getenv("META_ACCESS_TOKEN")

    if not all([app_id, app_secret, access_token]):
        raise ValueError(
            "Faltan credenciales en .env: META_APP_ID, META_APP_SECRET, META_ACCESS_TOKEN"
        )

    FacebookAdsApi.init(app_id, app_secret, access_token)
    return FacebookAdsApi.get_default_api()


def get_ad_account(account_id=None):
    """Retorna el objeto AdAccount configurado en .env o el pasado por parámetro."""
    if not account_id:
        account_id = os.getenv("META_AD_ACCOUNT_ID")
    if not account_id:
        raise ValueError("Falta el Ad Account ID en .env o parámetro")
    if not account_id.startswith("act_"):
        raise ValueError(f"El Ad Account ID debe empezar con 'act_'. Valor actual: {account_id}")
    init_api()
    return AdAccount(account_id)



def get_page_id():
    """Retorna el Page ID configurado en .env."""
    page_id = os.getenv("META_PAGE_ID")
    if not page_id:
        raise ValueError("Falta META_PAGE_ID en .env")
    return page_id
