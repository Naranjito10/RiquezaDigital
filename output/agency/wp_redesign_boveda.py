"""Redesign /boveda/ with proper CTAs and fix CSS double-brace bug on all 3 pages."""
import urllib.request, base64, json, os, sys, random, string
sys.stdout.reconfigure(encoding='utf-8')

url = os.environ['WP_RD_URL']
user = os.environ['WP_RD_USER']
pwd = os.environ['WP_RD_APP_PASSWORD']
token = base64.b64encode(f'{user}:{pwd}'.encode()).decode()
h = {'Authorization': f'Basic {token}', 'Content-Type': 'application/json; charset=utf-8'}

def make_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def wrap_elementor(html):
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

def push(page_id, title, html, seotitle, metadesc, focuskw):
    payload = {
        'title': title, 'status': 'publish', 'content': '',
        'meta': {
            '_elementor_edit_mode': 'builder',
            '_elementor_template_type': 'wp-page',
            '_elementor_data': wrap_elementor(html),
            'yoast_wpseo_title': seotitle,
            'yoast_wpseo_metadesc': metadesc,
            'yoast_wpseo_focuskw': focuskw,
        }
    }
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(f'{url}/wp-json/wp/v2/pages/{page_id}', data=body, headers=h, method='POST')
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read())
        print(f"OK — {res['slug']} | {res['link']}")

# ─────────────────────────────────────────────────────────────
# BÓVEDA — full redesign
# ─────────────────────────────────────────────────────────────
BOVEDA = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,400;0,9..144,800;1,9..144,300;1,9..144,400&family=Inter+Tight:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

.rd-bv {
  --rd-dark:#21123D;--rd-purple:#8000FC;--rd-blue:#0530FA;--rd-pink:#E300FF;
  --rd-text:#1f1f2e;--rd-text-2:#514b5f;--rd-border:#e8e4f0;--rd-soft:#f7f4fb;--rd-soft-2:#faf8fd;
  --rd-font-display:'Fraunces','Times New Roman',serif;
  --rd-font-body:'Inter Tight',-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
  --rd-font-mono:'JetBrains Mono',"SFMono-Regular",Consolas,monospace;
  width:100vw!important;max-width:100vw!important;
  margin-left:calc(50% - 50vw)!important;margin-right:calc(50% - 50vw)!important;
  background:#fff!important;color:var(--rd-text)!important;
  font-family:var(--rd-font-body)!important;overflow-x:hidden;
}
.rd-bv,.rd-bv * { box-sizing:border-box; }
.rd-bv-wrap { width:min(1200px,calc(100% - 48px));margin:0 auto; }

