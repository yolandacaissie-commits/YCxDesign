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

# ── Add showDashboardTool + renderDashboard + widget helpers ──────────────────
# Insert after showCustomizeMenu
rp(
    """function showCustomizeMenu(){
  showStub('Customize Menu','⚙️','Drag-and-drop sidebar customization coming in the next update.');
}""",
    """function showCustomizeMenu(){
  showStub('Customize Menu','⚙️','Drag-and-drop sidebar customization coming in the next update.');
}

// ═════════════════ DASHBOARD TOOL ═════════════════
function showDashboardTool(tool){
  if(!tool){showStub('Dashboard','📊','No dashboard configured for this workspace.');return;}
  curDashboardId=tool.id;
  const ws=WORKSPACES.find(w=>w.id===tool.wsId)||{name:'Workspace'};
  setTopbar(tool.name, ws.name+' › Tools',[
    `<button class="btn ghost" style="font-size:12px" onclick="openWidgetGallery()">+ Add widget</button>`,
  ]);
  curView='dashboard';showView('dashboard');closeNavIfMobile();
  renderDashboard(tool);
}

function renderDashboard(tool){
  const el=document.getElementById('view-dashboard');
  const wsId=tool.wsId;
  const wsProjects=PROJECTS.filter(p=>(p.locations||[]).some(l=>l.workspaceId===wsId));
  const allTasks=wsProjects.flatMap(p=>p.tasks.map(t=>({...t,projName:p.name,projId:p.id})));

  // ── KPI helpers
  const total=wsProjects.length;
  const doneTasks=allTasks.filter(t=>t.status==='done').length;
  const totalTasks=allTasks.length;
  const pct=totalTasks?Math.round(doneTasks/totalTasks*100):0;
  const atRisk=wsProjects.filter(p=>{
    const open=p.tasks.filter(t=>t.status!=='done');
    return open.some(t=>t.priority==='critical'||t.priority==='high');
  });
  const onHold=wsProjects.filter(p=>p.tasks.every(t=>t.status==='todo'||t.status==='done'));

  // ── Status counts for donut
  const SC2={todo:'#94a3b8',in_progress:'#1AA6B7',review:'#f59e0b',done:'#22c55e',blocked:'#ef4444'};
  const SL2={todo:'Not Started',in_progress:'In Progress',review:'Review',done:'Done',blocked:'Blocked'};
  const statusCounts={};
  wsProjects.forEach(p=>{const s=p.tasks.filter(t=>t.status!=='done').length>0?'in_progress':'done';statusCounts[s]=(statusCounts[s]||0)+1;});
  wsProjects.forEach(p=>{
    const hasDone=p.tasks.filter(t=>t.status==='done').length===p.tasks.length&&p.tasks.length>0;
    const hasBlocked=p.tasks.some(t=>t.status==='blocked');
    const hasInProg=p.tasks.some(t=>t.status==='in_progress');
    const s=hasDone?'done':hasBlocked?'blocked':hasInProg?'in_progress':'todo';
    if(!statusCounts[s]) statusCounts[s]=0;
    statusCounts[s]++;
  });
  // Reset and recalculate cleanly
  const pStatus={todo:0,in_progress:0,review:0,done:0,blocked:0};
  wsProjects.forEach(p=>{
    const hasDone=p.tasks.length>0&&p.tasks.every(t=>t.status==='done');
    const hasBlocked=p.tasks.some(t=>t.status==='blocked');
    const hasInProg=p.tasks.some(t=>t.status==='in_progress'||t.status==='review');
    if(hasDone) pStatus.done++;
    else if(hasBlocked) pStatus.blocked++;
    else if(hasInProg) pStatus.in_progress++;
    else pStatus.todo++;
  });

  // ── LOB distribution (from p.lob or default)
  const lobCounts={};
  wsProjects.forEach(p=>{
    const lobs=(p.lob&&p.lob.length)?p.lob:['Other'];
    lobs.forEach(l=>{lobCounts[l]=(lobCounts[l]||0)+1;});
  });

  function makeMiniDonut(counts,colors,size=80){
    const entries=Object.entries(counts).filter(([,v])=>v>0);
    const tot=entries.reduce((s,[,v])=>s+v,0);if(!tot)return '<circle cx="50" cy="50" r="35" fill="#eee"/>';
    let angle=-Math.PI/2;
    const R=35,cx=50,cy=50;
    return entries.map(([k,v],i)=>{
      const a=(v/tot)*2*Math.PI;
      const x1=cx+R*Math.cos(angle),y1=cy+R*Math.sin(angle);
      angle+=a;
      const x2=cx+R*Math.cos(angle),y2=cy+R*Math.sin(angle);
      const large=a>Math.PI?1:0;
      const color=colors[k]||'#94a3b8';
      if(entries.length===1) return `<circle cx="${cx}" cy="${cy}" r="${R}" fill="${color}" fill-opacity=".85"/>`;
      return `<path d="M${cx},${cy} L${x1},${y1} A${R},${R} 0 ${large},1 ${x2},${y2} Z" fill="${color}" fill-opacity=".85"/>`;
    }).join('');
  }

  const STATUS_COLORS={todo:'#94a3b8',in_progress:'#1AA6B7',review:'#f59e0b',done:'#22c55e',blocked:'#ef4444'};
  const LOB_COLORS=['#1AA6B7','#8b5cf6','#f59e0b','#22c55e','#ef4444','#3b82f6','#ec4899'];
  const lobColorMap={};Object.keys(lobCounts).forEach((k,i)=>{lobColorMap[k]=LOB_COLORS[i%LOB_COLORS.length];});

  // ── AI Highlights text
  const openCount=allTasks.filter(t=>t.status!=='done').length;
  const critCount=allTasks.filter(t=>t.priority==='critical'&&t.status!=='done').length;
  const aiText=`This workspace has <strong>${total} projects</strong> with <strong>${openCount} open tasks</strong> (${pct}% complete). ${critCount>0?`<strong>${critCount} critical priority tasks</strong> require immediate attention. `:''}${atRisk.length>0?`<strong>${atRisk.length} project${atRisk.length>1?'s':''}</strong> have high-priority open tasks. `:''}${pStatus.done>0?`<strong>${pStatus.done} project${pStatus.done>1?'s are':' is'}</strong> fully complete.`:''}`;

  el.innerHTML=`
  <div class="dash-header">
    <div class="dash-title">${tool.name}</div>
    <div style="display:flex;gap:8px">
      <button class="btn ghost" style="font-size:12px" onclick="openWidgetGallery()">+ Add widget</button>
    </div>
  </div>
  <div class="dash-grid">

    <!-- AI Highlights -->
    <div class="dash-widget wide">
      <div class="dash-widget-title">⚡ AI Highlights</div>
      <div style="font-size:13px;line-height:1.7;color:var(--text2)">${aiText}</div>
      ${critCount>0?`<div style="margin-top:10px;padding:8px 12px;background:#ef444411;border-radius:8px;border:1px solid #ef444433;font-size:12px;color:#ef4444;font-weight:500">
        ${critCount} critical task${critCount>1?'s':''}  pending — review recommended
      </div>`:''}
    </div>

    <!-- KPIs row -->
    <div class="dash-widget">
      <div class="dash-widget-title">📁 Project Count</div>
      <div class="dash-kpi">${total}</div>
      <div class="dash-kpi-label">Total projects in workspace</div>
    </div>
    <div class="dash-widget">
      <div class="dash-widget-title">✅ Task Progress</div>
      <div class="dash-kpi">${pct}%</div>
      <div class="dash-kpi-label">${doneTasks} of ${totalTasks} tasks complete</div>
      <div style="margin-top:10px;height:6px;background:var(--border2);border-radius:3px;overflow:hidden">
        <div style="height:100%;width:${pct}%;background:var(--accent);border-radius:3px;transition:width .4s"></div>
      </div>
    </div>
    <div class="dash-widget">
      <div class="dash-widget-title">⚠️ At Risk</div>
      <div class="dash-kpi" style="color:${atRisk.length>0?'#ef4444':'#22c55e'}">${atRisk.length}</div>
      <div class="dash-kpi-label">Projects with critical/high tasks open</div>
    </div>

    <!-- Project Status Donut -->
    <div class="dash-widget">
      <div class="dash-widget-title">📊 Project Status</div>
      <div style="display:flex;align-items:center;gap:14px">
        <svg viewBox="0 0 100 100" width="80" height="80">
          ${makeMiniDonut(pStatus,STATUS_COLORS)}
          <circle cx="50" cy="50" r="20" fill="var(--surface)"/>
          <text x="50" y="55" text-anchor="middle" font-size="14" font-weight="bold" fill="var(--text)">${total}</text>
        </svg>
        <div style="flex:1">
          ${Object.entries(pStatus).filter(([,v])=>v>0).map(([k,v])=>`
          <div style="display:flex;align-items:center;gap:6px;font-size:11px;margin-bottom:4px">
            <span style="width:8px;height:8px;border-radius:50%;background:${STATUS_COLORS[k]};flex-shrink:0"></span>
            <span style="flex:1;color:var(--text2)">${k.replace('_',' ')}</span>
            <span style="font-weight:600">${v}</span>
          </div>`).join('')}
        </div>
      </div>
    </div>

    <!-- Projects by LOB -->
    ${Object.keys(lobCounts).length>1?`<div class="dash-widget">
      <div class="dash-widget-title">🏷️ Projects by LOB</div>
      <div style="display:flex;align-items:center;gap:14px">
        <svg viewBox="0 0 100 100" width="80" height="80">
          ${makeMiniDonut(lobCounts,lobColorMap)}
          <circle cx="50" cy="50" r="20" fill="var(--surface)"/>
        </svg>
        <div style="flex:1">
          ${Object.entries(lobCounts).slice(0,5).map(([k,v])=>`
          <div style="display:flex;align-items:center;gap:6px;font-size:11px;margin-bottom:4px">
            <span style="width:8px;height:8px;border-radius:50%;background:${lobColorMap[k]};flex-shrink:0"></span>
            <span style="flex:1;color:var(--text2);overflow:hidden;text-overflow:ellipsis;white-space:nowrap">${k}</span>
            <span style="font-weight:600">${v}</span>
          </div>`).join('')}
        </div>
      </div>
    </div>`:''}

    <!-- At Risk Projects table -->
    ${atRisk.length?`<div class="dash-widget wide">
      <div class="dash-widget-title">🚨 At Risk Projects</div>
      ${atRisk.slice(0,5).map(p=>{
        const critT=p.tasks.filter(t=>t.priority==='critical'&&t.status!=='done');
        const u=USERS.find(u=>u.id===p.owner)||USERS[0];
        return `<div class="dash-widget-row" style="cursor:pointer" onclick="openProject('${p.id}')">
          <span class="dot" style="background:#ef4444"></span>
          <span style="flex:1;font-weight:500;font-size:12px">${p.name}</span>
          <span style="font-size:11px;color:#ef4444;font-weight:600">${critT.length} critical</span>
          <span style="font-size:11px;color:var(--text3);margin-left:8px">${u.name.split(' ')[0]}</span>
        </div>`;}).join('')}
    </div>`:''}

    <!-- Task list -->
    <div class="dash-widget wide">
      <div class="dash-widget-title">📋 Recent Tasks — My Work</div>
      ${allTasks.filter(t=>t.assignee===USERS[0].id&&t.status!=='done').slice(0,6).map(t=>`
        <div class="dash-widget-row" style="cursor:pointer" onclick="openProject('${t.projId}');setTimeout(()=>openTask('${t.id}'),200)">
          <span class="dot" style="background:${SC[t.status]||'#94a3b8'}"></span>
          <span style="flex:1;font-size:12px">${t.title}</span>
          <span style="font-size:11px;color:var(--text3)">${t.projName}</span>
          <span class="pill" style="font-size:10px;background:${SC[t.status]||'#94a3b8'}22;color:${SC[t.status]||'#94a3b8'};border:1px solid ${SC[t.status]||'#94a3b8'}44;margin-left:6px">${SL[t.status]}</span>
        </div>`).join('')||'<div style="font-size:12px;color:var(--text3);padding:8px 0">No open tasks assigned to you in this workspace</div>'}
    </div>

  </div>`;
}

function openWidgetGallery(){
  const widgets=[
    {key:'ai',label:'AI Highlights',desc:'AI-generated workspace summary',badge:'New'},
    {key:'kpi_projects',label:'Project count',desc:'Total number of projects',badge:'Indicator'},
    {key:'kpi_tasks',label:'Task count',desc:'Total number of tasks',badge:'Indicator'},
    {key:'kpi_progress',label:'Progress',desc:'Percentage of completed tasks',badge:'Indicator'},
    {key:'kpi_atrisk',label:'At Risk',desc:'Projects with critical tasks open',badge:'Indicator'},
    {key:'donut_status',label:'Projects by status',desc:'Donut chart by project status',badge:'Donut'},
    {key:'donut_lob',label:'Projects by LOB',desc:'Donut chart by line of business',badge:'Donut'},
    {key:'list_mytasks',label:'My tasks',desc:'All active tasks assigned to me',badge:'List'},
    {key:'list_tasks',label:'Task list',desc:'All tasks with details',badge:'List'},
    {key:'list_projects',label:'Project list',desc:'All projects with status',badge:'List'},
    {key:'table_atrisk',label:'At Risk projects',desc:'Table of high-priority open projects',badge:'Table'},
  ];
  const badge_colors={New:'#22c55e',Indicator:'#8b5cf6',Donut:'#f59e0b',List:'#1AA6B7',Table:'#3b82f6'};
  const modal=document.createElement('div');
  modal.className='modal-overlay';
  modal.innerHTML=`<div class="modal" style="max-width:720px;width:95vw">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
      <div style="font-size:16px;font-weight:700">Add widget</div>
      <button onclick="this.closest('.modal-overlay').remove()" style="background:none;border:none;font-size:20px;cursor:pointer;color:var(--text3)">&times;</button>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px">
      ${widgets.map(w=>`
        <div onclick="this.closest('.modal-overlay').remove()" style="padding:14px;background:var(--bg);border:1px solid var(--border2);border-radius:10px;cursor:pointer;transition:.15s" onmouseover="this.style.borderColor='var(--accent)'" onmouseout="this.style.borderColor='var(--border2)'">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px">
            <div style="font-size:13px;font-weight:600">${w.label}</div>
            <span style="font-size:9px;font-weight:700;padding:2px 6px;border-radius:8px;background:${badge_colors[w.badge]||'#94a3b8'}22;color:${badge_colors[w.badge]||'#94a3b8'}">${w.badge}</span>
          </div>
          <div style="font-size:11px;color:var(--text3)">${w.desc}</div>
        </div>`).join('')}
    </div>
    <div style="margin-top:14px;padding-top:14px;border-top:1px solid var(--border2);font-size:12px;color:var(--text3)">
      Widget data updates automatically from your workspace. Click any widget to add it to the current dashboard.
    </div>
  </div>`;
  document.body.appendChild(modal);
  modal.addEventListener('click',e=>{if(e.target===modal)modal.remove();});
}""",
    "Add showDashboardTool + renderDashboard + openWidgetGallery"
)

# ── JS validation ─────────────────────────────────────────────────────────────
tmp = src + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(tmp, src)
print(f"\nDone — {orig} -> {len(content)} chars ({len(content)-orig:+d})")
