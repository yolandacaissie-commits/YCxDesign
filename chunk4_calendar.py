#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

src = '/home/user/YCxDesign/team-nexus-v3.html'
content = open(src, encoding='utf-8').read()
orig = len(content)

def rp(old, new, label):
    global content
    assert old in content, f"ANCHOR NOT FOUND: {label}\n{repr(old[:80])}"
    content = content.replace(old, new, 1)
    print(f"  OK: {label}")

# ── 1. Add view-calendar div ────────────────────────────────────────────────
rp(
    '<div id="view-report-viewer" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>',
    '''<div id="view-report-viewer" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>
    <div id="view-calendar" style="display:none;position:absolute;inset:0;display:flex;flex-direction:column"></div>''',
    "Add view-calendar div"
)

# ── 2. Update showView list ──────────────────────────────────────────────────
rp(
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt','inbox','stream','created-by-me','starred','dashboard','reports','report-viewer'].forEach",
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt','inbox','stream','created-by-me','starred','dashboard','reports','report-viewer','calendar'].forEach",
    "Update showView list"
)

# ── 3. Add calendar state vars after curReportId ────────────────────────────
rp(
    "let curReportId=null;",
    """let curReportId=null;
let calYear=new Date().getFullYear();
let calMode='year'; // 'year' | 'quarter'
let calLayers={}; // {userId: true} — visible layers""",
    "Add calendar state vars"
)

