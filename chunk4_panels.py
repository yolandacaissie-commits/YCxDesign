#!/usr/bin/env python3
"""Chunk 4: field panel, custom field creator, +View, Sort/Filter/Group menus."""
with open('/home/user/YCxDesign/team-nexus-v3.html', 'r') as f:
    html = f.read()

NEW_PANEL_JS = r"""
// ═══════════════════ PROJECT TOOLBAR MENUS ═══════════════════

// ── Field toggle panel ──
function openFieldPanel(evt){
  closePtbMenus();
  const p=getP();if(!p)return;
  const vc=p.visibleColumns||['pred','duration','startDate','dueDate','status','assignee'];
  const BUILTIN=[
    {key:'pred',     label:'Predecessors'},
    {key:'duration', label:'Duration'},
    {key:'startDate',label:'Start date'},
    {key:'dueDate',  label:'Due date'},
    {key:'status',   label:'Status'},
    {key:'priority', label:'Priority'},
    {key:'assignee', label:'Assignee'},
  ];
  const builtinRows=BUILTIN.map(c=>{
    const on=vc.includes(c.key);
    return `<div class="field-row" onclick="toggleFieldVis('${c.key}',event)">
      <span class="field-row-name">${c.label}</span>
      <div class="toggle-sw${on?' on':''}" id="tsw-${c.key}"></div>
    </div>`;
  }).join('');
  const cfRows=CUSTOM_FIELDS.map(cf=>{
    const cfKey='cf_'+cf.id;
    const on=vc.includes(cfKey);
    return `<div class="field-row" onclick="toggleFieldVis('${cfKey}',event)">
      <span class="field-row-name">${cf.name} <span style="font-size:10px;color:var(--text3)">(${cf.type})</span></span>
      <div class="toggle-sw${on?' on':''}" id="tsw-${cfKey}"></div>
    </div>`;
  }).join('');
  const panel=document.createElement('div');
  panel.className='field-panel';
  panel.innerHTML=`
    <div class="field-panel-head">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
        <span style="font-size:13px;font-weight:700;color:var(--text)">Fields</span>
        <button onclick="closePtbMenus()" style="background:none;border:none;cursor:pointer;color:var(--text3);font-size:16px;line-height:1">×</button>
      </div>
      <div class="field-panel-search">
        <svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:var(--text3);stroke-width:2;fill:none;flex-shrink:0"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input placeholder="Search fields" oninput="filterFieldPanel(this.value)" id="field-panel-search-inp">
      </div>
    </div>
    <div class="field-panel-body" id="field-panel-body">
      <div class="field-panel-section">General</div>
      <div id="fp-builtin">${builtinRows}</div>
      ${CUSTOM_FIELDS.length?`<div class="field-panel-section">Custom fields</div><div id="fp-custom">${cfRows}</div>`:''}
    </div>
    <div style="border-top:1px solid var(--border2);padding:8px 10px">
      <button onclick="openCFCreator(event)" style="display:flex;align-items:center;gap:6px;padding:7px 10px;border-radius:6px;font-size:12.5px;font-weight:600;color:var(--accent);border:1px dashed var(--accent);background:var(--abg);cursor:pointer;width:100%;justify-content:center">
        <svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:2;fill:none"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Custom field
      </button>
    </div>`;
  positionMenu(panel, evt);
  document.body.appendChild(panel);
  setTimeout(()=>document.addEventListener('click',closePtbOnOutside),10);
}

function filterFieldPanel(q){
  const ql=q.toLowerCase();
  document.querySelectorAll('#field-panel-body .field-row').forEach(row=>{
    row.style.display=row.textContent.toLowerCase().includes(ql)?'':'none';
  });
}

function toggleFieldVis(key,evt){
  evt&&evt.stopPropagation();
  const p=getP();if(!p)return;
  if(!p.visibleColumns)p.visibleColumns=['pred','duration','startDate','dueDate','status','assignee'];
  const idx=p.visibleColumns.indexOf(key);
  if(idx>=0)p.visibleColumns.splice(idx,1);
  else p.visibleColumns.push(key);
  const sw=document.getElementById('tsw-'+key);
  if(sw)sw.classList.toggle('on',idx<0);
  if(curView==='table')renderTable();
}

// ── Custom field creator ──
let cfCreatorType='text';
function openCFCreator(evt){
  document.querySelectorAll('.cf-creator').forEach(el=>el.remove());
  const CF_TYPES=[
    {t:'text',     label:'Text',            icon:'Aa'},
    {t:'number',   label:'Number',          icon:'#'},
    {t:'currency', label:'Currency',        icon:'$'},
    {t:'percent',  label:'Percent',         icon:'%'},
    {t:'select',   label:'Single select',   icon:'○'},
    {t:'multiselect',label:'Multiple select',icon:'☰'},
    {t:'assignee', label:'People',          icon:'👤'},
    {t:'date',     label:'Date',            icon:'📅'},
    {t:'duration', label:'Duration',        icon:'⏱'},
    {t:'checkbox', label:'Checkbox',        icon:'☑'},
  ];
  cfCreatorType='text';
  const el=document.createElement('div');
  el.className='cf-creator';
  el.innerHTML=`
    <div class="cf-creator-title">New custom field</div>
    <input id="cf-new-name" placeholder="Field name" value="New field">
    <div class="cf-type-label">Select type</div>
    <div class="cf-type-grid" id="cf-type-grid">
      ${CF_TYPES.map(ct=>`
        <div class="cf-type-opt${ct.t==='text'?' sel':''}" onclick="selCFType('${ct.t}',this)">
          <span style="width:18px;text-align:center;font-size:12px">${ct.icon}</span>
          <span>${ct.label}</span>
        </div>`).join('')}
    </div>
    <div id="cf-options-area" style="display:none;margin-top:10px">
      <div class="cf-type-label">Options (one per line)</div>
      <textarea id="cf-options-inp" rows="3" style="width:100%;box-sizing:border-box;padding:6px 8px;border:1px solid var(--border2);border-radius:6px;font-size:12px;background:var(--surface2);color:var(--text);outline:none;resize:vertical"></textarea>
    </div>
    <div class="cf-creator-actions">
      <button onclick="closePtbMenus()" style="background:none">Cancel</button>
      <button class="cf-save" onclick="saveCFCreator()">Create field</button>
    </div>`;
  positionMenu(el, evt, true);
  document.body.appendChild(el);
}

function selCFType(t,el){
  cfCreatorType=t;
  document.querySelectorAll('.cf-type-opt').forEach(o=>o.classList.remove('sel'));
  el.classList.add('sel');
  const needsOpts=t==='select'||t==='multiselect';
  document.getElementById('cf-options-area').style.display=needsOpts?'block':'none';
}

function saveCFCreator(){
  const name=document.getElementById('cf-new-name')?.value.trim();
  if(!name)return;
  let options=[];
  if(cfCreatorType==='select'||cfCreatorType==='multiselect'){
    const raw=document.getElementById('cf-options-inp')?.value||'';
    options=raw.split('\n').map(s=>s.trim()).filter(Boolean);
  }
  const newCF={id:'cf'+Date.now(),name,type:cfCreatorType,options,visible:true,desc:''};
  CUSTOM_FIELDS.push(newCF);
  // Also add to current project's visibleColumns
  const p=getP();
  if(p){
    if(!p.visibleColumns)p.visibleColumns=['pred','duration','startDate','dueDate','status','assignee'];
    p.visibleColumns.push('cf_'+newCF.id);
  }
  closePtbMenus();
  if(curView==='table')renderTable();
  if(curView==='settings')renderSettings();
  // Re-open field panel so user sees the new field
  setTimeout(()=>{
    const fakeEvt={clientX:window.innerWidth-310,clientY:90};
    openFieldPanel(fakeEvt);
  },80);
}

// ── +View dropdown ──
function openAddViewMenu(evt){
  closePtbMenus();
  const p=getP();if(!p)return;
  const all=['table','gantt','board'];
  const available=all.filter(v=>!(p.views||['table']).includes(v));
  if(!available.length)return;
  const VIEW_LABELS={table:'Table',gantt:'Gantt chart',board:'Board'};
  const VIEW_ICONS={
    table:`<svg viewBox="0 0 24 24" style="width:14px;height:14px;stroke:currentColor;stroke-width:1.75;fill:none"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>`,
    gantt:`<svg viewBox="0 0 24 24" style="width:14px;height:14px;stroke:currentColor;stroke-width:1.75;fill:none"><line x1="3" y1="6" x2="21" y2="6"/><rect x="3" y="10" width="10" height="3" rx="1"/><rect x="9" y="15" width="10" height="3" rx="1"/><line x1="3" y1="21" x2="21" y2="21"/></svg>`,
    board:`<svg viewBox="0 0 24 24" style="width:14px;height:14px;stroke:currentColor;stroke-width:1.75;fill:none"><rect x="3" y="3" width="5" height="18" rx="1"/><rect x="11" y="3" width="5" height="12" rx="1"/><rect x="19" y="3" width="3" height="7" rx="1"/></svg>`,
  };
  const menu=document.createElement('div');
  menu.className='ptb-menu';
  menu.innerHTML=`<div class="ptb-menu-label">Add view</div>`+
    available.map(v=>`<div class="ptb-menu-item" onclick="addProjectView('${v}')">
      ${VIEW_ICONS[v]||''}<span>${VIEW_LABELS[v]||v}</span>
    </div>`).join('');
  positionMenu(menu, evt);
  document.body.appendChild(menu);
  setTimeout(()=>document.addEventListener('click',closePtbOnOutside),10);
}

function addProjectView(v){
  const p=getP();if(!p)return;
  if(!p.views)p.views=['table'];
  if(!p.views.includes(v))p.views.push(v);
  closePtbMenus();
  switchView(v);
}

// ── Sort menu ──
function openSortMenu(evt){
  closePtbMenus();
  const p=getP();if(!p)return;
  const FIELDS=[
    {key:'title',label:'Name'},{key:'pred',label:'Predecessors'},
    {key:'duration',label:'Duration'},{key:'startDate',label:'Start date'},
    {key:'dueDate',label:'Due date'},{key:'status',label:'Status'},
    {key:'priority',label:'Priority'},{key:'assignee',label:'Assignee'},
  ];
  const menu=document.createElement('div');
  menu.className='ptb-menu';
  menu.style.minWidth='190px';
  const sf=p.sortField||'startDate', sd=p.sortDir||'asc';
  menu.innerHTML=`<div class="ptb-menu-label">Sort by</div>`+
    FIELDS.map(f=>`<div class="ptb-menu-item${sf===f.key?' on':''}" style="${sf===f.key?'color:var(--accent);font-weight:600':''}" onclick="setTblSort('${f.key}')">
      ${f.label}${sf===f.key?' '+(sd==='asc'?'↑':'↓'):''}
    </div>`).join('')+
    `<div class="ptb-menu-sep"></div>
    <div class="ptb-menu-item" onclick="setTblSortDir('asc')" style="${sd==='asc'?'color:var(--accent);font-weight:600':''}">↑ Ascending</div>
    <div class="ptb-menu-item" onclick="setTblSortDir('desc')" style="${sd==='desc'?'color:var(--accent);font-weight:600':''}">↓ Descending</div>`;
  positionMenu(menu, evt);
  document.body.appendChild(menu);
  setTimeout(()=>document.addEventListener('click',closePtbOnOutside),10);
}

function setTblSort(field){
  const p=getP();if(!p)return;
  if(p.sortField===field)p.sortDir=p.sortDir==='asc'?'desc':'asc';
  else{p.sortField=field;p.sortDir='asc';}
  closePtbMenus();renderProjToolbar();if(curView==='table')renderTable();
}
function setTblSortDir(dir){
  const p=getP();if(!p)return;
  p.sortDir=dir;closePtbMenus();renderProjToolbar();if(curView==='table')renderTable();
}

// ── Group menu ──
function openGroupMenu(evt){
  closePtbMenus();
  const p=getP();if(!p)return;
  const GROUPS=[
    {key:'status',label:'Status'},{key:'assignee',label:'Assignee'},
    {key:'priority',label:'Priority'},{key:'dueDate',label:'Due date (month)'},
  ];
  const menu=document.createElement('div');
  menu.className='ptb-menu';
  menu.innerHTML=`<div class="ptb-menu-label">Group by</div>`+
    GROUPS.map(g=>`<div class="ptb-menu-item${p.groupBy===g.key?' on':''}" style="${p.groupBy===g.key?'color:var(--accent);font-weight:600':''}" onclick="setGroupBy('${g.key}')">
      ${g.label}${p.groupBy===g.key?' ✓':''}
    </div>`).join('')+
    `<div class="ptb-menu-sep"></div>
    <div class="ptb-menu-item${!p.groupBy?' on':''}" onclick="setGroupBy(null)">None${!p.groupBy?' ✓':''}</div>`;
  positionMenu(menu, evt);
  document.body.appendChild(menu);
  setTimeout(()=>document.addEventListener('click',closePtbOnOutside),10);
}

function setGroupBy(key){
  const p=getP();if(!p)return;
  p.groupBy=key||null;closePtbMenus();renderProjToolbar();if(curView==='table')renderTable();
}

// ── Filter panel ──
function openFilterPanel(evt){
  closePtbMenus();
  const p=getP();if(!p)return;
  if(!p.filterRules)p.filterRules=[];
  const FILTER_FIELDS=[
    {key:'title',label:'Name'},{key:'status',label:'Status'},
    {key:'priority',label:'Priority'},{key:'assignee',label:'Assignee'},
    {key:'dueDate',label:'Due date'},{key:'duration',label:'Duration'},
  ];
  const panel=document.createElement('div');
  panel.className='filter-panel';
  function renderRules(){
    panel.innerHTML=`
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:12px">
        <span style="font-size:13px;font-weight:700;color:var(--text)">Filter</span>
        <button onclick="closePtbMenus()" style="background:none;border:none;cursor:pointer;color:var(--text3);font-size:16px">×</button>
      </div>
      <div id="filter-rules-list">
        ${p.filterRules.map((r,i)=>`
          <div class="filter-rule-row">
            <select onchange="updateFilterRule(${i},'field',this.value)" style="flex:0 0 110px">
              ${FILTER_FIELDS.map(f=>`<option value="${f.key}"${r.field===f.key?' selected':''}>${f.label}</option>`).join('')}
            </select>
            <select onchange="updateFilterRule(${i},'op',this.value)" style="flex:0 0 120px">
              ${['contains','does not contain','is','is not','is empty','is not empty','>','<','before','after'].map(o=>`<option${r.op===o?' selected':''}>${o}</option>`).join('')}
            </select>
            <input value="${r.value||''}" placeholder="value" onblur="updateFilterRule(${i},'value',this.value)" onkeydown="if(event.key==='Enter')this.blur()">
            <button onclick="removeFilterRule(${i})" style="background:none;border:none;cursor:pointer;color:#ef4444;font-size:16px;padding:0 4px;flex-shrink:0">×</button>
          </div>`).join('')}
      </div>
      <button onclick="addFilterRule()" style="display:flex;align-items:center;gap:5px;padding:6px 10px;border-radius:6px;font-size:12.5px;color:var(--accent);border:none;background:none;cursor:pointer;margin-top:4px">
        <svg viewBox="0 0 24 24" style="width:12px;height:12px;stroke:currentColor;stroke-width:2;fill:none"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
        Add filter
      </button>
      ${p.filterRules.length?`<button onclick="clearFilters()" style="display:flex;align-items:center;gap:5px;padding:6px 10px;border-radius:6px;font-size:12.5px;color:#ef4444;border:none;background:none;cursor:pointer">Clear all</button>`:''}`;
  }
  renderRules();
  window._rerenderFilterPanel=renderRules;
  positionMenu(panel, evt);
  document.body.appendChild(panel);
  setTimeout(()=>document.addEventListener('click',closePtbOnOutside),10);
}

function addFilterRule(){
  const p=getP();if(!p)return;
  if(!p.filterRules)p.filterRules=[];
  p.filterRules.push({field:'title',op:'contains',value:''});
  if(window._rerenderFilterPanel)window._rerenderFilterPanel();
  renderProjToolbar();if(curView==='table')renderTable();
}
function removeFilterRule(i){
  const p=getP();if(!p)return;
  p.filterRules.splice(i,1);
  if(window._rerenderFilterPanel)window._rerenderFilterPanel();
  renderProjToolbar();if(curView==='table')renderTable();
}
function updateFilterRule(i,key,val){
  const p=getP();if(!p)return;
  p.filterRules[i][key]=val;
  renderProjToolbar();if(curView==='table')renderTable();
}
function clearFilters(){
  const p=getP();if(!p)return;
  p.filterRules=[];closePtbMenus();renderProjToolbar();if(curView==='table')renderTable();
}

// ── Shared positioning + outside-click helpers ──
function positionMenu(el, evt, leftAligned){
  el.style.position='fixed';
  el.style.zIndex='600';
  if(evt){
    const x=evt.clientX, y=evt.clientY;
    const spaceRight=window.innerWidth-x;
    el.style.top=(y+8)+'px';
    if(leftAligned||spaceRight>240) el.style.left=x+'px';
    else el.style.right=(window.innerWidth-x)+'px';
  } else {
    el.style.top='90px';el.style.right='20px';
  }
}

function closePtbOnOutside(e){
  const keep=e.target.closest('.ptb-menu,.field-panel,.cf-creator,.filter-panel,.proj-tb-add-view,.proj-tb-btn');
  if(!keep){
    closePtbMenus();
    document.removeEventListener('click',closePtbOnOutside);
  }
}

"""

anchor = '// showHome() is called by loginAs() after authentication'
assert anchor in html, 'script end anchor not found'
html = html.replace(anchor, NEW_PANEL_JS + anchor, 1)

with open('/home/user/YCxDesign/team-nexus-v3.html', 'w') as f:
    f.write(html)
print('Chunk 4 done')
