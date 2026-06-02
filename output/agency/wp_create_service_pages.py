"""Create service pages: /servicios-web-ia/ and /posicionamiento-ia/"""
import urllib.request, base64, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

url = os.environ['WP_RD_URL']
user = os.environ['WP_RD_USER']
pwd = os.environ['WP_RD_APP_PASSWORD']
token = base64.b64encode(f'{user}:{pwd}'.encode()).decode()
h = {'Authorization': f'Basic {token}', 'Content-Type': 'application/json; charset=utf-8'}

WEB_IA_CONTENT = """
<style>
.rd-svc{max-width:960px;margin:0 auto;padding:0 24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1f1f2e}
.rd-svc-hero{background:linear-gradient(135deg,#21123D 0%,#0530FA 100%);color:#fff;padding:72px 40px;border-radius:16px;margin-bottom:56px;text-align:center}
.rd-svc-hero h1{font-size:2.4em;margin:0 0 16px;line-height:1.2}
.rd-svc-hero p{font-size:1.2em;opacity:.85;max-width:600px;margin:0 auto 28px}
.rd-svc-hero a{display:inline-block;background:#fff;color:#21123D;font-weight:700;padding:14px 36px;border-radius:8px;text-decoration:none;font-size:1.05em}
.rd-section{margin-bottom:56px}
.rd-section h2{font-size:1.7em;color:#21123D;margin-bottom:20px}
.rd-section h3{font-size:1.15em;color:#21123D;margin:0 0 8px}
.rd-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:24px}
.rd-card{border:1.5px solid #e8e4f0;border-radius:12px;padding:24px;background:#faf8fd}
.rd-card .icon{font-size:1.8em;margin-bottom:12px}
.rd-card p{margin:0;font-size:.9em;color:#514b5f;line-height:1.6}
.rd-steps{counter-reset:steps;list-style:none;padding:0}
.rd-steps li{counter-increment:steps;padding:20px 20px 20px 72px;position:relative;border-left:3px solid #8000FC;margin-bottom:16px;background:#faf8fd;border-radius:0 12px 12px 0}
.rd-steps li::before{content:counter(steps);position:absolute;left:20px;top:20px;background:#8000FC;color:#fff;width:32px;height:32px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:.9em}
.rd-cta{background:linear-gradient(135deg,#21123D 0%,#2B174D 100%);color:#fff;padding:48px 40px;border-radius:16px;text-align:center;margin-top:56px}
.rd-cta h2{color:#fff;margin:0 0 16px;font-size:1.8em}
.rd-cta p{opacity:.9;margin:0 0 24px;font-size:1.05em}
.rd-cta a{display:inline-block;background:#8000FC;color:#fff;font-weight:700;padding:14px 36px;border-radius:8px;text-decoration:none;font-size:1.05em}
.rd-faq{margin-bottom:56px}
.rd-faq h2{font-size:1.7em;color:#21123D;margin-bottom:24px}
.rd-faq details{border:1.5px solid #e8e4f0;border-radius:10px;padding:16px 20px;margin-bottom:12px;background:#faf8fd}
.rd-faq summary{font-weight:600;cursor:pointer;color:#21123D;font-size:1em}
.rd-faq details p{margin:12px 0 0;color:#514b5f;line-height:1.6;font-size:.95em}
</style>

<div class="rd-svc">

<div class="rd-svc-hero">
<h1>Webs con IA Agéntica</h1>
<p>No solo un sitio web. Un sistema que capta visitas, cualifica leads y reserva llamadas mientras tú duermes.</p>
<a href="/contacto/">Pedir presupuesto &#8594;</a>
</div>

<div class="rd-section">
<h2>¿Qué es una web con IA agéntica?</h2>
<p>Una web tradicional muestra información. Una web con IA agéntica <strong>actúa</strong>: responde preguntas en tiempo real, cualifica al visitante según su perfil, le muestra el contenido más relevante y le guía hacia la conversión automáticamente. Sin depender de que alguien esté online.</p>
<p>En Riqueza Digital construimos webs que integran agentes de IA conectados a tus procesos de negocio: desde el primer clic hasta el lead cualificado en tu CRM.</p>
</div>

<div class="rd-section">
<h2>Qué incluye</h2>
<div class="rd-grid">
<div class="rd-card"><div class="icon">&#129302;</div><h3>Agente conversacional entrenado</h3><p>Un asistente IA que conoce tu negocio, responde preguntas frecuentes y capta leads 24/7 sin soporte humano.</p></div>
<div class="rd-card"><div class="icon">&#9889;</div><h3>Diseño Elementor profesional</h3><p>Landing pages y webs corporativas rápidas, responsive y optimizadas para conversión desde el primer día.</p></div>
<div class="rd-card"><div class="icon">&#128279;</div><h3>Integración con tus herramientas</h3><p>Conectamos la web con tu CRM, WhatsApp, email marketing y calendario. Los leads entran solos.</p></div>
<div class="rd-card"><div class="icon">&#128200;</div><h3>SEO técnico y de contenido</h3><p>Yoast SEO configurado, schema markup, velocidad optimizada y estructura pensada para posicionar en Google y en IAs.</p></div>
<div class="rd-card"><div class="icon">&#128202;</div><h3>Analytics y seguimiento</h3><p>Google Tag Manager, GA4 y seguimiento de conversiones para que sepas exactamente qué funciona.</p></div>
<div class="rd-card"><div class="icon">&#128737;</div><h3>Seguridad y mantenimiento</h3><p>SSL, backups, actualizaciones y monitorización. Tu web siempre operativa.</p></div>
</div>
</div>

<div class="rd-section">
<h2>Cómo trabajamos</h2>
<ol class="rd-steps">
<li><strong>Diagnóstico (1 semana):</strong> Analizamos tu negocio, clientes objetivo y competencia. Definimos la arquitectura de la web y los flujos del agente IA.</li>
<li><strong>Diseño y maquetación (2 semanas):</strong> Construcción en Elementor con tu identidad visual. Revisiones hasta aprobación.</li>
<li><strong>Integración IA (1 semana):</strong> Configuramos el agente, conectamos integraciones y probamos todos los flujos de captación.</li>
<li><strong>Lanzamiento y formación:</strong> Publicación, configuración SEO completa y sesión de formación para que gestiones la web de forma autónoma.</li>
</ol>
</div>

<div class="rd-section">
<h2>¿Para quién es?</h2>
<p>Este servicio es ideal si:</p>
<ul>
<li>Tienes una web antigua que no genera leads</li>
<li>Recibes muchas preguntas repetidas por WhatsApp o email y quieres automatizarlas</li>
<li>Quieres una presencia digital que trabaje sola mientras tú te centras en el negocio</li>
<li>Estás lanzando un nuevo servicio o producto y necesitas una landing de alta conversión</li>
</ul>
<p>¿Gestionas campañas de publicidad? Combina esta web con nuestro servicio de <a href="/servicios-google-ads/">Google Ads</a> o <a href="/posicionamiento-ia/">posicionamiento en IAs</a> para maximizar el retorno.</p>
</div>

<div class="rd-faq">
<h2>Preguntas frecuentes</h2>
<details><summary>¿Cuánto cuesta una web con IA agéntica?</summary><p>Cada proyecto es diferente. El precio depende del número de páginas, complejidad del agente IA y las integraciones requeridas. Escríbenos y te preparamos un presupuesto en 48 horas.</p></details>
<details><summary>¿Qué diferencia hay con una web normal?</summary><p>Una web normal muestra información estática. Una web agéntica tiene un sistema IA que interactúa con el visitante, responde preguntas, cualifica su interés y lo guía hacia la acción (llamada, formulario, compra) de forma personalizada.</p></details>
<details><summary>¿Necesito conocimientos técnicos para mantenerla?</summary><p>No. Usamos WordPress con Elementor, la plataforma más usada del mundo. Incluimos formación y soporte post-lanzamiento. La mayoría de nuestros clientes gestionan su web sin ayuda externa.</p></details>
<details><summary>¿Cuánto tarda en estar lista?</summary><p>Normalmente entre 4 y 6 semanas desde el inicio del proyecto hasta el lanzamiento. El plazo depende de la velocidad de revisiones y aprobaciones por tu parte.</p></details>
<details><summary>¿Podéis mejorar mi web actual en lugar de hacer una nueva?</summary><p>Sí. Podemos integrar el agente IA y las automatizaciones en una web WordPress existente sin rehacerla desde cero. Consúltanos tu caso.</p></details>
</div>

<div class="rd-cta">
<h2>¿Lista para tener una web que trabaja mientras duermes?</h2>
<p>Cuéntanos tu proyecto. Te respondemos en menos de 24 horas.</p>
<a href="/contacto/">Quiero más información &#8594;</a>
</div>

</div>
"""

