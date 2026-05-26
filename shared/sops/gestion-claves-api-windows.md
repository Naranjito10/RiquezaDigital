# SOP: Gestión de claves API con Variables de Entorno de Windows

**Área:** Desarrollo / Seguridad / Infraestructura  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-05-26  
**Clientes donde se aplicó:** Riqueza Digital (interno)  
**Tiempo estimado:** 20–30 minutos (primera vez) / 5 minutos (rotaciones posteriores)

---

## Resumen

Cómo almacenar claves API de forma segura en Windows usando variables de entorno de usuario, referenciarlas desde `.mcp.json` y rotarlas sin exponer secretos en archivos ni en el chat de Claude.

**Cuándo usar este proceso:**
- Primera configuración del entorno de desarrollo
- Rotación de claves comprometidas o por política periódica
- Incorporación de un nuevo servicio MCP al proyecto

---

## Pre-requisitos

- [ ] Acceso a Windows como el usuario que usa Claude Code
- [ ] Archivo `.mcp.json` localizado en la raíz del proyecto
- [ ] Acceso a los paneles de administración de cada servicio (Meta, Notion, Ahrefs, etc.)
- [ ] PowerShell disponible (viene con Windows — no requiere administrador)

---

## Pasos

### 1. Abrir `.mcp.json` manualmente y anotar los servicios

Abrir el archivo directamente en VS Code o Notepad. **No pedir a Claude que lo lea** — las claves quedarían expuestas en el contexto del chat.

Anotar en papel o en un bloc privado:
- Nombre del servicio (ej: `meta`, `notion`, `ahrefs`)
- El nombre del parámetro que contiene la clave (ej: `access_token`, `api_key`)

**Resultado esperado:** tienes una lista de N servicios con sus nombres de parámetro.

---

### 2. Crear las variables de entorno en Windows

Abrir PowerShell (Win + X → Terminal). **No necesita modo administrador.**

Por cada clave, ejecutar una línea:

```powershell
[Environment]::SetEnvironmentVariable("NOMBRE_VARIABLE", "VALOR_CLAVE", "User")
```

**Convenio de nombres recomendado:**

| Servicio | Nombre de variable sugerido |
|----------|-----------------------------|
| Meta / Facebook | `META_ACCESS_TOKEN` |
| Notion | `NOTION_API_KEY` |
| Ahrefs | `AHREFS_API_KEY` |
| Canva | `CANVA_API_KEY` |
| Google / Gemini | `GEMINI_API_KEY` |
| Anthropic | `ANTHROPIC_API_KEY` |
| n8n | `N8N_API_KEY` |
| MailerLite | `MAILERLITE_API_KEY` |
| Klaviyo | `KLAVIYO_API_KEY` |

Ejecutar una línea por cada servicio. Si no hay error, está guardado.

**¿Dónde se guardan?**  
En el Registro de Windows: `HKEY_CURRENT_USER\Environment`  
- No es un archivo en disco — no puede ser commiteado ni leído accidentalmente
- Solo accesible por el usuario de Windows activo
- Persiste entre reinicios del PC

**Resultado esperado:** PowerShell no devuelve error tras cada línea.

---

### 3. Verificar que se guardaron correctamente

```powershell
# Ver todas las variables de usuario (requiere .GetEnumerator() para iterar la Hashtable)
[Environment]::GetEnvironmentVariables("User").GetEnumerator() | Sort-Object Key
```

```powershell
# Filtrar solo las del proyecto
[Environment]::GetEnvironmentVariables("User").GetEnumerator() | Where-Object { $_.Key -match "META|GEMINI|NOTION|ANTHROPIC|N8N|AHREFS|CANVA|MAILER|KLAVIYO" }
```

```powershell
# Verificar una variable concreta por nombre exacto
[Environment]::GetEnvironmentVariable("META_ACCESS_TOKEN", "User")
```

> ⚠️ **Error frecuente:** usar `Where-Object` sin `.GetEnumerator()` devuelve vacío aunque las variables existan. La Hashtable se pasa como objeto único — `.GetEnumerator()` la convierte en lista de pares clave-valor.

**Resultado esperado:** se ven todas las variables con sus valores.

---

