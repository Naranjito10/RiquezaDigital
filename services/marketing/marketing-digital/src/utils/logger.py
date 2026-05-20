"""
Logger de auditoría para todas las operaciones de escritura.
Registra en logs/api_actions.log con timestamp, acción, params y resultado.
"""

import json
import logging
import os
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "logs", "api_actions.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def log_write(action: str, params: dict, result: dict | str):
    """Registra una operación de escritura en el log de auditoría."""
    entry = {
        "action": action,
        "params": params,
        "result": result,
    }
    logging.info(json.dumps(entry, ensure_ascii=False))
    print(f"[LOG] {action} registrado en {LOG_PATH}")


def log_error(action: str, params: dict, error: str):
    """Registra un error en el log de auditoría."""
    entry = {
        "action": action,
        "params": params,
        "error": error,
    }
    logging.error(json.dumps(entry, ensure_ascii=False))
    print(f"[ERROR] {action} fallido — ver {LOG_PATH}")
