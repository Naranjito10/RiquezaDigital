class ContextCompactor:
    """
    Optimiza la ventana de contexto (tokens) de los agentes compactando
    las versiones obsoletas de código y manteniendo solo las críticas y el estado actual.
    """
    @staticmethod
    def compact_history(iterations: list) -> str:
        """
        Recibe una lista de iteraciones pasadas y genera un resumen estructurado legible.
        Cada iteración en la lista debe tener la estructura:
        {
            "iteration": int,
            "critique": str,
            "passed": bool,
            "cost": float
        }
        Retorna un string con el resumen consolidado de fallos y correcciones previas,
        omitiendo el código fuente completo de los intentos pasados para ahorrar tokens.
        """
        if not iterations:
            return "No hay iteraciones previas."
            
        summary = ["### Historial de Iteraciones Previas y Críticas del Evaluador:\n"]
        for it in iterations:
            status = "Aprobado" if it.get("passed", False) else "Rechazado"
            summary.append(f"**Iteración {it.get('iteration', 1)}** (Resultado: {status}):")
            summary.append(f"- Crítica del Director de Arte (Evaluador): {it.get('critique', 'Sin comentarios')}")
            summary.append("-" * 40)
            
        return "\n".join(summary)
