# /Claudia — Activar canal Telegram

Activa la conexión con Telegram en la sesión actual.

## Qué hace

1. Crea el directorio `approved/` con el chatId autorizado
2. Confirma que el bot está corriendo
3. Envía un mensaje de prueba a Telegram avisando que Claudia está lista

## Pasos

```bash
# Crear directorio approved/ con chatId
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\channels\telegram\approved"
"approved" | Out-File -FilePath "$env:USERPROFILE\.claude\channels\telegram\approved\1067100103" -Encoding utf8
```

Después de ejecutar los pasos anteriores, usa la herramienta `mcp__plugin_telegram_telegram__reply` para enviar al chat_id `1067100103`:

> "✅ Claudia activa y escuchando. ¿En qué trabajamos hoy?"

## Nota

Si esta sesión **no fue iniciada con `--channels`**, los mensajes de Telegram no llegarán aunque el directorio esté creado. En ese caso, cierra y usa el script `Claudia.ps1` desde el terminal.
