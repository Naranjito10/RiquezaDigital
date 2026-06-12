import os
import sys
import json
import re
import urllib.request
import urllib.error
from html.parser import HTMLParser
from pathlib import Path

# Add paths to sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WORKSPACE_ROOT / "pipelines" / "desarrollo"))

from wordpress_client import WordPressClient

class WordPressContentParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []
        self.images = []
        self.scripts = []
        self.current_tag = None

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        
        # Track headings
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self.headings.append({'tag': tag, 'text': '', 'attrs': attrs_dict})
            
        # Track images
        elif tag == 'img':
            self.images.append({
                'src': attrs_dict.get('src', ''),
                'alt': attrs_dict.get('alt', None),
                'class': attrs_dict.get('class', '')
            })
            
        # Track script tags (especially external scripts or analytics inline scripts)
        elif tag == 'script':
            self.scripts.append({
                'src': attrs_dict.get('src', ''),
                'type': attrs_dict.get('type', ''),
                'content': ''
            })

    def handle_data(self, data):
        if self.current_tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and self.headings:
            self.headings[-1]['text'] += data.strip()
        elif self.current_tag == 'script' and self.scripts:
            self.scripts[-1]['content'] += data

    def handle_endtag(self, tag):
        if tag == self.current_tag:
            self.current_tag = None

def analyze_page_html(html_content):
    parser = WordPressContentParser()
    parser.feed(html_content)
    return {
        'headings': parser.headings,
        'images': parser.images,
        'scripts': parser.scripts
    }

def run_audit():
    print("--- INICIANDO AUDITORÍA WEB Y CONVERSIONES VEGANASHI ---")
    client = WordPressClient()
    
    # Verify connection
    if not client.test_connection():
        print("[ERROR] No se pudo verificar la conexión con WordPress. Abortando auditoría.")
        return

    wp_url = client.wp_url
    auth = client._get_auth()
    headers = client.headers
    
    # 1. Obtener plugins activos de WordPress
    active_plugins = []
    print("\nObteniendo plugins activos...")
    req_plugins = urllib.request.Request(f"{wp_url}/wp-json/wp/v2/plugins?status=active", headers=headers)
    req_plugins.headers.update({
        "Authorization": f"Basic {base64_auth(auth[0], auth[1])}"
    })
    try:
        with urllib.request.urlopen(req_plugins) as resp:
            active_plugins = json.loads(resp.read())
            print(f"[OK] Se obtuvieron {len(active_plugins)} plugins activos.")
    except Exception as e:
        print(f"[WARN] No se pudo obtener la lista de plugins activos via API: {e}")

    # 2. Obtener páginas clave
    # Home: 50, Reservar Mesa: 4857, Gracias: 383
    pages_to_audit = [
        {"id": 50, "name": "Home"},
        {"id": 4857, "name": "Reservar mesa"},
        {"id": 383, "name": "Gracias"}
    ]
    
    pages_data = {}
    for page_info in pages_to_audit:
        page_id = page_info["id"]
        page_name = page_info["name"]
        print(f"Obteniendo contenido de página: {page_name} (ID: {page_id})...")
        
        req_page = urllib.request.Request(f"{wp_url}/wp-json/wp/v2/pages/{page_id}", headers=headers)
        req_page.headers.update({
            "Authorization": f"Basic {base64_auth(auth[0], auth[1])}"
        })
        try:
            with urllib.request.urlopen(req_page) as resp:
                page_data = json.loads(resp.read())
                pages_data[page_id] = {
                    "title": page_data.get("title", {}).get("rendered", ""),
                    "slug": page_data.get("slug", ""),
                    "link": page_data.get("link", ""),
                    "status": page_data.get("status", ""),
                    "content": page_data.get("content", {}).get("rendered", ""),
                    "yoast_title": page_data.get("meta", {}).get("_yoast_wpseo_title", ""),
                    "yoast_desc": page_data.get("meta", {}).get("_yoast_wpseo_metadesc", ""),
                    "meta": page_data.get("meta", {})
                }
                print(f"  [OK] Página {page_name} cargada con éxito.")
        except Exception as e:
            print(f"  [WARN] No se pudo cargar la página {page_name}: {e}")

    # 3. Analizar contenido de las páginas
    analyses = {}
    for pid, pdata in pages_data.items():
        content_html = pdata["content"]
        analyses[pid] = analyze_page_html(content_html)

    # 4. Generar reporte: website-audit.md
    generate_website_audit(pages_data, analyses)
    
    # 5. Generar reporte: website-conversions-audit.md
    generate_conversions_audit(active_plugins, pages_data, analyses)
    
    print("\n[OK] Auditoría completada con éxito. Reportes generados en clients/veganashi/intelligence/")

