Genera un prompt optimizado para **Claude Design** para construir la web de un cliente.

## Flujo

1. Pide el nombre del cliente (o usa el contexto actual)
2. Lee el perfil del cliente en `clients/<nombre>/profile.md`
3. Busca si existe un plan de web en `clients/<nombre>/web/` o en artifacts/conversaciones recientes
4. Construye un prompt completo para Claude Design siguiendo la plantilla de abajo
5. Guarda el prompt en `clients/<nombre>/web/prompt-claude-design.md`
6. Muestra el prompt al usuario para que lo copie y envíe a Claude Design

## Plantilla del Prompt para Claude Design

El prompt generado debe incluir TODOS estos bloques:

```
# [Nombre de la Marca] — Diseño Web

## Contexto de marca
[Resumen del brief: qué es, propósito, posicionamiento, arquetipos, personalidad, tono de voz]

## Identidad Visual
- Logo: [descripción del logo, adjuntar imagen si posible]
- Paleta de colores: [colores exactos con hex del manual de marca]
- Tipografías: [fuentes, pesos, usos]
- Estilo visual: [referencias, estética, tipo de imágenes]

## Estructura de la web
[Lista de páginas con contenido de cada una]

## Página a diseñar: [nombre]
[Secciones detalladas con contenido, layout, interactividad]

## Audiencia
[ICP, edad, perfil, pain points]

## CTA principal
[Acción objetivo, enlace, canal]

## Requisitos técnicos
- Responsive: mobile (375px), tablet (768px), desktop (1440px)
- HTML5 semántico + CSS moderno + JS vanilla
- Animaciones: [nivel de interactividad deseado]
- SEO: títulos, meta, estructura de headings

## Referencia de estilo
[Palabras clave de la estética: quiet luxury, editorial, minimalismo, etc.]
```

## Reglas

- Usar SIEMPRE los colores exactos del manual de marca (hex)
- Incluir el tagline de la marca si existe
- Si hay fotos del cliente, mencionarlo para que se integren
- El prompt debe ser autocontenido: Claude Design debe poder generar el diseño sin preguntas adicionales
- Generar un prompt separado para CADA página (no todas juntas)
- Empezar siempre por la Home
