import urllib.request
import json
import os
import sys

# Ensure stdout uses UTF-8 to prevent encoding errors on Windows
sys.stdout.reconfigure(encoding='utf-8')

notion_key = os.environ.get("NOTION_API_KEY")
if not notion_key:
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment")
        notion_key, _ = winreg.QueryValueEx(key, "NOTION_API_KEY")
    except Exception as e:
        print("Error reading registry:", e)

if not notion_key:
    print("Error: NOTION_API_KEY not found in environment or registry.")
    sys.exit(1)

headers = {
    "Authorization": f"Bearer {notion_key}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def make_request(url, method="POST", data=None):
    data_bytes = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, headers=headers, data=data_bytes, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        try:
            error_json = json.loads(error_body)
            print(f"HTTP Error {e.code}: {error_json.get('message')}")
        except Exception:
            print(f"HTTP Error {e.code}: {error_body}")
        return e.code, None
    except Exception as e:
        print("Network error:", e)
        return 500, None

def append_block_children(parent_id, children):
    url = f"https://api.notion.com/v1/blocks/{parent_id}/children"
    body = {"children": children}
    print(f"Appending {len(children)} block(s) to parent {parent_id}...")
    status, res = make_request(url, "PATCH", body)
    if status == 200:
        print("Successfully appended blocks.")
    else:
        print("Failed to append blocks.")
    return status

def archive_page(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    body = {"archived": True}
    print(f"Archiving page {page_id}...")
    status, res = make_request(url, "PATCH", body)
    if status == 200:
        print(f"Successfully archived page {page_id}.")
    else:
        print(f"Failed to archive page {page_id}.")
    return status

print("--- NOTION TRIAGE EXECUTION ---")

# 1. D-02: Connect the two roots
# Append link to 'PROYECTOS CLIENTES' on 'RIQUEZA DIGITAL' (Home)
link_to_clients = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "🔗 Acceso Directo: "
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "link_to_page",
        "link_to_page": {
            "type": "page_id",
            "page_id": "249d2fec-4b82-80f9-bf37-cf738ad590cf" # PROYECTOS CLIENTES ID
        }
    }
]
append_block_children("9a5bbf82-b0a5-4000-b87d-d213a5e370d7", link_to_clients)

# Append link to 'RIQUEZA DIGITAL' on 'PROYECTOS CLIENTES' (Hub)
link_to_home = [
    {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "🏠 Volver a la Home: "
                    }
                }
            ]
        }
    },
    {
        "object": "block",
        "type": "link_to_page",
        "link_to_page": {
            "type": "page_id",
            "page_id": "9a5bbf82-b0a5-4000-b87d-d213a5e370d7" # RIQUEZA DIGITAL ID
        }
    }
]
append_block_children("249d2fec-4b82-80f9-bf37-cf738ad590cf", link_to_home)


# 2. D-03: Archive obsolete Brief Andrés
archive_page("36cd2fec-4b82-8109-a86d-f5438aadb5cb")


# 3. D-05: Archive obsolete Antigravity Projects
archive_page("2c7d2fec-4b82-80b1-adba-f96684ffe038")


# 4. D-08: Add warning disclaimer to Notion's CLAUDE.md page
disclaimer_block = [
    {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [
                {
                    "type": "text",
                    "text": {
                        "content": "⚠️ Fuente de verdad: El archivo CLAUDE.md oficial y actualizado reside en el repositorio Git local del proyecto. Esta versión de Notion sirve únicamente de referencia introductoria para agentes web."
                    }
                }
            ],
            "icon": {
                "emoji": "⚠️"
            },
            "color": "yellow_background"
        }
    }
]
append_block_children("337d2fec-4b82-8149-9f6f-dcb43afc8e4b", disclaimer_block)

print("\n--- NOTION TRIAGE COMPLETED ---")
