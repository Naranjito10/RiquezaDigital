# Auditoría de Conversiones y Plugins de Seguimiento — Veganashi
**Fecha de ejecución:** 2026-06-03  
**Web:** https://veganashi.es  

--- 

## 1. Auditoría de Plugins de Seguimiento Activos

Hemos analizado los plugins de WordPress y detectado los siguientes elementos relacionados con analítica y conversiones:

### 🔴 Meta for WooCommerce (`facebook-for-woocommerce`) — **ACTIVO**
- **Propósito:** Enlaza automáticamente la tienda de WooCommerce con el catálogo e inyecta el píxel de Meta para eventos de ecommerce (ViewContent, AddToCart, InitiateCheckout, Purchase).
- **Diagnóstico:** Si la web es principalmente un restaurante y no realiza ventas transaccionales directas (compras) de productos físicos en la web, este plugin está enviando eventos redundantes de comercio electrónico.
- **Riesgo de Duplicidad:** Si también tienes configurado el píxel de Meta en GTM o a través del plugin oficial de Meta Pixel, este plugin genera duplicidad de eventos. **Se recomienda desactivarlo si no se utiliza el catálogo de productos de Facebook Shops o Instagram Shopping.**

### 🔴 Meta pixel for WordPress (`official-facebook-pixel`) — **ACTIVO**
- **Propósito:** Inyecta de forma global el código básico de Meta Pixel (`PageView`) y permite medir conversiones estándar.
- **Riesgo de Duplicidad:** Si ya estás gestionando y disparando la etiqueta del Píxel de Meta a través de **Google Tag Manager (GTM)**, mantener este plugin activo duplicará el evento de `PageView` y las conversiones básicas. 
- **Recomendación:** Desactivar este plugin y centralizar el Píxel de Meta al 100% en GTM para controlar exactamente cuándo y cómo se disparan los eventos (respetando las preferencias del banner de cookies).

### 🟢 GTM4WP - Google Tag Manager for WordPress — **ACTIVO**
- **Propósito:** Inserta el código de GTM (ID: `GTM-WMDJQKLF` detectado en frontend) y prepara un dataLayer robusto.
- **Recomendación:** Mantener activo. Es la mejor herramienta para centralizar la analítica de la web y pasar datos limpios al dataLayer.

### 🟡 WooCommerce — **ACTIVO**
- **Propósito:** Sistema de ecommerce de WordPress.
- **Evaluación de uso:** Vemos páginas publicadas como `/tienda/`, `/carrito/`, `/finalizar-compra/` y `/tarjeta-regalo/`. Si únicamente se venden Tarjetas Regalo de forma esporádica, se debe vigilar que el píxel de Meta de WooCommerce no se dispare a menos que sea una compra real. Si no hay pasarela de pago activa y las tarjetas regalo no se compran online, WooCommerce se puede desactivar para limpiar la web y acelerar la velocidad.
- **Acción:** Kevin debe confirmar si los clientes pueden comprar tarjetas regalo online directamente o si es meramente informativo.

--- 

## 2. Integración de Conversiones con CoverManager y GTM

Para medir correctamente las reservas sin duplicidades ni redirecciones complejas, el flujo ideal es integrar **Google Tag Manager directamente en el motor de CoverManager** en lugar de forzar redirecciones web. 
### A. Cómo integrar GTM en CoverManager (Recomendado)
1. **Obtén tu ID de GTM:** El ID de contenedor de Veganashi es **`GTM-WMDJQKLF`**.
2. **Solicita la instalación a CoverManager:**
   - Envía un email a [hospitality@covermanager.com](mailto:hospitality@covermanager.com) solicitando que inyecten tu contenedor **`GTM-WMDJQKLF`** en tu motor de reservas de CoverManager.
   - Esto cargará automáticamente GTM dentro de su iframe/widget.
3. **El dataLayer de CoverManager:** Una vez integrado GTM en su sistema, CoverManager envía automáticamente un evento al dataLayer cuando se completa una reserva con éxito. El evento suele llamarse:
   - `booking_success` o `reservation_confirmed` (puedes verificarlo en el modo Preview de GTM al hacer una reserva de prueba).
4. **Configura el Disparador en GTM:**
   - Crea un activador de tipo **Evento Personalizado (Custom Event)**.
   - Nombre del evento: `booking_success` (o el nombre que aparezca en el dataLayer en el preview).
5. **Configura la Etiqueta de Meta Ads en GTM:**
   - Crea una etiqueta con el código del Píxel de Meta para registrar el evento de conversión (ej. `Lead` o un evento personalizado `ReservaMesa`).
   - Asigna el activador creado en el punto 4 para que se dispare únicamente cuando finalice la reserva dentro de CoverManager.