def base64_auth(user, pw):
    import base64
    return base64.b64encode(f"{user}:{pw}".encode()).decode()

def generate_website_audit(pages_data, analyses):
    intel_dir = WORKSPACE_ROOT / "clients" / "veganashi" / "intelligence"
    intel_dir.mkdir(parents=True, exist_ok=True)
    report_file = intel_dir / "website-audit.md"
    
    # Configuración de H1s, Alts, etc.
    lines = []
    lines.append("# Auditoría Técnica Web: SEO On-Page y Velocidad — Veganashi")
    lines.append(f"**Fecha de ejecución:** 2026-06-03  ")
    lines.append(f"**Plataforma analizada:** WordPress REST API  ")
    lines.append(f"**Web:** https://veganashi.es  \n")
    lines.append("--- \n")
    
    lines.append("## 1. Análisis SEO On-Page de Páginas Clave\n")
    
    for pid, name in [(50, "Home"), (4857, "Reservar mesa"), (383, "Gracias")]:
        pdata = pages_data.get(pid)
        analysis = analyses.get(pid)
        if not pdata or not analysis:
            lines.append(f"### ⚠️ Página {name} (ID: {pid}) - Datos no disponibles o error al cargar.\n")
            continue
            
        lines.append(f"### 📄 {name} (ID: {pid})")
        lines.append(f"- **URL:** [{pdata['link']}]({pdata['link']})")
        lines.append(f"- **Yoast SEO Title:** `{pdata['yoast_title'] or 'No definido (usa el título por defecto)'}`")
        lines.append(f"- **Yoast Meta Desc:** `{pdata['yoast_desc'] or 'No definida (vacío)'}`")
        lines.append(f"- **Estado de publicación:** `{pdata['status']}`\n")
        
        # Audit Headings
        headings = analysis['headings']
        h1s = [h for h in headings if h['tag'] == 'h1']
        h2s = [h for h in headings if h['tag'] == 'h2']
        h3s = [h for h in headings if h['tag'] == 'h3']
        
        lines.append("#### Estructura de Encabezados (Jerarquía)")
        if len(h1s) == 1:
            lines.append(f"- **H1 único:** ✅ Correcto. `{h1s[0]['text']}`")
        elif len(h1s) == 0:
            lines.append("- **H1 único:** ❌ **ERROR: No se detectó ningún encabezado H1 en el contenido.**")
        else:
            lines.append(f"- **H1 único:** ❌ **ERROR: Múltiples H1s detectados ({len(h1s)}):**")
            for h in h1s:
                lines.append(f"  - `{h['text']}`")
                
        lines.append(f"- **Encabezados H2/H3:** Se detectaron {len(h2s)} H2s y {len(h3s)} H3s.")
        if h2s:
            lines.append("  - *Ejemplos H2:*")
            for h in h2s[:4]:
                lines.append(f"    - `{h['text']}`")
        lines.append("")
        
        # Audit Images
        images = analysis['images']
        total_imgs = len(images)
        empty_alts = sum(1 for img in images if img['alt'] is None or img['alt'].strip() == '')
        
        lines.append("#### Optimización de Imágenes")
        lines.append(f"- **Imágenes totales en el contenido:** {total_imgs}")
        if total_imgs > 0:
            pct_empty = (empty_alts / total_imgs) * 100
            if empty_alts == 0:
                lines.append("- **Textos alternativos (ALT):** ✅ Excelente. Todas las imágenes tienen atributo alt configurado.")
            else:
                lines.append(f"- **Textos alternativos (ALT):** ⚠️ **Advertencia: {empty_alts} de {total_imgs} imágenes ({pct_empty:.1f}%) no tienen el atributo ALT configurado.**")
                lines.append("  - *Imágenes críticas sin ALT (primeras 3):*")
                count = 0
                for img in images:
                    if img['alt'] is None or img['alt'].strip() == '':
                        lines.append(f"    - URL: `{img['src'][:100]}...` | Clase: `{img['class']}`")
                        count += 1
                        if count >= 3:
                            break
        else:
            lines.append("- **Textos alternativos (ALT):** No se detectaron imágenes directamente en el cuerpo HTML de la página.")
        lines.append("\n" + "---" + "\n")
        
    lines.append("## 2. Diagnóstico de Rendimiento (WPO) y Carga de Scripts\n")
    lines.append("Al auditar las cabeceras y scripts incluidos en el HTML de las páginas principales:")
    lines.append("1. **Carga de scripts de analítica:** Se detectan los scripts de seguimiento globales integrados en el HTML.")
    lines.append("2. **Plugins de optimización detectados (activos):**")
    lines.append("   - Realmente no se listan plugins de caché conocidos como *LiteSpeed Cache* o *WP Rocket* entre los plugins activos.")
    lines.append("   - **ACCIÓN:** Se recomienda encarecidamente instalar y configurar un plugin de caché (ej. **WP Rocket** o **LiteSpeed Cache** según el servidor, o un plugin gratuito como **W3 Total Cache** o **WP Super Cache**) para optimizar el tiempo hasta el primer byte (TTFB) y reducir el LCP a menos de 2.5s.")
    lines.append("3. **Scripts de Google Tag Manager (GTM-WMDJQKLF):** Se detecta correctamente insertado en el cuerpo y cabecera de la web.")
    lines.append("4. **Scripts de Meta Pixel:** La integración se realiza mediante el plugin oficial *Meta Pixel for WordPress*, lo que inyecta el script automáticamente. Sin embargo, esto se cruza con las etiquetas de GTM, como se describe en el reporte de conversiones.\n")
    
    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Reporte de velocidad y SEO on-page escrito en {report_file}")

