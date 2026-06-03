# /wp-edit — Edición WordPress desde Claude Code

Flujo completo para leer, editar, validar y publicar páginas/posts en WordPress vía REST API. Aplica a riquezadigital.es y cualquier sitio cliente con las variables de entorno configuradas.

---

## Antes de empezar

1. Identificar el sitio: ¿`RD` (Riqueza Digital) u otro cliente (ej: `KELLER`)?
2. Identificar la página por **slug** o **ID**. Si no se sabe el ID, buscarlo por slug (ver Paso 1).
3. **Regla**: siempre leer el contenido actual antes de escribir. Nunca sobreescribir a ciegas.

**Variables de entorno requeridas** (en Windows Registry):
- `WP_<CLIENTE>_URL` — URL base del sitio (sin slash final)
- `WP_<CLIENTE>_USER` — usuario WordPress
- `WP_<CLIENTE>_APP_PASSWORD` — Application Password sin espacios

**Runtime Python**: usar `python` (no `python3` — en Windows el alias es `python`).

---

## Paso 1 — Encontrar la página

Si solo se sabe el slug:

```python
import winreg, base64, json, urllib.request

CLIENTE = "RD"  # cambiar por el prefijo del cliente

def get_env(name):
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")
    val, _ = winreg.QueryValueEx(key, name)
    winreg.CloseKey(key)
    return val

url  = get_env(f"WP_{CLIENTE}_URL").rstrip("/")
user = get_env(f"WP_{CLIENTE}_USER")
pw   = get_env(f"WP_{CLIENTE}_APP_PASSWORD")
auth = base64.b64encode(f"{user}:{pw}".encode()).decode()
h    = {"Authorization": f"Basic {auth}"}

# Buscar por slug
slug = "terminos-y-condiciones"
req  = urllib.request.Request(f"{url}/wp-json/wp/v2/pages?slug={slug}&_fields=id,slug,title,status,link", headers=h)
with urllib.request.urlopen(req) as r:
    pages = json.loads(r.read())
    for p in pages:
        print(f"ID:{p['id']} | {p['status']} | {p['slug']} | {p['link']}")
```

---

## Paso 2 — Leer contenido actual

**Siempre ejecutar antes de cualquier edición:**

```python
PAGE_ID = 6826  # ID encontrado en Paso 1

req = urllib.request.Request(
    f"{url}/wp-json/wp/v2/pages/{PAGE_ID}?context=edit&_fields=id,slug,title,status,content,meta",
    headers=h
)
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())
    raw_content = data["content"]["raw"]   # HTML editable (context=edit lo devuelve)
    print(f"Título: {data['title']['raw']}")
    print(f"Status: {data['status']}")
    print(f"Longitud contenido: {len(raw_content)} chars")
    print(raw_content[:500])  # preview primeras líneas
```

> ⚠️ Usar `context=edit` para obtener el HTML en crudo (sin renderizar). Requiere autenticación.

---

## Paso 3 — Editar el contenido

**Opción A — Cambio quirúrgico (preferida):**

```python
updated_content = raw_content.replace(
    "texto antiguo exacto",
    "texto nuevo"
)
# Verificar que el cambio se aplicó
assert updated_content != raw_content, "ERROR: el texto a reemplazar no se encontró"
print(f"Cambios aplicados. Nueva longitud: {len(updated_content)} chars")
```

**Opción B — Reescritura completa** (solo cuando el cambio es extenso):

```python
updated_content = """<h2>Nueva sección...</h2><p>...</p>"""
```

---

## Paso 4 — Publicar los cambios

```python
payload = {
    "content": updated_content,
    # Opcionales — incluir solo los que cambian:
    "title":  "Nuevo título si cambia",
    "status": "publish",   # o "draft" si quieres revisar antes
    # Yoast SEO (si necesitas actualizar meta):
    "meta": {
        "yoast_wpseo_title":    "Título SEO | Riqueza Digital",
        "yoast_wpseo_metadesc": "Meta descripción (max 160 chars).",
        "yoast_wpseo_focuskw":  "palabra clave principal",
    }
}

h["Content-Type"] = "application/json; charset=utf-8"
body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
req  = urllib.request.Request(f"{url}/wp-json/wp/v2/pages/{PAGE_ID}", data=body, headers=h, method="POST")

with urllib.request.urlopen(req) as r:
    result = json.loads(r.read())
    print(f"OK — ID:{result['id']} | Status:{result['status']}")
    print(f"URL: {result['link']}")
    print(f"WP Admin: {url}/wp-admin/post.php?post={result['id']}&action=edit")
```

