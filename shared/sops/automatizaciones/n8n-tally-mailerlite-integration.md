# SOP: Integración de Tally Forms con MailerLite vía n8n

**Área:** Automatizaciones  
**Estado:** 🔧 Verificado  
**Última actualización:** 2026-06-04  
**Clientes donde se aplicó:** Riqueza Digital  
**Tiempo estimado:** 15–20 minutos

---

## Resumen

Proceso paso a paso para configurar un formulario de Tally Forms, conectarlo con n8n mediante webhook y enviar los nuevos leads automáticamente a listas específicas de MailerLite utilizando la API.

---

## Pre-requisitos

- [ ] Cuenta de Tally Forms (tally.so) con el formulario creado y publicado
- [ ] Servidor n8n activo y accesible desde internet (para recibir webhooks externos)
- [ ] API Key de MailerLite y nombre/ID del grupo de destino para los suscriptores

---

## Pasos

### 1. Crear el Workflow en n8n
1. Crear un nuevo workflow en n8n y añadir un nodo **Webhook**.
2. Parámetros del nodo Webhook:
   - **Method:** `POST`
   - **Path:** `tally-leads-<cliente>`
   - **Authentication:** `None`
3. Guardar el nodo. Copiar la **Test URL** para la fase de pruebas inicial y la **Production URL** para la fase final.

### 2. Configurar la integración en Tally
1. Entrar en Tally.so, abrir el formulario y navegar a la pestaña **Integrations**.
2. Buscar **Webhooks** y hacer clic en conectar.
3. Pegar la **Test URL** copiada de n8n y guardar la integración.
4. En n8n, hacer clic en **Listen for test event** y en Tally enviar una respuesta de prueba al formulario.
5. Confirmar que n8n recibe el JSON completo con los datos ingresados en el formulario.

### 3. Procesar y Mapear los Datos
La estructura de datos enviada por Tally contiene un array bajo `data.fields`. Para procesarlo limpiamente en n8n:
1. Añadir un nodo **Code** (Javascript) o usar variables del webhook directamente en los nodos siguientes para mapear el email y el nombre.
2. Si usas javascript, extraer los campos clave:
   ```javascript
   const fields = $('Webhook').item.json.data.fields;
   const emailField = fields.find(f => f.type === 'EMAIL');
   const nameField = fields.find(f => f.type === 'INPUT_TEXT'); // Ajustar según ID
   return {
     json: {
       email: emailField.value,
       first_name: nameField ? nameField.value : ''
     }
   };
   ```

### 4. Conectar a MailerLite
1. Añadir un nodo **MailerLite** (o HTTP Request si usas la API v2 directamente).
2. Configurar las credenciales con tu API Key.
3. Configurar el nodo:
   - **Resource:** `Subscriber`
   - **Operation:** `Create or Update`
   - **Email:** `{{ $json.email }}`
   - **Fields:** `name = {{ $json.first_name }}`
   - **Groups:** Seleccionar o ingresar el ID del grupo de MailerLite (ej. Newsletter).

### 5. Activar y Pasar a Producción
1. Cambiar la URL del webhook en Tally por la **Production URL** de n8n.
2. Hacer clic en **Activate Workflow** en n8n.
3. Realizar una última prueba real introduciendo un email de prueba en la web y verificar que llega a MailerLite en menos de 10 segundos.

---

## Problemas comunes y soluciones

| Problema | Causa probable | Solución |
|----------|----------------|----------|
| n8n no recibe eventos en producción | El webhook de Tally está configurado con la URL "Test" de n8n y la sesión de escucha de test ya se cerró | Asegurarse de cambiar la URL en Tally a la Production URL de n8n y activar el flujo |
| Suscriptores sin nombre en MailerLite | El campo de texto en el formulario de Tally cambió de ID o de tipo | Verificar el JSON de Tally en la pestaña de historial de ejecuciones de n8n y ajustar el mapeo del Code block |
| Error 401 en MailerLite | API Key inválida o caducada | Regenerar la clave en la cuenta de MailerLite y actualizar la credencial en n8n |

---

## Decisiones clave

- **Decisión:** Usar el webhook directo de Tally en lugar de integraciones nativas directas de Tally.  
  **Razón:** n8n permite centralizar el tracking, aplicar filtros de descarte (ej. correos de spam), normalizar mayúsculas/minúsculas de nombres y enviar logs a Notion automáticamente.  
  **Alternativa descartada:** Conexión directa Tally-MailerLite (menos flexibilidad de procesamiento).

---

## Adaptación por cliente

| Variable | Dónde afecta | Ejemplo |
|----------|--------------|---------|
| ID del Grupo | MailerLite destination group | `Newsletter` vs `Clientes VIP` |

---

*Última sesión que actualizó este SOP: 2026-06-04 — Creación inicial del SOP de integración n8n Tally-MailerLite.*