### 4. Actualizar `.mcp.json` para referenciar variables

En `.mcp.json`, sustituir cada valor literal de clave por `${NOMBRE_VARIABLE}`:

```json
// ANTES — peligroso, valor hardcodeado
"access_token": "EAAxxxxxxxxxxxxxx"

// DESPUÉS — seguro, referencia a variable de entorno
"access_token": "${META_ACCESS_TOKEN}"
```

Hacer esto para cada clave del archivo. Al terminar, `.mcp.json` no debe contener ningún secreto — solo nombres de variables entre `${}`.

Claude Code resuelve los `${...}` automáticamente al arrancar leyendo las variables de entorno del usuario.

**Resultado esperado:** `.mcp.json` no contiene ninguna clave real. Se puede leer o compartir sin riesgo.

---

### 5. Reiniciar Claude Code y verificar conexión MCP

Cerrar Claude Code completamente y volver a abrirlo. Las variables de entorno se leen en el arranque.

Comprobar que los servidores MCP conectan correctamente (Notion, Meta, etc. aparecen disponibles sin errores de autenticación).

**Resultado esperado:** todos los MCPs conectan igual que antes del cambio.

---

### 6. Rotar las claves en cada plataforma (cuando sea necesario)

| Servicio | Dónde rotar la clave |
|----------|----------------------|
| **Meta / Facebook** | [business.facebook.com](https://business.facebook.com) → Configuración → Accesos del sistema |
| **Ahrefs** | [ahrefs.com](https://ahrefs.com) → Account → API |
| **Canva** | [canva.com/developers](https://www.canva.com/developers) → Tus integraciones |
| **Notion** | [notion.so/my-integrations](https://www.notion.so/my-integrations) → Regenerar token |
| **MailerLite** | Dashboard → Integraciones → API |
| **n8n** | Settings → API Keys |
| **Anthropic** | [console.anthropic.com](https://console.anthropic.com) → API Keys |
| **Google / Gemini** | [aistudio.google.com](https://aistudio.google.com) → API Keys |

Para cada servicio:
1. Generar nueva clave en la plataforma
2. Actualizar la variable de entorno en PowerShell:

```powershell
[Environment]::SetEnvironmentVariable("NOMBRE_VARIABLE", "NUEVA_CLAVE", "User")
```

3. Después de rotar **todas** las claves, reiniciar Claude Code una vez

> No hace falta reiniciar entre cada clave — basta con un reinicio al final.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| `Where-Object` no devuelve nada | Falta `.GetEnumerator()` al iterar la Hashtable | Usar `GetEnvironmentVariables("User").GetEnumerator() \| Where-Object {...}` |
| MCP no conecta tras el cambio | Claude Code no recargó las variables | Cerrar y reabrir Claude Code completamente |
| Variable devuelve vacío con `GetEnvironmentVariable` | El nombre no coincide exactamente (mayúsculas/minúsculas) | Verificar nombre con `GetEnvironmentVariables("User").GetEnumerator()` |
| Variable se pierde tras reiniciar PC | Se usó `"Process"` en vez de `"User"` como ámbito | Repetir `SetEnvironmentVariable` con `"User"` como tercer parámetro |

---

## Decisiones clave

- **Decisión:** Variables de entorno de Windows en vez de archivo `.env`  
  **Razón:** No existe archivo en disco — elimina el riesgo de commit accidental y de lectura por agentes IA  
  **Alternativa descartada:** `.env` + `.gitignore` — más frágil; si el `.gitignore` falla o el agente lee el archivo, las claves quedan expuestas

- **Decisión:** Ámbito `"User"` en vez de `"Machine"`  
  **Razón:** No requiere permisos de administrador; las variables son visibles solo para el usuario activo  
  **Alternativa descartada:** `"Machine"` — accesible a todos los usuarios del PC, requiere admin

---

## Notas adicionales

- `.mcp.json` ya está en `.gitignore` del proyecto — nunca se sube a GitHub
- Este proceso se ejecutó por primera vez el 2026-05-26 tras detectar que las claves quedaban expuestas al leer `.mcp.json` en el chat de Claude

---

*Última sesión que actualizó este SOP: 2026-05-26 — proceso completo documentado tras primera implementación verificada*
