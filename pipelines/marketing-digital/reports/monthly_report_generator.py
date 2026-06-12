#!/usr/bin/env python3
"""
Monthly Report Generator — Riqueza Digital Agency Skill
Genera informes mensuales premium en formato HTML listos para imprimir a PDF.
Lee configuraciones de branding y métricas desde el directorio del cliente.

Uso:
    python monthly_report_generator.py --client veganashi --month "2026-05"
"""

import os
import sys
import argparse
import json
from pathlib import Path

# Configurar rutas relativas al Workspace
WORKSPACE_ROOT = Path(__file__).resolve().parents[3]

def parse_args():
    parser = argparse.ArgumentParser(description="Generador de Informes Mensuales RD")
    parser.add_argument("--client", required=True, help="Slug del cliente (ej. veganashi)")
    parser.add_argument("--month", required=True, help="Año y mes del reporte (formato YYYY-MM, ej. 2026-05)")
    return parser.parse_args()

def load_json_file(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def format_currency(val):
    if val is None:
        return "—"
    return f"€{val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def format_number(val):
    if val is None:
        return "—"
    return f"{val:,}".replace(",", ".")

def format_pct(val):
    if val is None:
        return "—"
    return f"{val:.2f}%".replace(".", ",")

def main():
    args = parse_args()
    client = args.client.lower()
    month_slug = args.month
    
    # 1. Rutas de archivos
    client_dir = WORKSPACE_ROOT / "clients" / client
    config_path = client_dir / "report_config.json"
    metrics_path = client_dir / "intelligence" / f"monthly_metrics_{month_slug}.json"
    
    if not client_dir.exists():
        print(f"[ERROR] El directorio del cliente no existe: {client_dir}")
        sys.exit(1)
        
    # 2. Cargar configuraciones
    config = load_json_file(config_path)
    metrics = load_json_file(metrics_path)
    
    if not config:
        print(f"[WARN] No se encontró report_config.json. Usando branding por defecto.")
        config = {
          "client_name": client.capitalize(),
          "logo": f"💼 {client.capitalize()}",
          "tagline": "Servicios de Marketing Digital",
          "colors": {
            "primary": "#3498db",
            "secondary": "#9b59b6",
            "accent": "#e74c3c",
            "dark": "#2c3e50",
            "bg_light": "#ecf0f1",
            "border": "#bdc3c7"
          }
        }
        
    if not metrics:
        print(f"[ERROR] No se encontraron métricas para el mes {month_slug} en {metrics_path}")
        sys.exit(1)
        
    # Normalizar mes en texto
    months_es = {
        "01": "Enero", "02": "Febrero", "03": "Marzo", "04": "Abril", "05": "Mayo", "06": "Junio",
        "07": "Julio", "08": "Agosto", "09": "Septiembre", "10": "Octubre", "11": "Noviembre", "12": "Diciembre"
    }
    parts = month_slug.split("-")
    month_name = f"{months_es.get(parts[1], parts[1])} {parts[0]}" if len(parts) == 2 else month_slug
    
    # 3. Extraer métricas consolidadas
    meta = metrics.get("meta_ads", {})
    google = metrics.get("google_ads", {})
    
    meta_totals = meta.get("totals", {})
    google_totals = google.get("totals", {})
    
    total_spend = meta_totals.get("spend", 0) + google_totals.get("spend", 0)
    total_leads = meta_totals.get("leads", 0) + google_totals.get("leads", 0)
    avg_cpl = total_spend / total_leads if total_leads > 0 else 0
    
    # Calcular clics e impresiones globales para CTR medio
    total_clicks = meta_totals.get("clicks", 0) + google_totals.get("clicks", 0)
    total_impr = meta_totals.get("impressions", 0) + google_totals.get("impressions", 0)
    global_ctr = (total_clicks / total_impr) * 100 if total_impr > 0 else 0
    
    # Colores de marca
    colors = config.get("colors", {})
    p_color = colors.get("primary", "#2E7D52")
    s_color = colors.get("secondary", "#A8D5B5")
    a_color = colors.get("accent", "#F4A828")
    d_color = colors.get("dark", "#1A3C2A")
    bg_light = colors.get("bg_light", "#F7FAF8")
    border_color = colors.get("border", "#DDE8E2")

    # 4. Construir las filas de campañas de Meta Ads
    meta_rows_html = ""
    for camp in meta.get("campaigns", []):
        meta_rows_html += f"""
        <tr>
          <td>
            <span class="status-dot green"></span>
            <span class="campaign-name">{camp['name']}</span>
          </td>
          <td class="num">{format_currency(camp['spend'])}</td>
          <td class="num">{format_number(camp['impressions'])}</td>
          <td class="num">{format_pct(camp['ctr'])}</td>
          <td class="num">{format_currency(camp['cpc'])}</td>
          <td class="num"><strong>{camp['leads']}</strong></td>
          <td class="num" style="font-weight: 600; color: {'var(--positive)' if camp['cpl'] < 25 else 'var(--neutral)' if camp['cpl'] < 50 else 'var(--negative)'}">{format_currency(camp['cpl'])}</td>
        </tr>
        """

    # 5. Escribir plantilla HTML
    html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Informe Mensual — {config['client_name']} ({month_name})</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    /* === VARIABLES DE DISEÑO DINÁMICAS === */
    :root {{
      --brand-primary:   {p_color};
      --brand-secondary: {s_color};
      --brand-accent:    {a_color};
      --brand-dark:      {d_color};
      --text-main:       #1F2D27;
      --text-muted:      #6B7C74;
      --bg-light:        {bg_light};
      --bg-white:        #FFFFFF;
      --border:          {border_color};
      --positive:        #2E7D52;
      --negative:        #C0392B;
      --neutral:         #E67E22;
    }}

    * {{ box-sizing: border-box; margin: 0; padding: 0; }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      background: #EAEAEA;
      color: var(--text-main);
      line-height: 1.6;
      padding: 40px 0;
    }}

    /* === CONTENEDOR PRINCIPAL (A4/Print-ready) === */
    .wrapper {{
      max-width: 820px;
      margin: 0 auto;
      background: var(--bg-white);
      box-shadow: 0 8px 30px rgba(0,0,0,0.08);
      border-radius: 4px;
      overflow: hidden;
    }}

    /* === PORTADA === */
    .cover-page {{
      height: 100%;
      min-height: 1060px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 80px 70px;
      position: relative;
    }}
    .cover-page::after {{
      content: '';
      position: absolute;
      bottom: -100px; right: -100px;
      width: 400px; height: 400px;
      border-radius: 50%;
      background: rgba(168,213,181,0.08);
      z-index: 1;
    }}
    .cover-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--border);
      padding-bottom: 30px;
    }}
    .logo-area {{ display: flex; flex-direction: column; gap: 4px; }}
    .logo-name {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 32px;
      font-weight: 700;
      color: var(--brand-dark);
      letter-spacing: -0.5px;
    }}
    .logo-tagline {{
      font-size: 11px;
      color: var(--text-muted);
      letter-spacing: 2px;
      text-transform: uppercase;
    }}
    .badge-period {{
      background: var(--brand-primary);
      color: #fff;
      font-size: 11px;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 20px;
      letter-spacing: 1px;
      text-transform: uppercase;
    }}
    .cover-body {{
      margin: auto 0;
      z-index: 2;
    }}
    .cover-title-pre {{
      font-size: 13px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 4px;
      color: var(--brand-primary);
      margin-bottom: 15px;
    }}
    .cover-title {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 54px;
      font-weight: 300;
      line-height: 1.1;
      color: var(--brand-dark);
      margin-bottom: 25px;
    }}
    .cover-desc {{
      font-size: 15.5px;
      color: var(--text-muted);
      max-width: 520px;
    }}
    .cover-footer {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-top: 1px solid var(--border);
      padding-top: 30px;
      font-size: 12.5px;
    }}
    .agency-sig strong {{
      font-size: 15px;
      color: var(--brand-dark);
      display: block;
      margin-bottom: 4px;
    }}

    /* === CONTENIDO GENERAL === */
    .page-content {{
      padding: 60px 70px;
      border-top: 8px solid var(--brand-dark);
    }}
    
    .section {{
      margin-bottom: 45px;
    }}
    .section:last-child {{ margin-bottom: 0; }}
    
    .section-title {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 24px;
      font-weight: 600;
      color: var(--brand-dark);
      margin-bottom: 20px;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
    }}
    .section-title span {{
      font-size: 10px;
      font-family: 'Inter', sans-serif;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      color: var(--text-muted);
    }}

    /* === RESUMEN EJECUTIVO === */
    .exec-summary {{
      background: var(--bg-light);
      border-left: 4px solid var(--brand-primary);
      border-radius: 0 8px 8px 0;
      padding: 24px 28px;
    }}
    .bullet-list {{ list-style: none; display: flex; flex-direction: column; gap: 12px; }}
    .bullet-list li {{
      display: flex;
      gap: 12px;
      font-size: 14px;
      color: var(--text-main);
      line-height: 1.55;
    }}
    .bullet-list li::before {{
      content: '▸';
      color: var(--brand-primary);
      font-size: 14px;
      flex-shrink: 0;
      margin-top: 1px;
    }}

    /* === KPI GRID === */
    .kpi-grid {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 12px;
      margin-bottom: 25px;
    }}
    .kpi-card {{
      background: var(--bg-light);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 16px 14px;
      text-align: center;
    }}
    .kpi-card.highlight {{
      background: var(--brand-dark);
      border-color: var(--brand-dark);
    }}
    .kpi-label {{
      font-size: 9.5px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1.2px;
      color: var(--text-muted);
      margin-bottom: 8px;
    }}
    .kpi-card.highlight .kpi-label {{ color: var(--brand-secondary); }}
    .kpi-value {{
      font-size: 22px;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.1;
      margin-bottom: 4px;
    }}
    .kpi-card.highlight .kpi-value {{ color: #FFFFFF; }}
    .kpi-sub {{
      font-size: 10px;
      color: var(--text-muted);
    }}
    .kpi-card.highlight .kpi-sub {{ color: rgba(255,255,255,0.65); }}

    /* === TABLAS DE DATOS === */
    .table-container {{
      width: 100%;
      overflow-x: auto;
      margin-bottom: 15px;
    }}
    .data-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 13px;
    }}
    .data-table thead th {{
      background: var(--brand-dark);
      color: #FFFFFF;
      font-size: 9.5px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 10px 14px;
      text-align: left;
    }}
    .data-table thead th.num {{ text-align: right; }}
    .data-table tbody tr {{
      border-bottom: 1px solid var(--border);
    }}
    .data-table tbody tr:hover {{
      background: var(--bg-light);
    }}
    .data-table td {{
      padding: 12px 14px;
      color: var(--text-main);
    }}
    .data-table td.num {{
      text-align: right;
      font-variant-numeric: tabular-nums;
    }}
    .status-dot {{
      display: inline-block;
      width: 7px; height: 7px;
      border-radius: 50%;
      margin-right: 8px;
    }}
    .status-dot.green  {{ background: var(--positive); }}
    .status-dot.yellow {{ background: var(--neutral); }}
    .status-dot.red    {{ background: var(--negative); }}
    .campaign-name {{ font-weight: 500; }}

    /* === NOTAS Y ALERTAS === */
    .info-box {{
      background: #EDF4F8;
      border: 1px solid #B8D4E8;
      border-radius: 8px;
      padding: 14px 18px;
      font-size: 12.5px;
      color: #2C5F7A;
      display: flex;
      gap: 12px;
      align-items: flex-start;
      margin-top: 15px;
    }}
    .info-box-icon {{ font-size: 15px; margin-top: 1px; }}

    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 25px;
    }}

    /* === SANEAMIENTO TÉCNICO === */
    .audit-card {{
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
    }}
    .audit-card-title {{
      font-size: 13.5px;
      font-weight: 600;
      color: var(--brand-dark);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
    }}
    .audit-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }}
    .audit-list li {{
      font-size: 12.5px;
      padding-left: 18px;
      position: relative;
    }}
    .audit-list li::before {{
      content: '•';
      position: absolute;
      left: 4px;
      font-weight: bold;
    }}
    .audit-list li.fixed {{ color: var(--positive); }}
    .audit-list li.fixed::before {{ content: '✓'; color: var(--positive); left: 0; }}
    .audit-list li.error {{ color: var(--negative); }}
    .audit-list li.error::before {{ content: '✗'; color: var(--negative); left: 2px; }}
    .audit-list li.warn {{ color: var(--neutral); }}
    .audit-list li.warn::before {{ content: '⚠️'; left: -2px; font-size: 10px; top: 1px; }}

    /* === MATRIZ DE DECISIONES === */
    .matrix-table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 12.5px;
      margin-top: 10px;
    }}
    .matrix-table th {{
      background: var(--bg-light);
      color: var(--brand-dark);
      font-size: 9.5px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 8px 12px;
      text-align: left;
      border-bottom: 2px solid var(--border);
    }}
    .matrix-table td {{
      padding: 10px 12px;
      border-bottom: 1px solid var(--border);
    }}
    .priority-badge {{
      display: inline-block;
      font-size: 9px;
      font-weight: 700;
      text-transform: uppercase;
      padding: 2px 6px;
      border-radius: 4px;
    }}
    .priority-badge.high {{ background: #FDECEA; color: var(--negative); }}
    .priority-badge.med  {{ background: #FEF3E2; color: var(--neutral); }}
    .priority-badge.low  {{ background: #E8F5EE; color: var(--positive); }}

    /* === FOOTER DE PÁGINA === */
    .page-footer {{
      margin-top: 50px;
      border-top: 1px solid var(--border);
      padding-top: 15px;
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-muted);
    }}

    /* === ESTILOS DE IMPRESIÓN === */
    @media print {{
      body {{
        background: #FFFFFF;
        padding: 0;
      }}
      .wrapper {{
        max-width: 100%;
        box-shadow: none;
        border-radius: 0;
      }}
      .page-break {{
        page-break-before: always;
      }}
      .cover-page {{
        height: 100vh;
        page-break-after: always;
      }}
    }}
  </style>
</head>
<body>

<div class="wrapper">

  <!-- ================= PORTADA ================= -->
  <div class="cover-page">
    <div class="cover-header">
      <div class="logo-area">
        <span class="logo-name">{config['logo']}</span>
        <span class="logo-tagline">{config['tagline']}</span>
      </div>
      <span class="badge-period">Informe Mensual</span>
    </div>
    
    <div class="cover-body">
      <div class="cover-title-pre">Rendimiento &amp; Saneamiento</div>
      <h1 class="cover-title">Informe Estratégico<br>de Marketing Digital</h1>
      <p class="cover-desc">
        Resultados y análisis de las campañas de publicidad en Meta Ads correspondientes a {month_name}, auditoría de optimización técnica de la web y plan estratégico de lanzamiento en Google Ads.
      </p>
    </div>
    
    <div class="cover-footer">
      <div class="agency-sig">
        <strong>Riqueza Digital</strong>
        Agencia de Crecimiento &amp; Transformación
      </div>
      <div style="text-align: right; color: var(--text-muted);">
        Generado automáticamente via Pipeline RD<br>
        Fecha: 4 de Junio, 2026 · Privado / Cliente
      </div>
    </div>
  </div>

  <!-- ================= PÁGINA 1: RENDIMIENTO PUBLICITARIO ================= -->
  <div class="page-content page-break">
    
    <!-- RESUMEN EJECUTIVO -->
    <div class="section">
      <h2 class="section-title">Resumen Ejecutivo — {month_name} <span>Resumen</span></h2>
      <div class="exec-summary">
        <ul class="bullet-list">
          <li><strong>Medición Saneada:</strong> Hemos resuelto el multi-conteo analítico al desactivar los plugins duplicados de Meta. Las métricas actuales de Mayo son el primer punto de partida 100% fiable para tomar decisiones.</li>
          <li><strong>Retorno Meta Ads:</strong> Se han invertido <strong>{format_currency(total_spend)}</strong> en Meta Ads obteniendo <strong>{total_leads} leads de reserva</strong> a un CPL real consolidado de <strong>{format_currency(avg_cpl)}</strong>.</li>
          <li><strong>Oportunidad CTR:</strong> La campaña de Tráfico registró una tasa de clic excepcional del <strong>7,10% (CPC €0,03)</strong>. Sin embargo, no convirtió a reservas debido a la falta de optimización hacia eventos en destino. Proponemos redirigir este flujo hacia Conversión.</li>
          <li><strong>Estructuración Google Ads:</strong> La cuenta se encuentra conectada en baseline. Proponemos activar campañas de Búsqueda enfocadas a palabras de alta intención para captar leads entre semana.</li>
        </ul>
      </div>
    </div>

    <!-- RENDIMIENTO GLOBAL -->
    <div class="section">
      <h2 class="section-title">KPIs Globales Consolidados <span>Métricas generales</span></h2>
      <div class="kpi-grid">
        <div class="kpi-card highlight">
          <div class="kpi-label">Inversión Total</div>
          <div class="kpi-value">{format_currency(total_spend)}</div>
          <div class="kpi-sub">Mayo 2026</div>
        </div>
        <div class="kpi-card highlight">
          <div class="kpi-label">Leads Totales</div>
          <div class="kpi-value">{total_leads}</div>
          <div class="kpi-sub">Reservas Medidas</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">CPL Medio</div>
          <div class="kpi-value">{format_currency(avg_cpl)}</div>
          <div class="kpi-sub">Coste por Reserva</div>
        </div>
        <div class="kpi-card">
          <div class="kpi-label">CTR Medio</div>
          <div class="kpi-value">{global_ctr:.2f}%</div>
          <div class="kpi-sub">Benchmark: 1,4%</div>
        </div>
      </div>
    </div>

    <!-- DETALLE META ADS -->
    <div class="section">
      <h2 class="section-title">Rendimiento Detallado de Campañas — Meta Ads <span>Métricas de Canales</span></h2>
      <div class="table-container">
        <table class="data-table">
          <thead>
            <tr>
              <th>Campaña</th>
              <th class="num">Inversión</th>
              <th class="num">Impresiones</th>
              <th class="num">CTR</th>
              <th class="num">CPC</th>
              <th class="num">Leads</th>
              <th class="num">CPL Real</th>
            </tr>
          </thead>
          <tbody>
            {meta_rows_html}
          </tbody>
        </table>
      </div>
      
      <div class="info-box">
        <span class="info-box-icon">💡</span>
        <div>
          <strong>Análisis Crítico de la Campaña de Tráfico (T - Reservas):</strong>
          A pesar de obtener un <strong>CTR histórico de 7,10%</strong> (3.060 clics en el segmento sushi/veganismo con CPC de solo €0,03), solo se obtuvo 1 lead debido a que Meta optimiza por clics en el enlace y no por leads. La web perdió el 75% del tráfico antes de cargar (clics vs visitas). Es urgente migrar este presupuesto a Conversiones.
        </div>
      </div>
    </div>

    <!-- PIE DE PÁGINA -->
    <div class="page-footer">
      <span>🌿 Informe de Rendimiento — Veganashi</span>
      <span>Página 1 de 2</span>
    </div>
  </div>

  <!-- ================= PÁGINA 2: ESTRATEGIA TÉCNICA Y ACCIONES ================= -->
  <div class="page-content page-break">
    
    <!-- SANEAMIENTO Y AUDITORÍA -->
    <div class="section">
      <h2 class="section-title">Diagnóstico Técnico y Saneamiento Realizado <span>Auditoría</span></h2>
      <div class="grid-2">
        <div class="audit-card">
          <div class="audit-card-title">
            <span>⚙️</span> Analítica &amp; Tracking
          </div>
          <ul class="audit-list">
            <li class="fixed">Desactivación de <em>facebook-for-woocommerce</em> (eliminado duplicados de add_to_cart).</li>
            <li class="fixed">Desactivación de <em>official-facebook-pixel</em> (eliminada inyección duplicada de PageViews).</li>
            <li class="fixed">Centralización del tracking 100% en Google Tag Manager (GTM-WMDJQKLF).</li>
            <li class="fixed">Creación de la landing page <code>/reserva-realizada/</code> en WordPress para CoverManager.</li>
          </ul>
        </div>
        
        <div class="audit-card">
          <div class="audit-card-title">
            <span>🔍</span> SEO On-Page &amp; WPO
          </div>
          <ul class="audit-list">
            <li class="fixed">Inyección de títulos y meta-descripciones Yoast SEO actualizadas en Home, Reservas y Gracias.</li>
            <li class="error">Home sin encabezado H1 (crítico para SEO y estructura del motor de búsqueda).</li>
            <li class="error">11 de 11 imágenes de la Home no tienen atributo ALT configurado.</li>
            <li class="warn">Falta plugin de caché (ej: WP Rocket / LiteSpeed Cache) para reducir LCP móvil.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- COVERMANAGER INTEGRACIÓN -->
    <div class="section">
      <h2 class="section-title">Guía de Integración con CoverManager <span>Conversiones</span></h2>
      <div class="exec-summary" style="background: #F4FAF7; border-left-color: var(--brand-accent);">
        <p style="font-size: 13.5px; margin-bottom: 12px; font-weight: 600;">Procedimiento de Integración de GTM Directo (Recomendado):</p>
        <p style="font-size: 13px; margin-bottom: 10px; color: var(--text-main);">
          Para evitar pérdidas por redirecciones físicas, debemos pedirle a CoverManager que instale nuestro contenedor de GTM dentro de su widget. Envía el siguiente correo a su soporte técnico:
        </p>
        <div style="background: var(--bg-white); border: 1px solid var(--border); border-radius: 4px; padding: 12px 15px; font-family: monospace; font-size: 11.5px; white-space: pre-wrap; color: #2C3E50;">
Asunto: Solicitud de inyección de GTM - Rest. Veganashi
Para: hospitality@covermanager.com

Hola equipo,
Solicitamos que inyecten nuestro contenedor de Google Tag Manager con ID GTM-WMDJQKLF dentro del motor de reservas de nuestro restaurante (Veganashi). 

Por favor, confirmadnos cuando esté activo para que podamos comprobar la correcta recepción del evento "booking_success" en el dataLayer.

Muchas gracias.
        </div>
      </div>
    </div>

    <!-- MATRIZ DE DECISIONES Y SIGUIENTES PASOS -->
    <div class="section">
      <h2 class="section-title">Matriz de Decisiones Estratégicas <span>Próximos pasos</span></h2>
      <table class="matrix-table">
        <thead>
          <tr>
            <th>Acción Propuesta</th>
            <th>Prioridad</th>
            <th>Impacto Esperado</th>
            <th style="width: 140px;">Decisión Cliente</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Pivotar campaña 'T - Reservas' a Conversión:</strong> Usar el creativo ganador (CTR 7.10%) enfocado a conversiones de leads.</td>
            <td><span class="priority-badge high">Crítica</span></td>
            <td>Reducir el CPL medio de €124 a menos de €20.</td>
            <td>[ ] Aprobado / [ ] Rechazado</td>
          </tr>
          <tr>
            <td><strong>Integrar GTM en CoverManager:</strong> Enviar correo a soporte para medir reservas dentro del iframe.</td>
            <td><span class="priority-badge high">Crítica</span></td>
            <td>Medición exacta sin pérdida de datos en móviles.</td>
            <td>[ ] Aprobado / [ ] Rechazado</td>
          </tr>
          <tr>
            <td><strong>Corregir código HTML Home (H1 y ALTs):</strong> Añadir H1 de sushi vegano y etiquetas en imágenes.</td>
            <td><span class="priority-badge med">Media</span></td>
            <td>Aumentar el tráfico orgánico SEO en Barcelona.</td>
            <td>[ ] Aprobado / [ ] Rechazado</td>
          </tr>
          <tr>
            <td><strong>Activar Google Ads Search (Búsqueda):</strong> Campañas de intención de reserva (€200/mes).</td>
            <td><span class="priority-badge med">Media</span></td>
            <td>Captar mesas de alta intención entre semana.</td>
            <td>[ ] Aprobado / [ ] Rechazado</td>
          </tr>
          <tr>
            <td><strong>Instalar plugin de Caché (WPO):</strong> Optimizar TTFB y tiempos de carga.</td>
            <td><span class="priority-badge low">Baja</span></td>
            <td>Bajar la tasa de rebote móvil de las campañas.</td>
            <td>[ ] Aprobado / [ ] Rechazado</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- PIE DE PÁGINA -->
    <div class="page-footer">
      <span>🌿 Informe de Rendimiento — Veganashi</span>
      <span>Página 2 de 2</span>
    </div>
  </div>

</div>

</body>
</html>
"""
    
    # 6. Escribir archivo de salida
    reports_dir = client_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    output_path = reports_dir / f"{month_slug}_{client}_informe_mensual.html"
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"[OK] Reporte mensual generado con éxito en: {output_path}")

if __name__ == "__main__":
    main()
