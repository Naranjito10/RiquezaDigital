import argparse
import sys
import re
import json
from pathlib import Path

# Agregar la raíz del proyecto al path para asegurar importaciones limpias
workspace_root = Path(__file__).resolve().parents[3]
if str(workspace_root) not in sys.path:
    sys.path.append(str(workspace_root))

from pipelines.shared.agentic_harness.git_guard import GitGuard
from pipelines.shared.agentic_harness.budget_manager import BudgetManager
from pipelines.shared.agentic_harness.session_logger import SessionLogger
from pipelines.shared.agentic_harness.credential_vault import CredentialVault
from pipelines.shared.agentic_harness.context_compactor import ContextCompactor
from pipelines.desarrollo.generator_evaluator.evaluator_prompts import GENERATOR_SYSTEM_PROMPT, EVALUATOR_SYSTEM_PROMPT

def parse_and_save_files(response_text: str, target_dir: Path) -> list:
    """
    Busca delimitadores [FILE: filename]...[/FILE] en el texto de respuesta,
    limpia bloques markdown sobrantes y escribe los archivos en target_dir.
    """
    pattern = r"\[FILE:\s*([^\]]+)\](.*?)\[/FILE\]"
    matches = re.findall(pattern, response_text, re.DOTALL)
    
    saved_files = []
    for filename, content in matches:
        filename = filename.strip()
        content = content.strip()
        
        # Limpiar bloques de código markdown sobrantes
        if content.startswith("```"):
            content = "\n".join(content.split("\n")[1:])
        if content.endswith("```"):
            content = "\n".join(content.split("\n")[:-1])
            
        file_path = target_dir / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        saved_files.append(filename)
    return saved_files

def estimate_cost(provider: str, input_text: str, output_text: str) -> float:
    """
    Estima el coste de la llamada a la API basándose en los caracteres (1 token ≈ 4 chars).
    """
    input_tokens = len(input_text) / 4
    output_tokens = len(output_text) / 4
    
    if provider == "gemini":
        # Gemini 1.5 Flash: $0.075 / 1M input, $0.30 / 1M output
        return (input_tokens * 0.075 / 1000000) + (output_tokens * 0.30 / 1000000)
    elif provider == "anthropic":
        # Claude 3.5 Sonnet: $3.00 / 1M input, $15.00 / 1M output
        return (input_tokens * 3.00 / 1000000) + (output_tokens * 15.00 / 1000000)
    return 0.0

