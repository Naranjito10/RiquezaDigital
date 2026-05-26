"""
Watcher de carpetas para automatización de edición de video de Riqueza Digital.
Monitorea la carpeta 'input/' y procesa automáticamente cualquier video nuevo:
1. Transcribe con Whisper API.
2. Analiza con GPT-4o-mini para obtener un título catchy e identificar conceptos clave.
3. Genera iconos con la API de DALL-E 2 y les quita el fondo.
4. Genera el archivo edl.json.
5. Renderiza el video final usando render.py.
"""

import os
import time
import json
import requests
import argparse
from pathlib import Path
from openai import OpenAI

# Directorios de trabajo
BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
EDIT_DIR = BASE_DIR / "edit"
EXPORTADOS_DIR = EDIT_DIR / "exportados"
PROCESSED_FILE = EDIT_DIR / "watcher_processed.json"

# Cargar variables de entorno
def load_env():
    env_path = BASE_DIR.parent.parent / ".env"
    if env_path.exists():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip().strip('"').strip("'")

load_env()
API_KEY = os.environ.get("OPENAI_API_KEY", "")

def get_processed_files():
    if PROCESSED_FILE.exists():
        try:
            return set(json.loads(PROCESSED_FILE.read_text(encoding="utf-8")))
        except Exception:
            return set()
    return set()

def save_processed_file(filename):
    processed = get_processed_files()
    processed.add(filename)
    PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_FILE.write_text(json.dumps(list(processed), indent=2), encoding="utf-8")

