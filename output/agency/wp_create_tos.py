"""Crea la página Términos y Condiciones del Servicio en riquezadigital.es"""
import winreg, base64, json, urllib.request, urllib.error, sys

def get_env(name):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")
    val, _ = winreg.QueryValueEx(key, name)
    winreg.CloseKey(key)
    return val

WP_URL  = get_env("WP_RD_URL").rstrip("/")
WP_USER = get_env("WP_RD_USER")
WP_PW   = get_env("WP_RD_APP_PASSWORD")

auth = base64.b64encode(f"{WP_USER}:{WP_PW}".encode()).decode()
headers = {
    "Authorization": f"Basic {auth}",
    "Content-Type":  "application/json; charset=utf-8",
}

TOS_HTML = """
<h2>1. Objeto</h2>
<p>Las presentes Condiciones Generales del Servicio regulan la relación contractual entre <strong>Riqueza Digital Solutions SLU</strong> (en adelante, «Riqueza Digital» o el «Prestador») y sus clientes (en adelante, «el Cliente») en el marco de la prestación de servicios de marketing digital, publicidad en plataformas digitales, desarrollo web y formación.</p>

<h2>2. Datos identificativos del Prestador</h2>
<ul>
  <li><strong>Razón social:</strong> Riqueza Digital Solutions SLU</li>
  <li><strong>NIF:</strong> B26904409</li>
  <li><strong>Domicilio:</strong> C/Riera de Sant Andreu 90, Local, 08030 Barcelona, España</li>
  <li><strong>Correo electrónico:</strong> info@riquezadigital.es</li>
  <li><strong>Sitio web:</strong> <a href="https://www.riquezadigital.es">https://www.riquezadigital.es</a></li>
</ul>

<h2>3. Servicios prestados</h2>
<p>Riqueza Digital presta, entre otros, los siguientes servicios:</p>
<ul>
  <li><strong>Gestión de campañas de publicidad digital:</strong> Planificación, creación, optimización y seguimiento de campañas en plataformas como Google Ads, Meta Ads (Facebook e Instagram), TikTok Ads y otras redes publicitarias.</li>
  <li><strong>Marketing de contenidos y SEO:</strong> Estrategia de contenidos, optimización para motores de búsqueda y gestión de presencia digital orgánica.</li>
  <li><strong>Desarrollo web:</strong> Diseño, maquetación y desarrollo de sitios web, landing pages y tiendas online.</li>
  <li><strong>Automatizaciones e integraciones:</strong> Implementación de flujos automáticos, integraciones entre plataformas y sistemas de CRM.</li>
  <li><strong>Formación en inteligencia artificial y marketing digital:</strong> Talleres, cursos y mentoring para equipos y profesionales.</li>
</ul>

<h2>4. Acceso a cuentas y plataformas del Cliente</h2>
<p>Para la prestación de los servicios de gestión publicitaria, el Cliente otorga a Riqueza Digital acceso a sus cuentas en las plataformas correspondientes (Google Ads, Meta Business Manager, etc.) mediante los mecanismos de autorización propios de cada plataforma.</p>
<p>Riqueza Digital accede a dichas cuentas exclusivamente para la ejecución de los servicios contratados. No se compartirán datos de las cuentas del Cliente con terceros ajenos a la prestación del servicio, salvo obligación legal.</p>
<p>El Cliente es responsable de mantener actualizados los accesos y de comunicar a Riqueza Digital cualquier cambio en los permisos otorgados.</p>

<h2>5. Contratación y presupuestos</h2>
<p>La relación contractual se formaliza mediante la aceptación de un presupuesto o propuesta de servicios enviada por Riqueza Digital. Dicha aceptación puede realizarse por escrito (correo electrónico u otro medio fehaciente).</p>
<p>Los presupuestos tienen una validez de 30 días naturales desde su emisión, salvo indicación expresa en contrario.</p>

<h2>6. Precios y facturación</h2>
<p>Los precios de los servicios se establecen en el presupuesto aceptado por el Cliente. Todos los precios se expresan en euros y, salvo indicación contraria, no incluyen el IVA aplicable.</p>
<p>La facturación se realiza conforme a lo acordado en el presupuesto o contrato de servicios. El pago deberá efectuarse en el plazo indicado en la factura.</p>
<p>El presupuesto de inversión publicitaria (inversión en plataformas como Google Ads o Meta Ads) es independiente de los honorarios de gestión de Riqueza Digital y se factura por separado o se gestiona directamente desde la cuenta del Cliente.</p>

<h2>7. Obligaciones del Cliente</h2>
<p>El Cliente se compromete a:</p>
<ul>
  <li>Proporcionar a Riqueza Digital la información, accesos y materiales necesarios para la prestación del servicio en los plazos acordados.</li>
  <li>Revisar y aprobar los entregables (creatividades, copys, landing pages, informes) en tiempo y forma.</li>
  <li>Cumplir con las políticas de uso de las plataformas publicitarias en las que opera.</li>
  <li>Informar a Riqueza Digital de cualquier cambio relevante en su negocio que pueda afectar a la estrategia acordada.</li>
</ul>

<h2>8. Obligaciones de Riqueza Digital</h2>
<p>Riqueza Digital se compromete a:</p>
<ul>
  <li>Prestar los servicios contratados con diligencia profesional y conforme a las buenas prácticas del sector.</li>
  <li>Mantener la confidencialidad sobre la información del Cliente.</li>
  <li>Informar al Cliente de cualquier incidencia relevante que afecte al servicio.</li>
  <li>Actuar siempre dentro de las políticas de las plataformas y la normativa vigente.</li>
</ul>

<h2>9. Propiedad intelectual</h2>
<p>Los entregables creados por Riqueza Digital en el marco del servicio (creatividades, textos, diseños, código fuente) serán propiedad del Cliente una vez satisfecho el pago íntegro de los servicios, salvo acuerdo expreso en contrario.</p>
<p>Las herramientas, metodologías y sistemas internos de Riqueza Digital son de su propiedad exclusiva y no se transfieren al Cliente.</p>

<h2>10. Limitación de responsabilidad</h2>
<p>Riqueza Digital no garantiza resultados específicos en campañas publicitarias, dado que el rendimiento depende de factores externos como el mercado, la competencia y las propias plataformas.</p>
<p>Riqueza Digital no será responsable de las decisiones tomadas por las plataformas publicitarias (suspensiones de cuentas, cambios algorítmicos, modificaciones de políticas) que escapen a su control directo.</p>
<p>La responsabilidad máxima de Riqueza Digital frente al Cliente se limitará al importe de los honorarios de gestión abonados en el mes en curso, salvo dolo o negligencia grave.</p>

<h2>11. Duración y resolución</h2>
<p>Los servicios de carácter continuado (gestión de campañas, mantenimiento web) tienen la duración acordada en el presupuesto o contrato. Cualquiera de las partes podrá resolver el contrato mediante comunicación escrita con un preaviso mínimo de 30 días naturales, salvo incumplimiento grave que justifique resolución inmediata.</p>

<h2>12. Protección de datos</h2>
<p>El tratamiento de los datos personales derivado de la relación contractual se rige por la <a href="https://www.riquezadigital.es/politica-de-privacidad/">Política de Privacidad</a> de Riqueza Digital, de conformidad con el Reglamento (UE) 2016/679 (RGPD) y la Ley Orgánica 3/2018 (LOPDGDD).</p>

<h2>13. Modificación de las condiciones</h2>
<p>Riqueza Digital se reserva el derecho a modificar estas Condiciones Generales del Servicio. Las modificaciones serán comunicadas al Cliente con una antelación mínima de 15 días naturales antes de su entrada en vigor.</p>

<h2>14. Legislación aplicable y jurisdicción</h2>
<p>Las presentes Condiciones Generales se rigen por la legislación española. Para la resolución de cualquier controversia, las partes, con renuncia expresa a cualquier otro fuero que pudiera corresponderles, se someten a los Juzgados y Tribunales de la ciudad de Barcelona.</p>

<p><em>Última actualización: junio de 2026</em></p>
"""

# --- CREATE PAGE ---
payload = {
    "title":   "Términos y Condiciones del Servicio",
    "slug":    "terminos-y-condiciones",
    "status":  "publish",
    "parent":  0,
    "content": TOS_HTML,
    "meta": {
        "yoast_wpseo_title": "Términos y Condiciones | Riqueza Digital",
        "yoast_wpseo_metadesc": "Condiciones generales que regulan los servicios de marketing digital, gestión publicitaria (Google Ads, Meta Ads), desarrollo web y formación prestados por Riqueza Digital Solutions SLU.",
        "yoast_wpseo_focuskw": "términos y condiciones riqueza digital",
    }
}

body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
req  = urllib.request.Request(f"{WP_URL}/wp-json/wp/v2/pages", data=body, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        print(f"OK — ID: {data['id']} | Status: {data['status']} | Slug: {data['slug']}")
        print(f"URL: {data['link']}")
except urllib.error.HTTPError as e:
    print(f"ERROR {e.code}: {e.read().decode()}")
    sys.exit(1)
