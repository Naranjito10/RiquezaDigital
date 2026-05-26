# Prompts Capturados de Vibiz

> Cada vez que veamos qué prompt usa Vibiz internamente (visible vía Claude Code, logs, o output que delate el prompt), lo guardamos aquí.

## Convención de nombres

`YYYY-MM-DD_<comando-o-tool>.md`

Ejemplo: `2026-05-25_vibiz-post.md`, `2026-05-25_generate-carousel.md`

## Plantilla por archivo

```markdown
# [Comando / tool]

- **Fecha:** YYYY-MM-DD
- **Cómo se obtuvo:** [visible directamente / inferido del output / logs de Claude Code]
- **Confianza:** [alta / media / baja]

## Prompt observado

\`\`\`
[texto literal]
\`\`\`

## Observaciones

- Estructura: [system / user / few-shot / chain-of-thought]
- Variables que inyecta: [cuáles]
- Patrón replicable: [sí / no — por qué]
```
