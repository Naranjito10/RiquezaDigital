import json
import os
from pathlib import Path
from datetime import datetime

class SessionLogger:
    """
    Registra eventos estructurados de ejecución agéntica en un archivo JSON append-only.
    Permite auditar el comportamiento de los agentes y recuperar el estado si ocurre un fallo.
    """
    def __init__(self, session_id=None):
        # El workspace root es 3 niveles arriba de pipelines/shared/agentic_harness/session_logger.py
        self.workspace_root = Path(__file__).resolve().parents[3]
        if not session_id:
            session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_id = session_id
        self.log_file = self.workspace_root / "output" / "sessions" / f"session_{self.session_id}.json"
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Inicializar archivo si no existe
        if not self.log_file.exists():
            self.write_raw([])

    def write_raw(self, data):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def log_event(self, event_type: str, details: dict):
        """Añade un evento al archivo JSON de log."""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "details": details
        }
        
        # Leer existentes de forma segura
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                events = json.load(f)
        except (json.JSONDecodeError, IOError):
            events = []
            
        events.append(event)
        self.write_raw(events)
        return event

    def load_events(self) -> list:
        """Carga y retorna todos los eventos de la sesión."""
        if not self.log_file.exists():
            return []
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []

    def get_summary(self) -> dict:
        """Retorna un resumen de la sesión actual."""
        events = self.load_events()
        summary = {
            "session_id": self.session_id,
            "total_events": len(events),
            "errors": 0,
            "start_time": None,
            "end_time": None
        }
        if events:
            summary["start_time"] = events[0]["timestamp"]
            summary["end_time"] = events[-1]["timestamp"]
            summary["errors"] = sum(1 for e in events if e["event_type"] == "error")
        return summary
