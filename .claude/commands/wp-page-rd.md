# /wp-page-rd — Crear página WordPress con el design system de Riqueza Digital

Crea cualquier página nueva (servicio, landing, hub, manual) usando el widget HTML de Elementor y el sistema de diseño unificado de RD. Las páginas son editables desde Elementor → "Editar HTML".

---

## Cómo funciona (mecanismo técnico)

WordPress guarda el contenido de Elementor en el meta `_elementor_data` (accesible vía REST API). Para que la página se abra como "Editar HTML" en Elementor hay que:

1. Enviar `_elementor_edit_mode: "builder"` en el meta
2. Enviar `_elementor_data` con una estructura JSON que contenga un widget `html`
3. El campo `content` se deja vacío (Elementor lo ignora cuando `_elementor_data` está presente)

```python
import json, random, string

def make_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def elementor_html_widget(html_content):
    """Wraps HTML in a full-width Elementor HTML widget. Returns JSON string."""
    # CRITICAL: fix any double-brace CSS artifacts from Python template strings
    html_content = html_content.replace('{{', '{').replace('}}', '}')
    return json.dumps([{
        "id": make_id(),
        "elType": "section",
        "settings": {
            "stretch_section": "section-stretched",
            "layout": "full_width",
            "gap": "no",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [{
            "id": make_id(),
            "elType": "column",
            "settings": {"_column_size": 100, "_inline_size": None},
            "elements": [{
                "id": make_id(),
                "elType": "widget",
                "widgetType": "html",
                "settings": {"html": html_content},
                "elements": []
            }],
            "isInner": False
        }],
        "isInner": False
    }], ensure_ascii=False)

# Crear o actualizar página
payload = {
    'title': 'Título de la página',
    'slug': 'slug-url',
    'status': 'draft',       # siempre draft para revisar primero
    'content': '',
    'meta': {
        '_elementor_edit_mode': 'builder',
        '_elementor_template_type': 'wp-page',
        '_elementor_data': elementor_html_widget(FULL_HTML_CONTENT),
        'yoast_wpseo_title': 'Título SEO | Riqueza Digital',
        'yoast_wpseo_metadesc': 'Meta descripción max 160 chars.',
        'yoast_wpseo_focuskw': 'keyword principal',
    }
}
# POST a /wp-json/wp/v2/pages (crear) o /wp-json/wp/v2/pages/{ID} (actualizar)
```

---

## Design system RD — CSS base

Pegar al inicio de `FULL_HTML_CONTENT`. Reemplazar `{CLS}` por la clase del wrapper de la página (ej: `rd-google-ads`, `rd-boveda`, `rd-home`).

```css
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,800;1,9..144,300;1,9..144,400&family=Inter+Tight:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

.{CLS} {
  --rd-dark: #21123D;
  --rd-dark-2: #2B174D;
  --rd-purple: #8000FC;
  --rd-blue: #0530FA;
  --rd-pink: #E300FF;
  --rd-white: #ffffff;
  --rd-text: #1f1f2e;
  --rd-text-2: #514b5f;
  --rd-muted: #6f6f80;
  --rd-border: #e8e4f0;
  --rd-soft: #f7f4fb;
  --rd-soft-2: #faf8fd;
  --rd-font-display: 'Fraunces', 'Times New Roman', serif;
  --rd-font-body: 'Inter Tight', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --rd-font-mono: 'JetBrains Mono', "SFMono-Regular", Consolas, monospace;
  width: 100vw !important;
  max-width: 100vw !important;
  margin-left: calc(50% - 50vw) !important;
  margin-right: calc(50% - 50vw) !important;
  background: #fff !important;
  color: var(--rd-text) !important;
  font-family: var(--rd-font-body) !important;
  overflow-x: hidden;
}
.{CLS}, .{CLS} * { box-sizing: border-box; }
.{CLS}-container { width: min(1200px, calc(100% - 48px)); margin: 0 auto; }
```

---

## Componentes disponibles

### Hero (fondo oscuro degradado)