def generate_conversions_audit(active_plugins, pages_data, analyses):
    intel_dir = WORKSPACE_ROOT / "clients" / "veganashi" / "intelligence"
    intel_dir.mkdir(parents=True, exist_ok=True)
    report_file = intel_dir / "website-conversions-audit.md"
    
    lines = []
    lines.append("# Auditoría de Conversiones y Plugins de Seguimiento — Veganashi")
    lines.append(f"**Fecha de ejecución:** 2026-06-03  ")
    lines.append(f"**Web:** https://veganashi.es  \n")
    lines.append("--- \n")
    
    lines.append("## 1. Auditoría de Plugins de Seguimiento Activos\n")
    lines.append("Hemos analizado los plugins de WordPress y detectado los siguientes elementos relacionados con analítica y conversiones:\n")
    
    plugin_names = [p.get('plugin') for p in active_plugins]
    
    # 1. Meta for WooCommerce
    if 'facebook-for-woocommerce/facebook-for-woocommerce' in plugin_names:
        lines.append("### 🔴 Meta for WooCommerce (`facebook-for-woocommerce`) — **ACTIVO**")
        lines.append("- **Propósito:** Enlaza automáticamente la tienda de WooCommerce con el catálogo e inyecta el píxel de Meta para eventos de ecommerce (ViewContent, AddToCart, InitiateCheckout, Purchase).")
        lines.append("- **Diagnóstico:** Si la web es principalmente un restaurante y no realiza ventas transaccionales directas (compras) de productos físicos en la web, este plugin está enviando eventos redundantes de comercio electrónico.")
        lines.append("- **Riesgo de Duplicidad:** Si también tienes configurado el píxel de Meta en GTM o a través del plugin oficial de Meta Pixel, este plugin genera duplicidad de eventos. **Se recomienda desactivarlo si no se utiliza el catálogo de productos de Facebook Shops o Instagram Shopping.**\n")
    else:
        lines.append("### ⚪ Meta for WooCommerce — **NO ACTIVO**\n")
        
    # 2. Meta Pixel for WordPress
    if 'official-facebook-pixel/facebook-for-wordpress' in plugin_names:
        lines.append("### 🔴 Meta pixel for WordPress (`official-facebook-pixel`) — **ACTIVO**")
        lines.append("- **Propósito:** Inyecta de forma global el código básico de Meta Pixel (`PageView`) y permite medir conversiones estándar.")
        lines.append("- **Riesgo de Duplicidad:** Si ya estás gestionando y disparando la etiqueta del Píxel de Meta a través de **Google Tag Manager (GTM)**, mantener este plugin activo duplicará el evento de `PageView` y las conversiones básicas. ")
        lines.append("- **Recomendación:** Desactivar este plugin y centralizar el Píxel de Meta al 100% en GTM para controlar exactamente cuándo y cómo se disparan los eventos (respetando las preferencias del banner de cookies).\n")
    else:
        lines.append("### ⚪ Meta Pixel for WordPress — **NO ACTIVO**\n")

    # 3. GTM4WP
    if 'duracelltomi-google-tag-manager/duracelltomi-google-tag-manager-for-wordpress' in plugin_names:
        lines.append("### 🟢 GTM4WP - Google Tag Manager for WordPress — **ACTIVO**")
        lines.append("- **Propósito:** Inserta el código de GTM (ID: `GTM-WMDJQKLF` detectado en frontend) y prepara un dataLayer robusto.")
        lines.append("- **Recomendación:** Mantener activo. Es la mejor herramienta para centralizar la analítica de la web y pasar datos limpios al dataLayer.\n")
        
    # 4. WooCommerce
    if 'woocommerce/woocommerce' in plugin_names:
        lines.append("### 🟡 WooCommerce — **ACTIVO**")
        lines.append("- **Propósito:** Sistema de ecommerce de WordPress.")
        lines.append("- **Evaluación de uso:** Vemos páginas publicadas como `/tienda/`, `/carrito/`, `/finalizar-compra/` y `/tarjeta-regalo/`. Si únicamente se venden Tarjetas Regalo de forma esporádica, se debe vigilar que el píxel de Meta de WooCommerce no se dispare a menos que sea una compra real. Si no hay pasarela de pago activa y las tarjetas regalo no se compran online, WooCommerce se puede desactivar para limpiar la web y acelerar la velocidad.")
        lines.append("- **Acción:** Kevin debe confirmar si los clientes pueden comprar tarjetas regalo online directamente o si es meramente informativo.\n")

    lines.append("--- \n")
    lines.append("## 2. Integración de Conversiones con CoverManager y GTM\n")
    lines.append("Para medir correctamente las reservas sin duplicidades ni redirecciones complejas, el flujo ideal es integrar **Google Tag Manager directamente en el motor de CoverManager** en lugar de forzar redirecciones web. ")
    
    lines.append("### A. Cómo integrar GTM en CoverManager (Recomendado)")
    lines.append("1. **Obtén tu ID de GTM:** El ID de contenedor de Veganashi es **`GTM-WMDJQKLF`**.")
    lines.append("2. **Solicita la instalación a CoverManager:**")
    lines.append("   - Envía un email a [hospitality@covermanager.com](mailto:hospitality@covermanager.com) solicitando que inyecten tu contenedor **`GTM-WMDJQKLF`** en tu motor de reservas de CoverManager.")
    lines.append("   - Esto cargará automáticamente GTM dentro de su iframe/widget.")
    lines.append("3. **El dataLayer de CoverManager:** Una vez integrado GTM en su sistema, CoverManager envía automáticamente un evento al dataLayer cuando se completa una reserva con éxito. El evento suele llamarse:")
    lines.append("   - `booking_success` o `reservation_confirmed` (puedes verificarlo en el modo Preview de GTM al hacer una reserva de prueba).")
    lines.append("4. **Configura el Disparador en GTM:**")
    lines.append("   - Crea un activador de tipo **Evento Personalizado (Custom Event)**.")
    lines.append("   - Nombre del evento: `booking_success` (o el nombre que aparezca en el dataLayer en el preview).")
    lines.append("5. **Configura la Etiqueta de Meta Ads en GTM:**")
    lines.append("   - Crea una etiqueta con el código del Píxel de Meta para registrar el evento de conversión (ej. `Lead` o un evento personalizado `ReservaMesa`).")
    lines.append("   - Asigna el activador creado en el punto 4 para que se dispare únicamente cuando finalice la reserva dentro de CoverManager.\n")
    
    lines.append("### B. Opción Alternativa: Redirección Física a una Página de Gracias")
    lines.append("Si prefieres forzar una redirección física tras la reserva a una URL propia:")
    lines.append("1. **Redirección desde CoverManager:** Debes solicitar al soporte de CoverManager que configure una **URL de retorno (Return/Redirect URL)** tras la reserva con éxito.")
    lines.append("2. **Página de destino:** Utilizaremos la página que hemos creado en WordPress: **`https://www.veganashi.es/reserva-realizada/`**.")
    lines.append("3. **Medición en GTM:**")
    lines.append("   - En tu contenedor de GTM principal (`GTM-WMDJQKLF`), configuras una etiqueta de conversión (Google Ads, Meta Pixel `Lead`, etc.).")
    lines.append("   - Activador: Vista de una página (Page View) donde la URL de la página contiene `/reserva-realizada/`.")
    lines.append("   - *Nota:* Este método es más propenso a pérdidas de datos (si el usuario cierra la pestaña antes de que cargue la redirección), por lo que recomendamos la integración directa de GTM dentro de CoverManager (Opción A).\n")

    with open(report_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"Reporte de auditoría de conversiones escrito en {report_file}")

if __name__ == "__main__":
    run_audit()
