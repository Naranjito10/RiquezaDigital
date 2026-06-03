"""
Agente 4: Context Validator
Escanea los perfiles de clientes (profile.md), sesiones abiertas e interactúa con Notion
para detectar vacíos de contexto y tareas pendientes.
"""

import os
import re
import sys
import json
import urllib.request
from pathlib import Path

# Configurar encoding UTF-8 para consola de Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Raíz del workspace
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]

def get_notion_key() -> str:
    """Intenta recuperar la clave de Notion del entorno o del registro de Windows."""
    notion_key = os.environ.get("NOTION_API_KEY")
    if not notion_key:
        try:
            import winreg
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
            notion_key, _ = winreg.QueryValueEx(key, "NOTION_API_KEY")
        except Exception:
            pass
    return notion_key

def make_notion_request(url: str, method: str = "POST", data: dict = None) -> tuple:
    """Realiza una petición HTTPS a la API de Notion usando urllib."""
    notion_key = get_notion_key()
    if not notion_key:
        return 401, {"error": "NOTION_API_KEY no configurado"}
        
    headers = {
        "Authorization": f"Bearer {notion_key}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json"
    }
    
    data_bytes = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, headers=headers, data=data_bytes, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(error_body)
        except Exception:
            return e.code, {"error": error_body}
    except Exception as e:
        return 500, {"error": str(e)}

def validate_profiles() -> dict:
    """Escanea y valida todos los perfiles de clientes en clients/*."""
    clients_dir = WORKSPACE_ROOT / "clients"
    results = {}
    
    if not clients_dir.exists():
        print(f"[WARN] Directorio de clientes no encontrado en {clients_dir}")
        return results
        
    # Campos obligatorios y sus expresiones regulares básicas
    required_fields = {
        "Empresa": r"-\s+\*\*Empresa:\*\*\s*(.+)",
        "Sector": r"-\s+\*\*Sector:\*\*\s*(.+)",
        "Web": r"-\s+\*\*Web:\*\*\s*(.+)",
        "Prioridad": r"-\s+\*\*Prioridad:\*\*\s*(.+)",
        "CPL_Objetivo": r"-\s+\*\*CPL objetivo:\*\*\s*(.+)",
        "CPA_Objetivo": r"-\s+\*\*CPA objetivo:\*\*\s*(.+)",
        "Presupuesto_Mensual": r"-\s+\*\*Presupuesto mensual total:\*\*\s*(.+)",
        "Meta_Ad_Account": r"-\s+\*\*Meta Ad Account ID:\*\*\s*act_(.+)",
        "Google_Customer_ID": r"-\s+\*\*Google Customer ID:\*\*\s*(.+)"
    }
    
    for client_path in clients_dir.iterdir():
        if client_path.is_dir() and not client_path.name.startswith("_") and not client_path.name.startswith("."):
            profile_file = client_path / "profile.md"
            client_name = client_path.name
            results[client_name] = {
                "has_profile": False,
                "missing_fields": [],
                "fields": {}
            }
            
            if not profile_file.exists():
                results[client_name]["missing_fields"].append("profile.md no existe")
                continue
                
            results[client_name]["has_profile"] = True
            
            try:
                with open(profile_file, "r", encoding="utf-8") as f:
                    content = f.read()
                    
                # Validar cada campo
                for field_name, regex in required_fields.items():
                    match = re.search(regex, content, re.IGNORECASE)
                    if match:
                        value = match.group(1).strip()
                        # Si el valor está vacío o contiene indicaciones tipo "por completar"
                        if not value or "completar" in value.lower() or "definir" in value.lower() or value == "€":
                            results[client_name]["missing_fields"].append(field_name)
                        else:
                            results[client_name]["fields"][field_name] = value
                    else:
                        results[client_name]["missing_fields"].append(field_name)
            except Exception as e:
                results[client_name]["missing_fields"].append(f"Error de lectura: {str(e)}")
                
    return results

