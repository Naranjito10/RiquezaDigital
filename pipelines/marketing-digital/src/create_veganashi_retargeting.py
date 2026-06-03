"""
Crea la campaña de retargeting y su respectivo Ad Set en Meta Ads para Veganashi en estado PAUSED.
Usa la estrategia de puja LOWEST_COST_WITHOUT_CAP para evitar límites de puja (bid_amount) obligatorios.
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from dotenv import load_dotenv

# Asegurar importaciones
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / "pipelines" / "marketing-digital"))

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from utils.logger import log_write, log_error

load_dotenv(WORKSPACE_ROOT / ".env")

def init_meta_api():
    app_id = os.getenv("META_APP_ID")
    app_secret = os.getenv("META_APP_SECRET")
    access_token = os.getenv("META_ACCESS_TOKEN")
    
    if not all([app_id, app_secret, access_token]):
        raise ValueError("Faltan credenciales de Meta Ads en .env.")
        
    FacebookAdsApi.init(app_id, app_secret, access_token)
    return FacebookAdsApi.get_default_api()

def create_veganashi_retargeting():
    # ID de cuenta de anuncios de Veganashi
    ad_account_id = "act_928041200992402"
    
    print(f"--- [API META] Iniciando creacion de campaña de Retargeting para Veganashi ---")
    print(f"Cuenta de destino: {ad_account_id}")
    
    init_meta_api()
    account = AdAccount(ad_account_id)
    
    # 1. Crear Campaña con Presupuesto Advantage+ (CBO) y estrategia de menor coste
    campaign_name = "RE_Leads_Retargeting_V2"
    campaign_params = {
        "name": campaign_name,
        "objective": "OUTCOME_LEADS",
        "status": "PAUSED",
        "daily_budget": 500, # 5.00 EUR diarios en centavos
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP", # Forzar menor costo sin límite
        "special_ad_categories": []
    }
    
    try:
        print(f"\n[1/2] Creando Campana '{campaign_name}'...")
        campaign = account.create_campaign(
            fields=[Campaign.Field.id, Campaign.Field.name],
            params=campaign_params
        )
        campaign_id = campaign["id"]
        print(f"[OK] Campana creada: ID {campaign_id}")
        log_write("create_campaign_veganashi", campaign_params, dict(campaign))
    except Exception as e:
        print(f"[ERROR] Error al crear la campana: {e}")
        log_error("create_campaign_veganashi", campaign_params, str(e))
        return
        
    # 2. Crear Ad Set
    adset_name = "RE_Leads_WarmAudience_30d"
    start_time = (datetime.now() + timedelta(hours=2)).strftime("%Y-%m-%dT%H:%M:%S+0200")
    
    targeting = {
        "geo_locations": {
            "countries": ["ES"]
        },
        "age_min": 18,
        "age_max": 65
    }
    
    adset_params = {
        "campaign_id": campaign_id,
        "name": adset_name,
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "LEAD_GENERATION",
        "targeting": targeting,
        "start_time": start_time,
        "status": "PAUSED",
    }
    
    try:
        print(f"\n[2/2] Creando Ad Set '{adset_name}'...")
        adset = account.create_ad_set(
            fields=[AdSet.Field.id, AdSet.Field.name],
            params=adset_params
        )
        adset_id = adset["id"]
        print(f"[OK] Ad Set creado: ID {adset_id}")
        log_write("create_adset_veganashi", adset_params, dict(adset))
        
        print("\n==================================================")
        print("RESUMEN DE LA CREACION")
        print(f"Campana ID: {campaign_id} (PAUSED)")
        print(f"Ad Set ID:   {adset_id} (PAUSED)")
        print("==================================================")
        print("Proximo paso: Sube los creativos/anuncios a este Ad Set desde el Administrador de Anuncios.")
        
    except Exception as e:
        print(f"[ERROR] Error al crear el Ad Set: {e}")
        log_error("create_adset_veganashi", adset_params, str(e))
        
if __name__ == "__main__":
    create_veganashi_retargeting()
