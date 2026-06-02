# /boveda-post — Crear contenido para La Bóveda

Crea un artículo/manual optimizado para posicionar en Google e IAs **y** convertir en cliente.
Cada pieza sigue la estructura: Problema → Solución → FAQ → CTA.

---

## Antes de empezar

Pedir al usuario (si no lo ha dado):
1. **Tema / título provisional** del artículo
2. **Keyword principal** que quiere posicionar (o derivarla del tema)
3. **Servicio o curso relacionado** al que debe derivar el CTA

Si no sabe la keyword, proponer 3 opciones con volumen estimado antes de continuar.

---

## Paso 1 — Investigación de keyword e intención

1. Identificar la **intención de búsqueda** (informacional / comparativa / transaccional)
2. Definir el **keyword principal** y 3-5 **variantes long-tail** para las FAQs
3. Comprobar si RD tiene ya contenido sobre este tema (evitar canibalización):
   - Buscar en `/boveda/` y en los posts existentes
4. Identificar **enlace interno saliente obligatorio**: qué servicio o curso de RD es más relevante

**Output de este paso:**
```
Keyword principal: [X]
Variantes long-tail: [lista]
Intención: [informacional/comparativa/transaccional]
CTA destino: [/servicios-X/ o /curso-X/]
Canibalización: [ninguna / riesgo con página Y]
```

---

## Paso 2 — Estructura del artículo

Toda pieza de la bóveda sigue esta arquitectura fija:

```
H1: [Keyword principal — título atractivo, max 60 chars]

INTRO (150-200 palabras)
- Párrafo 1: El problema concreto que resuelve este artículo
- Párrafo 2: Qué va a aprender el lector y por qué es relevante para su negocio
- NO empezar con "En este artículo..." ni frases genéricas

CUERPO (según tipo de contenido)
├── Manual paso a paso: H2 por cada paso (4-7 pasos)
├── Guía conceptual: H2 por cada concepto clave (4-6 secciones)
└── Comparativa: H2 por cada opción + tabla comparativa + recomendación

ENLACE INTERNO (obligatorio, natural)
- Mínimo 2 enlaces a páginas de RD: 1 a servicio relacionado, 1 a otro recurso de la bóveda
- Ancla descriptiva, no "haz clic aquí"

FAQ (5-7 preguntas)
- Las preguntas = long-tail keywords del Paso 1
- Formato HTML <details><summary> para schema FAQ
- Respuestas de 2-4 frases, directas

BLOQUE SUSCRIPCIÓN (placeholder hasta integrar MailerLite)
<!-- MAILERLITE_FORM -->

CTA FINAL
- Título: frase orientada al beneficio, no al servicio
- Subtítulo: propuesta de valor en 1 línea
- Botón: acción específica → enlace al servicio/curso del Paso 1
```

---

## Paso 3 — Escribir el artículo

Escribir siguiendo la estructura del Paso 2. Reglas de estilo:

- **Tono**: directo, sin jerga innecesaria, como si lo explicara un experto a un empresario ocupado
- **Párrafos**: máximo 3-4 líneas. Aéreo, fácil de escanear.
- **Negritas**: destacar 1-2 conceptos clave por sección, no palabras aleatorias
- **Listas**: usar cuando hay 3+ elementos del mismo tipo
- **Evitar**: "Como ya sabrás", "En el mundo actual", "Hoy en día", frases de relleno
- **Longitud objetivo**: 1.200-2.000 palabras (suficiente para posicionar, sin relleno)

**Para IAs (GEO):**
- Incluir al menos 1 definición explícita del concepto principal ("X es...")
- Las FAQs deben responder preguntas que alguien haría a ChatGPT/Perplexity
- Mencionar casos de uso concretos con números cuando sea posible

---

## Paso 4 — Generar el HTML

Usar el diseño system de la bóveda. Template base:

```html
<style>
.rd-post{max-width:800px;margin:0 auto;padding:0 24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1f1f2e;line-height:1.7}
.rd-post h1{font-size:2em;color:#21123D;margin-bottom:8px}
.rd-post .rd-meta{color:#8000FC;font-size:.9em;margin-bottom:32px;font-weight:600}
.rd-post h2{font-size:1.4em;color:#21123D;margin-top:40px;margin-bottom:16px;border-left:4px solid #8000FC;padding-left:12px}
.rd-post h3{font-size:1.1em;color:#21123D;margin-top:24px}
.rd-post p{margin-bottom:16px}
.rd-post ul,
.rd-post ol{padding-left:24px;margin-bottom:16px}
.rd-post li{margin-bottom:8px}
.rd-post strong{color:#21123D}
.rd-post a{color:#8000FC;text-decoration:underline}
.rd-faq-section{background:#faf8fd;border-radius:12px;padding:32px;margin:40px 0}
.rd-faq-section h2{border:none;padding:0;margin-top:0}
.rd-faq-section details{border:1.5px solid #e8e4f0;border-radius:8px;padding:14px 18px;margin-bottom:10px;background:#fff}
.rd-faq-section summary{font-weight:600;cursor:pointer;color:#21123D}
.rd-faq-section details p{margin:10px 0 0;color:#514b5f;font-size:.95em}
.rd-suscripcion{background:#f7f4fb;border:2px dashed #8000FC;border-radius:12px;padding:24px;text-align:center;margin:40px 0;color:#514b5f;font-size:.9em}
.rd-cta-final{background:linear-gradient(135deg,#21123D 0%,#2B174D 100%);color:#fff;border-radius:16px;padding:40px;text-align:center;margin-top:48px}
.rd-cta-final h2{color:#fff;font-size:1.6em;margin:0 0 12px;border:none;padding:0}
.rd-cta-final p{opacity:.9;margin:0 0 20px}
.rd-cta-final a{display:inline-block;background:#8000FC;color:#fff;font-weight:700;padding:12px 32px;border-radius:8px;text-decoration:none}
</style>

<div class="rd-post">

<h1>[TITULO H1]</h1>
<p class="rd-meta">[Categoría] &bull; [Tiempo de lectura] min</p>

[INTRO]

[CUERPO con H2/H3]

[ENLACES INTERNOS integrados de forma natural en el texto]

<div class="rd-faq-section">
<h2>Preguntas frecuentes</h2>
<details><summary>[Pregunta 1]</summary><p>[Respuesta]</p></details>
<details><summary>[Pregunta 2]</summary><p>[Respuesta]</p></details>
<details><summary>[Pregunta 3]</summary><p>[Respuesta]</p></details>
<details><summary>[Pregunta 4]</summary><p>[Respuesta]</p></details>
<details><summary>[Pregunta 5]</summary><p>[Respuesta]</p></details>
</div>

<div class="rd-suscripcion">
<!-- MAILERLITE_FORM -->
<p><strong>Recibe los próximos recursos en tu correo.</strong><br>Próximamente: suscripción directa.</p>
</div>

<div class="rd-cta-final">
<h2>[Título CTA orientado al beneficio]</h2>
<p>[Propuesta de valor en 1 línea]</p>
<a href="/[servicio-o-curso]/">[Texto botón] &#8594;</a>
</div>

</div>
```

