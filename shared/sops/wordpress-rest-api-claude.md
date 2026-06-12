# SOP: Acceso WordPress REST API desde Claude Code

**Área:** Desarrollo Web  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-05-27  
**Clientes donde se aplicó:** Riqueza Digital (propio site)  
**Tiempo estimado:** 10–20 minutos (primera vez) / 2 minutos (uso recurrente)

---

## Resumen

Cómo conectar Claude Code a cualquier sitio WordPress vía REST API usando Application Passwords — sin MCP adicional. El patrón lee credenciales del Registry de Windows (nunca del `.env` ni del chat) y usa Python o PowerShell como proxy de autenticación.

---

## Pre-requisitos

- [ ] WordPress con Application Passwords habilitado (WP 5.6+ por defecto)
- [ ] Usuario WordPress con rol **Editor** o **Administrator**
- [ ] Application Password creada en WP Admin → Perfil → Application Passwords
- [ ] Variables de entorno guardadas en Windows Registry (ver SOP `gestion-claves-api-windows.md`)
- [ ] Python 3.x disponible en el sistema

---

## Pasos

### 1. Crear Application Password en WordPress

1. Entrar en WP Admin → **Usuarios → Tu perfil** (o el usuario API dedicado)
2. Bajar hasta la sección **Application Passwords**
3. Escribir un nombre descriptivo (ej: `claude-code-rd`) y clic en **Add New Application Password**
4. Copiar la contraseña generada — **solo se muestra una vez**
5. Guardarla **sin espacios** (WP acepta ambos formatos pero sin espacios es más limpio)

**Resultado esperado:** Password de 24 caracteres en grupos de 4 (ej: `WkTt 0Oxx ...`) — guardar sin espacios.

---

### 2. Guardar credenciales en Windows Registry

Seguir el SOP `gestion-claves-api-windows.md`. Convención de nombres:

| Variable | Contenido | Ejemplo |
|----------|-----------|---------|
| `WP_<CLIENTE>_URL` | URL base del sitio (sin trailing slash) | `https://riquezadigital.es` |
| `WP_<CLIENTE>_USER` | Usuario WordPress | `demo` |
| `WP_<CLIENTE>_APP_PASSWORD` | Application Password sin espacios | `WkTt0O...` |

Clientes actuales:

| Cliente | Prefijo | Variables |
|---------|---------|-----------|
| Riqueza Digital | `WP_RD_` | `WP_RD_URL`, `WP_RD_USER`, `WP_RD_APP_PASSWORD` |
| Keller | `WP_KELLER_` | `WP_KELLER_URL`, `WP_KELLER_USER`, `WP_KELLER_APP_PASSWORD` |

```powershell
# Guardar en Registry (ejecutar en PowerShell como usuario normal, no admin)
[System.Environment]::SetEnvironmentVariable("WP_RD_URL", "https://riquezadigital.es", "User")
[System.Environment]::SetEnvironmentVariable("WP_RD_USER", "usuario", "User")
[System.Environment]::SetEnvironmentVariable("WP_RD_APP_PASSWORD", "passwordSinEspacios", "User")
```

**Reiniciar Claude Code** después de guardar — el proceso hereda las variables al arrancar.

---

### 3. Verificar conexión

Desde Bash en Claude Code (vía PowerShell proxy):

```bash
powershell.exe -Command "
\$url = (Get-ItemProperty HKCU:\Environment).WP_RD_URL
\$user = (Get-ItemProperty HKCU:\Environment).WP_RD_USER
\$pw = (Get-ItemProperty HKCU:\Environment).WP_RD_APP_PASSWORD
\$bytes = [System.Text.Encoding]::ASCII.GetBytes(\"\${user}:\${pw}\")
\$b64 = [Convert]::ToBase64String(\$bytes)
\$headers = @{Authorization = \"Basic \$b64\"}
\$r = Invoke-RestMethod -Uri \"\${url}/wp-json/wp/v2/\" -Headers \$headers
Write-Host \"OK — namespace: \$(\$r.namespace)\"
"
```

**Resultado esperado:** `OK — namespace: wp/v2`

> ⚠️ **Por qué PowerShell y no Bash directo:** El shell Bash de Claude Code NO hereda variables de entorno de Windows (User scope). Solo hereda las del sistema (Machine scope). PowerShell sí puede leer el Registry directamente vía `HKCU:\Environment`.

---

### 4. Usar el helper Python para operaciones de contenido

Para crear o actualizar páginas/posts con HTML extenso, usar Python en lugar de PowerShell (maneja mejor el escape de JSON):

