"""
Agente 5: Knowledge Updater
Busca y evalúa actualizaciones de algoritmos, APIs o mejores prácticas en Ads,
comparándolas con los SOPs locales y proponiendo cambios estables en shared/sops/.
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

def check_sops_outdated() -> list:
    """Escanea los SOPs locales y simula la búsqueda de mejores prácticas de la industria en 2026."""
    sops_dir = WORKSPACE_ROOT / "shared" / "sops"
    updates = []
    
    if not sops_dir.exists():
        print(f"[WARN] Directorio de SOPs no encontrado: {sops_dir}")
        return updates
        
    print(f"[KNOWLEDGE UPDATER] Analizando SOPs en {sops_dir}...")
    
    # Simulación de inteligencia competitiva o cambio de APIs reales de Meta Ads v25.0
    # En un escenario real, esto usaría scrapers, feeds RSS, o llamadas a un LLM web.
    industry_updates_2026 = [
        {
            "topic": "Meta Ads API v25.0 Bidding",
            "context": "Meta ha consolidado las estrategias de puja Advantage+ obligando a usar 'Outcome' unificado.",
            "impact_est": 0.18, # 18% de mejora estimada en conversión
            "affected_sop": "wordpress-rest-api-claude.md", # O el SOP de ads correspondiente si existiese
            "proposed_change": "Actualizar el SOP de creación de campañas para forzar 'outcome_type' a 'OUTCOME_LEADS' o 'OUTCOME_SALES' y evitar pujas manuales obsoletas."
        },
        {
            "topic": "Google Ads API Developer Token Policies",
            "context": "Nuevas reglas de Google exigen que los tokens de desarrollo cuenten con auditoría anual de seguridad de datos (2026).",
            "impact_est": 0.05, # 5% de mejora (muy bajo para nuestro umbral de estabilidad)
            "affected_sop": "gestion-claves-api-windows.md",
            "proposed_change": "Añadir cláusula de auditoría obligatoria de credenciales."
        }
    ]
    
    for update in industry_updates_2026:
        # Umbral de estabilidad: delta > 15% (0.15)
        if update["impact_est"] >= 0.15:
            sop_file = sops_dir / update["affected_sop"]
            if sop_file.exists():
                updates.append({
                    "topic": update["topic"],
                    "sop_name": update["affected_sop"],
                    "reason": update["context"],
                    "delta": update["impact_est"],
                    "change": update["proposed_change"]
                })
            else:
                # Si el SOP no existe, se sugiere crear uno nuevo
                updates.append({
                    "topic": update["topic"],
                    "sop_name": "NUEVO_SOP_ADS.md",
                    "reason": update["context"],
                    "delta": update["impact_est"],
                    "change": update["proposed_change"]
                })
                
    return updates

def run_knowledge_updater() -> list:
    """Ejecuta la evaluación semanal de conocimiento del sector."""
    print("--- [KNOWLEDGE UPDATER] Iniciando auditoría semanal de SOPs ---")
    
    pending_updates = check_sops_outdated()
    
    print("\n==================================================")
    print("CAMBIOS PROPUESTAS A LA BASE DE CONOCIMIENTO (SOPs)")
    print("==================================================")
    
    if not pending_updates:
        print("✅ Todos los SOPs están actualizados. No se superó el umbral de estabilidad (delta > 15%).")
    else:
        for update in pending_updates:
            print(f"\n💡 Tema: {update['topic']}")
            print(f"   SOP Afectado: {update['sop_name']}")
            print(f"   Mejora Est.:  +{update['delta']*100:.1f}%")
            print(f"   Razón:        {update['reason']}")
            print(f"   Cambio:       {update['change']}")
            
    # Guardar reporte en output/agency/
    output_dir = WORKSPACE_ROOT / "output" / "agency"
    output_dir.mkdir(parents=True, exist_ok=True)
    report_file = output_dir / "knowledge_updates.json"
    
    try:
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "proposed_updates": pending_updates
            }, f, indent=2)
        print(f"\n[OK] Propuestas de conocimiento escritas en {report_file}")
    except Exception as e:
        print(f"[ERROR] No se pudo escribir reporte de conocimiento: {e}")
        
    return pending_updates

if __name__ == "__main__":
    run_knowledge_updater()