POS_IA_CONTENT = """
<style>
.rd-svc{max-width:960px;margin:0 auto;padding:0 24px;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;color:#1f1f2e}
.rd-svc-hero{background:linear-gradient(135deg,#0530FA 0%,#E300FF 100%);color:#fff;padding:72px 40px;border-radius:16px;margin-bottom:56px;text-align:center}
.rd-svc-hero h1{font-size:2.4em;margin:0 0 16px;line-height:1.2}
.rd-svc-hero p{font-size:1.2em;opacity:.85;max-width:600px;margin:0 auto 28px}
.rd-svc-hero a{display:inline-block;background:#fff;color:#21123D;font-weight:700;padding:14px 36px;border-radius:8px;text-decoration:none;font-size:1.05em}
.rd-section{margin-bottom:56px}
.rd-section h2{font-size:1.7em;color:#21123D;margin-bottom:20px}
.rd-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:24px}
.rd-card{border:1.5px solid #e8e4f0;border-radius:12px;padding:24px;background:#faf8fd}
.rd-card .icon{font-size:1.8em;margin-bottom:12px}
.rd-card h3{margin:0 0 8px;font-size:1.05em;color:#21123D}
.rd-card p{margin:0;font-size:.9em;color:#514b5f;line-height:1.6}
.rd-highlight{background:linear-gradient(135deg,#f7f4fb 0%,#faf8fd 100%);border:2px solid #8000FC;border-radius:16px;padding:32px;margin:32px 0;text-align:center}
.rd-highlight .big{font-size:2em;font-weight:800;color:#8000FC;margin:0 0 8px}
.rd-highlight p{color:#514b5f;margin:0;font-size:1.05em}
.rd-platforms{display:flex;gap:16px;flex-wrap:wrap;margin:24px 0}
.rd-platforms span{background:#21123D;color:#fff;padding:8px 20px;border-radius:20px;font-size:.9em;font-weight:600}
.rd-cta{background:linear-gradient(135deg,#0530FA 0%,#21123D 100%);color:#fff;padding:48px 40px;border-radius:16px;text-align:center;margin-top:56px}
.rd-cta h2{color:#fff;margin:0 0 16px;font-size:1.8em}
.rd-cta p{opacity:.9;margin:0 0 24px;font-size:1.05em}
.rd-cta a{display:inline-block;background:#fff;color:#0530FA;font-weight:700;padding:14px 36px;border-radius:8px;text-decoration:none;font-size:1.05em}
.rd-faq{margin-bottom:56px}
.rd-faq h2{font-size:1.7em;color:#21123D;margin-bottom:24px}
.rd-faq details{border:1.5px solid #e8e4f0;border-radius:10px;padding:16px 20px;margin-bottom:12px;background:#faf8fd}
.rd-faq summary{font-weight:600;cursor:pointer;color:#21123D}
.rd-faq details p{margin:12px 0 0;color:#514b5f;line-height:1.6;font-size:.95em}
</style>

<div class="rd-svc">

<div class="rd-svc-hero">
<h1>Aparece en ChatGPT, Perplexity y Google IA</h1>
<p>El 40% de las búsquedas de compra ya empiezan en un asistente de IA. ¿Aparece tu empresa cuando tu cliente potencial pregunta?</p>
<a href="/contacto/">Quiero aparecer en las IAs &#8594;</a>
</div>

<div class="rd-section">
<div class="rd-highlight">
<div class="big">40%</div>
<p>de las búsquedas comerciales ocurren en ChatGPT, Perplexity o Google AI Overviews. La mayoría de empresas españolas no aparecen en ninguna.</p>
</div>
<h2>El nuevo SEO es ser citado por las IAs</h2>
<p>Cuando alguien pregunta a ChatGPT <em>¿qué agencia de marketing digital es buena en Barcelona?</em> o a Perplexity <em>¿cómo mejorar el ROI de mis campañas?</em>, los modelos de IA responden con fuentes que han aprendido a considerar <strong>fiables y relevantes</strong>.</p>
<p>Esto no es magia. Es <strong>GEO (Generative Engine Optimization)</strong>: la disciplina de estructurar tu contenido, autoridad y presencia digital para que los sistemas de IA te citen como respuesta a las preguntas de tus clientes potenciales.</p>
<p>En Riqueza Digital somos pioneros en GEO para pymes en España. Combinamos estrategia de contenido, SEO técnico y señales de autoridad para posicionar tu marca donde están tus compradores ahora mismo.</p>
</div>

<div class="rd-section">
<h2>Dónde te posicionamos</h2>
<div class="rd-platforms">
<span>ChatGPT</span><span>Perplexity</span><span>Google AI Overviews</span><span>Gemini</span><span>Claude</span><span>Bing Copilot</span>
</div>
<p>Cada plataforma tiene sus propias señales de confianza. Diseñamos una estrategia específica para cada una, sin atajos ni técnicas que expiren al próximo algoritmo.</p>
</div>

<div class="rd-section">
<h2>Qué incluye el servicio</h2>
<div class="rd-grid">
<div class="rd-card"><div class="icon">&#127919;</div><h3>Auditoría de presencia en IAs</h3><p>Analizamos qué responden ChatGPT, Perplexity y Google IA cuando preguntan por tu sector. Identificamos el gap respecto a tu competencia.</p></div>
<div class="rd-card"><div class="icon">&#9998;</div><h3>Contenido estructurado para IA</h3><p>Creamos y optimizamos páginas, FAQs y artículos con el formato que los modelos de IA priorizan como fuente de respuesta.</p></div>
<div class="rd-card"><div class="icon">&#128278;</div><h3>Schema markup y datos estructurados</h3><p>Implementamos marcado técnico (JSON-LD) para que Google y los LLMs entiendan exactamente qué ofreces, dónde estás y a quién.</p></div>
<div class="rd-card"><div class="icon">&#127942;</div><h3>Construcción de autoridad digital</h3><p>Estrategia de menciones, backlinks y presencia en fuentes que los modelos de IA consideran fiables para tu industria.</p></div>
<div class="rd-card"><div class="icon">&#128225;</div><h3>Monitorización de citas en IA</h3><p>Seguimiento mensual de cuántas veces y cómo te citan los principales asistentes IA. Informe de evolución y ajuste de estrategia.</p></div>
<div class="rd-card"><div class="icon">&#128279;</div><h3>Integración con SEO tradicional</h3><p>GEO y SEO no son rivales. Coordinamos ambas estrategias para que se potencien mutuamente.</p></div>
</div>
</div>

<div class="rd-section">
<h2>¿Para quién es?</h2>
<p>Este servicio es ideal si:</p>
<ul>
<li>Vendes servicios B2B o de alto valor donde la confianza es fundamental</li>
<li>Tus clientes investigan mucho antes de comprar</li>
<li>Quieres ser la referencia en tu sector en los próximos 12-24 meses</li>
<li>Tu competencia todavía no está posicionada en IAs (ventana de oportunidad ahora)</li>
</ul>
<p>¿También tienes campañas de pago? Combina el posicionamiento orgánico con <a href="/servicios-google-ads/">Google Ads</a> o con una <a href="/servicios-web-ia/">web IA agéntica</a> para dominar todos los canales donde están tus clientes.</p>
</div>

<div class="rd-faq">
<h2>Preguntas frecuentes sobre posicionamiento en IAs</h2>
<details><summary>¿Qué es GEO y cómo se diferencia del SEO tradicional?</summary><p>SEO optimiza para que Google te muestre en sus resultados de búsqueda. GEO (Generative Engine Optimization) optimiza para que los modelos de IA te citen como fuente de respuesta cuando sus usuarios hacen preguntas. Son disciplinas complementarias: el SEO te da tráfico directo, el GEO te da autoridad e impacto indirecto en la decisión de compra.</p></details>
<details><summary>¿Cuánto tiempo tarda en dar resultados?</summary><p>Las primeras citas en IAs suelen aparecer entre 2 y 4 meses. La construcción de autoridad sostenible es un proceso de 6 a 12 meses. Es una inversión a largo plazo, pero quienes empiezan ahora tendrán una ventaja enorme sobre los que esperen.</p></details>
<details><summary>¿Se puede medir el impacto en las IAs?</summary><p>Sí. Monitorizamos regularmente las respuestas de ChatGPT, Perplexity y Google AI sobre queries clave de tu sector. También rastreamos el tráfico de referencia procedente de herramientas IA mediante UTMs y GA4.</p></details>
<details><summary>¿Funciona para cualquier sector?</summary><p>Especialmente bien en servicios profesionales, tecnología, salud, formación y cualquier sector donde el cliente investiga antes de comprar. Si tus clientes usan ChatGPT para buscar soluciones, el GEO es relevante para ti.</p></details>
<details><summary>¿Puedo combinarlo con mi SEO actual?</summary><p>Sí, y es lo recomendable. El contenido bien estructurado para IAs también mejora el posicionamiento en Google. Podemos coordinarnos con tu equipo SEO existente o gestionar ambos.</p></details>
</div>

<div class="rd-cta">
<h2>Tu competencia todavía no está en las IAs. Sé el primero.</h2>
<p>Auditamos gratis qué responden ChatGPT y Perplexity cuando preguntan por tu sector. Sin compromiso.</p>
<a href="/contacto/">Solicitar auditoría gratuita &#8594;</a>
</div>

</div>
"""

