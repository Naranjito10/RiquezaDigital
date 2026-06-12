"""
Cliente API de WordPress para Riqueza Digital.
Permite crear, actualizar, listar y gestionar páginas y metadatos SEO en WordPress.
Uso: python pipelines/desarrollo/wordpress_client.py --help
"""

import os
import sys
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()


class WordPressClient:
    def __init__(self):
        wp_url = None
        username = None
        app_password = None
        
        # Intentar cargar desde el Registro de Windows primero (para variables específicas de Veganashi)
        if sys.platform == "win32":
            try:
                import winreg
                def get_registry_env(name: str) -> str:
                    try:
                        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")
                        val, _ = winreg.QueryValueEx(key, name)
                        winreg.CloseKey(key)
                        return val
                    except:
                        return None
                
                wp_url = get_registry_env("WP_VEGANASHI_URL")
                username = get_registry_env("WP_VEGANASHI_USER")
                app_password = get_registry_env("WP_VEGANASHI_APP_PASSWORD")
            except Exception as e:
                print(f"[WARN] Error al leer del registro de Windows: {e}")
                
        # Si no se encuentran en el registro, usar variables de entorno / .env
        self.wp_url = (wp_url or os.getenv("WP_URL", "")).rstrip("/")
        self.username = username or os.getenv("WP_USERNAME")
        self.app_password = app_password or os.getenv("WP_APP_PASSWORD")
        
        # Eliminar espacios de la contraseña de aplicación si existen (WP acepta ambos, pero sin espacios es estándar)
        if self.app_password:
            self.app_password = self.app_password.replace(" ", "")

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def _get_auth(self):
        if not all([self.wp_url, self.username, self.app_password]):
            raise ValueError(
                "Faltan credenciales de WordPress en tu archivo .env o en el Registro de Windows.\n"
                "Asegúrate de configurar WP_VEGANASHI_URL, WP_VEGANASHI_USER y WP_VEGANASHI_APP_PASSWORD en el Registro."
            )
        return (self.username, self.app_password)

    def test_connection(self) -> bool:
        """Prueba la conexión y credenciales con WordPress REST API."""
        try:
            auth = self._get_auth()
            # Llamamos al endpoint de usuarios/me para verificar credenciales
            endpoint = f"{self.wp_url}/wp-json/wp/v2/users/me"
            response = requests.get(endpoint, auth=auth, headers=self.headers)
            
            if response.status_code == 200:
                user_data = response.json()
                print(f"[OK] Conexión establecida con éxito a {self.wp_url}.")
                print(f"     Usuario autenticado: {user_data.get('name')} (Rol: {user_data.get('roles', ['N/A'])[0]})")
                return True
            else:
                print(f"[ERROR] Falló la autenticación con WordPress. Código de estado: {response.status_code}")
                print(f"        Respuesta: {response.text}")
                return False
        except Exception as e:
            print(f"[ERROR] No se pudo conectar al servidor de WordPress: {e}")
            return False

    def list_pages(self) -> list:
        """Lista las páginas existentes en WordPress."""
        try:
            auth = self._get_auth()
            endpoint = f"{self.wp_url}/wp-json/wp/v2/pages"
            # Solicitamos solo campos relevantes para velocidad
            params = {"_fields": "id,title,link,status", "per_page": 20}
            response = requests.get(endpoint, auth=auth, params=params, headers=self.headers)
            response.raise_for_status()
            
            pages = response.json()
            print(f"\nPáginas encontradas en WordPress ({len(pages)}):")
            print(f"{'='*70}")
            for p in pages:
                print(f"ID: {p['id']:<6} | Título: {p['title']['rendered']:<25} | Estado: {p['status']:<8} | Enlace: {p['link']}")
            return pages
        except Exception as e:
            print(f"[ERROR] Error al listar páginas: {e}")
            return []

    def create_page(self, title: str, content: str, status: str = "draft") -> dict:
        """Crea una nueva página en WordPress."""
        try:
            auth = self._get_auth()
            endpoint = f"{self.wp_url}/wp-json/wp/v2/pages"
            
            data = {
                "title": title,
                "content": content,
                "status": status
            }
            
            response = requests.post(endpoint, auth=auth, json=data, headers=self.headers)
            response.raise_for_status()
            
            page = response.json()
            print(f"[OK] Página '{title}' creada con éxito (Estado: {status}). ID: {page.get('id')}")
            print(f"     Enlace: {page.get('link')}")
            return page
        except Exception as e:
            print(f"[ERROR] No se pudo crear la página: {e}")
            return {}

    def update_page_seo(self, page_id: int, meta_title: str = None, meta_description: str = None) -> bool:
        """
        Modifica metadatos SEO. 
        Soporta los metadatos más comunes expuestos por plugins como Yoast o Rank Math.
        """
        try:
            auth = self._get_auth()
            endpoint = f"{self.wp_url}/wp-json/wp/v2/pages/{page_id}"
            
            # Construimos la sección de meta de acuerdo a plugins
            meta_data = {}
            if meta_title:
                meta_data["_yoast_wpseo_title"] = meta_title
                meta_data["rank_math_title"] = meta_title
            if meta_description:
                meta_data["_yoast_wpseo_metadesc"] = meta_description
                meta_data["rank_math_description"] = meta_description
            
            if not meta_data:
                print("[INFO] No se especificaron metadatos SEO para actualizar.")
                return False
                
            data = {"meta": meta_data}
            response = requests.post(endpoint, auth=auth, json=data, headers=self.headers)
            
            if response.status_code == 200:
                print(f"[OK] Metadatos SEO de la página {page_id} actualizados.")
                return True
            else:
                print(f"[ERROR] No se pudieron guardar los metadatos SEO. Estado: {response.status_code}")
                # A veces el endpoint de meta requiere soporte explícito en WP REST API
                print("Nota: Asegúrate de que tu plugin SEO tiene activado el soporte REST API.")
                return False
        except Exception as e:
            print(f"[ERROR] Error al actualizar metadatos SEO: {e}")
            return False


