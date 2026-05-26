import os
import json
import urllib.request
import urllib.error
from pathlib import Path

class CredentialVault:
    """
    Realiza llamadas HTTP seguras a proveedores de LLM usando claves
    leídas dinámicamente, aislando las credenciales del código generado.
    Nativo de Windows: lee del registro si la variable no está en el entorno del proceso.
    """
    @staticmethod
    def _load_env_key(key_name: str) -> str:
        # 1. Intentar leer del entorno de proceso actual
        val = os.environ.get(key_name)
        if val:
            return val
            
        # 2. Fallback de Windows: leer directamente del Registro de Usuario (SOP Variables de Entorno)
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as key:
                reg_val, _ = winreg.QueryValueEx(key, key_name)
                if reg_val:
                    return reg_val
        except Exception:
            pass
            
        # 3. Fallback: leer del archivo .env en la raíz del proyecto
        workspace_root = Path(__file__).resolve().parents[3]
        env_file = workspace_root / ".env"
        if env_file.exists():
            try:
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        clean_line = line.strip()
                        if not clean_line or clean_line.startswith('#'):
                            continue
                        if '=' in clean_line:
                            k, v = clean_line.split('=', 1)
                            if k.strip() == key_name:
                                return v.strip().strip('"').strip("'")
            except Exception:
                pass
        return ""

    @classmethod
    def request(cls, provider: str, model: str, system_prompt: str, prompt: str, json_mode: bool = False) -> str:
        """
        Envía una petición al LLM (gemini o anthropic) sin exponer las keys en las variables de entorno locales.
        """
        provider = provider.lower()
        if provider == "gemini":
            return cls._request_gemini(model, system_prompt, prompt, json_mode)
        elif provider == "anthropic":
            return cls._request_anthropic(model, system_prompt, prompt, json_mode)
        else:
            raise ValueError(f"Proveedor no soportado: {provider}")

    @classmethod
    def _request_gemini(cls, model: str, system_prompt: str, prompt: str, json_mode: bool) -> str:
        api_key = cls._load_env_key("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no encontrada en variables de entorno, registro ni archivo .env.")
            
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ],
            "generationConfig": {}
        }
        
        if system_prompt:
            payload["systemInstruction"] = {
                "parts": [
                    {"text": system_prompt}
                ]
            }
            
        if json_mode:
            payload["generationConfig"]["responseMimeType"] = "application/json"
            
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                return text
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            raise RuntimeError(f"Gemini API HTTP Error {e.code}: {err_msg}") from e
        except Exception as e:
            raise RuntimeError(f"Error llamando a Gemini API: {str(e)}") from e

    @classmethod
    def _request_anthropic(cls, model: str, system_prompt: str, prompt: str, json_mode: bool) -> str:
        api_key = cls._load_env_key("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY no encontrada en variables de entorno, registro ni archivo .env.")
            
        url = "https://api.anthropic.com/v1/messages"
        
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        
        payload = {
            "model": model,
            "max_tokens": 4096,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
        
        if system_prompt:
            payload["system"] = system_prompt
            
        if json_mode and "json" not in prompt.lower():
            payload["messages"][0]["content"] += "\nResponde estrictamente en formato JSON."
            
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST"
        )
        
        try:
            with urllib.request.urlopen(req) as response:
                res_data = json.loads(response.read().decode("utf-8"))
                text = res_data["content"][0]["text"]
                return text
        except urllib.error.HTTPError as e:
            err_msg = e.read().decode("utf-8")
            raise RuntimeError(f"Anthropic API HTTP Error {e.code}: {err_msg}") from e
        except Exception as e:
            raise RuntimeError(f"Error llamando a Anthropic API: {str(e)}") from e
