# Plan de Mejora Web — riquezadigital.es

**Creado:** 2026-06-02  
**Basado en:** auditoría técnica + inventario de páginas + plugins activos  
**Ejecutor:** Claude Code vía `/web:wp-edit` + Kevin (decisiones estratégicas)

---

## Resumen ejecutivo

El sitio tiene una base sólida (Elementor, Yoast SEO, GTM, WP Fastest Cache) pero arrastraba varios problemas críticos ya corregidos y tiene un backlog técnico/SEO claro. Priorizados en 4 niveles.

---

## ✅ Ya corregido

| Fix | ID/Slug | Fecha | Notas |
|-----|---------|-------|-------|
| Aviso Legal: finalidad "Restaurante" → descripción correcta | ID 6450 | 2026-06-02 | Era un texto de plantilla genérica |
| Página Términos y Condiciones creada | ID 6826 / `/terminos-y-condiciones/` | 2026-06-02 | Requerida para Google Ads API |
| T&C añadido al footer | — | 2026-06-03 | Kevin lo hizo manualmente en Elementor |
| Blog off-brand eliminado (6 posts + página /blog) | IDs 6355-6360, 6405 | 2026-06-03 | Posts de consultoría industrial sin tráfico |
| Páginas draft de prueba eliminadas | 5664, 5940, 6817, 6818 | 2026-06-03 | Kevin limpió manualmente |
| Menú actualizado: Servicios dropdown + Bóveda | Menu ID 8 | 2026-06-03 | 3 hijos bajo Servicios; Manual NbLM quitado del menú |
| Bóveda creada: hub de recursos y manuales | ID 6835 / `/boveda/` | 2026-06-03 | Design system RD, Elementor HTML widget |
| Página /servicios-web-ia/ creada | ID 6836 | 2026-06-03 | Web con IA Agéntica — service page |
| Página /posicionamiento-ia/ creada | ID 6837 | 2026-06-03 | GEO — service page |

---

## 🔴 CRÍTICO — Hacer esta semana

### 1. Añadir T&C al menú de footer
La página `/terminos-y-condiciones/` está publicada pero no aparece en el menú legal del footer. Añadir al mismo menú donde están Aviso Legal, Política de Privacidad y Cookies.
- **Cómo:** WP Admin → Apariencia → Menús → Menú footer → añadir página "Términos y Condiciones"
- **Responsable:** Kevin (o Claude via REST API si el menú tiene ID conocido)

### 2. Publicar `/servicios-google-ads/` con datos reales
Draft ID 6822 está listo en estructura y SEO. Solo falta reemplazar benchmarks genéricos por datos reales de Tecniclima.
- **Bloqueante:** Kevin proporciona leads/mes y CPL de Tecniclima
- **Responsable:** Kevin (datos) → Claude (actualiza y publica)

### 3. Eliminar páginas draft de prueba
Los drafts sin usar contaminan el CMS y pueden indexarse accidentalmente.

| ID | Slug | Acción |
|----|------|--------|
| 5940 | prueba-pop-pup | Eliminar |
| 5664 | prueba | Eliminar |
| 5796 | pagina-registro | Revisar con Kevin antes de eliminar |
| 6817 | (sin slug - "Aviso Legal") | Eliminar — duplicado |
| 6818 | (sin slug - "Aviso Legal") | Eliminar — duplicado |
- **Responsable:** Kevin confirma → Claude ejecuta vía `/web:wp-edit`

---

## 🟠 ALTA — Hacer este mes

### 4. Seguridad: revisar WP File Manager
El plugin `WP File Manager` permite navegar y editar archivos del servidor desde el navegador. Es una superficie de ataque importante si alguien obtiene acceso al admin.
- **Opción A:** Desinstalar si no se usa activamente (recomendado)
- **Opción B:** Restringir acceso con contraseña adicional o limitarlo a IP
- **Responsable:** Kevin decide; si desinstalar → lo hace desde WP Admin o Claude via API

### 5. Seguridad: pro-elements (Elementor Pro Clone)
`pro-elements` es una versión gratuita de Elementor Pro mantenida por terceros. Funciona pero tiene riesgo de desactualizaciones y no está soportada por Elementor oficial.
- **Opción A:** Migrar a Elementor Pro legítimo (coste ~€69/año) — elimina el riesgo y accedes a soporte
- **Opción B:** Mantener y vigilar actualizaciones manualmente
- **Responsable:** Kevin decide

### 6. SEO: meta títulos y descripciones en todas las páginas
Verificar que cada página publicada tiene title tag y meta description configurados en Yoast.
Páginas prioritarias: Home, Empresa, Cursos, páginas de cursos individuales, Blog.
- **Herramienta:** Yoast SEO → Search Appearance → cada página
- **Responsable:** Claude puede hacer el audit via REST API + proponer textos; Kevin aprueba

### 7. Schema markup en la Home
La Home carece de `LocalBusiness` + `Organization` schema. Añadir via Yoast (Settings → Schema) o bloque HTML.

```json
{
  "@context": "https://schema.org",
  "@type": "LocalBusiness",
  "name": "Riqueza Digital Solutions SLU",
  "url": "https://www.riquezadigital.es",
  "email": "info@riquezadigital.es",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "C/Riera de Sant Andreu 90, Local",
    "addressLocality": "Barcelona",
    "postalCode": "08030",
    "addressCountry": "ES"
  },
  "serviceType": ["Marketing Digital", "Google Ads", "Meta Ads", "Desarrollo Web", "Formación IA"]
}
```
- **Responsable:** Claude añade vía `/web:wp-edit` en la Home (ID de la Home: 6676)

