# SOP: Bucle Generador-Evaluador e Integración de Guardrails

**Área:** Desarrollo / Automatizaciones  
**Estado:** 🌱 Draft  
**Última actualización:** 2026-05-26  
**Clientes donde se aplicó:** Riqueza Digital, Keller (Valentina Cuadrado)  
**Tiempo estimado:** 1 hora (setup inicial de la base de código)

---

## Resumen

Este procedimiento detalla cómo configurar un bucle autónomo multi-agente de generación y evaluación visual/técnica (basado en el patrón de ingeniería de Anthropic) y cómo dotarlo de guardrails de seguridad y presupuesto. Sirve para replicar el sistema con nuevos clientes de desarrollo web, software o marketing que requieran automatizaciones robustas.

---

## Pre-requisitos

Antes de empezar, confirmar que tienes:
- [ ] Acceso a las API Keys de LLM en el archivo `.env` (Anthropic, Gemini, OpenAI).
- [ ] Repositorio Git inicializado en el workspace del cliente.
- [ ] Python 3.10+ instalado.
- [ ] (Opcional) Instancia de n8n y credenciales para la orquestación visual.

---

## Pasos

### 1. Inicializar la Estructura en el Workspace
Para cada cliente o servicio nuevo que requiera el bucle, crea los directorios correspondientes si no existen:

```bash
mkdir -p pipelines/shared/agentic_harness/
mkdir -p pipelines/desarrollo/generator_evaluator/
```

### 2. Copiar e Inicializar los Guardrails
Copia los scripts base de Riqueza Digital al workspace de ejecución del cliente:
1. **[budget_manager.py](file:///c:/Users/kein-/OneDrive/Desktop/Riqueza%20Digital/pipelines/shared/agentic_harness/budget_manager.py)**: Copiar y configurar los límites de coste diarios y por ejecución en la clase.
2. **[git_guard.py](file:///c:/Users/kein-/OneDrive/Desktop/Riqueza%20Digital/pipelines/shared/agentic_harness/git_guard.py)**: Asegurar que el script tiene permisos para ejecutar comandos git locales (`git add`, `git commit`, `git reset`).

### 3. Definir los Prompts del Generador y Evaluador
Crea el archivo `evaluator_prompts.py` adaptado a las necesidades de la entrega del cliente:
*   Define el **Generador** con los tokens de diseño o directrices específicas (ej: tipografías, colores del manual de marca).
*   Define el **Evaluador** con los criterios de éxito estáticos y el formato de salida JSON estructurado.

### 4. Integración en la Capa de Orquestación (n8n o Python)
*   **En n8n (Recomendado para producción):** Crea un workflow que actúe como disparador (Webhook). Integra nodos de agentes de IA con el Generador (Gemini Flash) y el Evaluador (Claude Sonnet). Conecta los scripts de Python locales a través de nodos de ejecución de comandos.
*   **En Local (Para desarrollo interactivo):** Integra la llamada a `git_guard.py` antes de iniciar la generación de código y llama a `budget_manager.py` en cada iteración del bucle.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| `PermissionError: Presupuesto excedido` | La ejecución autónoma ha gastado más del límite configurado. | Analiza el coste de la sesión en `output/agency/api_budget.json`. Si el gasto es correcto, incrementa el parámetro `run_budget_limit` o resetea el contador llamando a `reset_run()`. |
| El código generado tiene bugs pero el Evaluador no los detecta. | Los criterios de evaluación son demasiado laxos o genéricos. | Endurece el prompt del Evaluador en `evaluator_prompts.py`, añadiendo ejemplos "few-shot" de código incorrecto para calibrar su juicio. |
| Pérdida de código manual tras una ejecución. | El script ejecutó un rollback automático sin previo aviso. | Asegúrate de hacer commit manual de tus cambios de desarrollo antes de arrancar el script agéntico. El agente solo hace rollback a su checkpoint inicial. |

---

## Decisiones clave

- **Decisión:** Usar n8n como orquestador y Python para utilidades locales.  
  **Razón:** Aporta alta vendibilidad visual al proyecto, excelente telemetría de fallos nativa y desacopla la lógica de ejecución del control de versiones.  
  **Alternativa descartada:** Todo programado en Python (descartado por la falta de interfaz visual para clientes finales no técnicos).

- **Decisión:** Usar Gemini Flash para generación y Claude Sonnet para evaluación.  
  **Razón:** Sonnet tiene un criterio de visión y originalidad excelente ("gusto" de diseño), mientras que Flash reduce los costes asociados a las iteraciones de escritura de código.

---

## Adaptación por cliente

Variables a cambiar en cada cliente:

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| Límite de coste (`run_budget_limit`) | `budget_manager.py` | $5.00 para copys de anuncios vs $25.00 para apps complejas |
| Tokens de Diseño | `evaluator_prompts.py` | Colores corporativos, fuentes oficiales |
| Criterios de Evaluación | `evaluator_prompts.py` | Añadir SEO y accesibilidad obligatorios para landings web |

---

*Última sesión que actualizó este SOP: 2026-05-26 — Creación del documento tras aprobación del plan híbrido de orquestación de Riqueza Digital.*
