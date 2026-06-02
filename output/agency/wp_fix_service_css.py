"""Fix double-brace CSS bug on servicios-web-ia (6836) and posicionamiento-ia (6837)."""
import urllib.request, base64, json, os, sys, random, string
sys.stdout.reconfigure(encoding='utf-8')

url = os.environ['WP_RD_URL']
user = os.environ['WP_RD_USER']
pwd = os.environ['WP_RD_APP_PASSWORD']
token = base64.b64encode(f'{user}:{pwd}'.encode()).decode()
h = {'Authorization': f'Basic {token}', 'Content-Type': 'application/json; charset=utf-8'}

def make_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def wrap(html):
    # Fix residual double-brace CSS bug before wrapping
    html = html.replace('{{', '{').replace('}}', '}')
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

def fetch_html(page_id):
    """Read current _elementor_data and extract the HTML from the html widget."""
    req = urllib.request.Request(
        f'{url}/wp-json/wp/v2/pages/{page_id}?context=edit&_fields=meta',
        headers={'Authorization': f'Basic {token}'}
    )
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())
    el_data = data.get('meta', {}).get('_elementor_data', '[]')
    structure = json.loads(el_data)
    # Navigate: section > column > html widget
    return structure[0]['elements'][0]['elements'][0]['settings']['html']

def push_fixed(page_id, slug):
    current_html = fetch_html(page_id)
    fixed_html = current_html.replace('{{', '{').replace('}}', '}')
    changes = current_html.count('{{')

    payload = {
        'meta': {
            '_elementor_edit_mode': 'builder',
            '_elementor_template_type': 'wp-page',
            '_elementor_data': wrap(fixed_html),
        }
    }
    body = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(f'{url}/wp-json/wp/v2/pages/{page_id}', data=body, headers=h, method='POST')
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read())
        print(f"Fixed {slug} | {changes} double-brace fixes applied | {res['link']}")

push_fixed(6836, 'servicios-web-ia')
push_fixed(6837, 'posicionamiento-ia')
print("CSS bug fixed on both service pages.")