pages = [
    {
        'title': 'Webs con IA Agéntica — Diseño Web Inteligente para Empresas',
        'slug': 'servicios-web-ia',
        'content': WEB_IA_CONTENT,
        'focuskw': 'web inteligencia artificial agéntica',
        'metadesc': 'Diseño y desarrollo de webs con inteligencia artificial agéntica. Tu web capta leads, responde preguntas y convierte visitas en clientes automáticamente.',
        'seotitle': 'Webs con IA Agéntica Barcelona | Riqueza Digital',
    },
    {
        'title': 'Posicionamiento en ChatGPT y otras IAs — GEO para Empresas',
        'slug': 'posicionamiento-ia',
        'content': POS_IA_CONTENT,
        'focuskw': 'posicionamiento chatgpt empresas',
        'metadesc': 'Aparece en ChatGPT, Perplexity y Google AI cuando tus clientes preguntan. Servicio GEO (Generative Engine Optimization) para pymes en España.',
        'seotitle': 'Posicionamiento en ChatGPT y Perplexity | GEO | Riqueza Digital',
    },
]

created = {}
for p in pages:
    payload = {
        'title': p['title'],
        'slug': p['slug'],
        'status': 'publish',
        'content': p['content'],
        'meta': {
            'yoast_wpseo_title': p['seotitle'],
            'yoast_wpseo_metadesc': p['metadesc'],
            'yoast_wpseo_focuskw': p['focuskw'],
        }
    }
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(f'{url}/wp-json/wp/v2/pages', data=body, headers=h, method='POST')
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read())
        created[p['slug']] = res['id']
        print(f"OK — {p['slug']} | ID:{res['id']} | {res['link']}")

print(json.dumps(created))
