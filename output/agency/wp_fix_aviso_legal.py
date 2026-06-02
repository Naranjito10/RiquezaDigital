"""Corrige el Aviso Legal: cambia 'Finalidad: Restaurante' por la correcta"""
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

# GET current content
req_get = urllib.request.Request(f"{WP_URL}/wp-json/wp/v2/pages/6450?_fields=content", headers={"Authorization": f"Basic {auth}"})
with urllib.request.urlopen(req_get) as resp:
    data = json.loads(resp.read())
    current = data["content"]["raw"] if "raw" in data["content"] else data["content"]["rendered"]

# Fix the wrong "Restaurante" purpose
fixed = current.replace(
    "La finalidad del Sitio Web es: Restaurante.",
    "La finalidad del Sitio Web es: Prestación de servicios de marketing digital, gestión de publicidad en plataformas digitales (Google Ads, Meta Ads), desarrollo web y formación en inteligencia artificial."
)

if fixed == current:
    # Try rendered version fix
    print("WARNING: Exact match not found. Checking rendered content...")
    req_r = urllib.request.Request(f"{WP_URL}/wp-json/wp/v2/pages/6450?_fields=content&context=edit", headers={"Authorization": f"Basic {auth}"})
    with urllib.request.urlopen(req_r) as resp:
        data2 = json.loads(resp.read())
        raw = data2["content"]["raw"]
        print(f"RAW excerpt: {raw[raw.find('finalidad'):raw.find('finalidad')+200]}")
    sys.exit(1)

payload = {"content": fixed}
body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
req_upd = urllib.request.Request(f"{WP_URL}/wp-json/wp/v2/pages/6450", data=body, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req_upd) as resp:
        result = json.loads(resp.read())
        print(f"OK — Aviso Legal updated. ID: {result['id']} | Status: {result['status']}")
except urllib.error.HTTPError as e:
    print(f"ERROR {e.code}: {e.read().decode()}")