### 8. GTM + Site Kit: verificar no hay doble tracking
Ambos plugins están activos. Si Site Kit está enviando eventos a GA4 Y GTM también tiene el tag de GA4, los conversiones se pueden contar doble.
- **Acción:** Entrar en GTM → verificar qué tags hay → si GA4 via GTM está activo, desactivar el de Site Kit o viceversa
- **Responsable:** Kevin revisa en GTM; Claude puede documentar la configuración final

---

## 🟡 MEDIA — Backlog técnico/SEO

### 9. WP Fastest Cache: verificar configuración
Comprobar que el caché está bien configurado: versión móvil activada, exclusiones para páginas con formularios (Contacto), integración con CDN si existe.

### 10. Imágenes: alt texts y WebP
- Todas las imágenes del sitio deben tener alt text descriptivo (SEO + accesibilidad)
- Convertir a WebP para mejor rendimiento (Smush, ShortPixel o Imagify — el que elija Kevin)
- **Impacto:** mejora LCP (Core Web Vitals) y posicionamiento

### 11. Core Web Vitals — audit PageSpeed
Correr PageSpeed Insights en las páginas clave (Home, Empresa, Cursos) y documentar scores actuales.
- **Objetivo:** LCP < 2.5s, CLS < 0.1, FID < 100ms
- **Herramienta:** `https://pagespeed.web.dev/` o Lighthouse

### 12. Enlazado interno
Añadir enlaces internos desde:
- Home → páginas de servicios (Google Ads, desarrollo web)
- Posts del blog → páginas de servicios relevantes
- Empresa → Contacto
Esto mejora el flujo de usuarios y el SEO interno.

### 13. Eliminar plugin inactivo: All-in-One WP Migration
Está inactivo. Si no se va a usar, mejor eliminarlo — reduce superficie de ataque y peso del admin.
- **Responsable:** Kevin elimina desde WP Admin → Plugins

### 14. Breadcrumbs
Activar los breadcrumbs de Yoast en páginas interiores y blog. Mejora navegación y aparece en resultados de Google (rich snippets).
- **Cómo:** Yoast → Appearance → Breadcrumbs → activar

### 15. Sitemap XML — verificar envío a GSC
Yoast genera automáticamente `/sitemap_index.xml`. Verificar que está enviado en Google Search Console.
- **Responsable:** Kevin verifica en GSC

---

## 🟢 BAJA — A futuro

### 16. Plugin de redirecciones
Cuando se cambien slugs o se eliminen páginas, se necesita un plugin de redirecciones para evitar 404s. Yoast Premium incluye esta función; alternativamente el plugin gratuito `Redirection`.

### 17. Página `/servicios/` o hub de servicios
Actualmente no hay una página que agrupe todos los servicios. Podría ser útil para SEO y para el flujo de usuario: Home → /servicios/ → servicio específico.

### 18. Sección de casos de éxito / testimonios
Añadir a la Home o en una página dedicada resultados de clientes (Tecniclima, Veganashi) con métricas reales. Alto impacto en conversión.

### 19. Chat o widget de contacto rápido
Un chat de WhatsApp flotante (ej. plugin `WP Social Chat`) o un botón fijo de WhatsApp mejoraría la captación de leads desde el sitio.

### 20. Postiz self-hosted
Para automatizar la publicación de contenido en redes sociales desde el sistema agéntico sin depender de SaaS externos. (P3.2 del plan inbound)

---

## Inventario de plugins (estado actual)

| Plugin | Estado | Acción recomendada |
|--------|--------|-------------------|
| Adapta RGPD | Activo | Mantener (gestiona cookies) |
| All-in-One WP Migration | **Inactivo** | **Eliminar** |
| Classic Editor | Activo | Mantener (compatibilidad) |
| Contact Form 7 | Activo | Mantener (formulario contacto) |
| Duplicate Page | Activo | Mantener (utilidad) |
| Elementor | Activo | Mantener |
| GTM4WP | Activo | Verificar no hay doble GA4 |
| Hostinger Migrator | **Inactivo** | **Eliminar** |
| Imunify Security | Activo | Mantener |
| pro-elements | Activo | ⚠️ Revisar (ver punto 5) |
| Site Kit by Google | Activo | Verificar no hay doble GA4 |
| WordPress Importer | Activo | Revisar si hace falta |
| WPCode Lite | Activo | Mantener (inserta snippets header/footer) |
| WP Consent API | Activo | Mantener (integración con Adapta RGPD) |
| WP Fastest Cache | Activo | Verificar configuración |
| WP File Manager | Activo | ⚠️ Revisar / Eliminar (ver punto 4) |
| WP SVG Images | Activo | Mantener |
| Yoast SEO | Activo | Mantener + configurar bien |

**Tema activo:** Hello Elementor — correcto para sitios Elementor.

---

## Cómo ejecutar este plan

1. **Claude ejecuta:** Puntos 2 (cuando Kevin da datos), 6 (audit SEO), 7 (schema markup Home), mediante `/web:wp-edit`
2. **Kevin ejecuta desde WP Admin:** Puntos 1 (footer menú), 3 (eliminar drafts tras confirmar), 8 (GTM audit), 13-14-15
3. **Kevin decide + Claude ejecuta:** Puntos 4 (File Manager), 5 (pro-elements)
4. **Sesión dedicada:** Puntos 9-12 (Core Web Vitals + performance audit)

---
*Última actualización: 2026-06-02*
