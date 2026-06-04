# SOP: Conectar cliente a Google Ads API

**Área:** Marketing — Google Ads  
**Estado:** 🌱 Draft  
**Última actualización:** 2026-06-04  
**Clientes donde se aplicó:** Tecniclima  
**Tiempo estimado:** 30–60 min (excluyendo espera de aprobación Google, 1–3 días hábiles)

---

## Resumen

Proceso completo para conectar una cuenta de cliente a la Google Ads API via OAuth2, desde la solicitud de Basic Access hasta el primer reporte ejecutado con el pipeline Python.

---

## Pre-requisitos

- [ ] Cliente tiene cuenta Google Ads activa con customer_id (formato XXX-XXX-XXXX)
- [ ] Acceso a Google Cloud Console (console.cloud.google.com) de la cuenta RD
- [ ] Developer token en Google Ads API Center (aceptar T&C primero)
- [ ] Pipeline `pipelines/marketing-digital/` operativo con `pip install -r requirements.txt`

---

## Pasos

### 1. Aceptar T&C y obtener el Developer Token

1. Google Ads → Herramientas → Centro de la API
2. Aceptar los Términos de Servicio de la API
3. Copiar el Developer Token (estado inicial: "Acceso de prueba")

**Resultado esperado:** Token visible, estado "Test Access" o "Basic Access".

### 2. Solicitar Basic Access (necesario para cuentas de clientes reales)

Acceder al formulario oficial de Google Ads API Basic Access.

Campos clave:
- **Company:** Riqueza Digital
- **Use case:** Marketing agency managing Google Ads accounts on behalf of clients. Read-only reporting plus manual campaign creation reviewed by a human before activation.
- **Accounts:** número de cuentas de cliente (~2-5)
- **Daily calls:** 100–500 (conservador)
- **Adjuntar:** `output/agency/google-ads-api-design-doc.rtf` (diseño técnico de la herramienta)

**Tiempo de espera:** 1–3 días hábiles. Sin Basic Access, el token solo sirve para cuentas de prueba.

### 3. Crear credenciales OAuth2 tipo Desktop en Google Cloud Console

1. console.cloud.google.com → seleccionar proyecto (o crear nuevo)
2. APIs y Servicios → Habilitar → buscar "Google Ads API" → Habilitar
3. Credenciales → Crear credenciales → **ID de cliente OAuth 2.0**
4. Tipo: **Aplicación de escritorio** (NO web — InstalledAppFlow requiere Desktop)
5. Nombre: `Riqueza Digital Ads Pipeline`
6. Descargar → copiar `client_id` y `client_secret`

> ⚠️ Si ya existe un cliente OAuth de tipo "Aplicación web", crear uno nuevo de tipo Escritorio igualmente. Son tipos distintos e incompatibles con InstalledAppFlow.

### 4. Crear profile.json del cliente

```bash
mkdir pipelines/marketing-digital/ads/clients/<cliente>
cp pipelines/marketing-digital/ads/clients/_template/profile.json \
   pipelines/marketing-digital/ads/clients/<cliente>/profile.json
```

Rellenar en el archivo:
```json
"google": {
  "enabled": false,
  "developer_token": "<token del paso 1>",
  "client_id": "<del paso 3>",
  "client_secret": "<del paso 3>",
  "refresh_token": "",
  "customer_id": "XXX-XXX-XXXX"
}
```

> ⚠️ Nunca pegar credenciales en el chat. Editar el archivo directamente en el IDE.

### 5. Generar refresh_token (OAuth2 interactivo, una sola vez)

```bash
cd pipelines/marketing-digital
python src/get_google_insights.py --setup <cliente>
```

Se abre el navegador → autorizar con la cuenta Google que tiene acceso al Google Ads del cliente → el refresh_token se guarda automáticamente en profile.json.

### 6. Activar y probar

En profile.json: `"enabled": true`

```bash
python src/get_google_insights.py --client <cliente>
# o con más detalle:
python src/get_google_insights.py --client <cliente> --range LAST_30_DAYS --level adgroup
```

**Resultado esperado:** Reporte en consola con campañas, gasto, clics, conversiones, ROAS.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| Error "developer token not approved" | Token en Test Access, cuenta no es de prueba | Esperar aprobación Basic Access |
| OAuth error redirect_uri_mismatch | Cliente OAuth es tipo Web, no Desktop | Crear nuevo cliente tipo Aplicación de escritorio |
| ImportError google.ads.googleads | SDK no instalado | `pip install google-ads` |
| "No existe profile.json" | Carpeta del cliente no creada | Crear estructura `ads/clients/<cliente>/` |

---

## Decisiones clave

- **Decisión:** Un profile.json por cliente (no .env global)  
  **Razón:** Multi-cliente — cada uno tiene sus propias credenciales OAuth2 y customer_id  
  **Alternativa descartada:** Variables de entorno globales — no escalan a múltiples clientes

- **Decisión:** Solicitar Basic Access desde el inicio  
  **Razón:** Test Access solo sirve para cuentas de prueba, inútil para datos reales de clientes

---

## Adaptación por cliente

| Variable | Dónde afecta |
|----------|-------------|
| customer_id | profile.json → google.customer_id |
| Cuenta Google autorizada | Debe ser la que tiene acceso al Google Ads del cliente |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Setup inicial para Tecniclima*
