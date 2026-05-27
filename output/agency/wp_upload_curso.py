"""
Sube o actualiza la página del curso Agencia Agéntica en WordPress.
Lee credenciales del Registry de Windows (User scope).
"""
import winreg, base64, json, urllib.request, urllib.error
from pathlib import Path

# ── Credenciales desde Registry ──────────────────────────────────────────────
def get_env(name: str) -> str:
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

# ── Contenido HTML ────────────────────────────────────────────────────────────
html_path = Path(__file__).parent / "curso-agencia-agentica-draft.html"
html = html_path.read_text(encoding="utf-8")

# ── Payload ───────────────────────────────────────────────────────────────────
PAGE_ID = 6820   # borrador ya creado — actualizamos en vez de crear nuevo

payload = {
    "title":   "Construye tu propia Agencia Agéntica",
    "slug":    "agencia-agentica",
    "status":  "draft",
    "parent":  6524,
    "content": html,
}

body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

# ── Request ───────────────────────────────────────────────────────────────────
endpoint = f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}"
req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
        print(f"OK - ID: {data['id']} | Status: {data['status']}")
        print(f"   Titulo: {data['title']['rendered']}")
        print(f"   Slug:   {data['slug']}")
        print(f"   Chars:  {len(data['content']['rendered'])}")
        print(f"   Preview: {WP_URL}/?p={data['id']}&preview=true")
except urllib.error.HTTPError as e:
    err = e.read().decode("utf-8", errors="replace")[:600]
    print(f"HTTP {e.code}: {err}")
except Exception as e:
    print(f"Error: {type(e).__name__}: {e}")
