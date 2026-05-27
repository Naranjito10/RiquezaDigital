import json
import os
import sys
from datetime import datetime

# Ensure stdout uses UTF-8 to prevent encoding errors on Windows
sys.stdout.reconfigure(encoding='utf-8')

dump_path = r"C:\Users\kein-\.gemini\antigravity-ide\scratch\notion_dump.json"
output_dir = r"c:\Users\kein-\OneDrive\Desktop\Riqueza Digital\agencia\producto\notion-audit"
output_file = os.path.join(output_dir, "01-inventario.md")

if not os.path.exists(dump_path):
    print(f"Error: Dump file {dump_path} does not exist.")
    sys.exit(1)

with open(dump_path, "r", encoding="utf-8") as f:
    items = json.load(f)

items_by_id = {item["id"]: item for item in items}

# Helper to resolve titles
def get_title(item):
    obj_type = item.get("object")
    if obj_type == "database":
        title_list = item.get("title", [])
        if title_list:
            return title_list[0].get("plain_text", "Sin título (Base de datos)")
        return "Sin título (Base de datos)"
    elif obj_type == "page":
        properties = item.get("properties", {})
        for prop_name, prop_val in properties.items():
            if isinstance(prop_val, dict) and prop_val.get("type") == "title":
                title_list = prop_val.get("title", [])
                if title_list:
                    return title_list[0].get("plain_text", "Sin título")
        return "Sin título"
    return "Objeto Desconocido"

# Reference date for time classification: 2026-05-28
ref_date = datetime(2026, 5, 28)

def get_status(item):
    if item.get("archived", False):
        return "Obsoleto (Archivado)"
    
    last_edited_str = item.get("last_edited_time")
    if not last_edited_str:
        return "Indefinido"
        
    try:
        # Notion timestamps are e.g. "2026-05-26T18:10:00.000Z"
        # Parse first 10 chars "YYYY-MM-DD"
        edited_date = datetime.strptime(last_edited_str[:10], "%Y-%m-%d")
        delta_days = (ref_date - edited_date).days
        
        if delta_days <= 30:
            return "Activo"
        elif delta_days <= 180:
            return "Dormido"
        else:
            return "Obsoleto"
    except Exception:
        return "Dormido"

# Build children mapping
children_map = {}
for item in items:
    parent_info = item.get("parent", {})
    parent_type = parent_info.get("type")
    
    parent_id = None
    if parent_type == "page_id":
        parent_id = parent_info.get("page_id")
    elif parent_type == "database_id":
        parent_id = parent_info.get("database_id")
    elif parent_type == "block_id":
        parent_id = parent_info.get("block_id")
        
    if parent_id:
        children_map.setdefault(parent_id, []).append(item["id"])

# We only include "Riqueza Digital" related items.
# Roots to include:
# 1. RIQUEZA DIGITAL (9a5bbf82-b0a5-4000-b87d-d213a5e370d7)
# 2. CEO (0e8d8db6-455f-424d-ac26-3ab7f31f5507)
# 3. RD - Tu departamento (2e7d2fec-4b82-8030-aba2-dcaa7dcfb88b)
# And any other items in the workspace that are under these roots, 
# OR contain "Riqueza Digital" / "RD" / "Contenido RD" / "Horas trabajadas" in their titles,
# but EXCLUDING client-specific root "PROYECTOS CLIENTES" and the "Tareas" database (as requested by user).

rd_roots = {
    "9a5bbf82-b0a5-4000-b87d-d213a5e370d7", # RIQUEZA DIGITAL
    "0e8d8db6-455f-424d-ac26-3ab7f31f5507", # CEO
    "2e7d2fec-4b82-8030-aba2-dcaa7dcfb88b"  # RD - Tu departamento
}

# Recursively find all descendants of these roots
rd_descendants = set()
def gather_descendants(node_id):
    if node_id in rd_descendants:
        return
    rd_descendants.add(node_id)
    for child_id in children_map.get(node_id, []):
        gather_descendants(child_id)

for root in rd_roots:
    if root in items_by_id:
        gather_descendants(root)

# Let's also find standalone pages/DBs matching "Riqueza Digital", "RD", "Contenido RD" etc.
# which might be parented by blocks not in the list, but are clearly ours.
# But make sure to EXCLUDE client-related nodes and Tareas DB.
exclude_keywords = ["proyecto", "cliente", "presupuesto", "tareas"]
exclude_ids = {
    "249d2fec-4b82-80f9-bf37-cf738ad590cf", # PROYECTOS CLIENTES root
    "b5c6d3aa-d462-4989-962e-8fc7034de3a9"  # Tareas DB
}

# Recursively gather descendants of PROYECTOS CLIENTES and Tareas to block them
blacklisted_ids = set()
def gather_blacklist(node_id):
    if node_id in blacklisted_ids:
        return
    blacklisted_ids.add(node_id)
    for child_id in children_map.get(node_id, []):
        gather_blacklist(child_id)

for ex_id in exclude_ids:
    gather_blacklist(ex_id)

matched_items_set = set(rd_descendants)

for item in items:
    item_id = item["id"]
    if item_id in blacklisted_ids:
        continue
        
    title = get_title(item).lower()
    # If the title explicitly contains agency names, include it and its subtree
    if ("riqueza digital" in title or "rd" in title or "contenido rd" in title or "horas trabajadas" in title) and not any(ek in title for ek in exclude_keywords):
        gather_descendants(item_id)