```python
import winreg, base64, json, urllib.request, urllib.error
from pathlib import Path

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

# Crear página
payload = {
    "title":   "Título de la página",
    "slug":    "slug-url",
    "status":  "draft",   # o "publish"
    "parent":  0,          # ID de la página padre (0 = raíz)
    "content": "<p>HTML aquí</p>",
}
body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
req = urllib.request.Request(f"{WP_URL}/wp-json/wp/v2/pages", data=body, headers=headers, method="POST")

with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read())
    print(f"ID: {data['id']} | Status: {data['status']}")
```

Script reutilizable en: `output/agency/wp_upload_curso.py`

---

### 5. Actualizar página existente

Cambiar el endpoint y el método:

```python
PAGE_ID = 6820  # ID de la página a actualizar
req = urllib.request.Request(
    f"{WP_URL}/wp-json/wp/v2/pages/{PAGE_ID}",
    data=body, headers=headers, method="POST"  # WP REST usa POST para update también
)
```

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Variables vacías en Bash (`$WP_RD_URL=""`) | Bash no hereda User env vars de Windows | Usar `powershell.exe` o Python con `winreg` |
| `401 Unauthorized` | Credenciales incorrectas o password con espacios | Verificar password sin espacios; regenerar si es necesario |
| `403 Forbidden` | Usuario sin permisos suficientes | Cambiar a rol Editor o Administrator |
| Contenido vacío tras crear página | `ConvertTo-Json` anida el HTML en `{"value":"..."}` | Usar Python con `json.dumps()` en lugar de PowerShell |
| `UnicodeEncodeError` en Python | Consola Windows en CP1252, no UTF-8 | Eliminar emojis de los `print()` o usar `sys.stdout.reconfigure(encoding='utf-8')` |
| Variables no disponibles tras guardarlas | Claude Code abierto antes de guardar las variables | Reiniciar Claude Code para que herede el entorno actualizado |

---

## Decisiones clave

- **Decisión:** Guardar credenciales en Windows Registry (User scope), no en `.env`  
  **Razón:** El `.env` puede acabar en git o en el chat; el Registry es el almacén seguro de Windows por diseño  
  **Alternativa descartada:** `.env` en raíz del proyecto — riesgo de exposición accidental

- **Decisión:** Python con `winreg` para operaciones de contenido extenso  
  **Razón:** `json.dumps(ensure_ascii=False)` maneja perfectamente el escape de HTML; PowerShell `ConvertTo-Json` introduce bugs con contenido mixto  
  **Alternativa descartada:** PowerShell puro — problemático con HTML grande

- **Decisión:** Siempre crear como `draft` primero, publicar manualmente desde WP Admin  
  **Razón:** Permite revisión visual antes de que sea público  
  **Alternativa descartada:** Publicar directo — riesgo de publicar contenido incompleto

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| Prefijo env vars | Todas las llamadas | `WP_RD_` vs `WP_KELLER_` |
| ID página padre | `parent` en el payload | `/cursos/` = 6524 en RD |
| Usuario y permisos | Qué endpoints están disponibles | `demo` (RD) vs usuario dedicado |

**Antes de empezar con un cliente nuevo:**
1. ¿Tiene WordPress autogestionado o managed (WP.com)?
2. ¿Qué usuario usamos? ¿Tiene rol Editor o superior?
3. ¿Cuál es la estructura de páginas padre relevante?

---

---

## Patrón avanzado: páginas Elementor con widget HTML

Descubierto el 2026-06-03. El meta `_elementor_data` **es accesible vía REST API** en esta instalación (Elementor lo registra con `show_in_rest: true`). Esto permite crear páginas que se abren como "Editar HTML" en Elementor en lugar del Text Editor básico.

### Por qué importa

- Las páginas creadas con `content` normal aparecen como **Text Editor widget** en Elementor — limitado
- Las páginas con `_elementor_data` configurado aparecen como **HTML widget** — editable como código completo con CSS, JS y el design system RD

### Patrón Python

```python
import json, random, string

def make_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))

def elementor_html_widget(html_content):
    # IMPORTANTE: corregir dobles llaves residuales de templates Python
    html_content = html_content.replace('{{', '{').replace('}}', '}')
    return json.dumps([{
        "id": make_id(), "elType": "section",
        "settings": {
            "stretch_section": "section-stretched",
            "layout": "full_width", "gap": "no",
            "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
        },
        "elements": [{
            "id": make_id(), "elType": "column",
            "settings": {"_column_size": 100, "_inline_size": None},
            "elements": [{
                "id": make_id(), "elType": "widget", "widgetType": "html",
                "settings": {"html": html_content}, "elements": []
            }],
            "isInner": False
        }],
        "isInner": False
    }], ensure_ascii=False)

# En el payload, dejar content vacío y poner el _elementor_data en meta:
payload = {
    "title": "Título",
    "slug": "slug",
    "status": "draft",
    "content": "",   # Elementor ignora esto cuando _elementor_data está presente
    "meta": {
        "_elementor_edit_mode": "builder",
        "_elementor_template_type": "wp-page",
        "_elementor_data": elementor_html_widget(FULL_HTML_CONTENT),
        "yoast_wpseo_title": "SEO Title | Marca",
        "yoast_wpseo_metadesc": "Meta descripción.",
        "yoast_wpseo_focuskw": "keyword",
    }
}
```