/* HERO */
.rd-bv-hero {
  background:radial-gradient(circle at 8% 20%,rgba(255,255,255,.07),transparent 18%),
             radial-gradient(circle at 92% 18%,rgba(255,255,255,.07),transparent 20%),
             linear-gradient(135deg,#21123D 0%,#35115f 50%,#4b0b68 100%);
  padding:80px 20px 72px;position:relative;overflow:hidden;
}
.rd-bv-hero-grid-bg {
  background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);
  background-size:56px 56px;
  -webkit-mask-image:radial-gradient(ellipse at center,black 30%,transparent 80%);
  mask-image:radial-gradient(ellipse at center,black 30%,transparent 80%);
  position:absolute;inset:0;pointer-events:none;
}
.rd-bv-hero-inner { position:relative;z-index:2;display:grid;grid-template-columns:1.1fr 0.9fr;gap:48px;align-items:center; }
.rd-bv-eyebrow {
  display:inline-flex;align-items:center;gap:10px;margin-bottom:20px;
  padding:7px 16px;border-radius:999px;
  background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.14);
  color:rgba(255,255,255,.85)!important;font-family:var(--rd-font-mono)!important;
  font-size:11px!important;letter-spacing:.12em;text-transform:uppercase;font-weight:500!important;
}
.rd-bv-eyebrow-dot {
  width:6px;height:6px;background:var(--rd-pink);border-radius:50%;
  box-shadow:0 0 10px var(--rd-pink);animation:rd-bv-pulse 2s infinite;
}
@keyframes rd-bv-pulse { 0%,100% { opacity:1;transform:scale(1); } 50% { opacity:.5;transform:scale(1.4); } }
.rd-bv-hero h1 {
  font-size:clamp(40px,5.5vw,68px)!important;line-height:1.02!important;
  letter-spacing:-.045em!important;font-weight:800!important;margin:0 0 20px!important;
  color:#fff!important;font-family:var(--rd-font-body)!important;
}
.rd-bv-hero h1 em {
  font-family:var(--rd-font-display)!important;font-style:italic;font-weight:400!important;
  background:linear-gradient(90deg,#fff 0%,#d4b3ff 40%,#f13fff 90%);
  -webkit-background-clip:text;background-clip:text;color:transparent!important;
}
.rd-bv-lead {
  font-size:17px!important;line-height:1.65!important;color:rgba(255,255,255,.8)!important;
  max-width:540px;margin:0 0 28px!important;font-weight:400!important;
}
.rd-bv-stats { display:flex;gap:20px;flex-wrap:wrap;margin-bottom:32px; }
.rd-bv-stat {
  display:flex;flex-direction:column;gap:3px;
  padding:12px 18px;border-radius:12px;
  background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);
}
.rd-bv-stat strong { color:#fff!important;font-size:18px!important;font-weight:800!important;font-family:var(--rd-font-display)!important;font-style:italic; }
.rd-bv-stat span { color:rgba(255,255,255,.6)!important;font-family:var(--rd-font-mono)!important;font-size:10px!important;letter-spacing:.1em;text-transform:uppercase; }
.rd-bv-actions { display:flex;gap:12px;flex-wrap:wrap; }
.rd-bv-btn {
  display:inline-flex;align-items:center;gap:9px;min-height:48px;padding:0 26px;
  border-radius:999px;text-decoration:none!important;font-size:14px!important;
  font-weight:700!important;font-family:var(--rd-font-body)!important;
  background:linear-gradient(90deg,var(--rd-blue),var(--rd-purple),var(--rd-pink))!important;
  color:#fff!important;box-shadow:0 12px 28px rgba(128,0,252,.3);
  transition:transform .2s,box-shadow .2s;
}
.rd-bv-btn:hover { transform:translateY(-2px);box-shadow:0 16px 34px rgba(227,0,255,.38);color:#fff!important; }
.rd-bv-btn-ghost {
  background:rgba(255,255,255,.07)!important;border:1px solid rgba(255,255,255,.18)!important;
  box-shadow:none!important;backdrop-filter:blur(10px);
}
.rd-bv-btn-ghost:hover { background:rgba(255,255,255,.13)!important;border-color:var(--rd-pink)!important; }
.rd-bv-btn-sm {
  min-height:38px;padding:0 18px;font-size:13px!important;
  background:linear-gradient(90deg,var(--rd-blue),var(--rd-purple),var(--rd-pink))!important;
  color:#fff!important;box-shadow:0 8px 20px rgba(128,0,252,.25);
}
.rd-bv-btn-outline {
  background:transparent!important;border:1.5px solid var(--rd-purple)!important;
  color:var(--rd-purple)!important;box-shadow:none!important;
}
.rd-bv-btn-outline:hover { background:var(--rd-purple)!important;color:#fff!important; }

/* Featured card (hero right) */
.rd-bv-featured-card {
  border-radius:24px;padding:24px;
  background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.14);
  backdrop-filter:blur(16px);
}
.rd-bv-featured-visual {
  border-radius:16px;overflow:hidden;margin-bottom:20px;
  background:linear-gradient(135deg,var(--rd-blue),var(--rd-purple),var(--rd-pink));
  aspect-ratio:16/9;display:flex;align-items:center;justify-content:center;
}
.rd-bv-featured-visual span {
  color:#fff;font-size:48px;opacity:.7;
}
.rd-bv-featured-card h3 { color:#fff!important;font-size:18px!important;font-weight:700!important;margin:0 0 8px!important; }
.rd-bv-featured-card p { color:rgba(255,255,255,.7)!important;font-size:14px!important;margin:0 0 16px!important;line-height:1.55!important; }
.rd-bv-featured-card .rd-bv-tag {
  display:inline-flex;padding:4px 12px;border-radius:999px;margin-bottom:12px;
  background:rgba(128,0,252,.25);color:#d4b3ff!important;
  font-family:var(--rd-font-mono)!important;font-size:10px!important;font-weight:600!important;letter-spacing:.1em;text-transform:uppercase;
}

/* SECTIONS */
.rd-bv-section { padding:80px 0;background:#fff!important; }
.rd-bv-section-soft { background:var(--rd-soft)!important; }
.rd-bv-section-dark {
  background:radial-gradient(circle at 82% 18%,rgba(227,0,255,.22),transparent 28%),
             linear-gradient(135deg,#21123D 0%,#32155b 100%)!important;
}
.rd-bv-section-title { max-width:760px;margin:0 auto 48px;text-align:center; }
.rd-bv-section-title-left { max-width:100%;text-align:left; }
.rd-bv-level { display:inline-flex;align-items:center;gap:10px;margin-bottom:14px; }
.rd-bv-level-line { width:32px;height:2px;background:linear-gradient(90deg,var(--rd-blue),var(--rd-pink)); }
.rd-bv-level span { color:var(--rd-purple)!important;text-transform:uppercase;letter-spacing:.12em;font-size:11px!important;font-weight:600!important;font-family:var(--rd-font-mono)!important; }
.rd-bv-section-title h2,.rd-bv-section-title-left h2 {
  font-size:clamp(28px,4vw,46px)!important;line-height:1.06!important;
  letter-spacing:-.04em!important;font-weight:800!important;margin:0 0 14px!important;
  color:#20152f!important;font-family:var(--rd-font-body)!important;
}
.rd-bv-section-dark .rd-bv-section-title h2 { color:#fff!important; }
.rd-bv-section-title h2 em,.rd-bv-section-title-left h2 em {
  font-family:var(--rd-font-display)!important;font-style:italic;font-weight:400!important;color:var(--rd-purple)!important;
}
.rd-bv-section-dark h2 em { color:#ff7cff!important; }
.rd-bv-section-title p { color:var(--rd-text-2)!important;font-size:16px!important;line-height:1.65!important;margin:0!important; }

/* RESOURCE CARDS */
.rd-bv-grid { display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:24px; }
.rd-bv-grid-2 { grid-template-columns:repeat(2,1fr); }
.rd-bv-card {
  border-radius:20px;background:#fff!important;border:1.5px solid var(--rd-border);
  overflow:hidden;transition:transform .35s cubic-bezier(.16,1,.3,1),border-color .3s,box-shadow .3s;
  display:flex;flex-direction:column;
}
.rd-bv-card:hover { transform:translateY(-4px);border-color:rgba(128,0,252,.25);box-shadow:0 20px 50px rgba(33,18,61,.08); }
.rd-bv-card-header {
  background:linear-gradient(135deg,var(--rd-soft) 0%,var(--rd-soft-2) 100%);
  padding:28px;border-bottom:1.5px solid var(--rd-border);
  display:flex;align-items:center;gap:16px;
}
.rd-bv-card-icon {
  width:52px;height:52px;border-radius:14px;flex-shrink:0;
  background:linear-gradient(135deg,var(--rd-blue),var(--rd-purple));
  display:flex;align-items:center;justify-content:center;font-size:22px;
}
.rd-bv-card-tag {
  display:inline-flex;padding:4px 10px;border-radius:999px;
  background:rgba(128,0,252,.09);color:var(--rd-purple)!important;
  font-family:var(--rd-font-mono)!important;font-size:10px!important;
  font-weight:600!important;letter-spacing:.1em;text-transform:uppercase;
}
.rd-bv-card-body { padding:24px;flex:1;display:flex;flex-direction:column;gap:10px; }
.rd-bv-card h3 { font-size:18px!important;font-weight:700!important;color:#20152f!important;margin:0!important;letter-spacing:-.02em; }
.rd-bv-card p { font-size:14px!important;color:var(--rd-text-2)!important;margin:0!important;line-height:1.6!important;flex:1; }
.rd-bv-card-footer { padding:0 24px 24px; }

/* INLINE PROMO BAND */
.rd-bv-promo {
  display:flex;align-items:center;justify-content:space-between;gap:20px;flex-wrap:wrap;
  padding:22px 28px;border-radius:14px;margin:40px 0;
  background:var(--rd-soft-2);border:1.5px solid var(--rd-border);border-left:4px solid var(--rd-purple);
}
.rd-bv-promo p { margin:0!important;color:var(--rd-text)!important;font-size:15px!important;font-weight:500!important; }
.rd-bv-promo p em { font-family:var(--rd-font-display)!important;font-style:italic;color:var(--rd-purple);font-weight:400!important; }

/* NEWSLETTER */
.rd-bv-newsletter-inner {
  border-radius:24px;padding:56px;
  background:radial-gradient(circle at 86% 16%,rgba(227,0,255,.24),transparent 30%),
             linear-gradient(135deg,#21123D 0%,#32155b 100%);
  display:grid;grid-template-columns:1.2fr 0.8fr;gap:40px;align-items:center;position:relative;overflow:hidden;
}
.rd-bv-newsletter-grid-bg {
  position:absolute;inset:0;
  background-image:linear-gradient(rgba(255,255,255,.04) 1px,transparent 1px),
                   linear-gradient(90deg,rgba(255,255,255,.04) 1px,transparent 1px);
  background-size:48px 48px;pointer-events:none;
}
.rd-bv-newsletter-inner > * { position:relative;z-index:1; }
.rd-bv-newsletter-inner h2 {
  color:#fff!important;font-size:clamp(26px,3.2vw,38px)!important;
  font-weight:800!important;margin:0 0 12px!important;letter-spacing:-.04em!important;
  font-family:var(--rd-font-body)!important;
}
.rd-bv-newsletter-inner h2 em {
  font-family:var(--rd-font-display)!important;font-style:italic;font-weight:400!important;
  background:linear-gradient(90deg,#fff,#f13fff);-webkit-background-clip:text;background-clip:text;color:transparent!important;
}
.rd-bv-newsletter-inner p { color:rgba(255,255,255,.78)!important;font-size:15px!important;margin:0!important;line-height:1.65!important; }
.rd-bv-newsletter-aside { display:flex;flex-direction:column;gap:16px; }
.rd-bv-newsletter-form { background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.14);border-radius:12px;padding:20px;text-align:center;color:rgba(255,255,255,.6)!important;font-size:13px!important; }
/* MAILERLITE_FORM */
.rd-bv-newsletter-meta { color:rgba(255,255,255,.5)!important;font-family:var(--rd-font-mono)!important;font-size:10px!important;text-transform:uppercase;letter-spacing:.1em;display:flex;flex-direction:column;gap:6px; }
.rd-bv-newsletter-meta span { display:flex;align-items:center;gap:8px; }
.rd-bv-newsletter-meta span::before { content:"";width:4px;height:4px;background:var(--rd-pink);border-radius:50%;flex-shrink:0; }

/* SERVICE CROSS-SELL */
.rd-bv-service-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:20px; }
.rd-bv-service-card {
  padding:28px;border-radius:18px;background:#fff!important;
  border:1.5px solid var(--rd-border);
  transition:transform .35s cubic-bezier(.16,1,.3,1),border-color .3s,box-shadow .3s;
}
.rd-bv-service-card:hover { transform:translateY(-3px);border-color:rgba(128,0,252,.22);box-shadow:0 16px 40px rgba(33,18,61,.06); }
.rd-bv-service-card-icon { font-size:28px;margin-bottom:14px;display:block; }
.rd-bv-service-card h3 { font-size:17px!important;font-weight:700!important;color:#20152f!important;margin:0 0 8px!important;letter-spacing:-.02em; }
.rd-bv-service-card p { font-size:14px!important;color:var(--rd-text-2)!important;margin:0 0 18px!important;line-height:1.55!important; }

/* COMING SOON */
.rd-bv-coming-list { display:grid;gap:12px;max-width:700px;margin:0 auto; }
.rd-bv-coming-item {
  display:flex;align-items:center;gap:16px;padding:16px 20px;
  border-radius:12px;background:var(--rd-soft-2);border:1.5px solid var(--rd-border);
  opacity:.65;
}
.rd-bv-coming-tag {
  flex-shrink:0;padding:4px 10px;border-radius:999px;
  background:rgba(128,0,252,.09);color:var(--rd-purple)!important;
  font-family:var(--rd-font-mono)!important;font-size:10px!important;font-weight:600!important;letter-spacing:.08em;text-transform:uppercase;
}
.rd-bv-coming-item span { font-size:14px!important;color:var(--rd-text-2)!important;font-weight:500!important; }

/* REVEAL */
.rd-bv-reveal { opacity:0;transform:translateY(22px);transition:opacity .8s cubic-bezier(.16,1,.3,1),transform .8s cubic-bezier(.16,1,.3,1); }
.rd-bv-reveal.in { opacity:1;transform:translateY(0); }

/* RESPONSIVE */
@media (max-width:940px) {
  .rd-bv-hero-inner { grid-template-columns:1fr; }
  .rd-bv-featured-card { display:none; }
  .rd-bv-newsletter-inner { grid-template-columns:1fr;padding:36px; }
  .rd-bv-service-grid { grid-template-columns:1fr 1fr; }
  .rd-bv-grid-2 { grid-template-columns:1fr; }
}
@media (max-width:600px) {
  .rd-bv-hero { padding:60px 20px 56px; }
  .rd-bv-section { padding:56px 0; }
  .rd-bv-grid { grid-template-columns:1fr; }
  .rd-bv-service-grid { grid-template-columns:1fr; }
  .rd-bv-actions { flex-direction:column;align-items:stretch; }
  .rd-bv-btn { width:100%;justify-content:center; }
  .rd-bv-promo { flex-direction:column;align-items:flex-start; }
  .rd-bv-stats { gap:12px; }
}
</style>

<div class="rd-bv">

<!-- HERO -->
<header class="rd-bv-hero">
  <div class="rd-bv-hero-grid-bg"></div>
  <div class="rd-bv-wrap">
    <div class="rd-bv-hero-inner">
      <div>
        <span class="rd-bv-eyebrow"><span class="rd-bv-eyebrow-dot"></span>Recursos gratuitos &bull; Actualizado mensualmente</span>
        <h1>La <em>B&oacute;veda.</em></h1>
        <p class="rd-bv-lead">Todo el conocimiento pr&aacute;ctico sobre IA para empresas, sin humo ni teor&iacute;a vac&iacute;a. Manuales que puedes aplicar esta semana.</p>
        <div class="rd-bv-stats">
          <div class="rd-bv-stat"><strong>2</strong><span>manuales activos</span></div>
          <div class="rd-bv-stat"><strong>3</strong><span>cursos disponibles</span></div>
          <div class="rd-bv-stat"><strong>&#8734;</strong><span>100% gratuito</span></div>
        </div>
        <div class="rd-bv-actions">
          <a href="#manuales" class="rd-bv-btn">Ver manuales &#8594;</a>
          <a href="#newsletter" class="rd-bv-btn rd-bv-btn-ghost">Suscribirme</a>
        </div>
      </div>
      <div class="rd-bv-featured-card">
        <div class="rd-bv-featured-visual"><span>&#128218;</span></div>
        <span class="rd-bv-tag">Destacado</span>
        <h3>Manual Notebook LM</h3>
        <p>La gu&iacute;a m&aacute;s completa para usar NotebookLM de Google en tu negocio. Paso a paso, con casos pr&aacute;cticos.</p>
        <a href="/manual-notebook-lm/" class="rd-bv-btn rd-bv-btn-sm">Leer manual &#8594;</a>
      </div>
    </div>
  </div>
</header>

<!-- MANUALES -->
<section id="manuales" class="rd-bv-section">
  <div class="rd-bv-wrap">
    <div class="rd-bv-section-title rd-bv-reveal">
      <div class="rd-bv-level"><div class="rd-bv-level-line"></div><span>Disponible ahora</span></div>
      <h2>Manuales <em>gratuitos.</em></h2>
      <p>Gu&iacute;as paso a paso para implementar herramientas de IA en tu d&iacute;a a d&iacute;a. Sin conocimientos t&eacute;cnicos previos.</p>
    </div>
    <div class="rd-bv-grid rd-bv-grid-2 rd-bv-reveal">

      <div class="rd-bv-card">
        <div class="rd-bv-card-header">
          <div class="rd-bv-card-icon">&#128218;</div>
          <div>
            <span class="rd-bv-card-tag">IA + Productividad</span>
          </div>
        </div>
        <div class="rd-bv-card-body">
          <h3>Manual Notebook LM</h3>
          <p>Aprende a usar NotebookLM de Google para analizar documentos, crear res&uacute;menes y generar audio autom&aacute;ticamente. El asistente de investigaci&oacute;n m&aacute;s potente y gratuito del mercado.</p>
        </div>
        <div class="rd-bv-card-footer">
          <a href="/manual-notebook-lm/" class="rd-bv-btn rd-bv-btn-sm">Leer manual &#8594;</a>
        </div>
      </div>

      <div class="rd-bv-card">
        <div class="rd-bv-card-header">
          <div class="rd-bv-card-icon" style="background:linear-gradient(135deg,#8000FC,#E300FF);">&#129302;</div>
          <div>
            <span class="rd-bv-card-tag">Agente IA</span>
          </div>
        </div>
        <div class="rd-bv-card-body">
          <h3>Manual de Claudia</h3>
          <p>C&oacute;mo configurar y trabajar con Claudia, el agente de IA de Riqueza Digital. Delega tareas complejas al agente y recupera horas de trabajo a la semana.</p>
        </div>
        <div class="rd-bv-card-footer">
          <a href="/manual-de-claudia/" class="rd-bv-btn rd-bv-btn-sm">Leer manual &#8594;</a>
        </div>
      </div>

    </div>

    <div class="rd-bv-promo rd-bv-reveal">
      <p>&#127891; &iquest;Tu equipo necesita formaci&oacute;n estructurada en <em>IA aplicada</em>?</p>
      <a href="/cursos/" class="rd-bv-btn rd-bv-btn-sm">Ver cursos &#8594;</a>
    </div>
  </div>
</section>

<!-- FORMACIÓN -->
<section class="rd-bv-section rd-bv-section-soft">
  <div class="rd-bv-wrap">
    <div class="rd-bv-section-title rd-bv-reveal">
      <div class="rd-bv-level"><div class="rd-bv-level-line"></div><span>Formaci&oacute;n</span></div>
      <h2>Cursos para tu <em>equipo.</em></h2>
      <p>Formaci&oacute;n pr&aacute;ctica para que tu empresa aplique la IA sin depender de consultores externos.</p>
    </div>
    <div class="rd-bv-grid rd-bv-reveal">
      <div class="rd-bv-card">
        <div class="rd-bv-card-header">
          <div class="rd-bv-card-icon" style="background:linear-gradient(135deg,#0530FA,#8000FC);">&#129504;</div>
          <span class="rd-bv-card-tag">Fundamentos</span>
        </div>
        <div class="rd-bv-card-body">
          <h3>Aprender a pensar en IA</h3>
          <p>Curso pr&aacute;ctico para empezar desde cero. Ideal para equipos que a&uacute;n no usan IA en su d&iacute;a a d&iacute;a.</p>
        </div>
        <div class="rd-bv-card-footer">
          <a href="/aprender-a-pensar-en-ia/" class="rd-bv-btn rd-bv-btn-sm rd-bv-btn-outline">Ver curso &#8594;</a>
        </div>
      </div>
      <div class="rd-bv-card">
        <div class="rd-bv-card-header">
          <div class="rd-bv-card-icon" style="background:linear-gradient(135deg,#0530FA,#E300FF);">&#127970;</div>
          <span class="rd-bv-card-tag">Empresa</span>
        </div>
        <div class="rd-bv-card-body">
          <h3>Integrar la IA en tu negocio</h3>
          <p>Estrategia y herramientas para implementar IA en los procesos de tu empresa de forma ordenada.</p>
        </div>
        <div class="rd-bv-card-footer">
          <a href="/integrar-ia-en-tu-negocio/" class="rd-bv-btn rd-bv-btn-sm rd-bv-btn-outline">Ver curso &#8594;</a>
        </div>
      </div>
      <div class="rd-bv-card">
        <div class="rd-bv-card-header">
          <div class="rd-bv-card-icon" style="background:linear-gradient(135deg,#8000FC,#E300FF);">&#128187;</div>
          <span class="rd-bv-card-tag">T&eacute;cnico</span>
        </div>
        <div class="rd-bv-card-body">
          <h3>Programar de forma ag&eacute;ntica</h3>
          <p>Para desarrolladores: construye sistemas de agentes que ejecutan tareas de forma aut&oacute;noma.</p>
        </div>
        <div class="rd-bv-card-footer">
          <a href="/programar-forma-agentica/" class="rd-bv-btn rd-bv-btn-sm rd-bv-btn-outline">Ver curso &#8594;</a>
        </div>
      </div>
    </div>

    <div class="rd-bv-promo rd-bv-reveal">
      <p>&#128640; &iquest;Prefieres que implementemos la IA en tu empresa <em>directamente</em>?</p>
      <a href="/contacto/" class="rd-bv-btn rd-bv-btn-sm">Hablemos &#8594;</a>
    </div>
  </div>
</section>

<!-- NEWSLETTER -->
<section id="newsletter" class="rd-bv-section" style="background:#fff!important;">
  <div class="rd-bv-wrap">
    <div class="rd-bv-newsletter-inner rd-bv-reveal">
      <div class="rd-bv-newsletter-grid-bg"></div>
      <div>
        <span style="display:inline-block;color:#ff7cff;font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;margin-bottom:14px;">Comunidad gratuita</span>
        <h2>Recibe los pr&oacute;ximos recursos <em>antes que nadie.</em></h2>
        <p>Cada nuevo manual, gu&iacute;a y recurso llega primero a los suscriptores. Sin spam, solo contenido que puedes aplicar esta semana.</p>
      </div>
      <div class="rd-bv-newsletter-aside">
        <div class="rd-bv-newsletter-form">
          <!-- MAILERLITE_FORM -->
          <p style="color:rgba(255,255,255,.5);margin:0;font-size:13px;">Formulario de suscripci&oacute;n<br><small>&#8594; Integrar MailerLite aqu&iacute;</small></p>
        </div>
        <div class="rd-bv-newsletter-meta">
          <span>Sin spam, s&oacute;lo valor</span>
          <span>Nuevo manual cada mes</span>
          <span>Pr&oacute;ximamente: canal Telegram</span>
        </div>
      </div>
    </div>
  </div>
</section>

<!-- SERVICIOS CROSS-SELL -->
<section class="rd-bv-section rd-bv-section-soft">
  <div class="rd-bv-wrap">
    <div class="rd-bv-section-title rd-bv-reveal">
      <div class="rd-bv-level"><div class="rd-bv-level-line"></div><span>Servicios</span></div>
      <h2>&iquest;Quieres que lo hagamos <em>nosotros?</em></h2>
      <p>Si prefieres delegar la implementaci&oacute;n, gestionamos tus campa&ntilde;as, dise&ntilde;amos tu web y posicionamos tu marca donde est&aacute;n tus clientes.</p>
    </div>
    <div class="rd-bv-service-grid rd-bv-reveal">
      <div class="rd-bv-service-card">
        <span class="rd-bv-service-card-icon">&#128200;</span>
        <h3>Google Ads</h3>
        <p>Gesti&oacute;n completa de campa&ntilde;as SEM. Captamos leads cualificados para tu negocio con presupuesto controlado.</p>
        <a href="/servicios-google-ads/" class="rd-bv-btn rd-bv-btn-sm">Ver servicio &#8594;</a>
      </div>
      <div class="rd-bv-service-card">
        <span class="rd-bv-service-card-icon">&#9889;</span>
        <h3>Web con IA Ag&eacute;ntica</h3>
        <p>Tu web capta visitas, cualifica leads y reserva llamadas autom&aacute;ticamente. Sin depender de que nadie est&eacute; online.</p>
        <a href="/servicios-web-ia/" class="rd-bv-btn rd-bv-btn-sm">Ver servicio &#8594;</a>
      </div>
      <div class="rd-bv-service-card">
        <span class="rd-bv-service-card-icon">&#127919;</span>
        <h3>Posicionamiento en IAs</h3>
        <p>Aparece en ChatGPT, Perplexity y Google IA cuando tus clientes buscan tu tipo de servicio. GEO para pymes.</p>
        <a href="/posicionamiento-ia/" class="rd-bv-btn rd-bv-btn-sm">Ver servicio &#8594;</a>
      </div>
    </div>
  </div>
</section>

<!-- COMING SOON -->
<section class="rd-bv-section">
  <div class="rd-bv-wrap">
    <div class="rd-bv-section-title rd-bv-reveal">
      <div class="rd-bv-level"><div class="rd-bv-level-line"></div><span>En camino</span></div>
      <h2>Pr&oacute;ximos <em>recursos.</em></h2>
      <p>Suscr&iacute;bete arriba para recibirlos cuando salgan.</p>
    </div>
    <div class="rd-bv-coming-list rd-bv-reveal">
      <div class="rd-bv-coming-item"><span class="rd-bv-coming-tag">Google Ads</span><span>Gu&iacute;a completa Google Ads para pymes con presupuesto ajustado</span></div>
      <div class="rd-bv-coming-item"><span class="rd-bv-coming-tag">Meta Ads</span><span>Meta Ads sin malgastar: segmentaci&oacute;n y creatividades que convierten</span></div>
      <div class="rd-bv-coming-item"><span class="rd-bv-coming-tag">Posicionamiento IA</span><span>C&oacute;mo aparecer en ChatGPT cuando buscan tu servicio</span></div>
      <div class="rd-bv-coming-item"><span class="rd-bv-coming-tag">WordPress</span><span>Checklist de lanzamiento web: SEO, velocidad y conversi&oacute;n</span></div>
    </div>
  </div>
</section>

</div>

<script>
(function() {
  var items = document.querySelectorAll('.rd-bv-reveal');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
    items.forEach(function(el) { io.observe(el); });
  } else {
    items.forEach(function(el) { el.classList.add('in'); });
  }
})();
</script>
"""

push(6835,
     'La Bóveda — Recursos y Manuales de IA',
     BOVEDA,
     'La Bóveda — Manuales y Recursos de IA | Riqueza Digital',
     'Manuales gratuitos, guías y recursos prácticos sobre inteligencia artificial para empresas.',
     'manuales inteligencia artificial empresas')
print("Bóveda done.")