---

## Paso 5 — Publicar en WordPress como widget HTML de Elementor

Usar `/wp-page-rd` para el patrón completo de Elementor HTML widget. El artículo debe usar el design system RD y publicarse con `_elementor_data`:

```python
import json, random, string

def make_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def elementor_html_widget(html):
    return json.dumps([{
        "id": make_id(), "elType": "section",
        "settings": {"stretch_section": "section-stretched", "layout": "full_width", "gap": "no",
                     "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}},
        "elements": [{"id": make_id(), "elType": "column",
                      "settings": {"_column_size": 100, "_inline_size": None},
                      "elements": [{"id": make_id(), "elType": "widget", "widgetType": "html",
                                    "settings": {"html": html}, "elements": []}],
                      "isInner": False}],
        "isInner": False
    }], ensure_ascii=False)

payload = {
    'title':   '[Título del artículo]',
    'slug':    '[slug-seo-friendly]',
    'parent':  6835,   # /boveda/ → URL queda como /boveda/slug/
    'status':  'draft',
    'content': '',     # Elementor ignora esto cuando _elementor_data está presente
    'meta': {
        '_elementor_edit_mode':    'builder',
        '_elementor_template_type': 'wp-page',
        '_elementor_data':          elementor_html_widget(html_content),
        'yoast_wpseo_title':        '[Título SEO | Riqueza Digital]',
        'yoast_wpseo_metadesc':     '[Meta descripción max 160 chars con keyword]',
        'yoast_wpseo_focuskw':      '[keyword principal]',
    }
}
# POST a /wp-json/wp/v2/pages
```

> **Nota slug**: usar `parent: 6835` para que los artículos queden bajo `/boveda/[slug]/`.
> La clase CSS wrapper debe ser única: `rd-bv-[slug]` (ej: `rd-bv-guia-google-ads`).

---

## Paso 6 — Actualizar el hub /boveda/

Después de publicar, añadir la card del nuevo artículo en la sección correspondiente de `/boveda/` (ID 6835):

```html
<a href="/boveda/[slug]/" class="rd-boveda-card">
  <span class="tag">[Categoría]</span>
  <h3>[Título del artículo]</h3>
  <p>[Descripción de 1-2 líneas]</p>
</a>
```

Editar la página con `POST /wp-json/wp/v2/pages/6835` actualizando el bloque de la sección correspondiente.

---

## Paso 7 — Reportar y mover a "Por hacer" en Notion

Al terminar:

```
Artículo creado: [título]
URL (draft):     https://www.riquezadigital.es/boveda/[slug]/
WP Admin:        [url]/wp-admin/post.php?post=[ID]&action=edit
Keyword:         [keyword principal]
CTA destino:     [/servicio-o-curso/]
Estado:          DRAFT — pendiente revisión Kevin
Próximo paso:    Kevin revisa y publica / Claude ajusta si hay feedback
```

Crear tarea Notion: "Revisar y publicar artículo bóveda: [título]" — asignado a Kevin.

---

## Categorías disponibles en la bóveda

| Categoría | Tag HTML | Servicios relacionados |
|-----------|----------|----------------------|
| IA + Productividad | `IA + Productividad` | /posicionamiento-ia/, cursos |
| Google Ads | `Google Ads` | /servicios-google-ads/ |
| Meta Ads | `Meta Ads` | (futuro) |
| Web + Diseño | `Web + IA` | /servicios-web-ia/ |
| Automatizaciones | `Automatizaciones` | (futuro) |
| Agente IA | `Agente IA` | /servicios-web-ia/, cursos |

---

## Checklist de calidad antes de publicar

- [ ] H1 contiene la keyword principal
- [ ] Meta descripción < 160 chars y contiene keyword
- [ ] Al menos 2 enlaces internos a servicios/cursos de RD
- [ ] FAQ con mínimo 5 preguntas en formato `<details>`
- [ ] CTA final apunta al servicio/curso más relevante
- [ ] Slug limpio (sin stopwords: de, en, la, el, y)
- [ ] Sin texto de relleno: cada párrafo aporta valor
- [ ] Card añadida al hub `/boveda/`
