#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

src = '/home/user/YCxDesign/team-nexus-v3.html'
content = open(src, encoding='utf-8').read()
orig = len(content)

def rp(old, new, label):
    global content
    assert old in content, f"ANCHOR NOT FOUND: {label}\nLooking for: {repr(old[:80])}"
    content = content.replace(old, new, 1)
    print(f"  OK: {label}")

# ── 1. Add WORKSPACE_TOOLS data after STARRED_ITEMS ─────────────────────────
rp(
    "let STARRED_ITEMS={projects:{},folders:{},tasks:{}};",
    """let STARRED_ITEMS={projects:{},folders:{},tasks:{}};

let WORKSPACE_TOOLS=[
  {id:'wt1',wsId:'ws1',type:'dashboard',name:'PMO Financial Dashboard'},
  {id:'wt2',wsId:'ws1',type:'report',name:'All Project Status Report'},
  {id:'wt3',wsId:'ws1',type:'calendar',name:'Project Roadmap'},
  {id:'wt4',wsId:'ws1',type:'calendar',name:'Team Roadmap'},
  {id:'wt5',wsId:'ws4',type:'dashboard',name:'Operations Overview'},
  {id:'wt6',wsId:'ws5',type:'dashboard',name:'Account Management Dashboard'},
  {id:'wt7',wsId:'ws2',type:'dashboard',name:'My Work Dashboard'},
];
let curDashboardId=null;""",
    "Add WORKSPACE_TOOLS"
)

# ── 2. Add view-dashboard div after view-stub ────────────────────────────────
rp(
    '<div id="view-stub" style="display:none;position:absolute;inset:0"></div>',
    '''<div id="view-stub" style="display:none;position:absolute;inset:0"></div>
    <div id="view-dashboard" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>''',
    "Add view-dashboard div"
)

# ── 3. Update showView list ──────────────────────────────────────────────────
rp(
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt','inbox','stream','created-by-me','starred'].forEach",
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt','inbox','stream','created-by-me','starred','dashboard'].forEach",
    "Update showView list"
)

# ── 4. Update renderNavWorkspaces to show Tools section ───────────────────────
# Modify the ws-nav-children section to include Tools
old_children = """      ${ws.expanded?`<div class="ws-nav-children">
        ${getFolders(ws.id).map(fl=>`
          <div class="ws-child" onclick="openFolder('${ws.id}','${fl.id}')">
            <span class="nav-icon" style="width:14px;height:14px;flex-shrink:0"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></span><span style="overflow:hidden;text-overflow:ellipsis">${fl.name}</span>
          </div>
          ${getProjectsInFolder(fl.id).map(p=>`
            <div class="ws-child ws-child-proj${curProjectId===p.id?' active':''}" onclick="openProject('${p.id}')">
              <span class="nav-icon" style="width:14px;height:14px;flex-shrink:0"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></span><span style="overflow:hidden;text-overflow:ellipsis">${p.name}</span>
            </div>`).join('')}
        `).join('')}
        ${getProjectsInWorkspaceNoFolder(ws.id).map(p=>`
          <div class="ws-child${curProjectId===p.id?' active':''}" onclick="openProject('${p.id}')">
            <span class="nav-icon" style="width:14px;height:14px;flex-shrink:0"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></span><span style="overflow:hidden;text-overflow:ellipsis">${p.name}</span>
          </div>`).join('')}
        <div class="ws-child" style="color:var(--text3);font-style:italic" onclick="showWorkspace('${ws.id}')">
          <span>···</span><span>View all</span>
        </div>
      </div>`:''}"""