def check_open_sessions() -> list:
    """Escanea la carpeta .remember para ver si hay sesiones abiertas sin consolidar."""
    remember_dir = WORKSPACE_ROOT / ".remember"
    open_sessions = []
    
    if not remember_dir.exists():
        return open_sessions
        
    index_file = remember_dir / "sessions" / "INDEX.md"
    if index_file.exists():
        try:
            with open(index_file, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Buscar cualquier línea que pueda indicar sesiones abiertas o pendientes
            # O simplemente ver el último registro
            lines = [line.strip() for line in content.split("\n") if line.strip()]
            if lines:
                open_sessions.append(f"Último registro de sesión en INDEX: {lines[-1]}")
        except Exception as e:
            open_sessions.append(f"Error leyendo index de sesiones: {str(e)}")
            
    return open_sessions

def check_notion_tasks() -> list:
    """Recupera tareas abiertas o sin responder en Notion de la Tareas DB."""
    notion_tasks = []
    tasks_db_id = "b5c6d3aa-d462-4989-962e-8fc7034de3a9" # ID Tareas DB de RD
    
    url = f"https://api.notion.com/v1/databases/{tasks_db_id}/query"
    # Filtrar por tareas cuyo estado no sea "Hecho"
    query_body = {
        "filter": {
            "property": "Estado",
            "status": {
                "does_not_equal": "Hecho"
            }
        },
        "page_size": 20
    }
    
    status, res = make_notion_request(url, "POST", query_body)
    if status == 200:
        for page in res.get("results", []):
            properties = page.get("properties", {})
            title = "Sin título"
            
            # Buscar título de la tarea
            for prop_name, prop_val in properties.items():
                if isinstance(prop_val, dict) and prop_val.get("type") == "title":
                    title_list = prop_val.get("title", [])
                    if title_list:
                        title = title_list[0].get("plain_text", "Sin título")
                        break
                        
            # Buscar estado
            status_val = "Desconocido"
            status_prop = properties.get("Estado", {})
            if status_prop.get("type") == "status":
                status_val = status_prop.get("status", {}).get("name", "Desconocido")
                
            notion_tasks.append({
                "id": page.get("id"),
                "title": title,
                "status": status_val,
                "url": page.get("url")
            })
    else:
        # Si falla (ej: sin API key o base de datos no compartida con la integración)
        notion_tasks.append({
            "error": f"No se pudieron cargar tareas de Notion (Status code: {status}, Error: {res.get('error', 'N/A')})"
        })
        
    return notion_tasks

def run_context_validation() -> dict:
    """Ejecuta toda la suite de validaciones del agente y genera el reporte."""
    print("--- [CONTEXT VALIDATOR] Iniciando escaneo de contexto ---")
    
    profiles = validate_profiles()
    sessions = check_open_sessions()
    tasks = check_notion_tasks()
    
    report = {
        "profiles": profiles,
        "open_sessions": sessions,
        "notion_tasks": tasks
    }
    
    print("\n--- RESULTADO DE LA VALIDACIÓN ---")
    
    # Reportar perfiles
    print("\n[Perfiles de Clientes]")
    for client, data in profiles.items():
        if data["missing_fields"]:
            print(f"❌ {client}: Faltan campos obligatorios: {', '.join(data['missing_fields'])}")
        else:
            print(f"✅ {client}: Perfil completo.")
            
    # Reportar sesiones
    print("\n[Sesiones Activas]")
    if sessions:
        for session in sessions:
            print(f"ℹ️ {session}")
    else:
        print("✅ No se detectaron drifts de sesión.")
        
    # Reportar tareas Notion
    print("\n[Tareas Abiertas Notion]")
    for task in tasks:
        if "error" in task:
            print(f"⚠️ {task['error']}")
        else:
            print(f"📌 [{task['status']}] {task['title']}")
            
    return report

def log_agent_action(action: str, client: str, platform: str, log_type: str) -> tuple:
    """Registra una acción en la base de datos de 'Log de Acciones Agenticas' (ID: 374d2fec-4b82-8148-bad1-c996c8b5f65e)"""
    db_id = "374d2fec-4b82-8148-bad1-c996c8b5f65e"
    url = "https://api.notion.com/v1/pages"
    
    from datetime import datetime
    
    # Normalizar Cliente
    client = client.lower().strip()
    if client == "riquezadigital" or client == "riqueza_digital":
        client = "riqueza-digital"
        
    # Normalizar Plataforma
    platform = platform.strip()
    if "meta" in platform.lower():
        platform = "Meta Ads"
    elif "google" in platform.lower():
        platform = "Google Ads"
    else:
        platform = "Sistema"
        
    # Normalizar Tipo
    # Options: "Alerta", "Propuesta", "Ejecucion"
    log_type = log_type.strip().capitalize()
    if log_type not in ["Alerta", "Propuesta", "Ejecucion"]:
        log_type = "Ejecucion"
        
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            "Accion": {
                "title": [
                    {
                        "text": {
                            "content": action
                        }
                    }
                ]
            },
            "Cliente": {
                "select": {
                    "name": client
                }
            },
            "Plataforma": {
                "select": {
                    "name": platform
                }
            },
            "Tipo": {
                "select": {
                    "name": log_type
                }
            },
            "Fecha": {
                "date": {
                    "start": datetime.now().strftime("%Y-%m-%d")
                }
            }
        }
    }
    
    return make_notion_request(url, "POST", payload)

if __name__ == "__main__":
    run_context_validation()
