# /sistema:buscar-sop — Buscador Inteligente de SOPs

Busca y localiza procedimientos operativos estándar (SOPs) en la biblioteca de la agencia para responder preguntas de tipo "¿cómo hacemos X?" o guiar en la ejecución de tareas.

---

## Paso 1 — Analizar la petición de búsqueda

1. Identificar el término clave, servicio o área solicitada por el usuario (ej. "WordPress", "Meta", "Google", "onboarding", "claves").

## Paso 2 — Buscar en el índice y archivos de SOPs

1. Leer el índice general de SOPs en [shared/sops/README.md](file:///c:/Users/kein-/OneDrive/Desktop/Riqueza%20Digital/shared/sops/README.md).
2. Si el término clave no se encuentra explícitamente en la tabla del índice, realizar una búsqueda recursiva rápida de archivos en `shared/sops/` buscando palabras clave en el contenido de los archivos.
3. Listar todos los SOPs que coincidan o sean relevantes para la consulta del usuario.

## Paso 3 — Presentar resultados

1. Devolver un listado ordenado de los SOPs encontrados, mostrando:
   - Nombre del SOP (con enlace directo clicable en formato `file:///` al archivo `.md`).
   - Área (Marketing, Desarrollo, Automatizaciones, Onboarding).
   - Estado actual (🌱 Draft, 🔧 Verificado, 💰 Maduro).
   - Resumen o descripción corta de para qué sirve.
2. Si se encuentra un SOP exacto y verificado/maduro, ofrecer al usuario guiarle a través de sus pasos directamente o abrir el archivo.
3. Si no se encuentra ningún SOP relevante, informar al usuario y proponer la creación de un nuevo draft basado en `shared/sops/_plantilla-sop.md` si es un proceso que se repetirá en el futuro.
