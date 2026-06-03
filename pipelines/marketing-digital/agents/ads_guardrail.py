"""
Módulo Ads Guardrail
Valida propuestas y acciones en las campañas contra la matriz de autoridad (authority-matrix.md)
y los límites de presupuesto de los perfiles de cliente para prevenir errores costosos.
"""

import os
import re
import sys
from pathlib import Path

# Asegurar encoding UTF-8
sys.stdout.reconfigure(encoding='utf-8')
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]

def parse_authority_matrix(client_name: str) -> dict:
    """Parsea el archivo authority-matrix.md del cliente para mapear los niveles de acción."""
    matrix_file = WORKSPACE_ROOT / "clients" / client_name / "authority-matrix.md"
    rules = {
        "analizar": "VERDE",
        "alertar": "VERDE",
        "pausar": "AMARILLO",
        "puja": "AMARILLO",
        "presupuesto_diario": "AMARILLO",
        "crear_campaña": "AMARILLO",
        "lanzar_campaña": "ROJO",
        "presupuesto_mensual": "ROJO"
    }
    
    if not matrix_file.exists():
        return rules # Retorna matriz por defecto
        
    try:
        with open(matrix_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parsea de forma sencilla buscando filas de la tabla markdown
        for line in content.split("\n"):
            if "|" not in line or line.strip().startswith("#") or line.strip().startswith("|-"):
                continue
                
            parts = [p.strip() for p in line.split("|") if p.strip()]
            if len(parts) < 2:
                continue
                
            action_name = parts[0].lower()
            
            # Buscar qué columna tiene la marca '✓' o 'check'
            is_verde = "✓" in parts[1] if len(parts) > 1 else False
            is_amarillo = "✓" in parts[2] if len(parts) > 2 else False
            is_rojo = "✓" in parts[3] if len(parts) > 3 else False
            
            # Mapear palabras clave de acción
            key = None
            if "analizar" in action_name or "reporte" in action_name:
                key = "analizar"
            elif "alertar" in action_name or "monitorear" in action_name:
                key = "alertar"
            elif "pausar" in action_name:
                key = "pausar"
            elif "puja" in action_name or "bidding" in action_name:
                key = "puja"
            elif "presupuesto diario" in action_name or "gasto" in action_name:
                key = "presupuesto_diario"
            elif "retargeting" in action_name or "crear" in action_name:
                key = "crear_campaña"
            elif "lanzar" in action_name or "fría" in action_name:
                key = "lanzar_campaña"
            elif "mensual" in action_name:
                key = "presupuesto_mensual"
                
            if key:
                if is_rojo:
                    rules[key] = "ROJO"
                elif is_amarillo:
                    rules[key] = "AMARILLO"
                elif is_verde:
                    rules[key] = "VERDE"
                    
    except Exception as e:
        print(f"[WARN] Error al parsear authority-matrix de {client_name}: {e}. Usando matriz por defecto.")
        
    return rules

def validate_action(client_name: str, action_type: str, delta_percent: float = None) -> dict:
    """
    Evalúa si la acción sobre la campaña está permitida según la autoridad del cliente.
    
    action_type: 'analizar', 'alertar', 'pausar', 'puja', 'presupuesto_diario', 'crear_campaña', 'lanzar_campaña', 'presupuesto_mensual'
    delta_percent: float indicando el porcentaje de cambio (ej: 0.10 para un 10% de incremento)
    """
    rules = parse_authority_matrix(client_name)
    level = rules.get(action_type, "ROJO")
    
    # Validaciones especiales de umbrales cuantitativos
    if action_type == "presupuesto_diario" and delta_percent is not None:
        if delta_percent > 0.20: # Más del 20% es siempre crítico (ROJO)
            level = "ROJO"
        elif delta_percent > 0.10: # Entre 10% y 20% requiere confirmación
            level = "AMARILLO"
            
    if action_type == "puja" and delta_percent is not None:
        if delta_percent > 0.15:
            level = "ROJO"
            
    # Formatear el veredicto
    if level == "VERDE":
        return {
            "allowed": True,
            "escalate": False,
            "level": "VERDE",
            "message": f"Accion '{action_type}' permitida automaticamente para el cliente '{client_name}'."
        }
    elif level == "AMARILLO":
        return {
            "allowed": False,
            "escalate": True,
            "level": "AMARILLO",
            "message": f"Accion '{action_type}' requiere aprobacion 1-tap de Kevin. Propuesta encolada."
        }
    else: # ROJO
        return {
            "allowed": False,
            "escalate": True,
            "level": "ROJO",
            "message": f"Accion critica '{action_type}' BLOQUEADA para ejecucion automatica. Requiere revision y confirmacion manual de Kevin."
        }

if __name__ == "__main__":
    # Test sencillo de demostración
    print("--- [ADS GUARDRAIL] Test de validaciones ---")
    
    # Caso 1: Monitoreo
    res1 = validate_action("veganashi", "alertar")
    print(f"Monitoreo Veganashi: {res1['level']} | Allowed: {res1['allowed']} | MSG: {res1['message']}")
    
    # Caso 2: Aumento de presupuesto del 5%
    res2 = validate_action("veganashi", "presupuesto_diario", 0.05)
    print(f"Aumento 5% Presupuesto Veganashi: {res2['level']} | Allowed: {res2['allowed']} | MSG: {res2['message']}")
    
    # Caso 3: Aumento de presupuesto del 25% (excede el umbral del 20%)
    res3 = validate_action("veganashi", "presupuesto_diario", 0.25)
    print(f"Aumento 25% Presupuesto Veganashi: {res3['level']} | Allowed: {res3['allowed']} | MSG: {res3['message']}")
    
    # Caso 4: Lanzar campaña fría
    res4 = validate_action("veganashi", "lanzar_campaña")
    print(f"Lanzar Campaña Fría: {res4['level']} | Allowed: {res4['allowed']} | MSG: {res4['message']}")
