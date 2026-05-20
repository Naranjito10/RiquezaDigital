"""
Validaciones de parámetros antes de llamar a la API.
Previene errores comunes y gastos accidentales.
"""

from datetime import datetime


def validate_budget(budget_cents: int, label: str = "budget") -> None:
    """Valida que el presupuesto sea entero positivo en centavos."""
    if not isinstance(budget_cents, int) or budget_cents <= 0:
        raise ValueError(f"{label} debe ser un entero positivo en centavos. Recibido: {budget_cents}")
    if budget_cents > 10_000_00:  # $10,000 USD como límite de alerta
        raise ValueError(
            f"{label} de ${budget_cents / 100:.2f} USD parece excesivo. "
            "Confirma que el valor es correcto."
        )


def validate_ad_account_id(account_id: str) -> None:
    """Valida formato act_XXXXXXXXX."""
    if not account_id or not account_id.startswith("act_"):
        raise ValueError(f"Ad Account ID debe empezar con 'act_'. Recibido: {account_id}")
    numeric_part = account_id[4:]
    if not numeric_part.isdigit():
        raise ValueError(f"Ad Account ID tiene formato inválido: {account_id}")


def validate_date(date_str: str, label: str = "date") -> None:
    """Valida formato ISO 8601 (YYYY-MM-DDTHH:MM:SS+0000)."""
    formats = ["%Y-%m-%dT%H:%M:%S+0000", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d"]
    for fmt in formats:
        try:
            datetime.strptime(date_str, fmt)
            return
        except ValueError:
            continue
    raise ValueError(f"{label} debe estar en formato ISO 8601. Recibido: {date_str}")


def validate_status(status: str) -> None:
    """Valida que el status sea PAUSED (requerido en creación)."""
    allowed = {"PAUSED", "ACTIVE", "DELETED", "ARCHIVED"}
    if status not in allowed:
        raise ValueError(f"Status inválido: {status}. Opciones: {allowed}")
    if status == "ACTIVE":
        raise ValueError(
            "No puedes crear objetos en ACTIVE. Crea siempre en PAUSED "
            "y activa manualmente después de revisar."
        )


def validate_objective(objective: str) -> None:
    """Valida que el objetivo de campaña sea válido."""
    valid_objectives = {
        "OUTCOME_AWARENESS",
        "OUTCOME_TRAFFIC",
        "OUTCOME_ENGAGEMENT",
        "OUTCOME_LEADS",
        "OUTCOME_APP_PROMOTION",
        "OUTCOME_SALES",
    }
    if objective not in valid_objectives:
        raise ValueError(f"Objetivo inválido: {objective}. Opciones: {valid_objectives}")
