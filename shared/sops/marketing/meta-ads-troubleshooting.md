# SOP: Meta Ads Troubleshooting y Optimización

**Área:** Marketing — Meta Ads  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-04  
**Clientes donde se aplicó:** Veganashi  
**Tiempo estimado:** 15–30 minutos

---

## Resumen

Guía para diagnosticar y resolver los problemas operativos más recurrentes en campañas de Meta Ads, abarcando desde la caída de eventos de píxel hasta la solución de limitaciones en la fase de aprendizaje.

---

## Pre-requisitos

- [ ] Acceso de administrador al Business Manager de Riqueza Digital
- [ ] Acceso de socio o administrador a la cuenta publicitaria del cliente
- [ ] Token de Acceso del Sistema (System User Token) de ~60 días de duración
- [ ] Extensión "Meta Pixel Helper" instalada en Chrome (para verificación manual)

---

## Pasos

### 1. Diagnóstico de Caídas de Eventos de Pixel
Si el cliente reporta que no se están registrando conversiones o eventos en el panel de Meta:
1. Acceder al **Administrador de Eventos** de Meta y verificar el estado del Píxel.
2. Utilizar la extensión **Meta Pixel Helper** en el sitio del cliente y ejecutar la acción del evento (ej: añadir al carrito, enviar formulario).
3. Verificar si el evento se dispara en el navegador y si reporta errores (parámetros duplicados, falta de ID del evento).
4. Comprobar si la API de Conversiones (CAPI) está registrando eventos del lado del servidor (verificando la tasa de coincidencia en el Administrador de Eventos).

### 2. Resolución de Errores de Conjunto de Anuncios (`WITH_ISSUES`)
Cuando un conjunto de anuncios (Ad Set) muestra el estado `WITH_ISSUES` y no publica impresiones:
1. Identificar la causa del error. Las causas comunes suelen ser:
   - Audiencia eliminada o archivada.
   - Fecha de fin anterior a la fecha actual.
   - Tarjeta de crédito del cliente sin fondos o rechazada.
2. Si el problema es de configuración y el Administrador de Anuncios en web está lento o bloqueado, ejecutar la solución rápida mediante la API de Graph como se describe en el SOP [meta-ads-error-fix-api.md](../meta-ads-error-fix-api.md):
   ```bash
   # Actualizar la fecha de finalización o la audiencia mediante script o curl
   ```
3. Si el problema es de facturación, notificar de inmediato al cliente.

### 3. Gestión de Limitación de Aprendizaje (`Learning Limited`)
Si un conjunto de anuncios entra en el estado "Aprendizaje limitado" (no consigue 50 conversiones en 7 días):
1. **Evaluar volumen de conversión:** ¿El evento seleccionado es demasiado profundo en el embudo? (ej. Compra en lugar de Añadir al carrito).
2. **Consolidar conjuntos:** Si hay múltiples ad sets con pequeñas variaciones de audiencia, unificarlos en uno solo para concentrar el volumen de datos.
3. **Ampliar el público:** Incrementar el tamaño de la audiencia (Lookalikes más amplios, segmentación abierta).
4. **Incrementar presupuesto:** Aumentar el presupuesto diario del ad set para permitir mayor volumen de subastas.

### 4. Renovación y Rotación de Meta Access Tokens
El token de la API de Meta expira periódicamente (~60 días). Si el pipeline de monitoreo o n8n reporta error de autenticación:
1. Ir al portal de **Meta for Developers** (developers.facebook.com) → Mis aplicaciones.
2. Seleccionar la aplicación de Riqueza Digital y abrir el **Explorador de la Graph API**.
3. Seleccionar el Sistema de Usuario o generar un Token de usuario de corto plazo.
4. Convertir el token de corto plazo a un token de acceso de largo plazo (~60 días) mediante el endpoint de intercambio de Meta:
   ```bash
   curl -i -X GET "https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={short-lived-token}"
   ```
5. Registrar el nuevo token en el script de configuración de n8n o variables del servidor.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Eventos duplicados (Deduplicación fallida) | El píxel web y la API de conversiones envían el mismo evento con distintos `event_id` | Configurar el gestor de eventos (GTM o backend) para que asigne exactamente el mismo identificador único `event_id` a ambos canales |
| Error `System user token has expired` | El token del usuario del sistema en el Business Manager expiró | Regenerar el token en la configuración del Business Manager de Meta (sección de Usuarios del sistema) |
| Ad Set no arranca tras resolver error | Meta necesita unos minutos para re-evaluar y activar la campaña | Esperar de 15 a 30 minutos o forzar un cambio menor en el presupuesto para re-lanzar el validador |

---

## Decisiones clave

- **Decisión:** Priorizar el uso de la Graph API mediante consola para resolver errores críticos en lugar de depender únicamente del Ads Manager web.  
  **Razón:** El panel de control web de Meta Ads Manager es propenso a ralentizaciones extremas y bloqueos de interfaz. La API permite diagnósticos directos y fixes inmediatos.  
  **Alternativa descartada:** Esperar a que la UI de Meta cargue o reportar incidencias a soporte técnico (proceso lento).

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| Capacidad presupuestaria | Umbral para resolver learning limited | Presupuestos bajos (<10€/día) requieren consolidación agresiva de audiencias |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Creación inicial del SOP de troubleshooting y optimización de Meta Ads.*
