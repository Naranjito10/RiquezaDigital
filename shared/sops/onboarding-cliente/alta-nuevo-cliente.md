# SOP: Alta e Incorporación de Nuevo Cliente (Onboarding)

**Área:** Onboarding Cliente  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-04  
**Clientes donde se aplicó:** Tecniclima, Veganashi, Keller  
**Tiempo estimado:** 20–30 minutos (setup inicial) + 4 sesiones estratégicas (F-001)

---

## Resumen

Establece el procedimiento operativo y administrativo para registrar a un nuevo cliente en los sistemas de Riqueza Digital, inicializar sus repositorios de información y activar el proceso estratégico de la agencia.

---

## Pre-requisitos

- [ ] Contrato firmado y primer pago confirmado
- [ ] Datos fiscales y de contacto del cliente
- [ ] Acceso a las cuentas publicitarias y sitios web del cliente

---

## Pasos

### 1. Inicialización en el Workspace Local
Para estandarizar el workspace de cada cliente, ejecutar el comando `/clientes:nuevo-cliente` de Claude Code o realizar los siguientes pasos manuales:
1. Crear el directorio del cliente en `clients/<nombre_del_cliente>/` (en minúsculas y kebab-case).
2. Crear la estructura interna de subcarpetas:
   ```
   clients/<cliente>/
   ├── strategy/        ← Entregables de estrategia F-001
   ├── reports/         ← Reportes semanales/mensuales
   ├── proposals/       ← Propuestas comerciales
   └── marketing/       ← Datos de campañas
       ├── meta/
       └── google/
   ```
3. Copiar la plantilla del perfil de cliente desde `clients/_template/profile.md` a `clients/<cliente>/profile.md` y rellenar toda la información de contacto, sector y objetivos del negocio.
4. Copiar la plantilla de control de horas de trabajo desde `clients/_template/imputacion-horas.md` a `clients/<cliente>/imputacion-horas.md`.

### 2. Registro del Cliente en el Orquestador
1. Abrir el archivo [CLAUDE.md](file:///c:/Users/kein-/OneDrive/Desktop/Riqueza%20Digital/CLAUDE.md).
2. Localizar la sección **CLIENTES** y añadir una nueva línea en la tabla de clientes con:
   - Nombre (en negrita)
   - Sector
   - Servicios activos
   - Prioridad
3. Guardar el archivo. Esto asegura que Claude reconozca al cliente como una entidad válida en las aperturas de sesión.

### 3. Configuración Segura de Credenciales y APIs
1. **Regla Crítica:** Nunca escribir contraseñas reales ni API keys dentro del archivo `profile.md` (ya que se sube al repositorio Git).
2. Las credenciales de APIs (Meta, Google, WordPress, etc.) deben guardarse en el archivo local `.env` (excluido de Git) o directamente en el Registro de Windows (`HKCU\Environment`) siguiendo las instrucciones del SOP [gestion-claves-api-windows.md](../gestion-claves-api-windows.md).
3. En `profile.md`, en la sección de credenciales, apuntar únicamente a los nombres de las variables de entorno asociadas (ej. "Usa la variable de entorno `WP_CLIENTE_URL`").

### 4. Alta en Notion (CRM y Tareas)
1. Acceder al Notion corporativo de Riqueza Digital.
2. En la base de datos de **Clientes**, registrar la ficha del cliente completando los datos de contacto, facturación, fecha de inicio y estado (`Onboarding`).
3. En la base de datos de **Proyectos**, crear un proyecto asociado y mapear los entregables iniciales.

### 5. Ejecución del Pack de Onboarding Estratégico (F-001)
El primer paso de trabajo real con el cliente es definir su rumbo estratégico. Utilizar la carpeta `shared/prompts/onboarding-estrategico/` para correr las 4 sesiones secuenciales con el cliente (o con el Fundador usando la información recopilada):
1. **Sesión 1 (Brief Estratégico):** Descubrir la propuesta de valor y modelo de negocio. Guardar output en `clients/<cliente>/strategy/brief-estrategico.md`.
2. **Sesión 2 (Estudio de Mercado):** Analizar competidores y públicos objetivos. Guardar en `clients/<cliente>/strategy/estudio-mercado.md`.
3. **Sesión 3 (PRD de Virales):** Configurar el detector de contenidos virales. Guardar en `clients/<cliente>/strategy/prd-deteccion-virales.md`.
4. **Sesión 4 (Plan de Marketing Inbound):** Diseñar el funnel completo. Guardar en `clients/<cliente>/strategy/plan-marketing-inbound.md`.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| El cliente no aparece en los comandos de Claude | No se añadió a la tabla de clientes en `CLAUDE.md` | Añadir el registro exacto a la tabla del archivo raíz `CLAUDE.md` y guardar |
| Fuga de credenciales en Git | Se escribieron contraseñas reales en `profile.md` | Eliminar el historial del commit inmediatamente con un rebase interactivo y regenerar las contraseñas expuestas. Seguir el SOP de gestión de claves de Windows |
| El cliente no responde al Brief estratégico | Falta de foco en las preguntas | Reducir el Brief a 5 preguntas clave de negocio y agendar una llamada rápida de 20 min en lugar de enviarlo por email |

---

## Decisiones clave

- **Decisión:** Mantener una estructura de carpetas local unificada por cliente bajo Git.  
  **Razón:** Facilita que Claude Code pueda leer el contexto histórico completo, auditorías pasadas y reportes directamente sin depender de conexiones lentas de bases de datos externas.  
  **Alternativa descartada:** Almacenar reportes y entregables únicamente en Notion o Google Drive (hace al agente ciego ante los trabajos previos).

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| Tipo de negocio | Foco de la carpeta de marketing | B2B Lead Gen (no requiere WooCommerce setup) vs E-commerce (requiere CAPI y datalayers de compra) |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Creación inicial del SOP de alta y onboarding de nuevo cliente.*
