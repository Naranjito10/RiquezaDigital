Ejecuta el bucle de diseño autónomo Generador-Evaluador compilado en Python para maquetar la web de un cliente.

## Flujo de Trabajo

1. **Obtener Cliente:** Pide el nombre del cliente (o lee el contexto actual).
2. **Pre-requisitos:**
   - Verifica que exista `clients/<cliente>/web/prompt-claude-design.md`. Si no existe, avisa al usuario de que debe ejecutar primero `/generar-prompt-web`.
3. **Ejecución del Bucle (Delegado a Python):**
   - Ejecuta el comando en terminal:
     ```powershell
     python pipelines/desarrollo/generator_evaluator/runner.py --client <cliente>
     ```
   - El script de Python gestionará internamente los checkpoints de Git (`git_guard.py`), el control de presupuesto (`budget_manager.py`), la compactación de contexto y el bucle generador-evaluador.
4. **Resultado y Entrega:**
   - Lee el resultado devuelto en consola por el script.
   - Muestra en el chat las calificaciones obtenidas por pilar, la crítica final y el coste total en dólares.
   - Proporciona un enlace al archivo HTML local para que el usuario pueda previsualizarlo:
     `[index.html](file:///c:/Users/kein-/OneDrive/Desktop/Riqueza%20Digital/clients/<cliente>/web/index.html)`
   - Pregunta al usuario si acepta el diseño:
     - **Si lo acepta:** Ejecuta el comando en terminal para consolidar los cambios:
       ```powershell
       python -c "from pipelines.shared.agentic_harness.git_guard import GitGuard; GitGuard().discard_checkpoint('autopilot_<cliente>')"
       ```
     - **Si lo rechaza:** Ejecuta el comando en terminal para realizar rollback:
       ```powershell
       python -c "from pipelines.shared.agentic_harness.git_guard import GitGuard; GitGuard().rollback('autopilot_<cliente>')"
       ```

## Reglas

- Si el runner de Python falla por presupuesto excedido o error técnico, informa inmediatamente del error al usuario.
- No alteres archivos fuera de `clients/<cliente>/web/` durante la ejecución.
