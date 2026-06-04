# SOP: WordPress Setup para Nuevo Cliente

**Área:** Desarrollo Web  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-04  
**Clientes donde se aplicó:** Keller, Riqueza Digital  
**Tiempo estimado:** 30–45 minutos

---

## Resumen

Este proceso establece la configuración base de WordPress para un nuevo cliente de forma que quede optimizado para SEO, analítica y conectividad con los agentes autónomos de Riqueza Digital mediante la REST API.

---

## Pre-requisitos

- [ ] Hosting del cliente activo (Siteground, Hostinger, Vercel, etc.)
- [ ] Acceso de administrador al panel de control de WordPress
- [ ] Acceso a la gestión DNS del dominio del cliente (Cloudflare, GoDaddy, etc.)

---

## Pasos

### 1. Configuración de DNS y Dominio
1. Apuntar los registros A del dominio del cliente a la IP del hosting.
2. Habilitar SSL (HTTPS) forzado desde el panel de control del hosting (ej. Let's Encrypt).
3. En Ajustes de WordPress → Generales: verificar que la Dirección de WordPress (URL) y Dirección del sitio (URL) comiencen con `https://`.

### 2. Ajustes Básicos de WordPress
1. **Ajustes → Lectura:** Asegurarse de que la casilla *"Disuadir a los motores de búsqueda de indexar este sitio"* esté **desmarcada** (salvo en entornos de desarrollo temporales).
2. **Ajustes → Enlaces permanentes:** Seleccionar la opción **"Nombre de la entrada"** (`/%postname%/`) para urls amigables SEO.

### 3. Instalación de Plugins Esenciales
Instalar y activar los siguientes plugins en WordPress:

* **Yoast SEO** o **RankMath**: Para optimización on-page, sitemaps XML y edición de metadatos.
* **GTM4WP (Google Tag Manager for WordPress)** por Thomas Geiger:
  1. Ir a Ajustes → Google Tag Manager.
  2. Introducir el ID de GTM (`GTM-XXXXXX`).
  3. Elegir el contenedor en el footer (seguro y recomendado) o custom.
  4. Habilitar la integración de WooCommerce en la pestaña de integración si el sitio es un e-commerce para datalayers automáticos.
* **Application Passwords** (Incluido en el core desde WP 5.6): Permite la integración directa con Claude Code y scripts Python.

### 4. Configurar Usuario API y Credenciales
Para permitir que Claude Code u otros agentes (como `/web:wp-edit`) operen en la web:
1. Ir a **Usuarios → Añadir nuevo**.
2. Crear un usuario con rol de **Editor** (o Administrador si requiere configurar plugins) llamado `riqueza-digital`.
3. Editar el usuario recién creado, hacer scroll hasta la sección **Contraseñas de aplicación**.
4. Añadir una nueva contraseña llamada `Claude Agent Connection` y copiar la contraseña generada (de 24 caracteres, sin los espacios).
5. Registrar la configuración en el Registro de Windows siguiendo el SOP [gestion-claves-api-windows.md](../gestion-claves-api-windows.md):
   - `WP_<CLIENTE>_URL`
   - `WP_<CLIENTE>_USER`
   - `WP_<CLIENTE>_APP_PASSWORD`

### 5. Verificar Conexión API
Ejecutar una consulta rápida desde la consola de Claude Code usando `curl` o el script de python para comprobar que el endpoint responde:

```bash
# Probar conexión al endpoint de posts (reemplazar variables o usar valores reales)
curl -s -u "WP_USER:WP_APP_PASSWORD" "https://dominio-cliente.com/wp-json/wp/v2/posts?per_page=1"
```

**Resultado esperado:** JSON con el último artículo publicado. Si devuelve un error `401 Unauthorized`, revisar que la contraseña de aplicación no contenga espacios intermedios y que el servidor no tenga bloqueadas las peticiones de cabecera de autorización.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Error 401 Unauthorized en llamadas API | Contraseña de aplicación copiada con espacios o el servidor bloquea cabecera Authorization | Introducir la clave sin espacios. Si persiste, añadir regla en `.htaccess` para forzar el paso de cabeceras de autorización de Apache |
| GTM4WP no inyecta el script | El tema de WordPress no tiene la llamada a `wp_body_open()` | Cambiar el método de inserción en GTM4WP a "Manual" y pegar el script en el header.php del child theme |
| URLs devuelven error 404 tras cambio de enlaces | El archivo `.htaccess` no se actualizó automáticamente | Ir a Ajustes → Enlaces permanentes y hacer clic en Guardar cambios sin modificar nada para regenerar el `.htaccess` |

---

## Decisiones clave

- **Decisión:** Usar el plugin GTM4WP en lugar de inyectar scripts en el tema.  
  **Razón:** GTM4WP inyecta de forma limpia la capa de datos (datalayer) para e-commerce y eventos del usuario, facilitando la analítica en Meta Ads y Google Ads sin necesidad de escribir código custom.  
  **Alternativa descartada:** Scripts hardcodeados en el archivo `header.php` (difíciles de mantener, se borran al actualizar temas).

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| WooCommerce activo | Requiere datalayer avanzado en GTM4WP | Activar ecommerce datalayer en pestaña Integración |
| Servidor Nginx puro | Permisos de reescritura | Configurar reglas en archivo de config de Nginx, no en `.htaccess` |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Creación inicial del SOP de configuración de WordPress para clientes.*