```html
<div class="{CLS}-hero">
  <!-- Rejilla decorativa -->
  <div style="position:absolute;inset:0;
    background-image:linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px);
    background-size:56px 56px;
    -webkit-mask-image:radial-gradient(ellipse at center,black 30%,transparent 80%);
    pointer-events:none;"></div>
  
  <div class="{CLS}-container" style="position:relative;z-index:2;">
    <!-- Badge eyebrow -->
    <span style="display:inline-flex;align-items:center;gap:10px;margin-bottom:20px;
      padding:7px 16px;border-radius:999px;background:rgba(255,255,255,0.08);
      border:1px solid rgba(255,255,255,0.14);color:rgba(255,255,255,0.85);
      font-family:var(--rd-font-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;">
      <span style="width:6px;height:6px;background:var(--rd-pink);border-radius:50%;
        box-shadow:0 0 10px var(--rd-pink);animation:{CLS}-pulse 2s infinite;"></span>
      Etiqueta · Subtipo
    </span>

    <h1 style="font-size:clamp(36px,5vw,62px);line-height:1.04;letter-spacing:-0.04em;
      font-weight:800;margin:0 0 20px;color:#fff;font-family:var(--rd-font-body);">
      Título principal con <em style="font-family:var(--rd-font-display);font-style:italic;
        font-weight:400;background:linear-gradient(90deg,#fff 0%,#d4b3ff 40%,#f13fff 90%);
        -webkit-background-clip:text;background-clip:text;color:transparent;">parte cursiva.</em>
    </h1>

    <p style="font-size:17px;line-height:1.6;color:rgba(255,255,255,0.8);max-width:620px;margin:0 0 32px;">
      Descripción del servicio o recurso en 1-2 frases.
    </p>

    <div style="display:flex;gap:14px;flex-wrap:wrap;">
      <!-- Botón primario -->
      <a href="/contacto/" style="display:inline-flex;align-items:center;gap:10px;
        min-height:50px;padding:0 28px;border-radius:999px;text-decoration:none;
        font-size:14px;font-weight:700;
        background:linear-gradient(90deg,var(--rd-blue),var(--rd-purple),var(--rd-pink));
        color:#fff;box-shadow:0 14px 30px rgba(128,0,252,.3);">
        CTA principal &#8594;
      </a>
      <!-- Botón ghost (opcional) -->
      <a href="#seccion" style="display:inline-flex;align-items:center;gap:10px;
        min-height:50px;padding:0 28px;border-radius:999px;text-decoration:none;
        font-size:14px;font-weight:700;
        background:rgba(255,255,255,0.07);border:1px solid rgba(255,255,255,0.18);
        color:#fff;backdrop-filter:blur(10px);">
        Ver más
      </a>
    </div>
  </div>
</div>
```

**CSS del hero (añadir en el `<style>`):**
```css
.{CLS}-hero {
  background: radial-gradient(circle at 8% 20%, rgba(255,255,255,0.07), transparent 18%),
              radial-gradient(circle at 92% 18%, rgba(255,255,255,0.07), transparent 20%),
              linear-gradient(135deg, #21123D 0%, #35115f 50%, #4b0b68 100%);
  color: #fff;
  padding: 80px 20px 72px;
  position: relative;
  overflow: hidden;
}
@keyframes {CLS}-pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.4); }
}
```

---

### Grid de cards

```html
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:20px;">
  <div style="padding:26px;border-radius:18px;background:#fff;
    border:1.5px solid var(--rd-border);transition:transform .35s,border-color .3s,box-shadow .3s;">
    <!-- Tag -->
    <span style="display:inline-flex;padding:5px 12px;border-radius:999px;margin-bottom:12px;
      background:rgba(128,0,252,.09);color:var(--rd-purple);
      font-family:var(--rd-font-mono);font-size:10px;font-weight:600;letter-spacing:.1em;text-transform:uppercase;">
      Categoría
    </span>
    <h3 style="font-size:17px;font-weight:700;color:#20152f;margin:0 0 10px;letter-spacing:-.02em;">
      Título con <em style="font-family:var(--rd-font-display);font-style:italic;
        font-weight:400;color:var(--rd-purple);">cursiva opcional.</em>
    </h3>
    <p style="font-size:14px;color:var(--rd-text-2);margin:0;line-height:1.6;">Descripción breve.</p>
  </div>
</div>
```

