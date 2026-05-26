import json
import os
from pathlib import Path

class BudgetManager:
    """
    Gestiona el presupuesto y consumo de API en ejecuciones agénticas de Riqueza Digital.
    """
    def __init__(self, limit_file_path=None, run_budget_limit=15.0, daily_budget_limit=50.0):
        self.workspace_root = Path(__file__).resolve().parents[3]
        self.tracking_file = self.workspace_root / "output" / "agency" / "api_budget.json"
        self.tracking_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.run_budget_limit = run_budget_limit
        self.daily_budget_limit = daily_budget_limit
        
        self.load_data()

    def load_data(self):
        if self.tracking_file.exists():
            try:
                with open(self.tracking_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.data = {"daily_spent": 0.0, "current_run_spent": 0.0, "last_reset_date": ""}
        else:
            self.data = {"daily_spent": 0.0, "current_run_spent": 0.0, "last_reset_date": ""}

    def save_data(self):
        with open(self.tracking_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4)

    def reset_run(self):
        """Reinicia el contador de la ejecución actual."""
        self.data["current_run_spent"] = 0.0
        self.save_data()

    def add_cost(self, cost: float):
        """Añade coste en USD a los contadores y valida límites."""
        self.data["daily_spent"] += cost
        self.data["current_run_spent"] += cost
        self.save_data()
        
        # Validar límites
        if self.data["current_run_spent"] > self.run_budget_limit:
            raise PermissionError(
                f"🚨 Presupuesto excedido: La ejecución actual ha consumido ${self.data['current_run_spent']:.2f} USD "
                f"(Límite: ${self.run_budget_limit:.2f} USD). Deteniendo ejecución por seguridad."
            )
            
        if self.data["daily_spent"] > self.daily_budget_limit:
            raise PermissionError(
                f"🚨 Presupuesto excedido: El gasto diario acumulado es de ${self.data['daily_spent']:.2f} USD "
                f"(Límite: ${self.daily_budget_limit:.2f} USD). Deteniendo ejecución por seguridad."
            )

    def get_status(self):
        return {
            "daily_spent": self.data["daily_spent"],
            "daily_limit": self.daily_budget_limit,
            "run_spent": self.data["current_run_spent"],
            "run_limit": self.run_budget_limit
        }