def load_legal_template(template_name: str) -> tuple:
    """Carga una plantilla legal desde local y extrae título y contenido."""
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    path = os.path.join(base_dir, "shared", "templates", "legal", f"{template_name}.md")
    
    if not os.path.exists(path):
        raise FileNotFoundError(f"No se encontró la plantilla en {path}")
        
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    # El primer encabezado markdown es el título
    title = "Documento Legal"
    content_lines = []
    
    for line in lines:
        if line.startswith("# ") and title == "Documento Legal":
            title = line.replace("# ", "").strip()
        else:
            content_lines.append(line)
            
    # Convertir markdown básico a HTML muy simple para que WordPress lo interprete bien
    # WordPress Gutenberg procesa bien saltos de línea y párrafos.
    content = "".join(content_lines)
    return title, content


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente WordPress de Riqueza Digital.")
    parser.add_argument("--test", action="store_true", help="Prueba de conexión y credenciales.")
    parser.add_argument("--list", action="store_true", help="Lista las primeras 20 páginas.")
    parser.add_argument("--create-page", nargs=2, metavar=("TITULO", "CONTENIDO"), help="Crea una página borrador.")
    parser.add_argument("--publish-legal", choices=["aviso-legal", "politica-privacidad", "terminos-servicio"], 
                        help="Publica un documento legal en borrador desde las plantillas locales.")
    parser.add_argument("--seo", nargs=3, metavar=("PAGE_ID", "TITLE", "DESCRIPTION"), 
                        help="Actualiza título y descripción SEO de una página.")
    
    args = parser.parse_args()
    client = WordPressClient()
    
    if args.test:
        client.test_connection()
    elif args.list:
        client.list_pages()
    elif args.create_page:
        client.create_page(args.create_page[0], args.create_page[1])
    elif args.publish_legal:
        try:
            title, content = load_legal_template(args.publish_legal)
            print(f"Cargada plantilla: '{title}'. Preparando subida a WordPress...")
            client.create_page(title, content, status="draft")
        except Exception as e:
            print(f"[ERROR] No se pudo cargar el archivo local: {e}")
    elif args.seo:
        client.update_page_seo(int(args.seo[0]), args.seo[1], args.seo[2])
    else:
        parser.print_help()
