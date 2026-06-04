# SOP: Resolución de Error HTTP 500 por Elementor Corrompido vía Base de Datos

**Área:** Desarrollo Web  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-04  
**Clientes donde se aplicó:** Riqueza Digital  
**Tiempo estimado:** 10–15 minutos

---

## Resumen

Procedimiento de emergencia para recuperar un sitio de WordPress con error HTTP 500 originado por Elementor (especialmente por la corrupción del campo `_elementor_data` en metadatos de post) realizando una reparación directa en la base de datos sin hooks, plugins ni la UI.

---

## Pre-requisitos

- [ ] Acceso a la base de datos de WordPress (vía phpMyAdmin, cPanel, SSH o plugin WPCode/PHP ejecutor activo)
- [ ] Conocer el ID del post o página que está causando el error HTTP 500
- [ ] Haber tomado un backup rápido de la tabla `wp_postmeta` antes de ejecutar cambios directos

---

## Pasos

### 1. Diagnosticar el Error
Cuando el sitio arroja HTTP 500 tras guardar una página en Elementor:
1. Activar el modo debug de WordPress en `wp-config.php`:
   ```php
   define( 'WP_DEBUG', true );
   define( 'WP_DEBUG_LOG', true );
   define( 'WP_DEBUG_DISPLAY', false );
   ```
2. Revisar el archivo `wp-content/debug.log` para encontrar el error exacto. Si el error menciona fallos en Yoast SEO o Elementor procesando `_elementor_data` debido a arrays mal estructurados u objetos vacíos, el archivo de metadatos está corrompido.

### 2. Identificar el Registro Corrompido
1. Acceder a la consola SQL de la base de datos.
2. Localizar el registro conflictivo buscando por el ID de la página afectada (ej: ID `6835`):
   ```sql
   SELECT * FROM wp_postmeta 
   WHERE post_id = 6835 
     AND meta_key = '_elementor_data';
   ```
3. Copiar el valor actual (normalmente un JSON serializado gigante) y guardarlo en un bloc de notas local como respaldo.

### 3. Reparación Quirúrgica en Base de Datos
Para bypassear el bucle de error y evitar que Elementor/Yoast rompan el renderizado:
* **Opción A (Desde WPCode / Script PHP ejecutor):**
  Ejecutar el siguiente script PHP para limpiar el JSON corrompido forzando a Elementor a guardar una estructura vacía inicial:
  ```php
  global $wpdb;
  $post_id = 6835; // Reemplazar con ID real
  $wpdb->update(
      $wpdb->postmeta,
      array('meta_value' => '[]'), // Array JSON vacío válido
      array('post_id' => $post_id, 'meta_key' => '_elementor_data')
  );
  ```
* **Opción B (Consulta SQL Directa):**
  ```sql
  UPDATE wp_postmeta 
  SET meta_value = '[]' 
  WHERE post_id = 6835 
    AND meta_key = '_elementor_data';
  ```

### 4. Validar Recuperación
1. Limpiar los transitorios de WordPress y la caché del servidor (WP Fastest Cache u otros).
2. Intentar cargar la página en el navegador. Debería abrirse en blanco (sin error 500) mostrando la cabecera y el pie.
3. Entrar a Elementor y restaurar la página a una versión anterior utilizando el historial de revisiones nativo de Elementor.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| El cambio se revierte solo al abrir el editor | La caché del navegador o del servidor (ej. Redis/Varnish) tiene almacenado el estado HTTP 500 | Purgar la caché del servidor de forma completa y abrir en una ventana de incógnito |
| Se pierde todo el diseño de la página | Escribir `[]` borra el diseño activo de Elementor | Es normal. Este paso es para revivir el sitio; la restauración del diseño real debe hacerse desde el historial de revisiones interno de Elementor o desde un backup de la tabla SQL |

---

## Decisiones clave

- **Decisión:** Usar `$wpdb->update` directo en lugar de `update_post_meta()`.  
  **Razón:** La función nativa `update_post_meta()` dispara hooks que cargan Elementor y Yoast en memoria, lo que causaría de nuevo el desbordamiento de pila y el error HTTP 500. La consulta directa a DB bypasser de forma segura todos los hooks.  
  **Alternativa descartada:** Borrar el plugin de Elementor temporalmente (inestable, puede romper configs globales).

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| Prefijo de tablas | Nombre de la tabla en SQL | `wp_postmeta` vs `wp_rd_postmeta` |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Creación del SOP tras la reparación de HTTP 500 en la Bóveda.*
