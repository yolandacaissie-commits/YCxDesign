#!/usr/bin/env python3
"""Chunk 2a: Add proj-toolbar-bar HTML + CSS; update COLS to include startDate."""
with open('/home/user/YCxDesign/team-nexus-v3.html', 'r') as f:
    html = f.read()

# ── 1. Insert proj-toolbar-bar div inside .content, before view-welcome ──
old_content_start = '  <div class="content">\n    <div id="view-welcome">'
new_content_start = '  <div class="content">\n    <div id="proj-toolbar-bar" class="proj-toolbar-bar" style="display:none"></div>\n    <div id="view-welcome">'
assert old_content_start in html, 'content start anchor not found'
html = html.replace(old_content_start, new_content_start, 1)

# ── 2. Add CSS before </style> ──
proj_tb_css = """
/* ── PROJECT TOOLBAR BAR ── */
.proj-toolbar-bar{display:flex;align-items:center;gap:0;border-bottom:1px solid var(--border2);background:var(--surface);padding:0 16px;min-height:42px;flex-shrink:0;flex-wrap:wrap;position:relative;z-index:5}
.proj-tb-views{display:flex;align-items:center;gap:1px}
.proj-tb-tab{display:flex;align-items:center;gap:5px;padding:0 14px;height:42px;font-size:12.5px;font-weight:500;color:var(--text3);border:none;background:none;cursor:pointer;border-bottom:2px solid transparent;transition:all .15s;white-space:nowrap}
.proj-tb-tab:hover{color:var(--text2);background:var(--surface2)}
.proj-tb-tab.on{color:var(--accent);border-bottom-color:var(--accent);font-weight:600}
.proj-tb-tab svg{opacity:.7}
.proj-tb-tab.on svg{opacity:1}
.proj-tb-add-view{display:flex;align-items:center;gap:4px;padding:4px 10px;height:30px;font-size:12px;font-weight:600;color:var(--text3);border:1px dashed var(--border2);border-radius:6px;background:none;cursor:pointer;margin:0 6px;transition:all .15s}
.proj-tb-add-view:hover{color:var(--accent);border-color:var(--accent);background:var(--abg)}
.proj-tb-sep{width:1px;background:var(--border2);height:20px;margin:0 10px;flex-shrink:0}
.proj-tb-controls{display:flex;align-items:center;gap:2px;flex:1;flex-wrap:wrap}
.proj-tb-btn{display:flex;align-items:center;gap:5px;padding:4px 10px;height:30px;font-size:12px;color:var(--text2);border:1px solid transparent;border-radius:6px;background:none;cursor:pointer;transition:all .15s;white-space:nowrap}
.proj-tb-btn:hover{background:var(--surface2);border-color:var(--border2)}
.proj-tb-btn.active{background:var(--abg);border-color:var(--accent);color:var(--accent)}
.proj-tb-btn svg{width:12px;height:12px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round;flex-shrink:0}
/* floatin menus */
.ptb-menu{position:fixed;background:var(--surface);border:1px solid var(--border2);border-radius:10px;box-shadow:0 8px 24px rgba(0,0,0,.12);z-index:600;min-width:200px;padding:6px}
.ptb-menu-item{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:6px;font-size:12.5px;cursor:pointer;color:var(--text)}
.ptb-menu-item:hover{background:var(--surface2)}
.ptb-menu-item.danger{color:#ef4444}
.ptb-menu-sep{height:1px;background:var(--border2);margin:4px 0}
.ptb-menu-label{font-size:10px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.6px;padding:4px 10px}
/* field panel */
.field-panel{position:fixed;background:var(--surface);border:1px solid var(--border2);border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.14);z-index:600;width:280px;padding:0;overflow:hidden}
.field-panel-head{padding:12px 14px;border-bottom:1px solid var(--border2)}
.field-panel-search{display:flex;align-items:center;gap:7px;background:var(--surface2);border:1px solid var(--border2);border-radius:7px;padding:5px 10px}
.field-panel-search input{flex:1;border:none;background:transparent;font-size:12.5px;color:var(--text);outline:none}
.field-panel-body{max-height:320px;overflow-y:auto;padding:6px}
.field-panel-section{font-size:10px;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:.6px;padding:8px 8px 4px}
.field-row{display:flex;align-items:center;gap:8px;padding:6px 8px;border-radius:6px;cursor:pointer;font-size:12.5px}
.field-row:hover{background:var(--surface2)}
.field-row-name{flex:1;color:var(--text)}
.toggle-sw{width:32px;height:18px;background:var(--border2);border-radius:9px;position:relative;transition:background .2s;flex-shrink:0;cursor:pointer}
.toggle-sw.on{background:var(--accent)}
.toggle-sw::after{content:'';position:absolute;top:2px;left:2px;width:14px;height:14px;border-radius:50%;background:#fff;transition:left .2s;box-shadow:0 1px 3px rgba(0,0,0,.2)}
.toggle-sw.on::after{left:16px}
/* custom field creator */
.cf-creator{position:fixed;background:var(--surface);border:1px solid var(--border2);border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.14);z-index:601;width:240px;padding:16px}
.cf-creator-title{font-size:13px;font-weight:700;color:var(--text);margin-bottom:12px}
.cf-creator input{width:100%;box-sizing:border-box;padding:7px 10px;border:1px solid var(--border2);border-radius:6px;font-size:13px;background:var(--surface2);color:var(--text);outline:none;margin-bottom:12px}
.cf-creator input:focus{border-color:var(--accent)}
.cf-type-label{font-size:11px;font-weight:600;color:var(--text3);margin-bottom:6px}
.cf-type-grid{display:flex;flex-direction:column;gap:2px}
.cf-type-opt{display:flex;align-items:center;gap:8px;padding:6px 8px;border-radius:6px;font-size:12.5px;cursor:pointer;color:var(--text)}
.cf-type-opt:hover{background:var(--surface2)}
.cf-type-opt.sel{background:var(--abg);color:var(--accent);font-weight:600}
.cf-creator-actions{display:flex;gap:8px;margin-top:14px}
.cf-creator-actions button{flex:1;padding:7px;border-radius:6px;font-size:12.5px;font-weight:600;cursor:pointer;border:1px solid var(--border2)}
.cf-creator-actions .cf-save{background:var(--accent);color:#fff;border-color:var(--accent)}
/* filter panel */
.filter-panel{position:fixed;background:var(--surface);border:1px solid var(--border2);border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.14);z-index:600;width:340px;padding:14px}
.filter-rule-row{display:flex;align-items:center;gap:6px;margin-bottom:8px}
.filter-rule-row select,.filter-rule-row input{flex:1;padding:5px 8px;border:1px solid var(--border2);border-radius:6px;font-size:12px;background:var(--surface2);color:var(--text);outline:none}
.filter-rule-row select:focus,.filter-rule-row input:focus{border-color:var(--accent)}
"""
assert '</style>' in html
html = html.replace('</style>', proj_tb_css + '</style>', 1)

