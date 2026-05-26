@echo off
:: Ir al directorio del proyecto de edición de vídeo
cd /d "%~dp0"
:: Ejecutar el watcher en el entorno virtual
.venv\Scripts\python.exe watcher.py