### Bug frecuente: CSS con dobles llaves

Si el CSS se generó en un Python f-string o con `.format()`, puede contener `{{` y `}}` como escape de `{` y `}`. Estos son **inválidos en CSS** y rompen todos los estilos.

La función `elementor_html_widget` ya aplica el fix automáticamente. Si se necesita corregir páginas ya publicadas:

```python
# Script de fix: output/agency/wp_fix_service_css.py
# Lee el _elementor_data actual, aplica replace('{{', '{'), actualiza.
```

### Páginas RD que usan este patrón

| Página | ID | Clase CSS wrapper |
|--------|----|-------------------|
| La Bóveda | 6835 | `rd-bv` |
| Web con IA Agéntica | 6836 | `rd-web-ia` |
| Posicionamiento en IAs | 6837 | `rd-pos-ia` |
| Manual Notebook LM | 6759 | (estructura propia) |
| Manual de Claudia | 6805 | `rd-manual-claudia` |
| Programar de forma agéntica | 6546 | `rd-taller-ia` |

Ver el design system completo invocando `/web:wp-page-rd`.

---

---

## Patrón avanzado: editar páginas Elementor existentes

Descubierto el 2026-06-04. Para modificar el HTML de una página ya creada con el patrón Elementor anterior, hay que editar `_elementor_data` directamente.

### Flujo PowerShell (edición quirúrgica)

```powershell
# 1. Descargar página con context=edit para acceder a meta
curl -s -u "$WP_RD_USER:$WP_RD_APP_PASSWORD" \
  "$WP_RD_URL/wp-json/wp/v2/pages/XXXX?context=edit" > "C:\Temp\page.json"

# 2. Parsear en PowerShell — ConvertFrom-Json decodifica el JSON exterior
$json = Get-Content "C:\Temp\page.json" -Raw | ConvertFrom-Json
$ed = $json.meta._elementor_data   # string con el JSON interior de Elementor

# 3. Hacer reemplazos directamente en la string decodificada
# CRÍTICO: usar caracteres Unicode reales (ó, é, ú...) NO escapes ó
$ed = $ed.Replace('<a href=\"/url-vieja/\">texto</a>', 'texto')
# Las comillas en atributos HTML son literales \" (barra + comilla)
# Las barras en URLs son literales \/ (barra + slash)
# Verificar: $ed.IndexOf("url-vieja") debe devolver -1 tras el replace

# 4. Construir body del PATCH y guardar en archivo
$patchBody = @{ meta = @{ _elementor_data = $ed } } | ConvertTo-Json -Depth 10 -Compress
$patchBody | Out-File "C:\Temp\patch.json" -Encoding UTF8 -NoNewline

# 5. Enviar PATCH
curl -s -X POST -u "$WP_RD_USER:$WP_RD_APP_PASSWORD" \
  "$WP_RD_URL/wp-json/wp/v2/pages/XXXX" \
  -H "Content-Type: application/json" \
  --data-binary @"C:\Temp\patch.json" | grep -o '"status":"[^"]*"\|"modified":"[^"]*"'
```

### Encoding — la trampa más habitual

| Lo que ves en el raw file JSON | Lo que obtienes tras ConvertFrom-Json | Lo que usar en Replace() |
|---|---|---|
| `formación` (6 chars ASCII) | `formación` (char Unicode ó) | `'formación'` (ó real) |
| `<a href=\"\/url\/\">` | `<a href=\"/url/\">` | `'<a href=\"/url/\">'` |
| `<\/div>` | `<\/div>` (\ conservado) | `'<\/div>'` |

**Regla**: tras `ConvertFrom-Json`, los escapes unicode `\uXXXX` se convierten en caracteres reales. Los `\"` y `\/` del JSON interior de Elementor se conservan como literales de dos caracteres.

### Por qué NO usar content.raw

`content.raw` del endpoint `context=edit` es el `post_content` filtrado por WP kses — **pierde todas las etiquetas `<div>`, `<style>`, etc.** Para páginas Elementor, siempre trabajar con `meta._elementor_data`.

### Páginas RD editadas con este patrón

| Página | ID | Operación |
|--------|----|-----------|
| Artículo Bóveda IA agencias | 6868 | Corrección enlaces rotos (2026-06-04) |
| Hub Bóveda | 6835 | Añadir card + cambio grid (2026-06-04) |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Añadido patrón edición Elementor existente, tabla encoding PowerShell, y advertencia content.raw.*