### B. Opción Alternativa: Redirección Física a una Página de Gracias
Si prefieres forzar una redirección física tras la reserva a una URL propia:
1. **Redirección desde CoverManager:** Debes solicitar al soporte de CoverManager que configure una **URL de retorno (Return/Redirect URL)** tras la reserva con éxito.
2. **Página de destino:** Utilizaremos la página que hemos creado en WordPress: **`https://www.veganashi.es/reserva-realizada/`**.
3. **Medición en GTM:**
   - En tu contenedor de GTM principal (`GTM-WMDJQKLF`), configuras una etiqueta de conversión (Google Ads, Meta Pixel `Lead`, etc.).
   - Activador: Vista de una página (Page View) donde la URL de la página contiene `/reserva-realizada/`.
   - *Nota:* Este método es más propenso a pérdidas de datos (si el usuario cierra la pestaña antes de que cargue la redirección), por lo que recomendamos la integración directa de GTM dentro de CoverManager (Opción A).

---

## 3. Análisis Técnico del Contenedor GTM de Veganashi (`GTM-WMDJQKLF`)

Al analizar la exportación de tu contenedor GTM, identificamos la estructura de tags y la raíz del problema de sobremedición:

### A. Diagnóstico de Etiquetas Activas en GTM
*   **Google Analytics 4:** Tienes la etiqueta de Google configurada con el ID de medición `G-L1D1GCJ37T`.
*   **Seguimiento de Reservas (GA4 / Google Ads):**
    *   Existe la etiqueta **`Google Analytics booking_done`** (evento `booking_done`).
    *   Existe la etiqueta **`GA4 - Reservar Mesa`** (evento `reservar`).
    *   Existe la etiqueta de Google Ads **`RESERVA`** (ID: `594567713`, Label: `-fQWCNrxs5QcEKHEwZsC`), que se dispara en el activador `52` (relacionado con confirmación de reserva).
*   **Píxel de Meta & Conversions API (CAPI):**
    *   Tienes una etiqueta HTML personalizada **`Meta Pixel ID 2735587510055839`** activa para medir `PageView` en todas las páginas.
    *   Tienes configurada la integración de **Conversions API de Facebook (CAPI)** mediante un servidor de Server-Side Tagging en `https://server-side-tagging-khjrhe3cdq-uc.a.run.app`. Esto se implementa con las etiquetas:
        *   `FB_CONVERSIONS_API-2735587510055839-Web-Tag-GA4_Config`
        *   `FB_CONVERSIONS_API-2735587510055839-Web-Tag-GA4_Event`
        *   `FB_CONVERSIONS_API-2735587510055839-Web-Tag-Pixel_Event`
        *   `FB_CONVERSIONS_API-2735587510055839-Web-Tag-Pixel_Setup`
        *   `FB_CONVERSIONS_API-2735587510055839-Web-Tag-ParamBuilder`

### B. Por qué se están duplicando/triplicando las conversiones de Meta
El multi-conteo se debe a que la inyección del píxel de Meta ocurre por **tres vías independientes** al mismo tiempo:
1.  **GTM (Client-Side & Server-Side CAPI):** Inyecta el píxel `2735587510055839` y dispara PageViews y eventos a través de la infraestructura cloud.
2.  **Plugin de WordPress `Meta pixel for WordPress`:** Inserta de nuevo de forma rígida el píxel en el código HTML de todas las páginas, disparando duplicados de `PageView`.
3.  **Plugin de WordPress `Meta for WooCommerce`:** Inserta de nuevo el píxel e inyecta eventos de compra y checkout automáticos para WooCommerce.

### C. Solución Paso a Paso para una Medición Limpia
Para resolver las duplicidades y centralizar la medición en GTM:
1.  **Desactiva los dos plugins de WordPress:** `Meta pixel for WordPress` y `Meta for WooCommerce`.
2.  **Mantén WooCommerce activo únicamente si es necesario:** Si no se procesan pagos de WooCommerce en la web y las tarjetas de regalo son meramente informativas, WooCommerce está sobrecargando la web. Pero si decides mantenerlo, apagar el plugin específico de *Meta for WooCommerce* es obligatorio.
3.  **Configura el evento "Lead" o "Reserva" en GTM:**
    *   Crea una etiqueta de Meta Pixel en GTM (usando la plantilla oficial de Meta o una etiqueta HTML personalizada).
    *   Configúrala para enviar el evento estándar `Lead` (o el evento personalizado `ReservaMesa`).
    *   Utiliza como activador el mismo que ya dispara la etiqueta **`Google Analytics booking_done`** o el de la etiqueta de Google Ads **`RESERVA`**.
    *   De este modo, tanto Google Ads, GA4 como Meta Ads medirán en el mismo instante y bajo el mismo disparador único, controlable desde GTM y compatible con Cookiebot.

