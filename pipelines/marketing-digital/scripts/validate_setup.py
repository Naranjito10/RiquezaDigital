"""
Script de diagnóstico: valida que el setup esté completo antes de operar.
Uso: python scripts/validate_setup.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = [
    "META_APP_ID",
    "META_APP_SECRET",
    "META_ACCESS_TOKEN",
    "META_AD_ACCOUNT_ID",
    "META_PAGE_ID",
]

print("\n=== DIAGNÓSTICO DE SETUP META ADS ===\n")

all_ok = True

# 1. Variables de entorno
print("1. Variables de entorno:")
for var in REQUIRED_VARS:
    value = os.getenv(var)
    if value and not value.startswith("PEGA_TU") and not value.startswith("your_"):
        print(f"   [OK] {var}")
    else:
        print(f"   [FALTA] {var} — edita tu archivo .env")
        all_ok = False

# 2. Formato de Ad Account ID
account_id = os.getenv("META_AD_ACCOUNT_ID", "")
if account_id and not account_id.startswith("act_"):
    print(f"\n   [ERROR] META_AD_ACCOUNT_ID debe empezar con 'act_'. Actual: {account_id}")
    all_ok = False

# 3. SDK instalado
print("\n2. Dependencias Python:")
try:
    import facebook_business
    print(f"   [OK] facebook-business instalado")
except ImportError:
    print(f"   [FALTA] Ejecuta: pip install -r requirements.txt")
    all_ok = False

try:
    import dotenv
    print(f"   [OK] python-dotenv instalado")
except ImportError:
    print(f"   [FALTA] Ejecuta: pip install python-dotenv")
    all_ok = False

# 4. Conexión a API
print("\n3. Conexión a Meta API:")
if all_ok:
    try:
        from utils.api_client import get_ad_account
        account = get_ad_account()
        info = account.api_get(fields=["name", "currency", "account_status"])
        print(f"   [OK] Cuenta conectada: {info.get('name')} | {info.get('currency')}")
        status_map = {1: "ACTIVE", 2: "DISABLED", 3: "UNSETTLED", 7: "PENDING_REVIEW", 9: "IN_GRACE_PERIOD", 100: "PENDING_CLOSURE", 101: "CLOSED", 201: "ANY_ACTIVE", 202: "ANY_CLOSED"}
        account_status = status_map.get(info.get("account_status"), "UNKNOWN")
        print(f"   Status cuenta: {account_status}")
    except Exception as e:
        print(f"   [ERROR] No se pudo conectar: {e}")
        all_ok = False
else:
    print("   [SKIP] Corrige las variables de entorno primero")

# Resultado final
print("\n" + "=" * 40)
if all_ok:
    print("RESULTADO: Setup completo. Listo para operar.")
else:
    print("RESULTADO: Hay items pendientes. Revisa los [FALTA] arriba.")
print("=" * 40 + "\n")
