"""
Generador matemático de efectos de sonido nativos (pop.wav y swoosh.wav).
Diseñado para funcionar sin dependencias externas como numpy o scipy, usando wave, math y random.
"""
import wave
import math
import random
from pathlib import Path

def generate_pop_sound(out_path: Path):
    """Genera un sonido pop limpio (tono de frecuencia ascendente con decaimiento rápido)."""
    sample_rate = 44100
    duration = 0.15  # 150 ms
    num_samples = int(sample_rate * duration)
    
    frames = bytearray()
    for i in range(num_samples):
        t = i / sample_rate
        # Deslizamiento de frecuencia rápido (600Hz a 1200Hz)
        freq = 600 + (1200 - 600) * (t / duration)
        # Onda senoidal
        val = math.sin(2 * math.pi * freq * t)
        # Caída exponencial rápida
        envelope = math.exp(-20 * t)
        sample = val * envelope
        
        # Normalizar y limitar
        int_sample = int(sample * 32767 * 0.85)
        int_sample = max(-32768, min(32767, int_sample))
        frames.extend(int_sample.to_bytes(2, byteorder='little', signed=True))
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(frames)
    print(f"  [OK] Sonido sintetizado: {out_path.name}")


def generate_swoosh_sound(out_path: Path):
    """Genera un sonido de swoosh/transición suave (barrido de frecuencia y filtrado de ruido)."""
    sample_rate = 44100
    duration = 0.45  # 450 ms
    num_samples = int(sample_rate * duration)
    
    frames = bytearray()
    prev_val = 0.0
    
    for i in range(num_samples):
        t = i / sample_rate
        progress = t / duration
        
        # Ruido blanco base
        noise = random.uniform(-1.0, 1.0)
        
        # Tono senoidal de barrido de graves a medios
        freq = 80 + 350 * progress
        sine = math.sin(2 * math.pi * freq * t)
        
        # Mezcla (70% tono, 30% ruido)
        mixed = 0.7 * sine + 0.3 * noise
        
        # Filtro pasa-bajos dinámico (coeficiente alfa varía en forma de campana)
        alpha = 0.005 + 0.15 * math.sin(math.pi * progress)
        filtered = prev_val + alpha * (mixed - prev_val)
        prev_val = filtered
        
        # Envolvente de volumen (forma de campana para entrada y salida suave)
        envelope = math.sin(math.pi * progress)
        
        sample = filtered * envelope
        
        # Normalizar y limitar
        int_sample = int(sample * 32767 * 0.75)
        int_sample = max(-32768, min(32767, int_sample))
        frames.extend(int_sample.to_bytes(2, byteorder='little', signed=True))
        
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_path), 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(frames)
    print(f"  [OK] Sonido sintetizado: {out_path.name}")


if __name__ == "__main__":
    # Test generation
    edit_dir = Path(__file__).resolve().parent.parent / "edit"
    generate_pop_sound(edit_dir / "pop.wav")
    generate_swoosh_sound(edit_dir / "swoosh.wav")