---

### Card oscura (para secciones de audiencia o destaque)

```html
<div style="padding:40px;border-radius:24px;color:#fff;
  background:radial-gradient(circle at 86% 16%,rgba(227,0,255,.22),transparent 28%),
  linear-gradient(135deg,#21123D 0%,#32155b 54%,#4b0b68 100%);
  overflow:hidden;position:relative;">
  <!-- Rejilla decorativa interna -->
  <div style="position:absolute;inset:0;
    background-image:linear-gradient(rgba(255,255,255,0.04) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.04) 1px,transparent 1px);
    background-size:48px 48px;
    -webkit-mask-image:radial-gradient(ellipse at right top,black 0%,transparent 60%);
    pointer-events:none;"></div>
  <div style="position:relative;z-index:1;">
    <h2 style="font-size:clamp(24px,3vw,34px);font-weight:800;color:#fff;margin:0 0 14px;">
      Título <em style="font-family:var(--rd-font-display);font-style:italic;font-weight:400;
        background:linear-gradient(90deg,#fff,#f13fff);-webkit-background-clip:text;
        background-clip:text;color:transparent;">cursiva.</em>
    </h2>
    <p style="color:rgba(255,255,255,.8);font-size:15px;line-height:1.65;margin:0 0 24px;">Texto.</p>
    <!-- Lista con checks -->
    <ul style="list-style:none;padding:0;margin:0;display:grid;gap:12px;">
      <li style="display:flex;gap:12px;align-items:flex-start;color:rgba(255,255,255,.85);font-size:14px;font-weight:500;">
        <span style="flex:0 0 22px;height:22px;border-radius:50%;
          background:linear-gradient(135deg,var(--rd-blue),var(--rd-pink));
          color:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;">&#10003;</span>
        <span>Punto de la lista</span>
      </li>
    </ul>
  </div>
</div>
```

---

### FAQ con acordeón

```html
<div style="max-width:820px;margin:0 auto;">
  <details style="border:1.5px solid var(--rd-border);border-radius:12px;
    padding:16px 20px;margin-bottom:12px;background:var(--rd-soft-2);">
    <summary style="font-weight:600;cursor:pointer;color:#20152f;font-size:15px;
      list-style:none;display:flex;justify-content:space-between;">
      Pregunta de ejemplo
      <span style="color:var(--rd-purple);font-size:20px;font-weight:400;">+</span>
    </summary>
    <p style="margin:14px 0 0;color:var(--rd-text-2);font-size:14px;line-height:1.65;">Respuesta aquí.</p>
  </details>
</div>
```

---

### CTA final (fondo oscuro con rejilla)

```html
<div style="padding:56px;border-radius:24px;display:grid;
  grid-template-columns:1.4fr 0.6fr;gap:40px;align-items:center;
  background:radial-gradient(circle at 82% 18%,rgba(227,0,255,.26),transparent 28%),
  radial-gradient(circle at 10% 80%,rgba(5,48,250,.2),transparent 32%),
  linear-gradient(135deg,#21123D 0%,#32155b 52%,#4b0b68 100%);
  box-shadow:0 24px 60px rgba(33,18,61,.16);overflow:hidden;position:relative;">
  
  <div style="position:absolute;inset:0;
    background-image:linear-gradient(rgba(255,255,255,0.03) 1px,transparent 1px),
    linear-gradient(90deg,rgba(255,255,255,0.03) 1px,transparent 1px);
    background-size:48px 48px;pointer-events:none;"></div>
  
  <div style="position:relative;z-index:1;">
    <h2 style="font-size:clamp(26px,3.4vw,40px);font-weight:800;color:#fff;
      margin:0 0 12px;letter-spacing:-.04em;">
      Título CTA con <em style="font-family:var(--rd-font-display);font-style:italic;font-weight:400;
        background:linear-gradient(90deg,#fff,#f13fff);-webkit-background-clip:text;
        background-clip:text;color:transparent;">cursiva.</em>
    </h2>
    <p style="color:rgba(255,255,255,.82);font-size:15px;margin:0;line-height:1.6;">Propuesta de valor.</p>
  </div>
  
  <div style="position:relative;z-index:1;display:flex;flex-direction:column;gap:14px;">
    <a href="/contacto/" style="display:inline-flex;align-items:center;gap:10px;
      min-height:50px;padding:0 28px;border-radius:999px;text-decoration:none;
      font-size:14px;font-weight:700;
      background:linear-gradient(90deg,var(--rd-blue),var(--rd-purple),var(--rd-pink));
      color:#fff;box-shadow:0 14px 30px rgba(128,0,252,.3);">
      CTA &#8594;
    </a>
    <!-- Metadata monospaced -->
    <div style="color:rgba(255,255,255,.6);font-family:var(--rd-font-mono);
      font-size:11px;letter-spacing:.07em;text-transform:uppercase;display:flex;flex-direction:column;gap:6px;">
      <span style="display:flex;align-items:center;gap:8px;">
        <span style="width:5px;height:5px;background:var(--rd-pink);border-radius:50%;"></span>
        Punto de confianza 1
      </span>
    </div>
  </div>
</div>
```