def analyze_transcript_with_gpt(text):
    """Llama a GPT-4o-mini para generar un título catchy y buscar conceptos clave."""
    client = OpenAI(api_key=API_KEY)
    
    prompt = f"""
    Analiza la siguiente transcripción de un video corto en español:
    "{text}"
    
    Tus tareas son:
    1. Generar un título catchy, corto y enganchador (máximo 6 palabras) enfocado al público objetivo de Riqueza Digital (emprendedores que buscan automatización con n8n, IA, productividad y crecimiento empresarial).
    2. Identificar entre 2 y 3 conceptos clave muy específicos de los que se hable en el video. Para cada concepto clave:
       - Indica la palabra o frase exacta (1-2 palabras máximo).
       - Estima los tiempos de inicio y fin (en segundos) basándote en la transcripción.
       - Crea un prompt en inglés para generar una ilustración o icono simple vectorizado, cozy y minimalista, sobre un fondo plano morado oscuro #21123D.
       
    Devuelve la respuesta en formato JSON estrictamente con la siguiente estructura:
    {{
      "title": "El título corto aquí",
      "concepts": [
        {{
          "word": "concepto",
          "start": 5.0,
          "end": 8.0,
          "image_prompt": "A cozy and professional minimalist vector icon of..."
        }}
      ]
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "Eres un asistente de inteligencia artificial experto en marketing digital y redacción de copys creativos para Riqueza Digital."},
            {"role": "user", "content": prompt}
        ]
    )
    
    return json.loads(response.choices[0].message.content)

def get_semantic_fallback(word):
    """Retorna la ruta del icono de marca pre-existente si tiene relación directa, de lo contrario None."""
    word_lower = word.lower()
    
    ai_keywords = [
        "claude", "inteligencia", "ia", "cerebro", "code", "ai", "openai", "gemini", 
        "gpt", "llm", "modelo", "pensamiento", "razonamiento", "tecnología", "computa", "máquina"
    ]
    network_keywords = [
        "agente", "sistema", "red", "nodos", "trabajador", "orquest", "herramienta",
        "automatiz", "n8n", "webhook", "api", "conectar", "flujo", "integración", "base", "datos"
    ]
    productivity_keywords = [
        "productividad", "cohete", "lanzamiento", "negocio", "crecimiento", "rápido", 
        "acelerar", "velocidad", "despegar", "éxito", "empresa", "ventas", "dinero", 
        "finanzas", "inversión", "eficiencia", "optimizar"
    ]
    
    if any(k in word_lower for k in ai_keywords):
        return "edit/ai_brain_icon.png"
    elif any(k in word_lower for k in network_keywords):
        return "edit/agents_network_icon.png"
    elif any(k in word_lower for k in productivity_keywords):
        return "edit/productivity_rocket_icon.png"
    
    return None

def generate_concept_icon(image_prompt, filename_base):
    """Genera un icono usando Imagen 3 -> DALL-E 3 -> DALL-E 2."""
    gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if gemini_key:
        try:
            print(f"    -> Generando imagen con Imagen 3 para: '{filename_base}'...")
            from google import genai
            from google.genai import types
            
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_images(
                model='imagen-3.0-generate-002',
                prompt=image_prompt,
                config=types.GenerateImagesConfig(
                    number_of_images=1,
                    aspect_ratio='1:1',
                    output_mime_type='image/png'
                )
            )
            image_bytes = response.generated_images[0].image.image_bytes
            out_path = EDIT_DIR / f"{filename_base}.png"
            out_path.write_text("", encoding="utf-8")
            with open(out_path, "wb") as handler:
                handler.write(image_bytes)
            print(f"    [OK] Icono (Imagen 3) guardado en: {out_path.name}")
            return f"edit/{filename_base}.png"
        except Exception as e:
            print(f"    [AVISO] Falló Imagen 3: {e}. Intentando fallback con DALL-E 3...")

    # DALL-E 3 Fallback
    if API_KEY:
        try:
            print(f"    -> Generando imagen con DALL-E 3 para: '{filename_base}'...")
            client = OpenAI(api_key=API_KEY)
            response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            img_data = requests.get(image_url).content
            out_path = EDIT_DIR / f"{filename_base}.png"
            out_path.write_text("", encoding="utf-8")
            with open(out_path, "wb") as handler:
                handler.write(img_data)
            print(f"    [OK] Icono (DALL-E 3) guardado en: {out_path.name}")
            return f"edit/{filename_base}.png"
        except Exception as e:
            print(f"    [AVISO] Falló DALL-E 3: {e}. Intentando fallback con DALL-E 2...")

    # DALL-E 2 Fallback
    if API_KEY:
        try:
            print(f"    -> Generando imagen con DALL-E 2 para: '{filename_base}'...")
            client = OpenAI(api_key=API_KEY)
            response = client.images.generate(
                model="dall-e-2",
                prompt=image_prompt,
                n=1,
                size="512x512"
            )
            image_url = response.data[0].url
            img_data = requests.get(image_url).content
            out_path = EDIT_DIR / f"{filename_base}.png"
            out_path.write_text("", encoding="utf-8")
            with open(out_path, "wb") as handler:
                handler.write(img_data)
            print(f"    [OK] Icono (DALL-E 2) guardado en: {out_path.name}")
            return f"edit/{filename_base}.png"
        except Exception as e:
            print(f"    [AVISO] Falló DALL-E 2: {e}.")

    raise RuntimeError("No se pudo generar la imagen con ninguna API de generación.")

def process_video(video_path):
    """Orquesta todo el pipeline para un único video."""
    print(f"\n==================================================")
    print(f"PROCESANDO NUEVO VIDEO: {video_path.name}")
    print(f"==================================================")
    
    # 1. Transcripción
    from helpers.transcribe import transcribe_one
    print("[1/5] Transcribiendo audio con Whisper...")
    transcript_json_path = transcribe_one(video_path, EDIT_DIR, API_KEY, language="es")
    
    with open(transcript_json_path, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)
    
    video_text = transcript_data.get("text", "")
    words = transcript_data.get("words", [])
    if not words:
        print("[ERROR] No se encontraron palabras en la transcripción.")
        return
    
    duration = words[-1]["end"]
    
    # 2. Análisis del texto con GPT
    print("[2/5] Analizando transcripción y diseñando ganchos con GPT...")
    gpt_analysis = analyze_transcript_with_gpt(video_text)
    title = gpt_analysis.get("title", "Riqueza Digital")
    concepts = gpt_analysis.get("concepts", [])
    
    print(f"    Título Catchy Generado: \"{title}\"")
    print(f"    Conceptos clave identificados: {[c['word'] for c in concepts]}")
    
    # 3. Generación de Iconos con DALL-E/Imagen 3
    print("[3/5] Generando iconos cozy para conceptos clave...")
    image_overlays = []
    for idx, concept in enumerate(concepts):
        concept_slug = f"icon_{video_path.stem}_{idx}"
        try:
            file_relative_path = generate_concept_icon(concept["image_prompt"], concept_slug)
            image_overlays.append({
                "file": file_relative_path,
                "start": concept["start"],
                "end": concept["end"]
            })
        except Exception as e:
            print(f"    [AVISO] No se pudo generar la imagen para '{concept['word']}': {e}")
            print(f"            Buscando coincidencia semántica para aplicar fallback...")
            
            fallback_file = get_semantic_fallback(concept["word"])
            if fallback_file:
                print(f"            [OK] Aplicando icono local: {fallback_file}")
                image_overlays.append({
                    "file": fallback_file,
                    "start": concept["start"],
                    "end": concept["end"]
                })
            else:
                print(f"            [AVISO] Sin coincidencia semántica. No se añadirá imagen para este concepto.")
            
    # 4. Creación de edl.json
    print("[4/5] Generando archivo edl.json...")
    edl_content = {
        "version": 1,
        "sources": {
            video_path.stem: f"input/{video_path.name}"
        },
        "ranges": [
            {
                "source": video_path.stem,
                "start": 0.0,
                "end": duration
            }
        ],
        "grade": "cool_modern",
        "subtitles": True,
        "aspect": "vertical",
        "title": title,
        "image_overlays": image_overlays
    }
    
    edl_path = EDIT_DIR / "edl.json"
    with open(edl_path, "w", encoding="utf-8") as f:
        json.dump(edl_content, f, indent=2, ensure_ascii=False)
        
    # 5. Renderizado del video final
    print("[5/5] Renderizando video con subtítulos estables e iconos...")
    from helpers.render import render
    final_video = render(edl_path, mode="final", aspect="vertical")
    
    print(f"\n[OK] ¡PROCESAMIENTO COMPLETADO CON ÉXITO!")
    print(f"     Vídeo final exportado en: {final_video}")

def start_watcher():
    """Inicia el bucle de polling para vigilar la carpeta input/"""
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    EDIT_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"==================================================")
    print(f"WATCHER DE RIQUEZA DIGITAL ACTIVO")
    print(f"Vigilando carpeta: {INPUT_DIR.resolve()}")
    print(f"Presiona Ctrl+C para detener...")
    print(f"==================================================")
    
    # Asegurar que existen los efectos de sonido de la marca
    click_sound = EDIT_DIR / "click.wav"
    if not click_sound.exists():
        print("  -> Generando sonido click.wav...")
        from helpers.utils import ffmpeg_bin
        import subprocess
        cmd = [
            ffmpeg_bin(), "-y", "-f", "lavfi", "-i",
            "sine=frequency=1200:duration=0.05,afade=t=out:st=0.01:d=0.04",
            str(click_sound)
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    pop_sound = EDIT_DIR / "pop.wav"
    swoosh_sound = EDIT_DIR / "swoosh.wav"
    
    if not pop_sound.exists() or not swoosh_sound.exists():
        print("  -> Sintetizando sonidos pop.wav / swoosh.wav...")
        from helpers.sounds import generate_pop_sound, generate_swoosh_sound
        if not pop_sound.exists():
            generate_pop_sound(pop_sound)
        if not swoosh_sound.exists():
            generate_swoosh_sound(swoosh_sound)
        
    while True:
        try:
            processed = get_processed_files()
            # Listar videos válidos en input/
            candidates = [
                f for f in INPUT_DIR.iterdir()
                if f.is_file() and f.suffix.lower() in [".mp4", ".mov", ".mkv", ".avi"]
            ]
            
            for video in candidates:
                if video.name not in processed:
                    # Encontró un video nuevo, lo procesamos
                    process_video(video)
                    save_processed_file(video.name)
                    
            time.sleep(5) # Poll cada 5 segundos
        except KeyboardInterrupt:
            print("\nDeteniendo Watcher...")
            break
        except Exception as e:
            print(f"\n[ERROR EN WATCHER]: {e}")
            time.sleep(10)

if __name__ == "__main__":
    if not API_KEY:
        print("[ERROR] OPENAI_API_KEY no encontrada en tu archivo .env.")
    else:
        start_watcher()