# ── 4. Replace showCalendars() ──────────────────────────────────────────────
rp(
    """function showCalendars(){
  curView='stub';setTopbar('Calendars','Task deadlines and events',[]);showView('stub');closeNavIfMobile();
  document.getElementById('view-stub').innerHTML=`<div class="stub-view topo-bg">
    <div class="stub-icon">📅</div><div class="stub-title">Calendars</div>
    <div class="stub-sub">View tasks with due dates across your workspaces on a calendar. Choose a data source:</div>
    <div class="stub-ds-row">
      <div class="stub-ds-btn on">Entire account</div>
      ${WORKSPACES.map(ws=>`<div class="stub-ds-btn" onclick="this.parentElement.querySelectorAll('.stub-ds-btn').forEach(b=>b.classList.remove('on'));this.classList.add('on')">${ws.name}</div>`).join('')}
    </div>
  </div>`;
}""",
    """function showCalendars(wsId){
  curView='calendar';
  const ws=wsId?WORKSPACES.find(w=>w.id===wsId):null;
  setTopbar(ws?ws.name+' Roadmap':'Team Roadmap','Project timeline by assignee',[]);
  showView('calendar');closeNavIfMobile();
  // Default all users visible
  USERS.forEach(u=>{if(calLayers[u.id]===undefined)calLayers[u.id]=true;});
  renderCalendar(wsId);
}
function renderCalendar(wsId){
  const el=document.getElementById('view-calendar');
  const allProjects=wsId?PROJECTS.filter(p=>(p.locations||[]).some(l=>l.workspaceId===wsId)):PROJECTS;
  const today=new Date();
  const todayStr=today.toISOString().slice(0,10);

  // ── Build months for current view ──────────────────────────────────────────
  const months=[];
  if(calMode==='year'){
    for(let m=0;m<12;m++) months.push({year:calYear,month:m});
  } else {
    const q=Math.floor((today.getMonth())/3);
    for(let m=q*3;m<q*3+3;m++) months.push({year:calYear,month:m});
  }
  const viewStart=new Date(months[0].year,months[0].month,1);
  const viewEnd=new Date(months[months.length-1].year,months[months.length-1].month+1,0);
  const totalDays=Math.round((viewEnd-viewStart)/86400000)+1;
  const MONTH_NAMES=['January','February','March','April','May','June','July','August','September','October','November','December'];
  const QUARTERS=['Q1','Q2','Q3','Q4'];

  function pctX(date){
    const d=typeof date==='string'?new Date(date):date;
    return Math.max(0,Math.min(100,((d-viewStart)/86400000/totalDays)*100));
  }

  // ── Group projects by assignee (use first task's assignee) ─────────────────
  const assigneeMap={};
  allProjects.forEach(p=>{
    const uid=p.tasks.length>0?(p.owner||p.tasks[0].assignee||1):1;
    if(!assigneeMap[uid]) assigneeMap[uid]=[];
    const start=p.tasks.reduce((m,t)=>t.start&&(!m||t.start<m)?t.start:m,null)||new Date(calYear,0,1);
    const end=p.tasks.reduce((m,t)=>t.end&&(!m||t.end>m)?t.end:m,null)||new Date(calYear,11,31);
    assigneeMap[uid].push({...p,_start:new Date(start),_end:new Date(end)});
  });

  // ── Month header columns ────────────────────────────────────────────────────
  const monthColW=100/months.length;
  const monthHeaders=months.map(({year,month})=>{
    const pct=pctX(new Date(year,month,1));
    return `<div class="cal-month-cell" style="width:${monthColW}%">${MONTH_NAMES[month]}</div>`;
  }).join('');

  // ── Quarter labels ──────────────────────────────────────────────────────────
  const qGroups={};
  months.forEach(({year,month})=>{
    const q=Math.floor(month/3);
    const key=`Q${q+1} ${year}`;
    if(!qGroups[key]) qGroups[key]=0;
    qGroups[key]++;
  });
  const quarterHeaders=Object.entries(qGroups).map(([q,cnt])=>
    `<div class="cal-quarter-cell" style="width:${(cnt/months.length)*100}%">${q}</div>`
  ).join('');

  // ── Today line position ─────────────────────────────────────────────────────
  const todayPct=pctX(today);
  const todayVisible=today>=viewStart&&today<=viewEnd;

  // ── Rows ────────────────────────────────────────────────────────────────────
  const BAR_COLORS=['#f472b6','#5AD2C9','#a78bfa','#fb923c','#22c55e','#3b82f6','#f59e0b','#ec4899'];
  const rows=USERS.filter(u=>assigneeMap[u.id]&&calLayers[u.id]!==false).map((u,ui)=>{
    const projs=(assigneeMap[u.id]||[]).filter(p=>p._end>=viewStart&&p._start<=viewEnd);
    const color=BAR_COLORS[ui%BAR_COLORS.length];
    return `<div class="cal-row">
      ${projs.map(p=>{
        const left=pctX(p._start);
        const right=100-pctX(p._end);
        const tooNarrow=(100-left-right)<2;
        return `<div class="cal-bar" style="left:${left}%;right:${right}%;background:${color};opacity:.85" title="${p.name}" onclick="openProject('${p.id}')">
          ${tooNarrow?'':p.name}
        </div>`;
      }).join('')}
      ${todayVisible?`<div class="cal-today-line" style="left:${todayPct}%"></div>`:''}
    </div>`;
  }).join('');

  // ── Left sidebar layers ─────────────────────────────────────────────────────
  const sidebarRows=USERS.filter(u=>assigneeMap[u.id]).map((u,ui)=>{
    const color=BAR_COLORS[ui%BAR_COLORS.length];
    const vis=calLayers[u.id]!==false;
    return `<div class="cal-side-row">
      <label style="display:flex;align-items:center;gap:6px;cursor:pointer;font-size:12px;font-weight:500;color:var(--text2)">
        <input type="checkbox" style="display:none" ${vis?'checked':''} onchange="calLayers[${u.id}]=this.checked;renderCalendar('${wsId||''}')">
        <span class="cal-layer-check${vis?' on':''}" style="border-color:${color};background:${vis?color:'transparent'}" onclick="calLayers[${u.id}]=!calLayers[${u.id}];renderCalendar('${wsId||''}')"></span>
        <span>${u.name.split(' ')[0]}</span>
        <button class="cal-layer-filter" title="Filter layer">▽</button>
      </label>
    </div>`;
  }).join('');

  el.style.display='flex';
  el.style.flexDirection='column';
  el.innerHTML=`
  <div class="cal-toolbar">
    <button class="btn ghost" onclick="calYear--;renderCalendar('${wsId||''}')">‹ Prev</button>
    <div class="cal-year-btn" onclick="calMode=calMode==='year'?'quarter':'year';renderCalendar('${wsId||''}')">${calMode==='year'?calYear:QUARTERS[Math.floor(today.getMonth()/3)]+' '+calYear} ▾</div>
    <button class="btn ghost" onclick="calYear++;renderCalendar('${wsId||''}')">Next ›</button>
    <button class="btn ghost" style="margin-left:8px;font-size:12px" onclick="calYear=new Date().getFullYear();calMode='year';renderCalendar('${wsId||'}')">Today</button>
    <div style="flex:1"></div>
    <button class="btn ghost" style="font-size:12px" onclick="openNewLayerModal('${wsId||''}')">+ New layer</button>
    <button class="btn ghost" style="font-size:12px">Fields</button>
    <button class="btn ghost" style="font-size:12px">Public links</button>
  </div>
  <div class="cal-layout">
    <!-- Left sidebar -->
    <div class="cal-sidebar">
      <div class="cal-sidebar-head">Calendars</div>
      <div class="cal-side-name" style="font-size:12px;font-weight:600;margin-bottom:4px">Team Roadmap</div>
      ${sidebarRows}
    </div>
    <!-- Timeline -->
    <div class="cal-timeline-wrap">
      <div class="cal-quarter-row">${quarterHeaders}</div>
      <div class="cal-month-row">${monthHeaders}</div>
      <div class="cal-rows-area" style="position:relative">
        ${USERS.filter(u=>assigneeMap[u.id]&&calLayers[u.id]!==false).map((u,ui)=>`
          <div class="cal-assignee-group">
            <div class="cal-assignee-name">${u.name.split(' ')[0]}</div>
            ${(assigneeMap[u.id]||[]).filter(p=>p._end>=viewStart&&p._start<=viewEnd).map(p=>{
              const left=pctX(p._start);
              const right=100-pctX(p._end);
              const color=BAR_COLORS[ui%BAR_COLORS.length];
              return `<div class="cal-row" style="position:relative">
                <div class="cal-bar" style="left:${left}%;right:${right}%;background:${color}" title="${p.name}" onclick="openProject('${p.id}')">${p.name}</div>
                ${todayVisible?`<div class="cal-today-line" style="left:${todayPct}%"></div>`:''}
              </div>`;
            }).join('')||'<div class="cal-row"></div>'}
          </div>`).join('')}
      </div>
    </div>
  </div>`;
}
function openNewLayerModal(wsId){
  const modal=document.createElement('div');
  modal.className='modal-overlay';
  modal.innerHTML=`<div class="modal" style="max-width:680px;width:95vw">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:18px">
      <div style="font-size:16px;font-weight:700">New layer</div>
      <button onclick="this.closest('.modal-overlay').remove()" style="background:none;border:none;font-size:20px;cursor:pointer;color:var(--text3)">&times;</button>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:20px">
      <!-- Name + type -->
      <div>
        <label style="display:block;font-size:12px;font-weight:600;margin-bottom:6px">Name</label>
        <input id="layer-name" class="field-inp" placeholder="Layer name" style="width:100%;box-sizing:border-box;margin-bottom:16px">
        <div style="font-size:12px;font-weight:600;margin-bottom:8px">Layer type</div>
        ${[{key:'smart_tasks',label:'Smart based on Tasks',desc:'Automatically display tasks based on location and filters.'},
           {key:'smart_projects',label:'Smart based on Projects',desc:'Automatically display projects based on location and filters.'},
           {key:'classic',label:'Classic',desc:'Manually manage which tasks should appear on your Calendar.'}
          ].map((t,i)=>`
          <label style="display:flex;align-items:flex-start;gap:8px;margin-bottom:14px;cursor:pointer">
            <input type="radio" name="layer-type" value="${t.key}"${i===0?' checked':''} style="margin-top:2px">
            <div>
              <div style="font-size:12px;font-weight:600">${t.label}</div>
              <div style="font-size:11px;color:var(--text3);margin-top:2px">${t.desc}</div>
            </div>
          </label>`).join('')}
      </div>
      <!-- Tasks source -->
      <div>
        <div style="font-size:12px;font-weight:600;margin-bottom:8px">Tasks source</div>
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:12px;font-size:12px;cursor:pointer;color:var(--accent)">+ Select</div>
        <label style="display:flex;align-items:center;gap:8px;font-size:12px;cursor:pointer;margin-bottom:12px">
          <input type="checkbox"> Include tasks from Subfolders
        </label>
        <div style="font-size:12px;font-weight:600;margin-bottom:8px">Filters</div>
        <div style="font-size:12px;color:var(--accent);cursor:pointer">+ Filter</div>
      </div>
      <!-- Duration -->
      <div>
        <div style="font-size:12px;font-weight:600;margin-bottom:8px">Task duration to display</div>
        ${['Full duration','End date'].map((d,i)=>`
          <label style="display:flex;align-items:center;gap:8px;font-size:12px;cursor:pointer;margin-bottom:10px">
            <input type="radio" name="layer-dur" value="${d}"${i===0?' checked':''}> ${d}
          </label>`).join('')}
      </div>
    </div>
    <div style="display:flex;gap:10px;justify-content:flex-end;margin-top:20px;padding-top:16px;border-top:1px solid var(--border2)">
      <button class="btn ghost" onclick="this.closest('.modal-overlay').remove()">Cancel</button>
      <button class="btn" onclick="this.closest('.modal-overlay').remove()">Save</button>
    </div>
  </div>`;
  document.body.appendChild(modal);
  modal.addEventListener('click',e=>{if(e.target===modal)modal.remove();});
}""",
    "Replace showCalendars with full roadmap"
)