# Filter items we want to audit
audit_items = [items_by_id[item_id] for item_id in rd_descendants if item_id in items_by_id and item_id not in blacklisted_ids]

# Let's build the tree only for the audited items
audit_ids = {item["id"] for item in audit_items}

# Separate by type
databases = [item for item in audit_items if item.get("object") == "database"]
pages = [item for item in audit_items if item.get("object") == "page"]

# Classify stats
stats = {"Activo": 0, "Dormido": 0, "Obsoleto": 0, "Obsoleto (Archivado)": 0}
for item in audit_items:
    st = get_status(item)
    stats[st] = stats.get(st, 0) + 1

# Generate tree representation helper
def render_tree_markdown(node_id, depth=0, visited=None):
    if visited is None:
        visited = set()
    if node_id in visited or node_id not in audit_ids:
        return ""
    visited.add(node_id)
    
    item = items_by_id[node_id]
    title = get_title(item)
    obj_type = "BD" if item.get("object") == "database" else "Pág"
    status = get_status(item)
    url = item.get("url", "#")
    
    status_emoji = "🟢" if status == "Activo" else "🟡" if status == "Dormido" else "🔴"
    indent = "  " * depth
    line = f"{indent}- {status_emoji} **[{obj_type}]** [{title}]({url}) `({status})`\n"
    
    # Sort children to maintain a clean order
    child_ids = children_map.get(node_id, [])
    child_ids = [c for c in child_ids if c in audit_ids]
    
    children_lines = ""
    for c_id in sorted(child_ids, key=lambda x: get_title(items_by_id[x])):
        children_lines += render_tree_markdown(c_id, depth + 1, visited)
        
    return line + children_lines

# Build output markdown
md = []
md.append("# Auditoría de Notion — Fase A: Inventario y Mapeo del Workspace")
md.append(f"**Fecha del Reporte:** {ref_date.strftime('%Y-%m-%d')}  ")
md.append("**Ámbito:** Riqueza Digital (Excluyendo Proyectos de Clientes y Base de Datos de Tareas Personales/Mixtas)  ")
md.append("**Estado General:** 🌱 PoC / Piloto de Auditoría de Workspace (F-010)")
md.append("\n---")
md.append("\n## 1. Resumen Ejecutivo")
md.append(f"- **Total de elementos auditados:** {len(audit_items)}")
md.append(f"  - **Páginas:** {len(pages)}")
md.append(f"  - **Bases de datos:** {len(databases)}")
md.append("\n### Distribución por Estado Sugerido:")
md.append(f"- 🟢 **Activo** (Modificado < 30 días): {stats.get('Activo', 0)}")
md.append(f"- 🟡 **Dormido** (Modificado 30-180 días): {stats.get('Dormido', 0)}")
md.append(f"- 🔴 **Obsoleto** (Modificado > 180 días o Archivado): {stats.get('Obsoleto', 0) + stats.get('Obsoleto (Archivado)', 0)}")

md.append("\n---")
md.append("\n## 2. Vista de Árbol Jerárquico")
md.append("Representación jerárquica de los elementos de Riqueza Digital compartidos con el bot:")

visited = set()
for root_id in sorted(rd_roots):
    if root_id in audit_ids:
        md.append(render_tree_markdown(root_id, 0, visited))

# Also add any audited items that were not visited (orphans relative to roots but match keywords)
orphans = audit_ids - visited
if orphans:
    md.append("\n### Elementos Independientes / Otros:")
    for o_id in sorted(orphans):
        # Only print if it's a top-level in this group
        parent_info = items_by_id[o_id].get("parent", {})
        p_type = parent_info.get("type")
        p_id = parent_info.get(p_type)
        if p_id not in audit_ids:
            md.append(render_tree_markdown(o_id, 0, visited))

md.append("\n---")
md.append("\n## 3. Inventario Completo")
md.append("| Nombre | Tipo | Estado Sugerido | Última Modificación | Enlace |")
md.append("|---|---|---|---|---|")

sorted_items = sorted(audit_items, key=lambda x: get_title(x))
for item in sorted_items:
    title = get_title(item)
    obj_type = "Base de datos" if item.get("object") == "database" else "Página"
    status = get_status(item)
    last_edited = item.get("last_edited_time")[:10] if item.get("last_edited_time") else "Desconocido"
    url = item.get("url", "")
    md.append(f"| {title} | {obj_type} | {status} | {last_edited} | [Abrir en Notion]({url}) |")

md.append("\n---")
md.append("\n## 4. Análisis de Áreas Temáticas Detectadas")
md.append("A partir del mapeo, se identifican las siguientes áreas de la organización:")
md.append("1. **Eventos y Relaciones Públicas:** Centrado en la base de datos `Eventos 2026` con 61 eventos de tecnología y ferias industriales.")
md.append("2. **Administración y CEO:** Espacios de toma de decisiones representados por la página raíz `CEO` y sus hojas de ruta asociadas.")
md.append("3. **Contenido y Posicionamiento:** Hojas de ruta de marketing digital e ideas de contenido para la propia agencia.")

os.makedirs(output_dir, exist_ok=True)
with open(output_file, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Report successfully generated at: {output_file}")
