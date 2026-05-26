"""
Script de Extracción y Adaptación de Contenido Viral de Instagram.
Identifica los vídeos con mejor rendimiento de las cuentas de referencia y adapta su estructura.
Uso: python services/marketing/marketing-digital/src/instagram_scraper.py
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

load_dotenv()


def get_mock_viral_posts() -> list:
    """Retorna un listado de posts simulados de la cuenta de referencia si no hay API Key."""
    return [
        {
            "id": "123456789_reel",
            "caption": "El secreto de la productividad empresarial 🚀 #automatizaciones #n8n",
            "views": 250000,
            "likes": 12500,
            "avg_views": 25000, # La media de la cuenta es 25k, por lo que es un 10x viral!
            "transcript": (
                "¿Por qué sigues respondiendo correos a las 11 de la noche? "
                "El 90% de los fundadores están atrapados en tareas de administración de 5 dólares la hora. "
                "Nosotros creamos un agente que lee el correo, califica el lead, lo mete en Notion y "
                "le agenda una llamada de consultoría solo si factura más de 10k al mes. "
                "El resultado: recuperamos 15 horas a la semana y multiplicamos las ventas. "
                "Si quieres la plantilla de este flujo, comenta AGENTE abajo y te la envío por privado."
            )
        },
        {
            "id": "987654321_reel",
            "caption": "El error número uno al hacer anuncios en Meta Ads ⚠️",
            "views": 35000,
            "likes": 1200,
            "avg_views": 25000, # 1.4x, normal
            "transcript": "No configures tus campañas de Meta Ads apuntando al botón promocionar post..."
        }
    ]


def scrape_instagram_reels(username: str) -> list:
    """
    Obtiene los reels recientes del usuario usando RapidAPI.
    Si no está configurado RAPIDAPI_KEY, cae en mock.
    """
    rapidapi_key = os.getenv("RAPIDAPI_KEY")
    if not rapidapi_key:
        print("[INFO] RAPIDAPI_KEY no encontrada en .env. Usando datos de prueba (MOCK).")
        return get_mock_viral_posts()
        
    print(f"Scrapeando perfil de Instagram de: @{username}...")
    # Usando un endpoint genérico de RapidAPI Instagram Scraper
    url = "https://instagram-bulk-scraper-latest.p.rapidapi.com/web_profile_reels"
    headers = {
        "x-rapidapi-key": rapidapi_key,
        "x-rapidapi-host": "instagram-bulk-scraper-latest.p.rapidapi.com"
    }
    params = {"username": username}
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        # Parsear reels del JSON retornado por la API
        reels = []
        items = data.get("data", {}).get("user", {}).get("edge_felix_video_timeline", {}).get("edges", [])
        
        # Calcular media de reproducciones para detectar virales
        total_views = 0
        count = 0
        temp_reels = []
        
        for item in items:
            node = item.get("node", {})
            views = node.get("video_view_count", 0)
            likes = node.get("edge_liked_by", {}).get("count", 0)
            caption = ""
            edges = node.get("edge_media_to_caption", {}).get("edges", [])
            if edges:
                caption = edges[0].get("node", {}).get("text", "")
            
            temp_reels.append({
                "id": node.get("id"),
                "caption": caption,
                "views": views,
                "likes": likes,
                # En un caso real necesitaríamos la transcripción del vídeo bajándolo y usando Whisper.
                # Para simplificar, asumiremos que se transcribe el audio o usamos el caption largo.
                "transcript": caption 
            })
            total_views += views
            count += 1
            
        avg_views = total_views / count if count > 0 else 1
        for r in temp_reels:
            r["avg_views"] = avg_views
            reels.append(r)
            
        return reels
    except Exception as e:
        print(f"[ERROR] Error al conectar con la API de scraping: {e}. Usando MOCK.")
        return get_mock_viral_posts()


def adapt_script_with_ai(original_transcript: str) -> str:
    """Usa Claude para adaptar el guion original al nicho de Riqueza Digital."""
    api_key = os.getenv("OPENAI_API_KEY") # Usamos OpenAI ya que tenemos la key validada en .env
    if not api_key:
        print("[ERROR] Falta la clave de API (OPENAI_API_KEY) en .env para realizar la adaptación.")
        return ""
        
    print("Adaptando guion con Inteligencia Artificial...")
    
    # Prompt estructurado para copiar el formato y ritmo de retención
    prompt = f"""
Eres un Copywriter experto en vídeos cortos (Reels/TikTok) de alto impacto y retención.
Tu tarea es tomar la transcripción de un vídeo viral de referencia y reescribir un guion nuevo adaptado a Riqueza Digital (nicho: Automatizaciones de negocio con n8n, CRM, inteligencia artificial, o libertad digital).

REGLAS DE ADAPTACIÓN:
1. Mantén exactamente la estructura y ritmo del guion original:
   - El gancho inicial impactante (primeros 3 segundos).
   - El planteamiento del problema cotidiano.
   - La demostración de la solución técnica/automatización.
   - La llamada a la acción (CTA) orientada a comentar una palabra clave (ej: "AGENTE" o "CRM") para activar ManyChat.
2. Traduce el contenido al contexto de Riqueza Digital (ej: automatizar la gestión de leads, auditoría automática de anuncios, librarse de tareas repetitivas).
3. Añade indicaciones visuales para la edición (cortes de cámara, zooms, efectos de sonido y HyperFrames).

TRANSCRIPCIÓN ORIGINAL DE REFERENCIA:
\"\"\"
{original_transcript}
\"\"\"

Por favor, formatea la salida en Markdown estructurado dividiendo el guion en escenas e incluyendo:
- Tiempo estimado (s)
- Lo que se dice (Voz en off / Kevin)
- Lo que se ve (Indicaciones de edición y HyperFrames)
"""

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": "Eres el copywriter especialista de Riqueza Digital."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[ERROR] Error al llamar a la API de OpenAI: {e}")
        return ""


def main():
    username = "soyenriquerocha"
    reels = scrape_instagram_reels(username)
    
    # Filtrar por virales (views > 2 * avg_views)
    viral_reels = [r for r in reels if r["views"] > (2 * r["avg_views"])]
    
    if not viral_reels:
        print("[INFO] No se encontraron reels especialmente virales (views > 2x la media). Usando el de mayor visualizaciones.")
        viral_reels = sorted(reels, key=lambda x: x["views"], reverse=True)[:1]
        
    winner = viral_reels[0]
    print(f"\n[GANADOR ENCONTRADO] ID: {winner['id']}")
    print(f"  Visualizaciones: {winner['views']} (Media de cuenta: {winner['avg_views']:.0f})")
    print(f"  Transcripción de referencia:\n  {winner['transcript']}\n")
    
    # Adaptar con IA
    adapted_script = adapt_script_with_ai(winner["transcript"])
    
    if adapted_script:
        # Guardar resultado
        output_dir = os.path.join("output", "marketing", "ideas-virales")
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, "propuesta_script_adaptado.md")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# Propuesta de Guion Adaptado desde @{username}\n\n")
            f.write(f"**Referencia original**: Reel ID {winner['id']} ({winner['views']} views)\n")
            f.write(f"**Fecha de extracción**: 2026-05-25\n\n")
            f.write("---\n\n")
            f.write(adapted_script)
            
        print(f"[OK] Propuesta de guion guardada en: {output_file}")
    else:
        print("[ERROR] No se pudo generar la propuesta adaptada.")


if __name__ == "__main__":
    main()
