Genera copy publicitario para un anuncio.

1. Pregunta qué cliente, plataforma y objetivo del anuncio
2. Lee `clients/<cliente>/profile.md` para tono y audiencia
3. Activa el agente Content Manager (`.claude/agents/content/CLAUDE.md`)
4. Genera 3 variantes de copy con ángulos distintos (emocional, racional, urgencia)
5. Para cada variante: primary text, headline, descripción y CTA
6. Valida límites de caracteres por plataforma — usa las tablas del skill `ad-copy` (`.claude/skills/ad-copy/`): límites RSA/PMax/Meta, fórmulas de hooks y formato de salida
7. Guarda en `clients/<cliente>/copy/YYYY-MM-DD_<tipo>_v1.md`