new_children = """      ${ws.expanded?`<div class="ws-nav-children">
        ${(()=>{const tools=WORKSPACE_TOOLS.filter(t=>t.wsId===ws.id);return tools.length?`
          <div class="ws-nav-section-head">
            <span>Tools</span>
            <button class="ws-nav-add-btn" onclick="event.stopPropagation();showWsToolsMenu('${ws.id}',event)" title="Add tool">+</button>
          </div>
          ${tools.map(t=>`<div class="ws-child${curDashboardId===t.id?' active':''}" onclick="openWsTool('${t.id}')">
            <span class="nav-icon" style="width:14px;height:14px;flex-shrink:0">${wsToolIcon(t.type)}</span>
            <span style="overflow:hidden;text-overflow:ellipsis">${t.name}</span>
          </div>`).join('')}`:`<div class="ws-nav-section-head"><span>Tools</span><button class="ws-nav-add-btn" onclick="event.stopPropagation();showWsToolsMenu('${ws.id}',event)" title="Add tool">+</button></div>`})()}
        <div class="ws-nav-section-head" style="margin-top:4px"><span>Projects and folders</span></div>
        ${getFolders(ws.id).map(fl=>`
          <div class="ws-child" onclick="openFolder('${ws.id}','${fl.id}')">
            <span class="nav-icon" style="width:14px;height:14px;flex-shrink:0"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></span><span style="overflow:hidden;text-overflow:ellipsis">${fl.name}</span>
          </div>
          ${getProjectsInFolder(fl.id).map(p=>`
            <div class="ws-child ws-child-proj${curProjectId===p.id?' active':''}" onclick="openProject('${p.id}')">
              <span class="nav-icon" style="width:14px;height:14px;flex-shrink:0"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></span><span style="overflow:hidden;text-overflow:ellipsis">${p.name}</span>
            </div>`).join('')}
        `).join('')}
        ${getProjectsInWorkspaceNoFolder(ws.id).map(p=>`
          <div class="ws-child${curProjectId===p.id?' active':''}" onclick="openProject('${p.id}')">
            <span class="nav-icon" style="width:14px;height:14px;flex-shrink:0"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></span><span style="overflow:hidden;text-overflow:ellipsis">${p.name}</span>
          </div>`).join('')}
        <div class="ws-child" style="color:var(--text3);font-style:italic" onclick="showWorkspace('${ws.id}')">
          <span>···</span><span>View all</span>
        </div>
      </div>`:''}"""

rp(old_children, new_children, "Update renderNavWorkspaces with Tools section")

# ── 5. Add wsToolIcon helper + openWsTool + showWsToolsMenu after toggleWsNav ─
old_toggle = """function toggleWsNav(wsId){
  const ws=WORKSPACES.find(w=>w.id===wsId);
  if(!ws)return;
  if(!ws.expanded){ws.expanded=true;showWorkspace(wsId);}
  else{ws.expanded=!ws.expanded;renderNavWorkspaces();}
}"""
new_toggle = """function toggleWsNav(wsId){
  const ws=WORKSPACES.find(w=>w.id===wsId);
  if(!ws)return;
  if(!ws.expanded){ws.expanded=true;showWorkspace(wsId);}
  else{ws.expanded=!ws.expanded;renderNavWorkspaces();}
}
function wsToolIcon(type){
  const icons={
    dashboard:`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`,
    report:`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>`,
    calendar:`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/></svg>`,
    whiteboard:`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
    workload:`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>`,
  };
  return icons[type]||icons.dashboard;
}
function openWsTool(toolId){
  const t=WORKSPACE_TOOLS.find(t=>t.id===toolId);if(!t)return;
  curDashboardId=toolId;
  if(t.type==='dashboard') showDashboardTool(t);
  else if(t.type==='report') showReports();
  else if(t.type==='calendar') showCalendars();
  else if(t.type==='whiteboard') showStub('Whiteboard','🖼','Collaborative whiteboard \u2014 coming soon.');
  else if(t.type==='workload') showStub('Workload','👥','Team capacity visualization \u2014 coming soon.');
  renderNavWorkspaces();
}
function showWsToolsMenu(wsId,evt){
  document.querySelectorAll('.ptb-menu').forEach(m=>m.remove());
  const types=[
    {type:'whiteboard',label:'Whiteboard',icon:'🖼'},
    {type:'dashboard',label:'Dashboard',icon:'📊'},
    {type:'calendar',label:'Calendar',icon:'📅'},
    {type:'report',label:'Report',icon:'📋'},
    {type:'workload',label:'Workload chart',icon:'👥'},
  ];
  const menu=document.createElement('div');
  menu.className='ptb-menu';
  menu.style.cssText=`left:${evt.clientX}px;top:${evt.clientY+6}px;min-width:160px`;
  menu.innerHTML=types.map(t=>`
    <div class="ptb-menu-item" onclick="addWsTool('${wsId}','${t.type}');this.closest('.ptb-menu').remove()">
      <span style="margin-right:6px">${t.icon}</span>${t.label}
    </div>`).join('');
  document.body.appendChild(menu);
  setTimeout(()=>document.addEventListener('click',()=>menu.remove(),{once:true}),10);
}
function addWsTool(wsId,type){
  const names={dashboard:'New Dashboard',report:'New Report',calendar:'New Calendar',whiteboard:'New Whiteboard',workload:'Workload Chart'};
  const id='wt'+Date.now();
  WORKSPACE_TOOLS.push({id,wsId,type,name:names[type]||'New Tool'});
  renderNavWorkspaces();
  openWsTool(id);
}"""
rp(old_toggle, new_toggle, "Add wsToolIcon + openWsTool + showWsToolsMenu")

