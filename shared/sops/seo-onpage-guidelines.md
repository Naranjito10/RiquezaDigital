# Guía de Optimización SEO On-Page y Marcado Schema — Riqueza Digital

Este documento sirve como guía de alineación estratégica entre la dirección de Riqueza Digital y la **agencia de SEO externa**. Define las bases de la arquitectura de la información, el marcado estructurado de datos recomendado, y las mejores prácticas SEO para `riquezadigital.es`.

---

## 1. Arquitectura de Información y Palabras Clave Objetivo

Proponemos una estructura web optimizada para captar tráfico local e institucional interesado en marketing digital y automatización de procesos:

| Página (URL) | Palabra Clave Objetivo Principal | Intención de Búsqueda / Contenido |
|--------------|----------------------------------|-----------------------------------|
| `/` (Home) | Agencia de transformación digital | Marca + Propuesta de valor global (Paid media + Automatizaciones) |
| `/servicios/gestion-google-ads/` | Agencia Google Ads | Servicios de configuración y optimización de campañas de búsqueda y PMax |
| `/servicios/gestion-meta-ads/` | Agencia Meta Ads | Servicios de paid social (Instagram, Facebook Ads, captación de leads) |
| `/servicios/automatizacion-procesos/` | Automatización de procesos n8n | Creación de flujos de trabajo, integración de CRM, eliminación de tareas manuales |

---

## 2. Checklist de Optimización SEO On-Page

La agencia externa y Riqueza Digital deben asegurar la implementación de los siguientes elementos en cada página:

### A. Títulos y Meta Descripciones (Title & Description Tags)
- **Título SEO (H1 / Title Tag)**: Longitud entre 50 y 60 caracteres. Debe contener la palabra clave principal al inicio.
  - *Ejemplo Home*: `Riqueza Digital | Agencia de Transformación Digital y Paid Media`
  - *Ejemplo Google Ads*: `Agencia de Google Ads: Creación y Optimización de Campañas`
- **Meta Descripción**: Longitud entre 120 y 155 caracteres. Debe incentivar el clic (CTA) e incluir la palabra clave secundaria.
  - *Ejemplo*: `Escala tu negocio con campañas optimizadas en Google Ads y Meta Ads. Automatizamos tus procesos con n8n para multiplicar tu rentabilidad. ¡Escríbenos!`

### B. Estructura de Encabezados (Header Hierarchy)
- **H1 Único**: Un solo título `<h1>` por página que describa la temática principal.
- **Jerarquía Semántica**: Uso ordenado de `<h2>` para las secciones clave y `<h3>` para subsecciones. No saltar niveles (ej. no pasar de `<h2>` a `<h4>` directamente).

### C. Optimización de Imágenes
- Todas las imágenes deben tener un atributo **ALT** (texto alternativo) descriptivo que incorpore variaciones semánticas de palabras clave.
- Compresión de imágenes en formatos modernos (como `.webp`) y carga diferida (lazy loading).

---

## 3. Marcado de Datos Estructurados (Schema Markup JSON-LD)

Para ayudar a los motores de búsqueda a entender el propósito empresarial de Riqueza Digital y destacar en los resultados enriquecidos de Google (Rich Snippets), se debe integrar el siguiente marcado estructurado en formato **JSON-LD** en la cabecera `<head>` de la página de inicio (Home):

```json
{
  "@context": "https://schema.org",
  "@type": "ProfessionalService",
  "name": "Riqueza Digital",
  "alternateName": "RD Agency",
  "url": "https://riquezadigital.es",
  "logo": "https://riquezadigital.es/wp-content/uploads/logo.png",
  "image": "https://riquezadigital.es/wp-content/uploads/og-image.jpg",
  "description": "Agencia de transformación digital especializada en la optimización de campañas de Google Ads, Meta Ads y automatización de procesos con n8n.",
  "email": "info@riquezadigital.es",
  "address": {
    "@type": "PostalAddress",
    "addressCountry": "ES"
  },
  "sameAs": [
    "https://www.instagram.com/soyenriquerocha/"
  ],
  "knowsAbout": [
    "Google Ads Management",
    "Meta Ads Management",
    "n8n Workflow Automation",
    "CRM Integrations",
    "Digital Transformation"
  ],
  "offers": {
    "@type": "Offer",
    "itemOffered": {
      "@type": "Service",
      "name": "Gestión de Campañas Publicitarias y Automatización"
    }
  }
}
```

---

## 4. Rendimiento y Core Web Vitals (WPO)

La agencia de SEO debe verificar y optimizar el rendimiento técnico de WordPress:
1. **Velocidad de Carga**: Lograr un tiempo de carga (LCP) inferior a 2.5 segundos.
2. **Uso de Caché**: Implementación de un plugin de caché robusto (como LiteSpeed Cache o WP Rocket).
3. **Optimización de Scripts**: Retrasar la carga de scripts de analítica (como el píxel de Facebook o Google Analytics) hasta la primera interacción del usuario para no penalizar la velocidad de renderizado inicial.