def main():
    parser = argparse.ArgumentParser(description="Runner del bucle agéntico Generador-Evaluador para Riqueza Digital.")
    parser.add_argument("--client", required=True, help="Nombre de la carpeta del cliente (ej. keller-valentina)")
    args = parser.parse_args()
    
    client = args.client
    
    # 1. Rutas
    client_dir = workspace_root / "clients" / client
    web_dir = client_dir / "web"
    prompt_file = web_dir / "prompt-claude-design.md"
    
    print(f"[START] Iniciando Autopilot de Diseno para el cliente: {client}")
    
    if not prompt_file.exists():
        print(f"[ERROR] No se encontro el archivo de directrices en {prompt_file}")
        print("Por favor, ejecuta primero el comando /generar-prompt-web para crear el prompt de diseno.")
        sys.exit(1)
        
    # 2. Inicializar Logger y Guardrails
    session_id = f"autopilot_{client}"
    logger = SessionLogger(session_id=session_id)
    git_guard = GitGuard()
    budget_manager = BudgetManager(run_budget_limit=15.0, daily_budget_limit=50.0)
    
    logger.log_event("session_started", {"client": client, "web_dir": str(web_dir)})
    budget_manager.reset_run()
    
    # 3. Crear Checkpoint en Git
    checkpoint_name = f"autopilot_{client}"
    print("[GIT] Creando checkpoint preventivo en Git...")
    checkpoint_status = git_guard.create_checkpoint(checkpoint_name)
    print(f"   {checkpoint_status}")
    logger.log_event("checkpoint_created", {"checkpoint_name": checkpoint_name, "status": checkpoint_status})
    
    # Cargar directrices de marca
    with open(prompt_file, 'r', encoding='utf-8') as f:
        brand_prompt = f.read()
        
    history = []
    success = False
    final_evaluation = {}
    
    # 4. Bucle Generador-Evaluador
    max_iterations = 5
    for i in range(1, max_iterations + 1):
        print(f"\n--- ITERACION {i}/{max_iterations} ---")
        
        # Leer archivos actuales (si existen) para pasarlos como contexto
        current_code = {}
        for filename in ["index.html", "styles.css", "script.js"]:
            file_path = web_dir / filename
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    current_code[filename] = f.read()
            else:
                current_code[filename] = ""
                
        current_code_context = "\n".join([f"--- {fn} ---\n{content}" for fn, content in current_code.items() if content])
        if not current_code_context:
            current_code_context = "(No hay archivos creados aun, es la primera generacion)."
            
        # Compactar historial
        compacted_history = ContextCompactor.compact_history(history)
        
        # Construir Prompt del Generador
        gen_prompt = f"""
Has sido contratado para maquetar el sitio web de un cliente.

### INSTRUCCIONES DE DISEÑO Y NEGOCIO:
{brand_prompt}

### CÓDIGO ACTUAL EN EL WORKSPACE (Si existe):
{current_code_context}

{compacted_history}

### INSTRUCCIÓN DE FORMATO DE SALIDA (MUY IMPORTANTE):
Debes generar todo el código necesario. Separa cada uno de los archivos usando la siguiente sintaxis exacta:

[FILE: index.html]
<!-- Código HTML aquí -->
[/FILE]

[FILE: styles.css]
/* Código CSS aquí */
[/FILE]

[FILE: script.js]
// Código JS aquí (si es necesario, si no, déjalo vacío)
[/FILE]

No incluyas textos explicativos fuera de los delimitadores de archivos. Ve directo al código.
"""
        
        print("[LLM] Generando maquetacion con Gemini Flash...")
        try:
            generator_response = CredentialVault.request(
                provider="gemini",
                model="gemini-2.5-flash",
                system_prompt=GENERATOR_SYSTEM_PROMPT,
                prompt=gen_prompt,
                json_mode=False
            )
        except Exception as e:
            error_msg = f"Error en generacion: {str(e)}"
            print(f"[ERROR] {error_msg}")
            logger.log_event("error", {"iteration": i, "step": "generator", "error": error_msg})
            break
            
        # Calcular coste del Generador
        gen_cost = estimate_cost("gemini", gen_prompt, generator_response)
        budget_manager.add_cost(gen_cost)
        
        # Guardar archivos
        saved_files = parse_and_save_files(generator_response, web_dir)
        print(f"[FILE] Archivos escritos: {', '.join(saved_files)}")
        logger.log_event("generation_attempt", {
            "iteration": i,
            "saved_files": saved_files,
            "cost_usd": gen_cost
        })
        
        # Cargar archivos escritos para la evaluación
        html_content = ""
        css_content = ""
        js_content = ""
        
        if (web_dir / "index.html").exists():
            with open(web_dir / "index.html", "r", encoding="utf-8") as f:
                html_content = f.read()
        if (web_dir / "styles.css").exists():
            with open(web_dir / "styles.css", "r", encoding="utf-8") as f:
                css_content = f.read()
        if (web_dir / "script.js").exists():
            with open(web_dir / "script.js", "r", encoding="utf-8") as f:
                js_content = f.read()
                
        # Construir Prompt del Evaluador
        eval_prompt = f"""
Por favor, evalúa el diseño web generado para el cliente. Los archivos actuales en el workspace son:

--- index.html ---
{html_content}

--- styles.css ---
{css_content}

--- script.js ---
{js_content}

Evalúa estos archivos contra los 4 criterios de diseño (Design Quality, Originality, Craft, Functionality).
Recuerda que debes devolver un JSON estructurado con la puntuación de cada criterio, un campo booleano 'passed' que sea true si y solo si todas las notas son >= 8, y una crítica detallada de los puntos débiles.
"""
        
        print("[LLM] Evaluando calidad visual y tecnica con Claude Sonnet...")
        try:
            eval_response = CredentialVault.request(
                provider="anthropic",
                model="claude-3-5-sonnet-20241022",
                system_prompt=EVALUATOR_SYSTEM_PROMPT,
                prompt=eval_prompt,
                json_mode=True
            )
        except Exception as e:
            error_msg = f"Error en evaluacion: {str(e)}"
            print(f"[ERROR] {error_msg}")
            logger.log_event("error", {"iteration": i, "step": "evaluator", "error": error_msg})
            break
            
        # Calcular coste del Evaluador
        eval_cost = estimate_cost("anthropic", eval_prompt, eval_response)
        budget_manager.add_cost(eval_cost)
        
        # Intentar parsear JSON de la evaluación
        try:
            # Eliminar tags markdown ```json si el modelo los inyectó por error
            clean_eval = eval_response.strip()
            if clean_eval.startswith("```json"):
                clean_eval = "\n".join(clean_eval.split("\n")[1:])
            if clean_eval.endswith("```"):
                clean_eval = "\n".join(clean_eval.split("\n")[:-1])
                
            eval_data = json.loads(clean_eval)
        except json.JSONDecodeError:
            print("[WARN] La respuesta del evaluador no es JSON valido. Forzando re-intento.")
            eval_data = {
                "scores": {"design_quality": 0, "originality": 0, "craft": 0, "functionality": 0},
                "passed": False,
                "critique": "El evaluador devolvio un formato no estructurado. Corrige la consistencia tecnica."
            }
            
        print(f"[EVAL] Notas obtenidas:")
        print(f"   - Calidad de Diseno: {eval_data['scores'].get('design_quality', 0)}/10")
        print(f"   - Originalidad:      {eval_data['scores'].get('originality', 0)}/10")
        print(f"   - Craft Tecnico:     {eval_data['scores'].get('craft', 0)}/10")
        print(f"   - Usabilidad:        {eval_data['scores'].get('functionality', 0)}/10")
        
        passed = eval_data.get("passed", False)
        critique = eval_data.get("critique", "Sin comentarios adicionales.")
        
        print(f"[QA] Aprobado por QA:  {'SI' if passed else 'NO'}")
        if not passed:
            print(f"[QA] Critica: {critique}")
            
        # Guardar en historial
        history_item = {
            "iteration": i,
            "scores": eval_data["scores"],
            "passed": passed,
            "critique": critique,
            "cost": gen_cost + eval_cost
        }
        history.append(history_item)
        logger.log_event("evaluation_received", history_item)
        
        if passed:
            success = True
            final_evaluation = eval_data
            break
            
    # 5. Cierre de sesión y reporte final
    status = budget_manager.get_status()
    total_cost = status["run_spent"]
    
    print("\n==================================================")
    print("RESUMEN DEL AUTOPILOT DE DISENO")
    print(f"Cliente:        {client}")
    print(f"Estado Final:   {'APROBADO CON EXITO' if success else 'LIMITE DE ITERACIONES EXCEDIDO'}")
    print(f"Coste de API:   ${total_cost:.4f} USD")
    print(f"Sesion ID:      {session_id}")
    print("==================================================")
    
    summary_data = {
        "client": client,
        "success": success,
        "total_cost": total_cost,
        "iterations": len(history),
        "history": history
    }
    logger.log_event("session_completed", summary_data)
    
    if not success:
        sys.exit(2) # Retornar código de salida 2 para indicar que completó pero no pasó la evaluación final

if __name__ == "__main__":
    main()
