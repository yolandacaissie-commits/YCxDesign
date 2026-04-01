#!/usr/bin/env python3
"""Chunk 1: rename kanban→board everywhere, add views/visibleColumns to projects."""
with open('/home/user/YCxDesign/team-nexus-v3.html', 'r') as f:
    html = f.read()

original_len = len(html)

# ── 1. CSS rename ──
html = html.replace('#view-kanban{', '#view-board{', 1)
html = html.replace('#view-kanban ', '#view-board ', 1)
html = html.replace('.kanban-board{', '.board-layout{', 1)

# ── 2. HTML rename ──
html = html.replace(
    '<div id="view-kanban" style="display:none"><div class="kanban-board" id="kanban-board"></div></div>',
    '<div id="view-board"  style="display:none"><div class="board-layout"  id="board-layout"></div></div>',
    1
)

# ── 3. showView list ──
html = html.replace(
    "['welcome','home','projects','workspace','kanban','table','gantt','settings','forms','timesheet','stub','financial']",
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial']",
    1
)

# ── 4. openProject: default to table view (not board) ──
html = html.replace(
    "curProjectId=id;curView='kanban';",
    "curProjectId=id;curView='table';",
    1
)
html = html.replace(
    "showView('kanban');renderKanban();closeDetail();closeColPanel();",
    "showView('table');renderTable();closeDetail();closeColPanel();",
    1
)

# ── 5. switchView: kanban→board ──
html = html.replace(
    "if(v==='kanban')renderKanban();",
    "if(v==='board')renderBoard();",
    1
)

# ── 6. All curView==='kanban' comparisons ──
html = html.replace("curView==='kanban'", "curView==='board'")

# ── 7. renderKanban → renderBoard, kanban-board → board-layout ──
html = html.replace('function renderKanban()', 'function renderBoard()', 1)
html = html.replace("document.getElementById('kanban-board')", "document.getElementById('board-layout')", 1)
html = html.replace('renderKanban()', 'renderBoard()')  # all remaining calls

# ── 8. viewTabsHTML: rename kanban label + id ──
html = html.replace(
    "['kanban',`<svg viewBox=\"0 0 24 24\" style=\"width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px;margin-right:4px\"><rect x=\"3\" y=\"3\" width=\"5\" height=\"18\" rx=\"1\"/><rect x=\"11\" y=\"3\" width=\"5\" height=\"12\" rx=\"1\"/><rect x=\"19\" y=\"3\" width=\"3\" height=\"7\" rx=\"1\"/></svg>Kanban`]",
    "['board',`<svg viewBox=\"0 0 24 24\" style=\"width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px;margin-right:4px\"><rect x=\"3\" y=\"3\" width=\"5\" height=\"18\" rx=\"1\"/><rect x=\"11\" y=\"3\" width=\"5\" height=\"12\" rx=\"1\"/><rect x=\"19\" y=\"3\" width=\"3\" height=\"7\" rx=\"1\"/></svg>Board`]",
    1
)

# ── 9. Add views[] and visibleColumns[] to each project in PROJECTS ──
# Insert after each project's color field — find common pattern and inject.
# Strategy: add views/visibleColumns right after the emoji field in each project header.
# All projects start with: {id:'pN',name:'...',desc:'...',status:'...',priority:'...',emoji:'...',color:'...',
# We add views and visibleColumns after color.

import re

# Match project opening objects (the top-level ones with locations:[])
# We'll inject views + visibleColumns right before `locations:[`
def inject_project_fields(m):
    return m.group(0).replace(
        'locations:[',
        "views:['table'],visibleColumns:['pred','duration','startDate','dueDate','status','assignee'],sortField:'startDate',sortDir:'asc',filterRules:[],groupBy:null,locations:[",
        1
    )

# Find each project object that has a `locations:[` key and inject the new fields
html = re.sub(
    r'\{id:\'p\d+\'.*?locations:\[',
    inject_project_fields,
    html,
    flags=re.DOTALL
)

with open('/home/user/YCxDesign/team-nexus-v3.html', 'w') as f:
    f.write(html)

print(f"Chunk 1 done. Size: {original_len} → {len(html)}")
