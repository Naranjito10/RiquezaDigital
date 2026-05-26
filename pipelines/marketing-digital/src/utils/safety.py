"""
Capa de seguridad: confirmaciones humanas antes de writes costosos.
"""


def confirm_write(action: str, summary: dict) -> bool:
    """
    Muestra resumen de la operación y pide confirmación explícita.
    Retorna True si el usuario confirma, False si cancela.
    """
    print("\n" + "=" * 60)
    print(f"OPERACION DE ESCRITURA: {action}")
    print("=" * 60)
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print("=" * 60)
    print("IMPORTANTE: Esta operacion modificara tu cuenta de Meta Ads.")
    response = input("Confirmar? (escribe 'si' para continuar): ").strip().lower()
    if response == "si":
        print("[OK] Operacion confirmada.\n")
        return True
    print("[CANCELADO] Operacion cancelada por el usuario.\n")
    return False


def confirm_budget_increase(current_budget: int, new_budget: int) -> bool:
    """Confirmacion especial para aumentos de presupuesto."""
    increase_pct = ((new_budget - current_budget) / current_budget) * 100
    print(f"\n[ALERTA DE PRESUPUESTO]")
    print(f"  Presupuesto actual: ${current_budget / 100:.2f} USD")
    print(f"  Presupuesto nuevo:  ${new_budget / 100:.2f} USD")
    print(f"  Incremento:         {increase_pct:.1f}%")
    if increase_pct > 20:
        print(f"  ADVERTENCIA: Incrementos >20% reinician la fase de aprendizaje.")
    response = input("Confirmar cambio de presupuesto? (escribe 'si' para continuar): ").strip().lower()
    return response == "si"
