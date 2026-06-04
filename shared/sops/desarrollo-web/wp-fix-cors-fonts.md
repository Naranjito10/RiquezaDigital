# SOP: Resolución de Errores CORS de Fuentes en WordPress/Elementor

**Área:** Desarrollo Web  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-04  
**Clientes donde se aplicó:** Riqueza Digital (Home CORS fix)  
**Tiempo estimado:** 10–15 minutos

---

## Resumen

Diagnóstico y resolución de bloqueos CORS (Cross-Origin Resource Sharing) en WordPress/Elementor que impiden que fuentes web externas (como Poppins o Heebo) se carguen correctamente, provocando fallos visuales y textos en tipografías por defecto del sistema.

---

## Pre-requisitos

- [ ] Acceso FTP, SSH o administrador de archivos del hosting
- [ ] Permisos de administrador de WordPress para limpiar cachés de plugins
- [ ] Acceso de consola en el navegador (F12) para ver errores de red

---

## Pasos

### 1. Detectar el Error en Consola
1. Cargar la página web afectada.
2. Abrir la Consola de Desarrollador (F12) → Pestaña **Console**.
3. Buscar errores de color rojo que digan:
   > `Access to font at 'https://dominio.com/wp-content/...' from origin 'https://www.dominio.com' has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.`
4. Identificar la diferencia entre las URLs (ej: una tiene `www.` y la otra no, o una carga por HTTP y la otra por HTTPS).

### 2. Configurar la Cabecera CORS en el Servidor
Para indicar al navegador que permita la carga de fuentes desde subdominios u orígenes cruzados del mismo sitio:

* **Opción A: Servidores Apache / Litespeed (Archivo `.htaccess`):**
   1. Abrir el archivo `.htaccess` en la raíz de WordPress.
   2. Añadir el siguiente bloque de código al inicio del archivo:
      ```apache
      # Permitir CORS para fuentes tipográficas
      <FilesMatch "\.(ttf|otf|eot|woff|woff2)$">
          <IfModule mod_headers.c>
              Header set Access-Control-Allow-Origin "*"
          </IfModule>
      </FilesMatch>
      ```
* **Opción B: Servidores Nginx (Archivo de configuración del bloque server):**
   1. Editar el archivo de configuración del sitio en Nginx (ej: `/etc/nginx/sites-available/default`).
   2. Añadir la regla dentro del bloque `server`:
      ```nginx
      location ~* \.(eot|otf|ttf|woff|woff2)$ {
          add_header Access-Control-Allow-Origin *;
      }
      ```

### 3. Sincronizar Direcciones en WordPress
Asegurarse de que WordPress no esté forzando URLs incoherentes:
1. Ir a **Ajustes → Generales**.
2. Verificar que tanto **Dirección de WordPress (URL)** como **Dirección del sitio (URL)** utilicen exactamente el mismo protocolo y subdominio (ambas con `www.` o ambas sin `www.`, y ambas con `https://`).

### 4. Regenerar Archivos de Elementor y Purgar Cachés
Elementor guarda en caché las rutas de las fuentes CSS generadas:
1. Ir a **Elementor → Herramientas → General**.
2. Hacer clic en el botón **Regenerar archivos y datos**.
3. Purgar la caché de los plugins de optimización instalados (ej: WP Fastest Cache, WP Rocket).
4. Recargar la página con `Ctrl + F5` y verificar que los errores CORS en la consola hayan desaparecido.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| El error persiste tras modificar `.htaccess` | El servidor tiene un proxy inverso (como Nginx o Cloudflare) delante que no está pasando las cabeceras | Limpiar la caché de Cloudflare y configurar las reglas de cabeceras en el panel del proxy inverso si fuera necesario |
| Error `Header cannot be set` en Apache | El módulo `mod_headers` no está activo en el servidor | Contactar con soporte de hosting para habilitar `mod_headers` o usar Opción B si dispones de VPS |

---

## Decisiones clave

- **Decisión:** Habilitar cabecera `Access-Control-Allow-Origin "*"` específica para archivos de fuentes en lugar de permitir todo de forma global.  
  **Razón:** Limitar el comodín `*` solo a las extensiones tipográficas (`.woff2`, `.ttf`, etc.) previene problemas de seguridad (como vulnerabilidades de scripts cruzados) que ocurrirían si se permitiera de forma global para todo el dominio.  
  **Alternativa descartada:** Habilitar CORS general para todos los archivos del sitio.

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| Tipo de Servidor Web | Qué archivo editar | `.htaccess` (Apache/Litespeed) vs `nginx.conf` (Nginx) |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Creación inicial del SOP de resolución de CORS para tipografías en Elementor.*
