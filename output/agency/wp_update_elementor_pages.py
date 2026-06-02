"""
Update existing pages to use Elementor HTML widget with full RD design system.
Pages: /boveda/ (6835), /servicios-web-ia/ (6836), /posicionamiento-ia/ (6837)
"""
import urllib.request, base64, json, os, sys, random, string
sys.stdout.reconfigure(encoding='utf-8')

url = os.environ['WP_RD_URL']
user = os.environ['WP_RD_USER']
pwd = os.environ['WP_RD_APP_PASSWORD']
token = base64.b64encode(f'{user}:{pwd}'.encode()).decode()
h = {'Authorization': f'Basic {token}', 'Content-Type': 'application/json; charset=utf-8'}

def make_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def elementor_html_widget(html_content):
    """Wrap HTML in a full-width Elementor HTML widget. Returns JSON string."""
    sid, cid, wid = make_id(), make_id(), make_id()
    return json.dumps([{
        "id": sid,
        "elType": "section",
        "settings": {
            "stretch_section": "section-stretched",
            "layout": "full_width",
            "gap": "no",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [{
            "id": cid,
            "elType": "column",
            "settings": {"_column_size": 100, "_inline_size": None},
            "elements": [{
                "id": wid,
                "elType": "widget",
                "widgetType": "html",
                "settings": {"html": html_content},
                "elements": []
            }],
            "isInner": False
        }],
        "isInner": False
    }], ensure_ascii=False)

RD_CSS_BASE = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,800;1,9..144,300;1,9..144,400&family=Inter+Tight:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

.{cls} {
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
.{cls}, .{cls} * { box-sizing: border-box; }
.{cls}-container { width: min(1200px, calc(100% - 48px)); margin: 0 auto; }
.{cls}-hero {
  background: radial-gradient(circle at 8% 20%, rgba(255,255,255,0.07), transparent 18%),
              radial-gradient(circle at 92% 18%, rgba(255,255,255,0.07), transparent 20%),
              linear-gradient(135deg, #21123D 0%, #35115f 50%, #4b0b68 100%);
  color: #fff; padding: 80px 20px 72px; position: relative; overflow: hidden;
}
.{cls}-hero-grid {
  background-image: linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 56px 56px;
  -webkit-mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
  mask-image: radial-gradient(ellipse at center, black 30%, transparent 80%);
  position: absolute; inset: 0; pointer-events: none;
}
.{cls}-eyebrow {
  display: inline-flex; align-items: center; gap: 10px; margin-bottom: 20px;
  padding: 7px 16px; border-radius: 999px;
  background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.14);
  color: rgba(255,255,255,0.85) !important; font-family: var(--rd-font-mono) !important;
  font-size: 11px !important; letter-spacing: .12em; text-transform: uppercase; font-weight: 500 !important;
}
.{cls}-eyebrow-dot {
  width: 6px; height: 6px; background: var(--rd-pink); border-radius: 50%;
  box-shadow: 0 0 10px var(--rd-pink); animation: {cls}-pulse 2s infinite;
}
@keyframes {cls}-pulse { 0%,100%{{ opacity:1; transform:scale(1); }} 50%{{ opacity:.5; transform:scale(1.4); }} }
.{cls}-hero h1 {
  font-size: clamp(36px, 5vw, 62px) !important; line-height: 1.04 !important;
  letter-spacing: -0.04em !important; font-weight: 800 !important; margin: 0 0 20px !important;
  color: #fff !important; font-family: var(--rd-font-body) !important; max-width: 860px;
}
.{cls}-hero h1 em {
  font-family: var(--rd-font-display) !important; font-style: italic; font-weight: 400 !important;
  background: linear-gradient(90deg, #fff 0%, #d4b3ff 40%, #f13fff 90%);
  -webkit-background-clip: text; background-clip: text; color: transparent !important;
}
.{cls}-hero-lead {
  font-size: 17px !important; line-height: 1.6 !important; color: rgba(255,255,255,0.8) !important;
  max-width: 620px; margin: 0 0 32px !important; font-weight: 400 !important;
}
.{cls}-btn {
  display: inline-flex; align-items: center; gap: 10px; min-height: 50px; padding: 0 28px;
  border-radius: 999px; border: 0; text-decoration: none !important; font-size: 14px !important;
  font-weight: 700 !important; font-family: var(--rd-font-body) !important;
  background: linear-gradient(90deg, var(--rd-blue), var(--rd-purple), var(--rd-pink)) !important;
  color: #fff !important; box-shadow: 0 14px 30px rgba(128,0,252,.3);
  transition: transform .2s, box-shadow .2s;
}
.{cls}-btn:hover {{ transform: translateY(-2px); box-shadow: 0 18px 36px rgba(227,0,255,.35); color: #fff !important; }}
.{cls}-btn-ghost {
  background: rgba(255,255,255,0.07) !important; border: 1px solid rgba(255,255,255,0.18) !important;
  box-shadow: none !important; backdrop-filter: blur(10px);
}
.{cls}-btn-ghost:hover {{ background: rgba(255,255,255,0.13) !important; border-color: var(--rd-pink) !important; }}
.{cls}-actions {{ display: flex; gap: 14px; flex-wrap: wrap; align-items: center; }}
.{cls}-section {{ padding: 80px 0; }}
.{cls}-section-soft {{ background: var(--rd-soft) !important; }}
.{cls}-section-title {{ max-width: 760px; margin: 0 auto 48px; text-align: center; }}
.{cls}-level {{ display: inline-flex; align-items: center; gap: 10px; margin-bottom: 14px; }}
.{cls}-level-line {{ width: 32px; height: 2px; background: linear-gradient(90deg, var(--rd-blue), var(--rd-pink)); }}
.{cls}-level span {{ color: var(--rd-purple) !important; text-transform: uppercase; letter-spacing: .12em; font-size: 11px !important; font-weight: 600 !important; font-family: var(--rd-font-mono) !important; }}
.{cls}-section-title h2 {{
  font-size: clamp(28px, 4vw, 46px) !important; line-height: 1.06 !important;
  letter-spacing: -0.04em !important; font-weight: 800 !important; margin: 0 0 14px !important;
  color: #20152f !important; font-family: var(--rd-font-body) !important;
}}
.{cls}-section-title h2 em {{
  font-family: var(--rd-font-display) !important; font-style: italic; font-weight: 400 !important; color: var(--rd-purple) !important;
}}
.{cls}-section-title p {{ color: var(--rd-text-2) !important; font-size: 16px !important; line-height: 1.65 !important; margin: 0 !important; }}
.{cls}-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 20px; }}
.{cls}-card {{
  padding: 26px; border-radius: 18px; background: #fff !important;
  border: 1.5px solid var(--rd-border); transition: transform .35s cubic-bezier(.16,1,.3,1), border-color .3s, box-shadow .3s;
}}
.{cls}-card:hover {{ transform: translateY(-3px); border-color: rgba(128,0,252,.22); box-shadow: 0 16px 40px rgba(33,18,61,.06); }}
.{cls}-card-tag {{
  display: inline-flex; padding: 5px 12px; border-radius: 999px; margin-bottom: 12px;
  background: rgba(128,0,252,.09); color: var(--rd-purple) !important;
  font-family: var(--rd-font-mono) !important; font-size: 10px !important;
  font-weight: 600 !important; letter-spacing: .1em; text-transform: uppercase;
}}
.{cls}-card h3 {{ font-size: 17px !important; font-weight: 700 !important; color: #20152f !important; margin: 0 0 10px !important; letter-spacing: -.02em; font-family: var(--rd-font-body) !important; }}
.{cls}-card h3 em {{ font-family: var(--rd-font-display) !important; font-style: italic; font-weight: 400 !important; color: var(--rd-purple) !important; }}
.{cls}-card p {{ font-size: 14px !important; color: var(--rd-text-2) !important; margin: 0 !important; line-height: 1.6 !important; }}
.{cls}-card a {{ text-decoration: none !important; color: inherit !important; display: block; }}
.{cls}-dark-card {{
  padding: 40px; border-radius: 24px; color: #fff;
  background: radial-gradient(circle at 86% 16%, rgba(227,0,255,.22), transparent 28%),
              linear-gradient(135deg, #21123D 0%, #32155b 54%, #4b0b68 100%) !important;
  overflow: hidden; position: relative;
}}
.{cls}-dark-card::before {{
  content: ""; position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  -webkit-mask-image: radial-gradient(ellipse at right top, black 0%, transparent 60%);
  mask-image: radial-gradient(ellipse at right top, black 0%, transparent 60%);
  pointer-events: none;
}}
.{cls}-dark-card > * {{ position: relative; z-index: 1; }}
.{cls}-dark-card h2 {{
  font-size: clamp(24px, 3vw, 34px) !important; font-weight: 800 !important; color: #fff !important;
  margin: 0 0 14px !important; letter-spacing: -.035em !important; font-family: var(--rd-font-body) !important; line-height: 1.1 !important;
}}
.{cls}-dark-card h2 em {{
  font-family: var(--rd-font-display) !important; font-style: italic; font-weight: 400 !important;
  background: linear-gradient(90deg, #fff, #f13fff); -webkit-background-clip: text; background-clip: text; color: transparent !important;
}}
.{cls}-dark-card p {{ color: rgba(255,255,255,.8) !important; font-size: 15px !important; line-height: 1.65 !important; margin: 0 0 24px !important; }}
.{cls}-check-list {{ list-style: none; padding: 0; margin: 0; display: grid; gap: 12px; }}
.{cls}-check-list li {{ display: flex; gap: 12px; align-items: flex-start; color: rgba(255,255,255,.85) !important; font-size: 14px !important; font-weight: 500 !important; }}
.{cls}-check {{ flex: 0 0 22px; height: 22px; border-radius: 50%; background: linear-gradient(135deg, var(--rd-blue), var(--rd-pink)); color: #fff !important; display: flex; align-items: center; justify-content: center; font-size: 11px !important; font-weight: 700 !important; margin-top: 1px; }}
.{cls}-steps {{ list-style: none; padding: 0; margin: 0; counter-reset: steps; }}
.{cls}-steps li {{
  counter-increment: steps; padding: 20px 20px 20px 68px; position: relative;
  border-left: 3px solid var(--rd-purple); margin-bottom: 14px;
  background: var(--rd-soft-2); border-radius: 0 14px 14px 0;
}}
.{cls}-steps li::before {{
  content: counter(steps); position: absolute; left: 18px; top: 20px;
  background: var(--rd-purple); color: #fff; width: 30px; height: 30px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 13px;
}}
.{cls}-steps li strong {{ color: #20152f; display: block; margin-bottom: 4px; font-size: 15px; }}
.{cls}-steps li p {{ margin: 0 !important; color: var(--rd-text-2) !important; font-size: 14px !important; line-height: 1.55 !important; }}
.{cls}-stat-box {{
  border: 2px solid var(--rd-purple); border-radius: 18px; padding: 32px;
  background: linear-gradient(135deg, var(--rd-soft) 0%, var(--rd-soft-2) 100%) !important;
  text-align: center; margin-bottom: 32px;
}}
.{cls}-stat-box .big {{ font-size: 3em; font-weight: 800; color: var(--rd-purple); display: block; margin-bottom: 6px; font-family: var(--rd-font-display) !important; font-style: italic; }}
.{cls}-stat-box p {{ color: var(--rd-text-2) !important; margin: 0 !important; font-size: 1.05em !important; }}
.{cls}-faq-section {{ padding: 72px 0; }}
.{cls}-faq-section h2 {{
  font-size: clamp(26px, 3.5vw, 40px) !important; font-weight: 800 !important;
  color: #20152f !important; margin: 0 0 32px !important; letter-spacing: -.04em !important;
  font-family: var(--rd-font-body) !important; text-align: center;
}}
.{cls}-faq-section h2 em {{ font-family: var(--rd-font-display) !important; font-style: italic; font-weight: 400 !important; color: var(--rd-purple) !important; }}
.{cls}-faq-list {{ max-width: 820px; margin: 0 auto; }}
.{cls}-faq-list details {{ border: 1.5px solid var(--rd-border); border-radius: 12px; padding: 16px 20px; margin-bottom: 12px; background: var(--rd-soft-2) !important; }}
.{cls}-faq-list details[open] {{ border-color: var(--rd-purple); }}
.{cls}-faq-list summary {{ font-weight: 600; cursor: pointer; color: #20152f !important; font-size: 15px !important; font-family: var(--rd-font-body) !important; list-style: none; display: flex; justify-content: space-between; align-items: center; gap: 12px; }}
.{cls}-faq-list summary::after {{ content: "+"; color: var(--rd-purple); font-size: 20px; font-weight: 400; flex-shrink: 0; transition: transform .2s; }}
.{cls}-faq-list details[open] summary::after {{ transform: rotate(45deg); }}
.{cls}-faq-list details p {{ margin: 14px 0 0 !important; color: var(--rd-text-2) !important; font-size: 14px !important; line-height: 1.65 !important; }}
.{cls}-final-cta {{
  padding: 56px; border-radius: 24px; display: grid; grid-template-columns: 1.4fr 0.6fr; gap: 40px; align-items: center;
  background: radial-gradient(circle at 82% 18%, rgba(227,0,255,.26), transparent 28%),
              radial-gradient(circle at 10% 80%, rgba(5,48,250,.2), transparent 32%),
              linear-gradient(135deg, #21123D 0%, #32155b 52%, #4b0b68 100%) !important;
  box-shadow: 0 24px 60px rgba(33,18,61,.16); overflow: hidden; position: relative;
}}
.{cls}-final-cta::before {{
  content: ""; position: absolute; inset: 0;
  background-image: linear-gradient(rgba(255,255,255,0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,0.03) 1px, transparent 1px);
  background-size: 48px 48px; pointer-events: none;
}}
.{cls}-final-cta > * {{ position: relative; z-index: 1; }}
.{cls}-final-cta h2 {{
  font-size: clamp(26px, 3.4vw, 40px) !important; font-weight: 800 !important; color: #fff !important;
  margin: 0 0 12px !important; letter-spacing: -.04em !important; font-family: var(--rd-font-body) !important;
}}
.{cls}-final-cta h2 em {{
  font-family: var(--rd-font-display) !important; font-style: italic; font-weight: 400 !important;
  background: linear-gradient(90deg, #fff, #f13fff); -webkit-background-clip: text; background-clip: text; color: transparent !important;
}}
.{cls}-final-cta p {{ color: rgba(255,255,255,.82) !important; font-size: 15px !important; margin: 0 !important; line-height: 1.6 !important; }}
.{cls}-final-action {{ display: flex; flex-direction: column; gap: 14px; }}
.{cls}-final-meta {{ color: rgba(255,255,255,.6) !important; font-family: var(--rd-font-mono) !important; font-size: 11px !important; letter-spacing: .07em; text-transform: uppercase; display: flex; flex-direction: column; gap: 6px; }}
.{cls}-final-meta span {{ display: flex; align-items: center; gap: 8px; }}
.{cls}-final-meta span::before {{ content: ""; width: 5px; height: 5px; background: var(--rd-pink); border-radius: 50%; flex-shrink: 0; }}
.{cls}-chips {{ display: flex; flex-wrap: wrap; gap: 8px; margin-top: 16px; }}
.{cls}-chip {{ display: inline-flex; padding: 6px 12px; border-radius: 999px; background: #21123D; color: #fff !important; font-family: var(--rd-font-mono) !important; font-size: 11px !important; font-weight: 500 !important; }}
.{cls}-reveal {{ opacity: 0; transform: translateY(24px); transition: opacity .8s cubic-bezier(.16,1,.3,1), transform .8s cubic-bezier(.16,1,.3,1); }}
.{cls}-reveal.in-view {{ opacity: 1; transform: translateY(0); }}
@media (max-width: 860px) {{
  .{cls}-final-cta {{ grid-template-columns: 1fr !important; padding: 36px; }}
  .{cls}-hero {{ padding: 60px 20px; }}
}}
@media (max-width: 600px) {{
  .{cls}-grid {{ grid-template-columns: 1fr !important; }}
  .{cls}-section {{ padding: 56px 0; }}
  .{cls}-actions {{ flex-direction: column; align-items: stretch; }}
  .{cls}-btn {{ width: 100%; justify-content: center; }}
}}
"""

RD_JS = """
<script>
(function() {
  var cls = '{cls}';
  var items = document.querySelectorAll('.' + cls + '-reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) { if (e.isIntersecting) { e.target.classList.add('in-view'); io.unobserve(e.target); } });
    }, { threshold: 0.08, rootMargin: '0px 0px -50px 0px' });
    items.forEach(function(el) { io.observe(el); });
  } else {
    items.forEach(function(el) { el.classList.add('in-view'); });
  }
})();
</script>
"""

# ─────────────────────────────────────────────────────────────
# PAGE CONTENT
# ─────────────────────────────────────────────────────────────

BOVEDA_HTML = """
<style>
""" + RD_CSS_BASE.replace('{cls}', 'rd-boveda') + """
.rd-boveda-hero-inner { position: relative; z-index: 2; }
.rd-boveda-search-hint { display: inline-flex; align-items: center; gap: 10px; margin-top: 24px; padding: 12px 20px; border-radius: 12px; background: rgba(255,255,255,.07); border: 1px solid rgba(255,255,255,.14); color: rgba(255,255,255,.7) !important; font-size: 14px !important; }
.rd-boveda-coming { opacity: .45; pointer-events: none; }
.rd-boveda-card-link { text-decoration: none !important; color: inherit !important; display: block; }
.rd-boveda-card-link .rd-boveda-card:hover { transform: translateY(-3px); border-color: rgba(128,0,252,.3); box-shadow: 0 16px 40px rgba(33,18,61,.07); }
.rd-boveda-subs { border: 2px dashed var(--rd-purple); border-radius: 16px; padding: 32px; text-align: center; background: var(--rd-soft) !important; margin: 0 auto; max-width: 600px; }
.rd-boveda-subs p { color: var(--rd-text-2) !important; margin: 0 !important; font-size: 15px !important; }
.rd-boveda-subs strong { color: #20152f; }
</style>

<section class="rd-boveda">
<div class="rd-boveda-hero">
  <div class="rd-boveda-hero-grid"></div>
  <div class="rd-boveda-container rd-boveda-hero-inner">
    <span class="rd-boveda-eyebrow"><span class="rd-boveda-eyebrow-dot"></span>Recursos gratuitos · Manuales · Guías</span>
    <h1>La <em>Bóveda.</em></h1>
    <p class="rd-boveda-hero-lead">Todo lo que necesitas para aplicar la inteligencia artificial en tu negocio. Sin humo. Sin teoría vacía. Solo recursos que funcionan.</p>
    <div class="rd-boveda-search-hint">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
      Manuales · Cursos · Guías prácticas
    </div>
  </div>
</div>

<div class="rd-boveda-section">
  <div class="rd-boveda-container">
    <div class="rd-boveda-section-title rd-boveda-reveal">
      <div class="rd-boveda-level"><div class="rd-boveda-level-line"></div><span>Disponible ahora</span></div>
      <h2>Manuales <em>gratuitos.</em></h2>
      <p>Guías paso a paso para implementar herramientas de IA en tu día a día sin necesitar conocimientos técnicos previos.</p>
    </div>
    <div class="rd-boveda-grid rd-boveda-reveal">
      <a href="/manual-notebook-lm/" class="rd-boveda-card-link">
        <div class="rd-boveda-card">
          <span class="rd-boveda-card-tag">IA + Productividad</span>
          <h3>Manual Notebook LM</h3>
          <p>Aprende a usar NotebookLM de Google para analizar documentos, crear resúmenes y generar audio automáticamente. Paso a paso.</p>
        </div>
      </a>
      <a href="/manual-de-claudia/" class="rd-boveda-card-link">
        <div class="rd-boveda-card">
          <span class="rd-boveda-card-tag">Agente IA</span>
          <h3>Manual de Claudia</h3>
          <p>Cómo configurar y trabajar con Claudia, el agente de IA de Riqueza Digital. Delega tareas complejas al agente paso a paso.</p>
        </div>
      </a>
    </div>
  </div>
</div>

<div class="rd-boveda-section rd-boveda-section-soft">
  <div class="rd-boveda-container">
    <div class="rd-boveda-section-title rd-boveda-reveal">
      <div class="rd-boveda-level"><div class="rd-boveda-level-line"></div><span>Formación</span></div>
      <h2>Cursos para tu <em>equipo.</em></h2>
      <p>Formación práctica para que tu empresa aplique la IA sin depender de consultores externos.</p>
    </div>
    <div class="rd-boveda-grid rd-boveda-reveal">
      <a href="/aprender-a-pensar-en-ia/" class="rd-boveda-card-link">
        <div class="rd-boveda-card"><span class="rd-boveda-card-tag">Curso</span><h3>Aprender a pensar en IA</h3><p>Curso práctico para empezar desde cero con inteligencia artificial aplicada a tu negocio.</p></div>
      </a>
      <a href="/integrar-ia-en-tu-negocio/" class="rd-boveda-card-link">
        <div class="rd-boveda-card"><span class="rd-boveda-card-tag">Curso</span><h3>Integrar la IA en tu negocio</h3><p>Estrategia y herramientas para implementar IA en los procesos de tu empresa.</p></div>
      </a>
      <a href="/programar-forma-agentica/" class="rd-boveda-card-link">
        <div class="rd-boveda-card"><span class="rd-boveda-card-tag">Curso técnico</span><h3>Programar de forma agéntica</h3><p>Para desarrolladores: construye sistemas de agentes que ejecutan tareas autónomamente.</p></div>
      </a>
    </div>
  </div>
</div>

<div class="rd-boveda-section">
  <div class="rd-boveda-container">
    <div class="rd-boveda-section-title rd-boveda-reveal">
      <div class="rd-boveda-level"><div class="rd-boveda-level-line"></div><span>Próximamente</span></div>
      <h2>Más recursos en <em>camino.</em></h2>
    </div>
    <div class="rd-boveda-grid rd-boveda-reveal">
      <div class="rd-boveda-card rd-boveda-coming"><span class="rd-boveda-card-tag">Google Ads</span><h3>Guía Google Ads para pymes</h3><p>Cómo montar una campaña rentable con presupuesto ajustado. Estructura, keywords y conversiones.</p></div>
      <div class="rd-boveda-card rd-boveda-coming"><span class="rd-boveda-card-tag">Meta Ads</span><h3>Meta Ads sin malgastar</h3><p>Segmentación, creatividades y métricas clave para campañas rentables en Facebook e Instagram.</p></div>
      <div class="rd-boveda-card rd-boveda-coming"><span class="rd-boveda-card-tag">Posicionamiento IA</span><h3>Aparecer en ChatGPT</h3><p>Cómo estructurar tu contenido para que los buscadores de IA citen tu marca.</p></div>
    </div>
    <div style="text-align:center;margin-top:40px;" class="rd-boveda-reveal">
      <div class="rd-boveda-subs">
        <strong>¿Quieres recibir los próximos recursos?</strong>
        <p>Próximamente: suscripción directa para no perderte ningún manual nuevo.</p>
        <!-- MAILERLITE_FORM -->
      </div>
    </div>
  </div>
</div>

<div class="rd-boveda-section rd-boveda-section-soft">
  <div class="rd-boveda-container">
    <div class="rd-boveda-final-cta rd-boveda-reveal">
      <div>
        <h2>¿Prefieres que lo <em>implementemos nosotros?</em></h2>
        <p>Gestionamos tus campañas, diseñamos tu web con IA y posicionamos tu marca donde están tus clientes — en Google y en las IAs.</p>
      </div>
      <div class="rd-boveda-final-action">
        <a href="/contacto/" class="rd-boveda-btn">Hablemos &#8594;</a>
        <div class="rd-boveda-final-meta">
          <span>Google Ads</span>
          <span>Webs con IA</span>
          <span>Posicionamiento en IAs</span>
        </div>
      </div>
    </div>
  </div>
</div>
</section>
""" + RD_JS.replace('{cls}', 'rd-boveda')

WEB_IA_HTML = """
<style>
""" + RD_CSS_BASE.replace('{cls}', 'rd-web-ia') + """
.rd-web-ia-two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
@media (max-width: 720px) { .rd-web-ia-two-col { grid-template-columns: 1fr !important; } }
</style>

<section class="rd-web-ia">
<div class="rd-web-ia-hero">
  <div class="rd-web-ia-hero-grid"></div>
  <div class="rd-web-ia-container" style="position:relative;z-index:2;">
    <span class="rd-web-ia-eyebrow"><span class="rd-web-ia-eyebrow-dot"></span>Servicio · Desarrollo Web · IA Agéntica</span>
    <h1>Webs con <em>IA agéntica.</em></h1>
    <p class="rd-web-ia-hero-lead">No solo un sitio web. Un sistema que capta visitas, cualifica leads y reserva llamadas mientras tú duermes.</p>
    <div class="rd-web-ia-actions">
      <a href="/contacto/" class="rd-web-ia-btn">Pedir presupuesto &#8594;</a>
      <a href="#que-incluye" class="rd-web-ia-btn rd-web-ia-btn-ghost">Ver qué incluye</a>
    </div>
  </div>
</div>

<div class="rd-web-ia-section">
  <div class="rd-web-ia-container">
    <div class="rd-web-ia-section-title rd-web-ia-reveal">
      <div class="rd-web-ia-level"><div class="rd-web-ia-level-line"></div><span>Concepto</span></div>
      <h2>Más que una web, un <em>vendedor 24/7.</em></h2>
      <p>Una web tradicional muestra información. Una web con IA agéntica <strong>actúa</strong>: responde preguntas, cualifica al visitante y lo guía hacia la conversión automáticamente — sin depender de que nadie esté disponible.</p>
    </div>
  </div>
</div>

<div id="que-incluye" class="rd-web-ia-section rd-web-ia-section-soft">
  <div class="rd-web-ia-container">
    <div class="rd-web-ia-section-title rd-web-ia-reveal">
      <div class="rd-web-ia-level"><div class="rd-web-ia-level-line"></div><span>Qué incluye</span></div>
      <h2>Todo lo que <em>necesitas.</em></h2>
    </div>
    <div class="rd-web-ia-grid rd-web-ia-reveal">
      <div class="rd-web-ia-card"><span class="rd-web-ia-card-tag">IA</span><h3>Agente conversacional entrenado</h3><p>Un asistente IA que conoce tu negocio, responde preguntas frecuentes y capta leads 24/7 sin soporte humano.</p></div>
      <div class="rd-web-ia-card"><span class="rd-web-ia-card-tag">Diseño</span><h3>Maquetación Elementor profesional</h3><p>Landing pages y webs corporativas rápidas, responsive y optimizadas para conversión desde el primer día.</p></div>
      <div class="rd-web-ia-card"><span class="rd-web-ia-card-tag">Integraciones</span><h3>Conectado con tus herramientas</h3><p>CRM, WhatsApp, email marketing y calendario. Los leads entran solos en tus sistemas.</p></div>
      <div class="rd-web-ia-card"><span class="rd-web-ia-card-tag">SEO</span><h3>SEO técnico y de contenido</h3><p>Yoast SEO configurado, schema markup y estructura pensada para posicionar en Google y en IAs.</p></div>
      <div class="rd-web-ia-card"><span class="rd-web-ia-card-tag">Analytics</span><h3>GTM, GA4 y conversiones</h3><p>Seguimiento completo para saber exactamente qué genera resultados y dónde mejorar.</p></div>
      <div class="rd-web-ia-card"><span class="rd-web-ia-card-tag">Mantenimiento</span><h3>Seguridad y soporte continuo</h3><p>SSL, backups, actualizaciones y monitorización. Tu web siempre operativa.</p></div>
    </div>
  </div>
</div>

<div class="rd-web-ia-section">
  <div class="rd-web-ia-container">
    <div class="rd-web-ia-section-title rd-web-ia-reveal">
      <div class="rd-web-ia-level"><div class="rd-web-ia-level-line"></div><span>Proceso</span></div>
      <h2>De cero a <em>publicado</em> en 4 semanas.</h2>
    </div>
    <ol class="rd-web-ia-steps rd-web-ia-reveal">
      <li><strong>Semana 1 — Diagnóstico</strong><p>Analizamos tu negocio, clientes y competencia. Definimos la arquitectura de la web y los flujos del agente IA.</p></li>
      <li><strong>Semanas 2-3 — Diseño y maquetación</strong><p>Construcción en Elementor con tu identidad visual. Revisiones hasta aprobación.</p></li>
      <li><strong>Semana 3-4 — Integración IA</strong><p>Configuramos el agente, conectamos integraciones y probamos todos los flujos de captación.</p></li>
      <li><strong>Lanzamiento y formación</strong><p>Publicación, configuración SEO completa y sesión de formación para que gestiones la web de forma autónoma.</p></li>
    </ol>
  </div>
</div>

<div class="rd-web-ia-section rd-web-ia-section-soft">
  <div class="rd-web-ia-container">
    <div class="rd-web-ia-two-col rd-web-ia-reveal">
      <div class="rd-web-ia-dark-card">
        <h2>¿Para quién <em>es?</em></h2>
        <p>Ideal si tu web actual no genera leads, recibes preguntas repetitivas que quieres automatizar, o necesitas una landing de alta conversión para una campaña.</p>
        <ul class="rd-web-ia-check-list">
          <li><span class="rd-web-ia-check">&#10003;</span><span>Web antigua que no convierte</span></li>
          <li><span class="rd-web-ia-check">&#10003;</span><span>Quieres automatizar la captación de leads</span></li>
          <li><span class="rd-web-ia-check">&#10003;</span><span>Lanzamiento de nuevo servicio o producto</span></li>
          <li><span class="rd-web-ia-check">&#10003;</span><span>Necesitas integrar IA sin rehacer todo</span></li>
        </ul>
      </div>
      <div class="rd-web-ia-dark-card">
        <h2>Combínalo con <em>más servicios.</em></h2>
        <p>La web es el punto de llegada. Para maximizar el retorno, combínala con tráfico de calidad desde publicidad o desde las IAs.</p>
        <ul class="rd-web-ia-check-list">
          <li><span class="rd-web-ia-check">&#10003;</span><span><a href="/servicios-google-ads/" style="color:#d4b3ff;">Google Ads</a> — tráfico cualificado inmediato</span></li>
          <li><span class="rd-web-ia-check">&#10003;</span><span><a href="/posicionamiento-ia/" style="color:#d4b3ff;">Posicionamiento en IAs</a> — presencia en ChatGPT y Perplexity</span></li>
          <li><span class="rd-web-ia-check">&#10003;</span><span>Email marketing con MailerLite</span></li>
        </ul>
      </div>
    </div>
  </div>
</div>

<div class="rd-web-ia-faq-section">
  <div class="rd-web-ia-container">
    <h2>Preguntas <em>frecuentes.</em></h2>
    <div class="rd-web-ia-faq-list rd-web-ia-reveal">
      <details><summary>¿Cuánto cuesta una web con IA agéntica?</summary><p>Cada proyecto es diferente. El precio depende del número de páginas, complejidad del agente IA y las integraciones requeridas. Escríbenos y preparamos un presupuesto en 48 horas.</p></details>
      <details><summary>¿Qué diferencia hay con una web normal?</summary><p>Una web normal muestra información estática. Una web agéntica tiene un sistema IA que interactúa con el visitante, responde preguntas, cualifica su interés y lo guía hacia la acción de forma personalizada.</p></details>
      <details><summary>¿Necesito conocimientos técnicos para mantenerla?</summary><p>No. Usamos WordPress con Elementor. Incluimos formación post-lanzamiento. La mayoría de nuestros clientes gestionan su web sin ayuda externa.</p></details>
      <details><summary>¿Podéis mejorar mi web actual en lugar de hacer una nueva?</summary><p>Sí. Podemos integrar el agente IA y las automatizaciones en una web WordPress existente sin rehacerla desde cero. Consúltanos tu caso.</p></details>
    </div>
  </div>
</div>

<div class="rd-web-ia-section">
  <div class="rd-web-ia-container">
    <div class="rd-web-ia-final-cta rd-web-ia-reveal">
      <div>
        <h2>Una web que trabaja <em>mientras duermes.</em></h2>
        <p>Cuéntanos tu proyecto. Te respondemos en menos de 24 horas con una propuesta adaptada a tu negocio.</p>
      </div>
      <div class="rd-web-ia-final-action">
        <a href="/contacto/" class="rd-web-ia-btn">Quiero más información &#8594;</a>
        <div class="rd-web-ia-final-meta">
          <span>Respuesta en 24h</span>
          <span>Presupuesto sin compromiso</span>
        </div>
      </div>
    </div>
  </div>
</div>
</section>
""" + RD_JS.replace('{cls}', 'rd-web-ia')

POS_IA_HTML = """
<style>
""" + RD_CSS_BASE.replace('{cls}', 'rd-pos-ia') + """
.rd-pos-ia-platforms { display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0; }
</style>

<section class="rd-pos-ia">
<div class="rd-pos-ia-hero">
  <div class="rd-pos-ia-hero-grid"></div>
  <div class="rd-pos-ia-container" style="position:relative;z-index:2;">
    <span class="rd-pos-ia-eyebrow"><span class="rd-pos-ia-eyebrow-dot"></span>Servicio · GEO · Generative Engine Optimization</span>
    <h1>Aparece en <em>ChatGPT,</em> Perplexity y Google IA.</h1>
    <p class="rd-pos-ia-hero-lead">El 40% de las búsquedas de compra ya empiezan en un asistente de IA. ¿Aparece tu empresa cuando tu cliente potencial pregunta?</p>
    <div class="rd-pos-ia-actions">
      <a href="/contacto/" class="rd-pos-ia-btn">Solicitar auditoría gratuita &#8594;</a>
      <a href="#como-funciona" class="rd-pos-ia-btn rd-pos-ia-btn-ghost">Cómo funciona</a>
    </div>
  </div>
</div>

<div class="rd-pos-ia-section">
  <div class="rd-pos-ia-container">
    <div class="rd-pos-ia-stat-box rd-pos-ia-reveal">
      <span class="big">40%</span>
      <p>de las búsquedas comerciales ocurren en ChatGPT, Perplexity o Google AI Overviews. La mayoría de empresas españolas no aparecen en ninguna.</p>
    </div>
    <div class="rd-pos-ia-section-title rd-pos-ia-reveal" style="text-align:left;max-width:100%;margin-bottom:20px;">
      <div class="rd-pos-ia-level"><div class="rd-pos-ia-level-line"></div><span>El contexto</span></div>
      <h2 style="text-align:left;">El nuevo SEO es ser <em>citado por las IAs.</em></h2>
    </div>
    <p style="color:var(--rd-text-2);font-size:16px;line-height:1.7;max-width:760px;" class="rd-pos-ia-reveal">Cuando alguien pregunta a ChatGPT <em>"¿qué agencia de marketing digital es buena en Barcelona?"</em> o a Perplexity <em>"¿cómo mejorar el ROI de mis campañas?"</em>, los modelos de IA responden con fuentes que han aprendido a considerar <strong>fiables y relevantes</strong>. Esto se llama <strong>GEO (Generative Engine Optimization)</strong>.</p>
  </div>
</div>

<div id="como-funciona" class="rd-pos-ia-section rd-pos-ia-section-soft">
  <div class="rd-pos-ia-container">
    <div class="rd-pos-ia-section-title rd-pos-ia-reveal">
      <div class="rd-pos-ia-level"><div class="rd-pos-ia-level-line"></div><span>Plataformas</span></div>
      <h2>Dónde te <em>posicionamos.</em></h2>
    </div>
    <div class="rd-pos-ia-platforms rd-pos-ia-reveal">
      <span class="rd-pos-ia-chip">ChatGPT</span><span class="rd-pos-ia-chip">Perplexity</span><span class="rd-pos-ia-chip">Google AI Overviews</span><span class="rd-pos-ia-chip">Gemini</span><span class="rd-pos-ia-chip">Claude</span><span class="rd-pos-ia-chip">Bing Copilot</span>
    </div>
    <div class="rd-pos-ia-grid rd-pos-ia-reveal" style="margin-top:32px;">
      <div class="rd-pos-ia-card"><span class="rd-pos-ia-card-tag">Auditoría</span><h3>Análisis de presencia actual</h3><p>Analizamos qué responden las IAs sobre tu sector y tu competencia. Identificamos el gap exacto.</p></div>
      <div class="rd-pos-ia-card"><span class="rd-pos-ia-card-tag">Contenido</span><h3>Contenido estructurado para IA</h3><p>Creamos páginas, FAQs y artículos con el formato que los modelos de IA priorizan como fuente.</p></div>
      <div class="rd-pos-ia-card"><span class="rd-pos-ia-card-tag">Técnico</span><h3>Schema markup y datos estructurados</h3><p>JSON-LD para que Google y los LLMs entiendan exactamente qué ofreces, dónde estás y a quién.</p></div>
      <div class="rd-pos-ia-card"><span class="rd-pos-ia-card-tag">Autoridad</span><h3>Construcción de autoridad digital</h3><p>Menciones, backlinks y presencia en fuentes que los modelos de IA consideran fiables en tu industria.</p></div>
      <div class="rd-pos-ia-card"><span class="rd-pos-ia-card-tag">Seguimiento</span><h3>Monitorización mensual de citas</h3><p>Seguimiento de cuántas veces y cómo te citan los asistentes IA. Informe de evolución mensual.</p></div>
      <div class="rd-pos-ia-card"><span class="rd-pos-ia-card-tag">Sinergia</span><h3>Integración con SEO tradicional</h3><p>GEO y SEO se potencian mutuamente. Coordinamos ambas estrategias para maximizar el alcance.</p></div>
    </div>
  </div>
</div>

<div class="rd-pos-ia-section">
  <div class="rd-pos-ia-container">
    <div class="rd-pos-ia-section-title rd-pos-ia-reveal">
      <div class="rd-pos-ia-level"><div class="rd-pos-ia-level-line"></div><span>Audiencia</span></div>
      <h2>¿Para quién tiene <em>más sentido?</em></h2>
    </div>
    <div class="rd-pos-ia-dark-card rd-pos-ia-reveal">
      <h2>Ideal si tus clientes <em>investigan antes de comprar.</em></h2>
      <p>Servicios B2B, tecnología, salud, formación, consultoría... cualquier sector donde el cliente pregunta a Google o a una IA antes de decidir.</p>
      <ul class="rd-pos-ia-check-list">
        <li><span class="rd-pos-ia-check">&#10003;</span><span>Vendes servicios de alto valor donde la confianza importa</span></li>
        <li><span class="rd-pos-ia-check">&#10003;</span><span>Quieres ser la referencia en tu sector en 12-24 meses</span></li>
        <li><span class="rd-pos-ia-check">&#10003;</span><span>Tu competencia todavía no está posicionada en IAs (ventana de oportunidad)</span></li>
        <li><span class="rd-pos-ia-check">&#10003;</span><span>Quieres combinar SEO clásico con el nuevo paradigma de búsqueda por IA</span></li>
      </ul>
      <div style="margin-top:20px;">
        <p style="font-size:14px;">Combínalo con <a href="/servicios-google-ads/" style="color:#d4b3ff;">Google Ads</a> o <a href="/servicios-web-ia/" style="color:#d4b3ff;">webs con IA</a> para dominar todos los canales.</p>
      </div>
    </div>
  </div>
</div>

<div class="rd-pos-ia-faq-section">
  <div class="rd-pos-ia-container">
    <h2>Preguntas <em>frecuentes.</em></h2>
    <div class="rd-pos-ia-faq-list rd-pos-ia-reveal">
      <details><summary>¿Qué es GEO y cómo se diferencia del SEO?</summary><p>SEO optimiza para que Google te muestre en sus resultados. GEO (Generative Engine Optimization) optimiza para que los modelos de IA te citen como fuente de respuesta cuando sus usuarios hacen preguntas. Son complementarios: el SEO da tráfico directo, el GEO da autoridad e impacto en la decisión de compra.</p></details>
      <details><summary>¿Cuánto tiempo tarda en dar resultados?</summary><p>Las primeras citas en IAs suelen aparecer entre 2 y 4 meses. La construcción de autoridad sostenible tarda 6-12 meses. Es inversión a largo plazo, pero la ventaja competitiva para quienes empiezan ahora es enorme.</p></details>
      <details><summary>¿Se puede medir el impacto en las IAs?</summary><p>Sí. Monitorizamos regularmente las respuestas de ChatGPT, Perplexity y Google AI sobre queries clave. También rastreamos el tráfico procedente de herramientas IA mediante UTMs y GA4.</p></details>
      <details><summary>¿Funciona para cualquier sector?</summary><p>Especialmente bien en servicios profesionales, tecnología, salud y formación. Si tus clientes usan ChatGPT para buscar soluciones, el GEO es relevante para ti.</p></details>
      <details><summary>¿Podéis hacer una auditoría antes de contratar?</summary><p>Sí. Ofrecemos una auditoría gratuita de cómo te mencionan (o no te mencionan) las principales IAs cuando preguntan por tu sector. Sin compromiso.</p></details>
    </div>
  </div>
</div>

<div class="rd-pos-ia-section">
  <div class="rd-pos-ia-container">
    <div class="rd-pos-ia-final-cta rd-pos-ia-reveal">
      <div>
        <h2>Tu competencia todavía no está. <em>Sé el primero.</em></h2>
        <p>Auditamos gratis qué responden ChatGPT y Perplexity cuando preguntan por tu sector. Descubre la oportunidad antes de que lo haga tu competencia.</p>
      </div>
      <div class="rd-pos-ia-final-action">
        <a href="/contacto/" class="rd-pos-ia-btn">Solicitar auditoría gratuita &#8594;</a>
        <div class="rd-pos-ia-final-meta">
          <span>Auditoría gratuita</span>
          <span>Sin compromiso</span>
          <span>Respuesta en 24h</span>
        </div>
      </div>
    </div>
  </div>
</div>
</section>
""" + RD_JS.replace('{cls}', 'rd-pos-ia')

# ─────────────────────────────────────────────────────────────
# UPDATE PAGES
# ─────────────────────────────────────────────────────────────

pages = [
    {
        'id': 6835,
        'slug': 'boveda',
        'title': 'La Bóveda — Recursos y Manuales de IA',
        'html': BOVEDA_HTML,
        'focuskw': 'manuales inteligencia artificial empresas',
        'metadesc': 'Manuales gratuitos, guías y recursos prácticos sobre inteligencia artificial para empresas. Directamente aplicables a tu negocio.',
        'seotitle': 'La Bóveda — Manuales y Recursos de IA | Riqueza Digital',
    },
    {
        'id': 6836,
        'slug': 'servicios-web-ia',
        'title': 'Webs con IA Agéntica — Diseño Web Inteligente para Empresas',
        'html': WEB_IA_HTML,
        'focuskw': 'web inteligencia artificial agéntica',
        'metadesc': 'Diseño y desarrollo de webs con inteligencia artificial agéntica. Tu web capta leads, responde preguntas y convierte visitas en clientes automáticamente.',
        'seotitle': 'Webs con IA Agéntica Barcelona | Riqueza Digital',
    },
    {
        'id': 6837,
        'slug': 'posicionamiento-ia',
        'title': 'Posicionamiento en ChatGPT y otras IAs — GEO para Empresas',
        'html': POS_IA_HTML,
        'focuskw': 'posicionamiento chatgpt empresas',
        'metadesc': 'Aparece en ChatGPT, Perplexity y Google AI cuando tus clientes preguntan. Servicio GEO (Generative Engine Optimization) para pymes en España.',
        'seotitle': 'Posicionamiento en ChatGPT y Perplexity | GEO | Riqueza Digital',
    },
]

for p in pages:
    el_data = elementor_html_widget(p['html'])
    payload = {
        'title': p['title'],
        'status': 'publish',
        'content': '',  # Elementor ignores this when _elementor_data is set
        'meta': {
            '_elementor_edit_mode': 'builder',
            '_elementor_template_type': 'wp-page',
            '_elementor_data': el_data,
            'yoast_wpseo_title': p['seotitle'],
            'yoast_wpseo_metadesc': p['metadesc'],
            'yoast_wpseo_focuskw': p['focuskw'],
        }
    }
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(
        f'{url}/wp-json/wp/v2/pages/{p["id"]}',
        data=body, headers=h, method='POST'
    )
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read())
        print(f"OK — {p['slug']} | ID:{res['id']} | {res['link']}")
        print(f"     Elementor data set: {'_elementor_data' in res.get('meta', {})}")

print("\nAll pages updated with Elementor HTML widget format.")
