Ejecuta el bucle de diseño autónomo Generador-Evaluador para maquetar la web de un cliente.

## Flujo de Trabajo

1. **Obtener Cliente:** Pide el nombre del cliente (o lee el contexto actual).
2. **Pre-requisitos:**
   - Verifica que exista `clients/<cliente>/web/prompt-claude-design.md`. Si no existe, avisa al usuario de que debe ejecutar primero `/generar-prompt-web`.
   - Carga e importa los guardrails en `pipelines/shared/agentic_harness/`.
3. **Paso de Seguridad (Checkpoint):**
   - Llama al script `git_guard.py` para crear un checkpoint de Git llamado `pre_autopilot_<cliente>`.
4. **Ejecución del Bucle (Generador-Evaluador):**
   - Inicializa el `budget_manager.py` con un límite estricto de $15.00 USD para esta corrida.
   - **Iteración (Máximo 5 ciclos):**
     1. Llama al **Generador** para escribir/actualizar los archivos de maquetación en `clients/<cliente>/web/` (`index.html`, `styles.css`, `script.js`) basándose en el prompt de diseño y el feedback acumulado.
     2. Llama al **Evaluador** para auditar el código generado contra los 4 pilares: *Design Quality*, *Originality*, *Craft* y *Functionality* usando las guías de `evaluator_prompts.py`.
     3. Registra el coste de tokens estimado de la llamada en `budget_manager.py`.
     4. Si el Evaluador aprueba con nota >= 8 en todos los pilares (campo `"passed": true`), detiene el bucle e informa del éxito.
     5. Si el Evaluador rechaza, pasa el feedback detallado de la crítica a la siguiente iteración del Generador.
5. **Resultado y Entrega:**
   - Muestra las calificaciones obtenidas por pilar, la crítica del Evaluador y el coste total en dólares consumido de la API.
   - Proporciona un enlace al archivo index.html local para que el usuario pueda previsualizarlo.
   - Pregunta al usuario si acepta el diseño:
     - **Si lo acepta:** Ejecuta `git_guard.py` con `discard_checkpoint` para limpiar la historia de Git y conservar los archivos.
     - **Si lo rechaza:** Ejecuta `git_guard.py` con `rollback` para deshacer todos los cambios y dejar el workspace limpio.

## Reglas

- Detén el bucle inmediatamente si `budget_manager.py` lanza una excepción de presupuesto excedido.
- No alteres archivos fuera del directorio `clients/<cliente>/web/` durante la generación.