---

## Paso 5 — Validar el resultado

**Validación mínima (siempre):**

```python
req_check = urllib.request.Request(
    f"{url}/wp-json/wp/v2/pages/{PAGE_ID}?_fields=content,status",
    headers={"Authorization": f"Basic {auth}"}
)
with urllib.request.urlopen(req_check) as r:
    check = json.loads(r.read())
    rendered = check["content"]["rendered"]
    print(f"Status: {check['status']}")
    print(f"Contenido renderizado: {len(rendered)} chars")
    # Verificar que el cambio está presente
    assert "texto nuevo" in rendered, "ERROR: el cambio no aparece en el renderizado"
    print("Validación OK")
```

**Validación visual con Playwright (cuando sea importante):**

```
# Usar el MCP de Playwright:
browser_navigate(url="https://www.riquezadigital.es/slug-de-la-pagina/")
browser_take_screenshot()
# Revisar visualmente que el diseño es correcto
```

> Playwright muestra cómo ve el visitante la página. Úsalo siempre para cambios de diseño o cuando el cliente vaya a verlo.

---

## Paso 6 — Reportar al usuario

Al terminar, presentar siempre:

```
Página actualizada: [nombre]
URL pública:        https://www.riquezadigital.es/slug/
WP Admin:           [url]/wp-admin/post.php?post=[ID]&action=edit
Validación:         ✅ contenido verificado ([N] chars)
Yoast SEO:          ✅ título y meta actualizados / ⏭️ sin cambios
Próximo paso:       [publicar / revisar visualmente / nada]
```

---

## Patrones frecuentes

### Listar todas las páginas de un sitio

```python
req = urllib.request.Request(
    f"{url}/wp-json/wp/v2/pages?per_page=50&status=publish,draft&_fields=id,slug,title,status",
    headers=h
)
with urllib.request.urlopen(req) as r:
    for p in json.loads(r.read()):
        print(f"ID:{p['id']} | {p['status']} | {p['slug']} | {p['title']['rendered']}")
```

### Actualizar solo el SEO Yoast (sin tocar el contenido)

```python
payload = {"meta": {
    "yoast_wpseo_title":    "Título | Marca",
    "yoast_wpseo_metadesc": "Descripción.",
}}
# ... (mismo patrón de POST con PAGE_ID)
```

### Cambiar status de draft a publish

```python
payload = {"status": "publish"}
```

### Crear página nueva

```python
payload = {
    "title":   "Título",
    "slug":    "slug-url",
    "status":  "draft",    # siempre draft primero
    "parent":  0,
    "content": "<h2>...</h2>",
}
req = urllib.request.Request(f"{url}/wp-json/wp/v2/pages", data=body, headers=h, method="POST")
```

---

## Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| Variables vacías en Bash | Bash no hereda env vars de Windows | Usar Python con `winreg` |
| `401 Unauthorized` | Password con espacios o expirada | Regenerar Application Password en WP Admin |
| `403 Forbidden` | Usuario sin rol Editor/Admin | Elevar permisos o usar otro usuario |
| `assert` falla en validación | El cambio no se aplicó | Revisar escaping del string; usar `context=edit` para ver raw |
| Contenido vacío tras crear | Payload mal formado | Verificar `json.dumps(ensure_ascii=False)` |
| `python3` not found | Windows usa `python` no `python3` | Usar siempre `python` en este sistema |

---

## Referencias

- SOP completo: [wordpress-rest-api-claude.md](../../shared/sops/wordpress-rest-api-claude.md)
- Helper de creación de páginas: `output/agency/wp_upload_curso.py`
- Variables de entorno: `shared/sops/gestion-claves-api-windows.md`
