import argparse
import sys
import json
import re
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Ejecutor de Evals de Regresión para Riqueza Digital.")
    parser.add_argument("--target", required=True, help="Ruta al directorio que contiene los archivos generados.")
    parser.add_argument("--cases", default=None, help="Ruta opcional al archivo eval_cases.json.")
    args = parser.parse_args()

    target_dir = Path(args.target)
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"❌ Error: El directorio destino no existe: {target_dir}")
        sys.exit(1)

    cases_file = Path(args.cases) if args.cases else Path(__file__).resolve().parent / "eval_cases.json"
    if not cases_file.exists():
        print(f"❌ Error: No se encontró el archivo de casos de prueba: {cases_file}")
        sys.exit(1)

    try:
        with open(cases_file, "r", encoding="utf-8") as f:
            cases = json.load(f)
    except Exception as e:
        print(f"❌ Error leyendo el archivo de casos: {e}")
        sys.exit(1)

    print(f"🧪 Iniciando batería de Evals sobre: {target_dir}")
    print(f"Total casos cargados: {len(cases)}\n")

    passed_count = 0
    results = []

    for case in cases:
        case_id = case.get("id")
        desc = case.get("description")
        filename = case.get("file")
        rules = case.get("rules", [])

        file_path = target_dir / filename
        if not file_path.exists():
            print(f"❌ [{case_id}] {desc} -> FAILED (Archivo {filename} no encontrado)")
            results.append({"id": case_id, "passed": False, "reason": f"Archivo {filename} no encontrado"})
            continue

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"❌ [{case_id}] {desc} -> FAILED (No se pudo leer el archivo: {e})")
            results.append({"id": case_id, "passed": False, "reason": f"Error de lectura: {e}"})
            continue

        failed_rules = []
        for rule in rules:
            # Compilar regex ignorando mayúsculas y permitiendo que punto coincida con nueva línea
            try:
                pattern = re.compile(rule, re.IGNORECASE | re.DOTALL)
                if not pattern.search(content):
                    failed_rules.append(rule)
            except re.error as err:
                print(f"⚠️ Warning: Regex inválida '{rule}': {err}")
                failed_rules.append(rule)

        if failed_rules:
            print(f"❌ [{case_id}] {desc} -> FAILED (Fallas en reglas: {', '.join(failed_rules)})")
            results.append({"id": case_id, "passed": False, "reason": f"Reglas fallidas: {failed_rules}"})
        else:
            print(f"✅ [{case_id}] {desc} -> PASSED")
            results.append({"id": case_id, "passed": True})
            passed_count += 1

    success_rate = (passed_count / len(cases)) * 100 if cases else 0
    print("\n==================================================")
    print(f"📊 RESULTADO DE BATERÍA DE EVALS")
    print(f"Aprobados:  {passed_count}/{len(cases)} ({success_rate:.1f}%)")
    print(f"Estado:     {'ÉXITO ✅' if passed_count == len(cases) else 'FALLÓ ❌'}")
    print("==================================================")

    if passed_count < len(cases):
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
