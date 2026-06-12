# Auditoría Técnica Web: SEO On-Page y Velocidad — Veganashi
**Fecha de ejecución:** 2026-06-03  
**Plataforma analizada:** WordPress REST API  
**Web:** https://veganashi.es  

--- 

## 1. Análisis SEO On-Page de Páginas Clave

### 📄 Home (ID: 50)
- **URL:** [https://www.veganashi.es/](https://www.veganashi.es/)
- **Yoast SEO Title:** `Veganashi | Primer Restaurante de Sushi Sin Azúcar en Barcelona` (✅ Actualizado vía API 2026-06-03)
- **Yoast Meta Desc:** `Disfruta del primer y único sushi vegano y sin azúcar de Barcelona. Elaborado con ingredientes 100% naturales, saludables y libres de crueldad. ¡Reserva mesa!` (✅ Actualizado vía API 2026-06-03)
- **Estado de publicación:** `publish`

#### Estructura de Encabezados (Jerarquía)
- **H1 único:** ❌ **ERROR: No se detectó ningún encabezado H1 en el contenido.**
- **Encabezados H2/H3:** Se detectaron 6 H2s y 3 H3s.
  - *Ejemplos H2:*
    - `La evolución`
    - `Desafiamos lo Convencional`
    - `Desafiamos lo Convencional`
    - `¡Veganashi es el primer y único restaurante de sushi sin azucar!`

#### Optimización de Imágenes
- **Imágenes totales en el contenido:** 11
- **Textos alternativos (ALT):** ⚠️ **Advertencia: 11 de 11 imágenes (100.0%) no tienen el atributo ALT configurado.**
  - *Imágenes críticas sin ALT (primeras 3):*
    - URL: `https://www.veganashi.es/wp-content/uploads/2026/02/home-1.webp...` | Clase: `attachment-large size-large wp-image-4317`
    - URL: `https://www.veganashi.es/wp-content/uploads/2026/02/home-2.webp...` | Clase: `attachment-large size-large wp-image-4314`
    - URL: `https://www.veganashi.es/wp-content/uploads/2025/01/img-home_06.png...` | Clase: `attachment-large size-large wp-image-170`

---

### 📄 Reservar mesa (ID: 4857)
- **URL:** [https://www.veganashi.es/reservar-mesa/](https://www.veganashi.es/reservar-mesa/)
- **Yoast SEO Title:** `Reservar Mesa | Restaurante Veganashi Barcelona` (✅ Actualizado vía API 2026-06-03)
- **Yoast Meta Desc:** `Reserva tu mesa online de forma rápida y sencilla en Veganashi, tu restaurante de sushi vegano y saludable en Barcelona. ¡Te esperamos!` (✅ Actualizado vía API 2026-06-03)
- **Estado de publicación:** `publish`

#### Estructura de Encabezados (Jerarquía)
- **H1 único:** ❌ **ERROR: No se detectó ningún encabezado H1 en el contenido.**
- **Encabezados H2/H3:** Se detectaron 0 H2s y 0 H3s.

#### Optimización de Imágenes
- **Imágenes totales en el contenido:** 0
- **Textos alternativos (ALT):** No se detectaron imágenes directamente en el cuerpo HTML de la página.

---

### 📄 Gracias (ID: 383)
- **URL:** [https://www.veganashi.es/gracias/](https://www.veganashi.es/gracias/)
- **Yoast SEO Title:** `¡Gracias por tu Reserva! | Veganashi Barcelona` (✅ Actualizado vía API 2026-06-03)
- **Yoast Meta Desc:** `Tu mesa en Veganashi ha sido reservada correctamente. Esperamos que disfrutes de la evolución consciente del sushi en Barcelona.` (✅ Actualizado vía API 2026-06-03)
- **Estado de publicación:** `publish`

#### Estructura de Encabezados (Jerarquía)
- **H1 único:** ❌ **ERROR: No se detectó ningún encabezado H1 en el contenido.**
- **Encabezados H2/H3:** Se detectaron 0 H2s y 2 H3s.

#### Optimización de Imágenes
- **Imágenes totales en el contenido:** 1
- **Textos alternativos (ALT):** ⚠️ **Advertencia: 1 de 1 imágenes (100.0%) no tienen el atributo ALT configurado.**
  - *Imágenes críticas sin ALT (primeras 3):*
    - URL: `https://www.veganashi.es/wp-content/uploads/2025/01/img-gracias_01.png...` | Clase: `attachment-large size-large wp-image-385`

---

## 2. Diagnóstico de Rendimiento (WPO) y Carga de Scripts

Al auditar las cabeceras y scripts incluidos en el HTML de las páginas principales:
1. **Carga de scripts de analítica:** Se detectan los scripts de seguimiento globales integrados en el HTML.
2. **Plugins de optimización detectados (activos):**
   - Realmente no se listan plugins de caché conocidos como *LiteSpeed Cache* o *WP Rocket* entre los plugins activos.
   - **ACCIÓN:** Se recomienda encarecidamente instalar y configurar un plugin de caché (ej. **WP Rocket** o **LiteSpeed Cache** según el servidor, o un plugin gratuito como **W3 Total Cache** o **WP Super Cache**) para optimizar el tiempo hasta el primer byte (TTFB) y reducir el LCP a menos de 2.5s.
3. **Scripts de Google Tag Manager (GTM-WMDJQKLF):** Se detecta correctamente insertado en el cuerpo y cabecera de la web.
4. **Scripts de Meta Pixel:** La integración se realiza mediante el plugin oficial *Meta Pixel for WordPress*, lo que inyecta el script automáticamente. Sin embargo, esto se cruza con las etiquetas de GTM, como se describe en el reporte de conversiones.