---

### JavaScript de reveal on scroll

Añadir antes de `</section>` en cualquier página. Cambiar `{CLS}` por la clase del wrapper.

```html
<script>
(function() {
  var items = document.querySelectorAll('.{CLS}-reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) {
        if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); }
      });
    }, { threshold: 0.08, rootMargin: '0px 0px -50px 0px' });
    items.forEach(function(el) { io.observe(el); });
  } else {
    items.forEach(function(el) { el.classList.add('in-view'); });
  }
})();
</script>
```

**CSS para los elementos reveal (añadir en `<style>`):**
```css
.{CLS}-reveal {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity .8s cubic-bezier(.16,1,.3,1), transform .8s cubic-bezier(.16,1,.3,1);
}
.{CLS}-reveal.in-view { opacity: 1; transform: translateY(0); }
```

---

### Partículas en el hero (opcional — para páginas de alto impacto)

Ver el código completo en `/programar-forma-agentica/` (ID 6546) o en el Manual de Claudia (ID 6805). Requiere un `<canvas>` dentro del hero con `id` único.

---

## Responsive básico

Añadir siempre al final del `<style>`:

```css
@media (max-width: 860px) {
  .{CLS}-final-cta-grid { grid-template-columns: 1fr !important; padding: 36px; }
}
@media (max-width: 600px) {
  .{CLS}-grid { grid-template-columns: 1fr !important; }
  .{CLS}-hero { padding: 60px 20px; }
  .{CLS}-btn { width: 100%; justify-content: center; }
}
```

---

## Páginas existentes para referencia

| Página | ID | Clase CSS | Notas |
|--------|----|-----------|-------|
| Programar de forma agéntica | 6546 | `rd-taller-ia` | Referencia completa con partículas |
| Manual de Claudia | 6805 | `rd-manual-claudia` | Partículas + diseño editorial |
| La Bóveda | 6835 | `rd-boveda` | Hub con grid de cards |
| Web con IA Agéntica | 6836 | `rd-web-ia` | Página de servicio |
| Posicionamiento en IAs | 6837 | `rd-pos-ia` | Página de servicio GEO |

---

## Checklist antes de publicar

- [ ] Clase wrapper única (no colisiona con otra página)
- [ ] CSS variables definidas en `.{CLS}` (no en `:root` — evita conflictos)
- [ ] `width: 100vw` + `margin-left: calc(50% - 50vw)` para full bleed
- [ ] Todos los elementos `.{CLS}-reveal` tienen CSS de reveal + JS añadido
- [ ] Meta SEO configurados: title (max 60), metadesc (max 160), focuskw
- [ ] `status: 'draft'` al crear — revisar antes de publicar
- [ ] Responsive: testar en 360px, 768px y 1280px

---

## Referencia de scripts existentes

- `output/agency/wp_update_elementor_pages.py` — Actualiza las 3 páginas principales con RD design system
- `output/agency/wp_create_service_pages.py` — Crea páginas de servicio (patrón antiguo sin Elementor)
- `output/agency/wp_create_tos.py` — Crea páginas legales simples