# ── 5. Add Calendar CSS ──────────────────────────────────────────────────────
rp(
    ".rpt-data-table tr:hover td{background:var(--surface)}",
    """.rpt-data-table tr:hover td{background:var(--surface)}
/* Calendar / Roadmap */
.cal-toolbar{display:flex;align-items:center;gap:8px;padding:10px 16px;border-bottom:1px solid var(--border2);flex-shrink:0;flex-wrap:wrap}
.cal-year-btn{font-size:14px;font-weight:700;cursor:pointer;padding:4px 10px;border-radius:6px;background:var(--surface);border:1px solid var(--border2)}
.cal-year-btn:hover{border-color:var(--accent)}
.cal-layout{display:flex;flex:1;overflow:hidden;min-height:0}
.cal-sidebar{width:160px;flex-shrink:0;border-right:1px solid var(--border2);overflow-y:auto;padding:10px 8px}
.cal-sidebar-head{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--text3);margin-bottom:8px;display:flex;align-items:center;justify-content:space-between}
.cal-side-name{font-size:12px;font-weight:600;padding:4px 6px;margin-bottom:4px}
.cal-side-row{padding:3px 0}
.cal-layer-check{display:inline-flex;width:14px;height:14px;border-radius:3px;border:2px solid;flex-shrink:0;align-items:center;justify-content:center;cursor:pointer;transition:.15s}
.cal-layer-check.on::after{content:'✓';font-size:9px;color:#fff;font-weight:700}
.cal-layer-filter{background:none;border:none;cursor:pointer;font-size:9px;color:var(--text3);margin-left:auto;padding:0 2px}
.cal-timeline-wrap{flex:1;overflow-x:auto;overflow-y:auto;display:flex;flex-direction:column}
.cal-quarter-row,.cal-month-row{display:flex;border-bottom:1px solid var(--border2);flex-shrink:0;background:var(--surface)}
.cal-quarter-cell{padding:4px 8px;font-size:11px;font-weight:700;color:var(--text3);border-right:1px solid var(--border2);white-space:nowrap;overflow:hidden}
.cal-month-cell{padding:4px 6px;font-size:11px;color:var(--text3);border-right:1px solid var(--border2);white-space:nowrap;overflow:hidden;min-width:60px}
.cal-rows-area{flex:1;overflow-y:auto}
.cal-assignee-group{margin-bottom:2px}
.cal-assignee-name{font-size:11px;font-weight:700;color:var(--text2);padding:8px 8px 2px;background:var(--bg);position:sticky;left:0}
.cal-row{position:relative;height:32px;border-bottom:1px solid var(--border2);min-width:100%}
.cal-bar{position:absolute;top:4px;height:24px;border-radius:4px;font-size:10px;font-weight:600;color:#fff;padding:0 6px;display:flex;align-items:center;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;cursor:pointer;transition:opacity .15s;z-index:2;min-width:4px}
.cal-bar:hover{opacity:.9;filter:brightness(1.05)}
.cal-today-line{position:absolute;top:0;bottom:0;width:2px;background:#3b82f6;z-index:3;pointer-events:none}
.cal-today-line::before{content:'';position:absolute;top:-1px;left:-4px;width:10px;height:10px;border-radius:50%;background:#3b82f6}""",
    "Add Calendar CSS"
)

# ── Safe write ────────────────────────────────────────────────────────────────
tmp = src + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(tmp, src)
print(f"\nDone — {orig} -> {len(content)} chars ({len(content)-orig:+d})")
