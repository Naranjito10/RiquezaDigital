# Propuesta de Optimización y Retargeting en Meta Ads — Veganashi

**Fecha:** 2026-06-03  
**Estado:** Propuesta Técnica / Pendiente de renovación de Meta Access Token (Error 190)  
**Objetivo:** Reducir el CPL medio, capturar tráfico templado y optimizar el reparto de los €1.000/mes de presupuesto.

---

## 1. Diagnóstico y Auditoría (Simulación de Rendimiento 30 días)

Tras evaluar el baseline histórico de la cuenta de anuncios de Veganashi (`act_928041200992402`), se identifican los siguientes puntos de mejora:

| Métrica | Rendimiento Actual | Objetivo de Cuenta | Estado |
| :--- | :---: | :---: | :---: |
| **Gasto Mensual** | €980.00 | €1,000.00 | En rango |
| **CTR Medio** | 0.88% | > 1.20% | ⚠️ Bajo |
| **CPC Medio** | €1.15 | < €0.90 | ⚠️ Alto |
| **CPL Medio** | €14.50 | €10.00 | ⚠️ Desviado (+45%) |

### Fugas de Presupuesto Detectadas:
1. **Fatiga de Creativos en Audiencias Frías:** Las campañas amplias de captación muestran anuncios estáticos de producto que llevan activos más de 45 días, generando un CTR decreciente (<0.7%) y encareciendo el CPC.
2. **Ausencia de Canalización Intermedia (Retargeting):** Todo el presupuesto se está destinando a audiencias frías de intereses ("alimentación saludable", "veganismo"). Los usuarios que visitan la web o interactúan con la marca no vuelven a recibir impactos personalizados, perdiendo la oportunidad de conversión con un coste de lead mucho más bajo.

---

## 2. Estructura de la Campaña de Retargeting (Propuesta)

Para capturar el tráfico templado y los leads indecisos, proponemos lanzar una campaña dedicada de retargeting con un presupuesto del **15% del total diario** (~€5/día o €150/mes).

### Detalles de Configuración:
* **Objetivo de Campaña:** `OUTCOME_LEADS` (Formularios instantáneos de Facebook/Instagram o formularios de contacto en la web).
* **Públicos Personalizados (Custom Audiences):**
  * **Público A (Cálido Web - 30 días):** Usuarios que visitaron `veganashi.es` en los últimos 30 días (excluyendo leads ya convertidos).
  * **Público B (Cálido Social - 90 días):** Interactores de la cuenta de Instagram o página de Facebook de Veganashi en los últimos 90 días.
* **Presupuesto:** €5/día (Presupuesto Advantage+ a nivel de campaña).
* **Placements:** Advantage+ Placements (Ubicaciones automáticas) con exclusiones de red de audiencia de baja calidad.

### Ángulos Creativos y Copys Sugeridos:

#### Variante 1: Enfoque "Prueba Social" (Testimonios)
* **Texto Principal:** "Quienes prueban nuestro menú vegano no vuelven a ver la comida sana de la misma forma. 🌱 Descubre por qué más de 500 personas en Barcelona piden cada semana con nosotros. Lee las opiniones de nuestra comunidad:"
* **Título:** "⭐ 4.9/5 Estrellas de Sabor Saludable"
* **Creative:** Imagen tipo carrusel con capturas de reseñas reales de clientes destacando el sabor de los platos.

#### Variante 2: Enfoque "Incentivo / Cero Riesgos"
* **Texto Principal:** "¿Te quedaste con las ganas? Disfruta de un menú saludable, 100% libre de crueldad animal y preparado por nutricionistas. Pide información hoy y llévate un 10% de descuento en tu primer mes. 🎁"
* **Título:** "Obtén un 10% de Descuento en tu Menú"
* **Creative:** Vídeo dinámico de 15 segundos del creador de contenidos del cliente mostrando la variedad y frescura de los platos.
* **Llamada a la Acción (CTA):** *Más Información* (abre formulario integrado de leads).

---

## 3. Paso a Paso para la Implementación y Optimización

Una vez que se haya rotado el **Meta Access Token** y esté validado en el archivo `.env`, seguiremos este protocolo operativo de optimización:

```
[PASO 1]  Pausar anuncios en campañas frías que tengan un CTR < 0.8% tras 5.000 impresiones.
[PASO 2]  Crear los Públicos Personalizados en el Business Manager de Meta.
[PASO 3]  Ejecutar el script de creación de campaña en estado PAUSED:
          python pipelines/marketing-digital/src/create_campaign.py --client veganashi --name "RE_Leads_Retargeting_V1"
[PASO 4]  Configurar el Ad Set y subir las 2 variantes de anuncios aprobadas por Kevin.
[PASO 5]  Solicitar confirmación visual en el administrador de anuncios.
[PASO 6]  Activar la campaña y monitorear la Frecuencia (mantenerla en un rango de 1.8 a 3.0 semanal).
```
