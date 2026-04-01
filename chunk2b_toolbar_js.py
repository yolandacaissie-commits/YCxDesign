#!/usr/bin/env python3
"""Chunk 2b: Replace openProject, switchView, viewTabsHTML; update showView to auto-show/hide toolbar."""
with open('/home/user/YCxDesign/team-nexus-v3.html', 'r') as f:
    html = f.read()

# ── Replace openProject ──
old_op = """function openProject(id){
  curProjectId=id;curView='table';
  renderNavWorkspaces();
  const p=getP();
  setTopbar(p.name,p.desc||'',[viewTabsHTML(),`<button class="btn" onclick="openM('modal-task')">＋ Task</button>`]);
  showView('table');renderTable();closeDetail();closeColPanel();
}"""
new_op = """function openProject(id){
  curProjectId=id;curView='table';
  renderNavWorkspaces();
  const p=getP();if(!p)return;
  setTopbar(p.name,p.desc||'',[`<button class="btn" onclick="openM('modal-task')">＋ Task</button>`]);
  showView('table');renderProjToolbar();renderTable();closeDetail();closeColPanel();
  closeNavIfMobile();
}"""
assert old_op in html, 'openProject anchor not found'
html = html.replace(old_op, new_op, 1)

# ── Replace switchView ──
old_sv = """function switchView(v){
  curView=v;const p=getP();if(!p)return;
  setTopbar(p.name,p.desc||'',[viewTabsHTML(),`<button class="btn" onclick="openM('modal-task')">＋ Task</button>`]);
  showView(v);closeColPanel();
  if(v==='board')renderBoard();
  else if(v==='table')renderTable();
  else if(v==='gantt'){renderGantt();setTimeout(goToday,80);}
}"""
new_sv = """function switchView(v){
  curView=v;const p=getP();if(!p)return;
  closePtbMenus();
  showView(v);renderProjToolbar();closeColPanel();
  if(v==='board')renderBoard();
  else if(v==='table')renderTable();
  else if(v==='gantt'){renderGantt();setTimeout(goToday,80);}
}"""
assert old_sv in html, 'switchView anchor not found'
html = html.replace(old_sv, new_sv, 1)

# ── Update showView to auto-show/hide proj-toolbar-bar ──
old_showview = """function showView(v){
  ['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial'].forEach(n=>{
    const el=document.getElementById('view-'+n);
    if(el)el.style.display=n===v?'':'none';
  });
}"""
new_showview = """function showView(v){
  const projViews=new Set(['board','table','gantt']);
  const tb=document.getElementById('proj-toolbar-bar');
  if(tb) tb.style.display=(projViews.has(v)&&curProjectId)?'flex':'none';
  ['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial'].forEach(n=>{
    const el=document.getElementById('view-'+n);
    if(el)el.style.display=n===v?'':'none';
  });
}"""
assert old_showview in html, 'showView anchor not found'
html = html.replace(old_showview, new_showview, 1)

# ── Replace viewTabsHTML with renderProjToolbar ──
old_vtabs = """function viewTabsHTML(){
  return `<div class="view-tabs">${[['board',`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px;margin-right:4px"><rect x="3" y="3" width="5" height="18" rx="1"/><rect x="11" y="3" width="5" height="12" rx="1"/><rect x="19" y="3" width="3" height="7" rx="1"/></svg>Board`],['table',`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px;margin-right:4px"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>Table`],['gantt',`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px;margin-right:4px"><line x1="3" y1="6" x2="21" y2="6"/><rect x="3" y="10" width="10" height="3" rx="1"/><rect x="9" y="15" width="10" height="3" rx="1"/><line x1="3" y1="21" x2="21" y2="21"/></svg>Gantt`]].map(([v,l])=>`<button class="vtab${curView===v?' on':''}" onclick="switchView('${v}')">${l}</button>`).join('')}</div>`;
}"""

new_vtabs = r"""function renderProjToolbar(){
  const p=getP();if(!p)return;
  const bar=document.getElementById('proj-toolbar-bar');if(!bar)return;
  const views=p.views||['table'];
  const VIEW_ICONS={
    table:`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>`,
    gantt:`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><line x1="3" y1="6" x2="21" y2="6"/><rect x="3" y="10" width="10" height="3" rx="1"/><rect x="9" y="15" width="10" height="3" rx="1"/><line x1="3" y1="21" x2="21" y2="21"/></svg>`,
    board:`<svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><rect x="3" y="3" width="5" height="18" rx="1"/><rect x="11" y="3" width="5" height="12" rx="1"/><rect x="19" y="3" width="3" height="7" rx="1"/></svg>`,
  };
  const VIEW_LABELS={table:'Table',gantt:'Gantt',board:'Board'};
  const tabsHTML=views.map(v=>`<button class="proj-tb-tab${curView===v?' on':''}" onclick="switchView('${v}')">${VIEW_ICONS[v]||''}${VIEW_LABELS[v]||v}</button>`).join('');
  const addViewBtn=`<button class="proj-tb-add-view" onclick="openAddViewMenu(event)"><svg viewBox="0 0 24 24" style="width:11px;height:11px;stroke:currentColor;stroke-width:2;fill:none"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>View</button>`;
  const sf=p.sortField||'startDate',sd=p.sortDir||'asc';
  const SORT_LABELS={title:'Name',pred:'Predecessors',duration:'Duration',startDate:'Start date',dueDate:'Due date',status:'Status',priority:'Priority',assignee:'Assignee'};
  const filterOn=(p.filterRules||[]).length>0;
  const groupOn=!!p.groupBy;
  const GROUP_LABELS={status:'Status',assignee:'Assignee',priority:'Priority',dueDate:'Due date'};
  bar.innerHTML=`
    <div class="proj-tb-views">${tabsHTML}${addViewBtn}</div>
    <div class="proj-tb-sep"></div>
    <div class="proj-tb-controls">
      <button class="proj-tb-btn${filterOn?' active':''}" onclick="openFilterPanel(event)"><svg viewBox="0 0 24 24"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>Filter${filterOn?' ('+p.filterRules.length+')':''}</button>
      <button class="proj-tb-btn" onclick="openSortMenu(event)"><svg viewBox="0 0 24 24"><line x1="12" y1="5" x2="12" y2="19"/><polyline points="${sd==='asc'?'5 12 12 5 19 12':'5 12 12 19 19 12'}"/></svg>${sd==='asc'?'↑':'↓'} ${SORT_LABELS[sf]||sf}</button>
      <button class="proj-tb-btn${groupOn?' active':''}" onclick="openGroupMenu(event)"><svg viewBox="0 0 24 24"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>Group${groupOn?': '+(GROUP_LABELS[p.groupBy]||p.groupBy):''}</button>
      <button class="proj-tb-btn" onclick="openFieldPanel(event)"><svg viewBox="0 0 24 24"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><circle cx="3" cy="6" r="1" fill="currentColor"/><circle cx="3" cy="12" r="1" fill="currentColor"/><circle cx="3" cy="18" r="1" fill="currentColor"/></svg>Fields</button>
    </div>`;
}

function closePtbMenus(){
  document.querySelectorAll('.ptb-menu,.field-panel,.cf-creator,.filter-panel').forEach(el=>el.remove());
}"""

assert old_vtabs in html, 'viewTabsHTML anchor not found'
html = html.replace(old_vtabs, new_vtabs, 1)

with open('/home/user/YCxDesign/team-nexus-v3.html', 'w') as f:
    f.write(html)
print('Chunk 2b done')
