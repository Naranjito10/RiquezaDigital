"""
Agente 2: Daily Briefing
Consolida las alertas del Campaign Monitor, las tareas de Notion y las sesiones activas,
y genera un reporte resumido diario recomendando el foco de la jornada para el CEO.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Asegurar importaciones correctas
sys.stdout.reconfigure(encoding='utf-8')
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / "pipelines" / "marketing-digital"))

from agents.context_validator import check_notion_tasks, check_open_sessions
from agents.campaign_optimizer import load_active_alerts

def calculate_recommended_focus(alerts_count: int, tasks: list) -> str:
    """Calcula dinámicamente la sugerencia de foco diaria."""
    system_tasks = 0
    execute_tasks = 0
    
    for t in tasks:
        if "error" in t:
            continue
        title = t.get("title", "").lower()
        # Clasificar según palabras clave
        if any(w in title for w in ["mejora", "desarrollo", "setup", "vps", "automatizacion", "script"]):
            system_tasks += 1
        else:
            execute_tasks += 1
            
    if alerts_count > 0 or execute_tasks > 3:
        return "EJECUTAR (Foco en optimizar campañas y resolver bloqueos de clientes)"
    elif system_tasks > 2:
        return "SISTEMA (Foco en desarrollo de infraestructura, automatización y mejoras web)"
    else:
        return "VENDER (Foco en prospección, estrategias comerciales y outbound)"

def generate_daily_briefing() -> str:
    """Ejecuta el briefing consolidado."""
    print("--- [DAILY BRIEFING] Generando resumen ejecutivo diario ---")
    
    # 1. Cargar alertas
    alerts = load_active_alerts()
    critical_alerts = [a for a in alerts if a.get("severity") == "CRITICAL"]
    warning_alerts = [a for a in alerts if a.get("severity") == "WARNING"]
    
    # 2. Cargar tareas de Notion
    tasks = check_notion_tasks()
    valid_tasks = [t for t in tasks if "error" not in t]
    
    # 3. Cargar sesiones abiertas
    sessions = check_open_sessions()
    
    # 4. Calcular foco recomendado
    focus = calculate_recommended_focus(len(alerts), tasks)
    
    # 5. Estructurar Briefing de 5 líneas para el canal CEO
    brief_lines = [
        f"📅 *Briefing del Día — {datetime.now().strftime('%d/%m/%Y')}*",
        f"🎯 *Foco Sugerido:* {focus}",
        f"🚨 *Campañas:* {len(critical_alerts)} alertas críticas, {len(warning_alerts)} advertencias activas.",
        f"📌 *Notion Tareas:* {len(valid_tasks)} tareas pendientes para hoy/atrasadas.",
        f"💬 *Sesiones:* {'⚠️ Sesión abierta detectada' if sessions else '✅ Sesiones limpias y cerradas.'}"
    ]
    
    brief_text = "\n".join(brief_lines)
    
    # Mostrar por consola
    print("\n" + "="*50)
    print("DAILY BRIEFING - MENSAJE TELEGRAM (CEO)")
    print("="*50)
    print(brief_text)
    print("="*50 + "\n")
    
    # Guardar en output/agency/daily_brief.md
    output_dir = WORKSPACE_ROOT / "output" / "agency"
    output_dir.mkdir(parents=True, exist_ok=True)
    brief_file = output_dir / "daily_brief.md"
    
    try:
        with open(brief_file, "w", encoding="utf-8") as f:
            f.write(brief_text)
        print(f"[OK] Briefing diario guardado en {brief_file}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar daily_brief.md: {e}")
        
    return brief_text

if __name__ == "__main__":
    generate_daily_briefing()