# ── 3. Extend COLS to include startDate, reorder ──
old_cols = """let COLS=[
  {key:'title',    label:'Task Name',  type:'builtin', tableVisible:true,  ganttVisible:true},
  {key:'status',   label:'Status',     type:'builtin', tableVisible:true,  ganttVisible:true},
  {key:'priority', label:'Priority',   type:'builtin', tableVisible:true,  ganttVisible:false},
  {key:'assignee', label:'Assignee',   type:'builtin', tableVisible:true,  ganttVisible:true},
  {key:'duration', label:'Duration',   type:'builtin', tableVisible:true,  ganttVisible:false},
  {key:'dueDate',  label:'Due Date',   type:'builtin', tableVisible:true,  ganttVisible:false},
  {key:'pred',     label:'Predecessor',type:'builtin', tableVisible:false, ganttVisible:false},
];"""
new_cols = """let COLS=[
  {key:'title',    label:'Task Name',   type:'builtin', tableVisible:true,  ganttVisible:true},
  {key:'pred',     label:'Predecessors',type:'builtin', tableVisible:true,  ganttVisible:false},
  {key:'duration', label:'Duration',    type:'builtin', tableVisible:true,  ganttVisible:false},
  {key:'startDate',label:'Start date',  type:'builtin', tableVisible:true,  ganttVisible:false},
  {key:'dueDate',  label:'Due date',    type:'builtin', tableVisible:true,  ganttVisible:false},
  {key:'status',   label:'Status',      type:'builtin', tableVisible:true,  ganttVisible:true},
  {key:'priority', label:'Priority',    type:'builtin', tableVisible:false, ganttVisible:false},
  {key:'assignee', label:'Assignee',    type:'builtin', tableVisible:true,  ganttVisible:true},
];"""
assert old_cols in html, 'COLS anchor not found'
html = html.replace(old_cols, new_cols, 1)

with open('/home/user/YCxDesign/team-nexus-v3.html', 'w') as f:
    f.write(html)
print('Chunk 2a done')