# ── 6. Wire Dashboard + Calendar buttons on workspace toolbar to use tools ────
rp(
    "onclick=\"showStub('Calendar','\📅','View tasks and deadlines in calendar format.')\"",
    "onclick=\"showCalendars()\"",
    "Wire Calendar ws-tool-btn"
) if "onclick=\"showStub('Calendar','\📅'," in content else None

# Try alternate
old_cal_btn = "onclick=\"showStub('Calendar','📅','View tasks and deadlines in calendar format.')\""
if old_cal_btn in content:
    content = content.replace(old_cal_btn, "onclick=\"showCalendars()\"", 1)
    print("  OK: Wire Calendar ws-tool-btn")

old_dash_btn = "onclick=\"showStub('Dashboard','🔲','Visual KPI dashboard for this workspace.')\""
if old_dash_btn in content:
    content = content.replace(old_dash_btn, "onclick=\"showDashboardTool(WORKSPACE_TOOLS.find(t=>t.wsId===wsId&&t.type==='dashboard')||WORKSPACE_TOOLS[0])\"", 1)
    print("  OK: Wire Dashboard ws-tool-btn")

old_rep_btn = "onclick=\"showStub('Reports','📊','Reporting and analytics for this workspace.')\""
if old_rep_btn in content:
    content = content.replace(old_rep_btn, "onclick=\"showReports()\"", 1)
    print("  OK: Wire Reports ws-tool-btn")

# ── 7. Add CSS for nav Tools section ─────────────────────────────────────────
rp(
    ".stream-time{font-size:11px;color:var(--text3)}",
    """.stream-time{font-size:11px;color:var(--text3)}
/* Workspace nav tools */
.ws-nav-section-head{display:flex;align-items:center;justify-content:space-between;padding:6px 8px 2px 20px;font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text3)}
.ws-nav-add-btn{width:18px;height:18px;border-radius:4px;border:none;background:transparent;cursor:pointer;color:var(--text3);font-size:14px;display:flex;align-items:center;justify-content:center;line-height:1;padding:0}
.ws-nav-add-btn:hover{background:var(--abg);color:var(--accent)}
/* Dashboard view */
.dash-header{display:flex;align-items:center;justify-content:space-between;padding:16px 20px 12px;border-bottom:1px solid var(--border2)}
.dash-title{font-size:17px;font-weight:700}
.dash-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;padding:20px}
.dash-widget{background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:16px;min-height:140px}
.dash-widget-title{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text3);margin-bottom:12px;display:flex;align-items:center;gap:6px}
.dash-widget.wide{grid-column:span 2}
.dash-kpi{font-size:32px;font-weight:700;color:var(--accent);margin-bottom:4px}
.dash-kpi-label{font-size:12px;color:var(--text3)}
.dash-widget-row{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--border2);font-size:12px}
.dash-widget-row:last-child{border-bottom:none}""",
    "Add Dashboard CSS"
)

# ── Safe write ────────────────────────────────────────────────────────────────
tmp = src + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(tmp, src)
print(f"\nDone — {orig} -> {len(content)} chars ({len(content)-orig:+d})")
