# Claudia.ps1 — Inicia sesión Claude con canal Telegram activo
# Uso: .\Claudia.ps1

Write-Host "🛑 Cerrando sesiones activas de Telegram..." -ForegroundColor Yellow
Stop-Process -Name "Telegram" -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

$approvedDir = "$env:USERPROFILE\.claude\channels\telegram\approved"
$chatId = "1067100103"

# Crear directorio approved/ con chatId autorizado
New-Item -ItemType Directory -Force $approvedDir | Out-Null
"approved" | Out-File -FilePath "$approvedDir\$chatId" -Encoding utf8

Write-Host "✅ Canal Telegram configurado (chatId: $chatId)" -ForegroundColor Green
Write-Host "🚀 Iniciando Claudia con --channels..." -ForegroundColor Cyan

# Iniciar Claude con canal Telegram
claude --channels plugin:telegram@claude-plugins-official
