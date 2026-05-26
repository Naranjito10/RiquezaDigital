# Handoff — Vibiz / Marca RD

## State
Vibiz plugin instalado vía `claude plugin install vibiz@vibiz` (scope user). MCP `plugin:vibiz:vibiz` registrado, estado `! Needs authentication`. Dossier de inteligencia competitiva creado en `agencia/inteligencia-competitiva/vibiz/` con protocolo. `AGENCIA-AGENTICA.md` actualizado (F-008, F-009, sección Inteligencia Competitiva). 6 tareas Notion creadas en la Tareas DB del fundador.

## Next
1. **Bloqueante usuario:** reiniciar Claude Code → `/mcp` → autenticar `vibiz` → conectar SOLO Meta, LinkedIn, TikTok (saltar X y Threads).
2. Tras auth, primer trabajo de captura: `/mcp` → volcar las tools de vibiz en `agencia/inteligencia-competitiva/vibiz/arquitectura-producto.md` (Notion task #3, la más rentable).
3. Confirmar política `[skip-vibiz]` en commits y añadir convención a `CLAUDE.md` (Notion task #2).

## Context
- Hook `PostToolUse` de vibiz ya activo — cualquier `git commit` sin `[skip-vibiz]` o `[no-post]` disparará borrador de post social. Aplicar tag por defecto hasta confirmar política.
- Foco solo en Meta/LinkedIn/TikTok. **Nunca** usar vibiz con datos de cliente — solo para contenido de RD misma.
- Decisión de continuidad agendada 2026-06-08 (Notion task #6): si < 5 entradas en `decisiones-roadmap.md`, cancelar.
- Coste fijo de vibiz: ~533 tok always-on por sesión.
