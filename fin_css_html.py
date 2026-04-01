#!/usr/bin/env python3
with open('/home/user/YCxDesign/team-nexus-v3.html','r') as f:
    html = f.read()

# 1. Add view-financial div after view-settings
old_div = '<div id="view-settings" style="display:none"></div>'
new_div = '<div id="view-settings" style="display:none"></div>\n    <div id="view-financial" style="display:none;position:absolute;inset:0;overflow-y:auto;padding:24px"></div>'
assert old_div in html, "view-settings div not found"
html = html.replace(old_div, new_div, 1)

# 2. Add financial dashboard CSS before </style>
fin_css = """
/* ── FINANCIAL DASHBOARD ── */
.fin-page{max-width:1080px;margin:0 auto}
.fin-section{margin-bottom:28px}
.fin-section-title{font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.8px;margin-bottom:12px;display:flex;align-items:center;gap:6px}
.fin-table{width:100%;border-collapse:collapse;font-size:12.5px}
.fin-table th{text-align:left;padding:8px 12px;font-weight:600;font-size:11px;color:var(--text3);text-transform:uppercase;letter-spacing:.4px;border-bottom:2px solid var(--border2);white-space:nowrap}
.fin-table td{padding:9px 12px;border-bottom:1px solid var(--border);vertical-align:middle}
.fin-table tr:last-child td{border-bottom:none}
.fin-table tbody tr:hover td{background:var(--surface2)}
.fin-util-bar{height:6px;background:var(--border2);border-radius:3px;overflow:hidden;min-width:80px;margin-top:4px}
.fin-util-fill{height:100%;border-radius:3px}
.fin-badge{display:inline-block;padding:2px 7px;border-radius:8px;font-size:10px;font-weight:600;letter-spacing:.2px}
.fin-lob-tag{display:inline-block;padding:2px 7px;border-radius:8px;font-size:10px;font-weight:600;margin:1px 2px}
.fin-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:28px}
.fin-chart-box{background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:16px}
.fin-chart-title{font-size:12px;font-weight:700;color:var(--text2);margin-bottom:14px}
.fin-lob-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.fin-stat-row{display:flex;gap:12px;margin-bottom:20px;flex-wrap:wrap}
.fin-stat{background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:14px 18px;flex:1;min-width:140px}
.fin-stat-val{font-size:22px;font-weight:700;color:var(--text);line-height:1.1;margin-bottom:2px}
.fin-stat-lbl{font-size:11px;color:var(--text3);font-weight:500}
.fin-legend{display:flex;gap:14px;margin-bottom:10px;flex-wrap:wrap}
.fin-legend-item{display:flex;align-items:center;gap:5px;font-size:11px;color:var(--text2)}
.fin-legend-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
@media(max-width:700px){.fin-grid,.fin-lob-grid{grid-template-columns:1fr}}
"""
old_style_end = "</style>"
assert old_style_end in html, "</style> not found"
html = html.replace(old_style_end, fin_css + "</style>", 1)

with open('/home/user/YCxDesign/team-nexus-v3.html','w') as f:
    f.write(html)

print("Chunk 2 done — HTML div + CSS added")
