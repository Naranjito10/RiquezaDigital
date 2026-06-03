"""
Agente 3: Campaign Optimizer
Analiza rendimiento semanal, consulta el histórico de feedback y genera
propuestas concretas de optimización en formato de menú interactivo.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Asegurar importaciones correctas
sys.stdout.reconfigure(encoding='utf-8')
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(WORKSPACE_ROOT / "pipelines" / "marketing-digital"))

from agents.campaign_monitor import parse_profile_objectives, get_baseline_data
from agents.context_validator import log_agent_action

def get_feedback_log(client_name: str) -> list:
    """Recupera el historial de acciones y aprendizajes de optimización."""
    intelligence_dir = WORKSPACE_ROOT / "clients" / client_name / "intelligence"
    intelligence_dir.mkdir(parents=True, exist_ok=True)
    feedback_file = intelligence_dir / "feedback-log.json"
    
    if feedback_file.exists():
        try:
            with open(feedback_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Error leyendo feedback-log de {client_name}: {e}")
            
    return []

def save_feedback_log(client_name: str, log_data: list) -> None:
    """Guarda el feedback-log del cliente en su directorio de inteligencia."""
    intelligence_dir = WORKSPACE_ROOT / "clients" / client_name / "intelligence"
    feedback_file = intelligence_dir / "feedback-log.json"
    
    try:
        with open(feedback_file, "w", encoding="utf-8") as f:
            json.dump(log_data, f, indent=2)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar feedback-log de {client_name}: {e}")

def load_active_alerts() -> list:
    """Carga las alertas activas generadas por el Campaign Monitor."""
    alerts_file = WORKSPACE_ROOT / "output" / "agency" / "active_alerts.json"
    if alerts_file.exists():
        try:
            with open(alerts_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("alerts", [])
        except Exception as e:
            print(f"[WARN] No se pudieron leer las alertas de {alerts_file}: {e}")
    return []

def generate_optimizations() -> dict:
    """Genera propuestas de optimización a partir de las alertas de monitoreo."""
    print("--- [CAMPAIGN OPTIMIZER] Generando propuestas de optimización ---")
    alerts = load_active_alerts()
    proposals = {}
    
    # Agrupar alertas por cliente
    client_alerts = {}
    for alert in alerts:
        client_name = alert["client"]
        client_alerts.setdefault(client_name, []).append(alert)
        
    global_proposal_index = 1
    pending_proposals = []
    
    for client_path in (WORKSPACE_ROOT / "clients").iterdir():
        if client_path.is_dir() and not client_path.name.startswith("_") and not client_path.name.startswith("."):
            client_name = client_path.name
            client_proposals = []
            
            cpa_target, presupuesto, meta_id, google_id = parse_profile_objectives(client_name)
            feedback = get_feedback_log(client_name)
            
            # Obtener alertas de este cliente
            alerts_list = client_alerts.get(client_name, [])
            
            # Analizar alertas y cruzarlas con feedback histórico
            for alert in alerts_list:
                alert_type = alert["type"]
                campaign = alert["campaign"]
                platform = alert["platform"]
                
                # Ejemplo de prevención basada en feedback histórico
                # Si una propuesta similar de subir puja ya falló en los últimos 30 días, no proponerla.
                recent_failures = [
                    f for f in feedback 
                    if f.get("accion", "").lower() in ["subir puja", "aumentar puja"] 
                    and f.get("resultado_7d", {}).get("conversiones_delta", 0) < 0
                ]
                
                if alert_type == "CPA_ANOMALY":
                    action_desc = f"Pausar anuncio o conjunto ineficiente en '{campaign}'"
                    rationale = f"El CPA (€{alert['value']:.2f}) supera en un 20% el CPA objetivo de €{alert['limit']:.2f}."
                    
                    if recent_failures:
                        rationale += " Nota: El ajuste de puja falló recientemente, por lo que se sugiere pausar creativos y no pujar."
                        
                    client_proposals.append({
                        "index": global_proposal_index,
                        "client": client_name,
                        "platform": platform,
                        "campaign": campaign,
                        "action": "PAUSE_UNDERPERFORMING",
                        "description": action_desc,
                        "rationale": rationale,
                        "estimated_impact": "Reducción de coste ineficiente y mejora del CPA medio."
                    })
                    global_proposal_index += 1
                    
                elif alert_type == "CTR_ANOMALY":
                    client_proposals.append({
                        "index": global_proposal_index,
                        "client": client_name,
                        "platform": platform,
                        "campaign": campaign,
                        "action": "REWRITE_CREATIVES",
                        "description": f"Probar variante de copy/creative en conjunto de anuncios de '{campaign}'",
                        "rationale": f"El CTR de {alert['value']:.2f}% está por debajo del piso de marca ({alert['limit']:.2f}%).",
                        "estimated_impact": "Incremento de clics calificados y descenso del CPC medio."
                    })
                    global_proposal_index += 1
            
            # Si el cliente es Veganashi, agregar proactivamente la propuesta de Retargeting (Fase 2)
            if client_name == "veganashi":
                # Comprobar si ya existe una propuesta de retargeting en el log
                has_retargeting_run = any("retargeting" in f.get("accion", "").lower() for f in feedback)
                if not has_retargeting_run:
                    client_proposals.append({
                        "index": global_proposal_index,
                        "client": client_name,
                        "platform": "Meta Ads",
                        "campaign": "Meta_Retargeting_Sales_V1",
                        "action": "CREATE_RETARGETING_CAMPAIGN",
                        "description": "Lanzar campaña de Retargeting enfocada a Conversión (Ventas)",
                        "rationale": "Capturar el tráfico web templado de los últimos 30 días e interactores de redes sociales (últimos 90 días).",
                        "estimated_impact": "Incremento de conversiones directas con un CPA inferior en un 30% a la media fría."
                    })
                    global_proposal_index += 1
                    
            if client_proposals:
                proposals[client_name] = client_proposals
                pending_proposals.extend(client_proposals)
                
    # Guardar en output/agency/pending_optimizations.json
    output_file = WORKSPACE_ROOT / "output" / "agency" / "pending_optimizations.json"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pending_proposals, f, indent=2)
    except Exception as e:
        print(f"[ERROR] No se pudo guardar pending_optimizations.json: {e}")
        
    # Registrar las propuestas en Notion
    for p in pending_proposals:
        try:
            status, res = log_agent_action(
                action=f"Propuesta: {p['description']} - Razón: {p['rationale']}",
                client=p["client"],
                platform=p["platform"],
                log_type="Propuesta"
            )
            if status == 200:
                print(f"[Notion Log] Propuesta registrada para {p['client']}: {p['description']}")
            else:
                print(f"[Notion Log ERROR] Fallo al registrar propuesta: Status {status}, Res: {res}")
        except Exception as e:
            print(f"[Notion Log ERROR] Excepción al registrar propuesta: {e}")
         
    # Mostrar por consola
    print("\n==================================================")
    print("PROPUESTAS DE OPTIMIZACIÓN DISPONIBLES")
    print("==================================================")
    for client, props in proposals.items():
        print(f"\n📢 Cliente: {client.upper()}")
        for p in props:
            print(f"  [{p['index']}] {p['description']}")
            print(f"      Plataforma:  {p['platform']}")
            print(f"      Razón:       {p['rationale']}")
            print(f"      Impacto:     {p['estimated_impact']}")
            
    print("\nInstrucción: Ejecuta el script con --approve <numero> para simular la confirmación e integrar al feedback-log.")
    return proposals

def approve_proposal(proposal_index: int) -> None:
    """Simula la aprobación de una propuesta y escribe al feedback-log."""
    opts_file = WORKSPACE_ROOT / "output" / "agency" / "pending_optimizations.json"
    if not opts_file.exists():
        print("[ERROR] No hay propuestas pendientes registradas.")
        return
        
    try:
        with open(opts_file, "r", encoding="utf-8") as f:
            proposals = json.load(f)
            
        target = None
        for p in proposals:
            if p["index"] == proposal_index:
                target = p
                break
                
        if not target:
            print(f"[ERROR] No se encontró la propuesta número {proposal_index}.")
            return
            
        print(f"\n[APROBADO] Procesando propuesta {proposal_index} para {target['client']}...")
        
        # Guardar en feedback-log.json
        feedback = get_feedback_log(target["client"])
        feedback.append({
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "accion": target["description"],
            "contexto": target["rationale"],
            "resultado_7d": {
                "cpa_delta": 0,
                "conversiones_delta": 0
            },
            "aprendizaje": "pendiente_evaluacion_7d"
        })
        save_feedback_log(target["client"], feedback)
        print(f"[OK] Añadido al feedback-log.json del cliente {target['client']}.")
        
        # Registrar la ejecución en Notion
        try:
            status, res = log_agent_action(
                action=f"Ejecución: {target['description']}",
                client=target["client"],
                platform=target["platform"],
                log_type="Ejecucion"
            )
            if status == 200:
                print(f"[Notion Log] Ejecución registrada para {target['client']}: {target['description']}")
            else:
                print(f"[Notion Log ERROR] Fallo al registrar ejecución: Status {status}, Res: {res}")
        except Exception as e:
            print(f"[Notion Log ERROR] Excepción al registrar ejecución: {e}")
        
        # Eliminar la propuesta del archivo de pendientes
        proposals = [p for p in proposals if p["index"] != proposal_index]
        with open(opts_file, "w", encoding="utf-8") as f:
            json.dump(proposals, f, indent=2)
            
    except Exception as e:
        print(f"[ERROR] Al procesar la aprobación: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Optimizer de campañas de Ads")
    parser.add_argument("--approve", type=int, help="ID de la propuesta a aprobar")
    args = parser.parse_args()
    
    if args.approve:
        approve_proposal(args.approve)
    else:
        generate_optimizations()
