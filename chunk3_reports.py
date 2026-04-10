#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, re

src = '/home/user/YCxDesign/team-nexus-v3.html'
content = open(src, encoding='utf-8').read()
orig = len(content)

def rp(old, new, label):
    global content
    assert old in content, f"ANCHOR NOT FOUND: {label}\n{repr(old[:80])}"
    content = content.replace(old, new, 1)
    print(f"  OK: {label}")

# ── 1. Add SAVED_REPORTS data after WORKSPACE_TOOLS ──────────────────────────
rp(
    "let curDashboardId=null;",
    """let curDashboardId=null;
let SAVED_REPORTS=[
  {id:'sr1',name:'All Project Status Report',type:'project_status',basedOn:'projects',
   wsId:'ws1',sharing:'Shared',created:'2025-09-11',updated:'2025-11-18',layout:'table',
   groupBy:'status',filters:[],desc:'Report on projects'},
  {id:'sr2',name:'Monthly Time Entries',type:'time_entries',basedOn:'time_entries',
   wsId:'ws4',sharing:'Shared',created:'2025-10-15',updated:'2025-12-10',layout:'table',
   groupBy:'assignee',filters:[],desc:'Report on entries'},
  {id:'sr3',name:'Relearn it',type:'custom',basedOn:'projects',
   wsId:'ws2',sharing:'Private',created:'2025-09-23',updated:'2025-09-23',layout:'table',
   groupBy:null,filters:[],desc:'Report on projects'},
  {id:'sr4',name:'Time Entries This Month',type:'time_entries',basedOn:'time_entries',
   wsId:'ws3',sharing:'Shared',created:'2025-12-28',updated:'2025-12-28',layout:'table',
   groupBy:'date',filters:[],desc:'Report on entries'},
];
let curReportId=null;""",
    "Add SAVED_REPORTS"
)

# ── 2. Add view-reports div ───────────────────────────────────────────────────
rp(
    '<div id="view-dashboard" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>',
    '''<div id="view-dashboard" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>
    <div id="view-reports" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>
    <div id="view-report-viewer" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>''',
    "Add view-reports + view-report-viewer"
)

# ── 3. Update showView list ───────────────────────────────────────────────────
rp(
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt','inbox','stream','created-by-me','starred','dashboard'].forEach",
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt','inbox','stream','created-by-me','starred','dashboard','reports','report-viewer'].forEach",
    "Update showView list"
)

# ── 4. Replace showReports() with full implementation ────────────────────────
rp(
    """function showReports(){
  curView='stub';setTopbar('Reports','Analytics and reporting',[]);showView('stub');closeNavIfMobile();
  document.getElementById('view-stub').innerHTML=`<div class="stub-view topo-bg">
    <div class="stub-icon">📊</div><div class="stub-title">Reports</div>
    <div class="stub-sub">Track progress, velocity and team performance. Choose a data source to get started.</div>
    <div class="stub-ds-row">
      <div class="stub-ds-btn on">Entire account</div>
      ${WORKSPACES.map(ws=>`<div class="stub-ds-btn" onclick="this.parentElement.querySelectorAll('.stub-ds-btn').forEach(b=>b.classList.remove('on'));this.classList.add('on')">${ws.name}</div>`).join('')}
    </div>
  </div>`;
}""",
    """function showReports(){
  curView='reports';setTopbar('Reports','Build and manage reports across your workspaces',[
    `<button class="btn" onclick="openCreateReportModal()">+ New report</button>`,
  ]);
  showView('reports');closeNavIfMobile();renderReportsHome();
}
function renderReportsHome(){
  const el=document.getElementById('view-reports');
  const templates=[
    {key:'custom',label:'Custom report',icon:'➕',desc:'Build from scratch'},
    {key:'active_tasks',label:'Active tasks by assignee',icon:'👤',desc:'Tasks grouped by person'},
    {key:'weekly_status',label:'Weekly project status',icon:'📅',desc:'Project health this week'},
    {key:'overdue_tasks',label:'Overdue tasks by assignee',icon:'⚠️',desc:'Past-due task list'},
    {key:'projects_due',label:'Projects due this month',icon:'📆',desc:'Upcoming deadlines'},
    {key:'unassigned',label:'Unassigned tasks',icon:'❓',desc:'Tasks with no owner'},
    {key:'time_spent',label:'Time spent this week',icon:'⏱️',desc:'Timesheet summary'},
    {key:'team_util',label:'Team utilization',icon:'📊',desc:'Capacity overview'},
  ];
  el.innerHTML=`
  <div style="padding:24px">
    <div style="font-size:13px;font-weight:700;color:var(--text2);margin-bottom:14px;cursor:pointer" onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'grid':'none'">
      &#8964; Create a report
    </div>
    <div class="rpt-template-grid" style="margin-bottom:28px">
      ${templates.map(t=>`
        <div class="rpt-template-card" onclick="openCreateReportModal('${t.key}')">
          <div class="rpt-tmpl-icon">${t.icon}</div>
          <div class="rpt-tmpl-label">${t.label}</div>
          <div class="rpt-tmpl-desc">${t.desc}</div>
        </div>`).join('')}
    </div>
    <div class="rpt-list-header">
      <div style="flex:3">Name</div>
      <div>Created by</div>
      <div>Space</div>
      <div>Sharing</div>
      <div>Created date</div>
      <div>Last updated</div>
    </div>
    ${SAVED_REPORTS.map(r=>{
      const ws=WORKSPACES.find(w=>w.id===r.wsId)||{name:'Personal'};
      return `<div class="rpt-list-row" onclick="openReport('${r.id}')">
        <div style="flex:3;display:flex;align-items:flex-start;gap:8px;flex-direction:column">
          <span style="font-weight:600;color:var(--accent)">${r.name}</span>
          <span style="font-size:10px;color:var(--text3)">${r.desc}</span>
        </div>
        <div style="font-size:12px;color:var(--text2)">Me</div>
        <div style="font-size:12px;color:var(--accent);font-weight:500">${ws.name}</div>
        <div><span class="rpt-sharing-badge ${r.sharing.toLowerCase()}">${r.sharing}</span></div>
        <div style="font-size:12px;color:var(--text3)">${r.created}</div>
        <div style="font-size:12px;color:var(--accent)">${r.updated}</div>
      </div>`;}).join('')}
  </div>`;
}
function openCreateReportModal(templateKey){
  const templates={
    active_tasks:{name:'Active tasks by assignee',basedOn:'tasks',groupBy:'assignee'},
    weekly_status:{name:'Weekly project status',basedOn:'projects',groupBy:'status'},
    overdue_tasks:{name:'Overdue tasks by assignee',basedOn:'tasks',groupBy:'assignee',filters:['overdue']},
    projects_due:{name:'Projects due this month',basedOn:'projects',groupBy:null},
    unassigned:{name:'Unassigned tasks',basedOn:'tasks',groupBy:null,filters:['unassigned']},
    time_spent:{name:'Time spent this week',basedOn:'time_entries',groupBy:'assignee'},
    team_util:{name:'Team utilization',basedOn:'time_entries',groupBy:'assignee'},
  };
  const tmpl=templates[templateKey]||{name:'',basedOn:'tasks',groupBy:null};
  const modal=document.createElement('div');
  modal.className='modal-overlay';
  modal.innerHTML=`<div class="modal" style="max-width:780px;width:96vw;padding:0;overflow:hidden">
    <div style="display:flex;height:520px">
      <!-- Left: type picker -->
      <div style="width:220px;border-right:1px solid var(--border2);padding:16px;overflow-y:auto;background:var(--bg);flex-shrink:0">
        <div style="font-size:13px;font-weight:700;margin-bottom:12px">Title</div>
        <input id="rpt-title-inp" class="field-inp" placeholder="Report name" value="${tmpl.name}" style="width:100%;margin-bottom:16px;box-sizing:border-box">
        <div style="font-size:11px;font-weight:700;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:8px">Type</div>
        <input class="field-inp" placeholder="Search..." style="width:100%;margin-bottom:8px;box-sizing:border-box;font-size:11px">
        ${[{key:'custom',label:'Custom report'},{key:'active_tasks',label:'Active tasks by assignee'},{key:'weekly_status',label:'Weekly project status'},{key:'overdue_tasks',label:'Overdue tasks by assignee'},{key:'projects_due',label:'Projects due this month'},{key:'unassigned',label:'Unassigned tasks'},{key:'time_spent',label:'Time spent this week'},{key:'team_util',label:'Team utilization'}].map(t=>`
          <div class="rpt-type-opt${templateKey===t.key?' on':''}" onclick="this.parentElement.querySelectorAll('.rpt-type-opt').forEach(x=>x.classList.remove('on'));this.classList.add('on');document.getElementById('rpt-title-inp').value=document.getElementById('rpt-title-inp').value||'${t.label}'">${t.label}</div>`).join('')}
      </div>
      <!-- Middle: config -->
      <div style="flex:1;padding:20px;overflow-y:auto">
        <div style="font-size:13px;font-weight:700;margin-bottom:12px">Location</div>
        <div style="display:flex;align-items:center;gap:8px;margin-bottom:16px;padding:8px 12px;background:var(--bg);border:1px solid var(--border2);border-radius:8px;font-size:12px">
          <span>🏠</span><span>Personal</span>
        </div>
        <div style="font-size:13px;font-weight:700;margin-bottom:8px">Data source</div>
        <div style="font-size:12px;color:var(--accent);margin-bottom:16px;cursor:pointer">Select project, folder or space</div>
        <div style="font-size:13px;font-weight:700;margin-bottom:8px">Based on</div>
        <div style="display:flex;flex-direction:column;gap:6px;margin-bottom:16px">
          ${['projects','tasks','time_entries'].map(b=>`
          <label style="display:flex;align-items:center;gap:8px;font-size:12px;cursor:pointer">
            <input type="radio" name="rpt-based" value="${b}"${tmpl.basedOn===b?' checked':b==='tasks'&&!tmpl.basedOn?' checked':''}> ${b.replace('_',' ').replace(/\b\w/g,c=>c.toUpperCase())}
          </label>`).join('')}
        </div>
        <div style="font-size:13px;font-weight:700;margin-bottom:8px">Layout</div>
        <div style="display:flex;gap:6px;margin-bottom:16px">
          ${['Table','Column'].map(l=>`
          <label style="display:flex;align-items:center;gap:8px;font-size:12px;cursor:pointer">
            <input type="radio" name="rpt-layout" value="${l.toLowerCase()}"${l==='Table'?' checked':''}> ${l}
          </label>`).join('')}
        </div>
        <div style="font-size:13px;font-weight:700;margin-bottom:8px">Group by</div>
        <div style="display:flex;gap:6px;flex-wrap:wrap">
          ${['Status group','Assignee','Priority','Due date'].map(g=>`
          <span class="pill" style="cursor:pointer;padding:4px 10px;background:var(--abg);color:var(--accent);border:1px solid var(--accent)33;font-size:11px">${g}</span>`).join('')}
          <span class="pill" style="cursor:pointer;padding:4px 10px;background:transparent;color:var(--text3);border:1px dashed var(--border2);font-size:11px">+ Add</span>
        </div>
      </div>
      <!-- Right: filters -->
      <div style="width:200px;border-left:1px solid var(--border2);padding:16px;overflow-y:auto;flex-shrink:0">
        <div style="font-size:13px;font-weight:700;margin-bottom:12px">Filters</div>
        ${['Custom item type','Status','Assignee','Tasks to do','Approvals','Task type','Importance','Effort','Created date','Start date','Due date','Completed date','Last modified date','Author'].map(f=>`
          <div style="display:flex;align-items:center;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--border2);cursor:pointer;font-size:12px;color:var(--text2)" onclick="this.querySelector('.rpt-filter-exp').classList.toggle('open')">
            <span>${f}</span><span class="rpt-filter-exp">›</span>
          </div>`).join('')}
      </div>
    </div>
    <div style="padding:14px 20px;border-top:1px solid var(--border2);display:flex;gap:10px;justify-content:flex-end">
      <button class="btn ghost" onclick="this.closest('.modal-overlay').remove()">Cancel</button>
      <button class="btn" onclick="saveNewReport(this)">Create</button>
    </div>
  </div>`;
  document.body.appendChild(modal);
  modal.addEventListener('click',e=>{if(e.target===modal)modal.remove();});
}
function saveNewReport(btn){
  const modal=btn.closest('.modal-overlay');
  const name=modal.querySelector('#rpt-title-inp').value||'New Report';
  const basedOn=modal.querySelector('[name=rpt-based]:checked')?.value||'tasks';
  const id='sr'+Date.now();
  SAVED_REPORTS.unshift({id,name,type:'custom',basedOn,wsId:WORKSPACES[0].id,
    sharing:'Private',created:new Date().toISOString().slice(0,10),
    updated:new Date().toISOString().slice(0,10),layout:'table',groupBy:'status',filters:[],desc:'Report on '+basedOn});
  modal.remove();
  openReport(id);
}
function openReport(reportId){
  const r=SAVED_REPORTS.find(r=>r.id===reportId);if(!r)return;
  curReportId=reportId;
  curView='report-viewer';
  setTopbar(r.name,'',[
    `<button class="btn ghost" style="font-size:12px" onclick="openCreateReportModal()">Edit</button>`,
    `<button class="btn ghost" style="font-size:12px">Share</button>`,
    `<button class="btn ghost" style="font-size:12px">Subscribe</button>`,
    `<button class="btn" style="font-size:12px">Export as Excel</button>`,
  ]);
  showView('report-viewer');renderReportViewer(r);
}
function renderReportViewer(r){
  const el=document.getElementById('view-report-viewer');
  const ws=WORKSPACES.find(w=>w.id===r.wsId);
  let rows=[];
  if(r.basedOn==='projects'){
    rows=PROJECTS.map(p=>{
      const done=p.tasks.filter(t=>t.status==='done').length;
      const total=p.tasks.length;
      const pct=total?Math.round(done/total*100):0;
      const owner=USERS.find(u=>u.id===(p.owner||1))||USERS[0];
      const hasRisk=p.tasks.some(t=>t.priority==='critical'&&t.status!=='done');
      return {
        title:p.name,
        status:p.tasks.every(t=>t.status==='done')&&total>0?'Completed':p.tasks.some(t=>t.status==='in_progress')?'In Progress - On Track':'Not Started',
        start:p.tasks.reduce((m,t)=>t.start&&(!m||t.start<m)?t.start:m,null),
        due:p.tasks.reduce((m,t)=>t.end&&(!m||t.end>m)?t.end:m,null),
        owner:owner.name,
        contractValue:p.contractValue||null,
        progress:pct,
        risk:hasRisk,
      };
    });
  } else if(r.basedOn==='tasks'){
    rows=PROJECTS.flatMap(p=>p.tasks.map(t=>({
      title:t.title,status:t.status,priority:t.priority,
      assignee:(USERS.find(u=>u.id===t.assignee)||USERS[0]).name,
      project:p.name,due:t.dueDate||null,
    })));
  } else {
    rows=TIMESHEET_ENTRIES.slice(-30).map(e=>{
      const u=USERS.find(u=>u.id===e.userId)||USERS[0];
      const t=PROJECTS.flatMap(p=>p.tasks).find(t=>t.id===e.taskId);
      return {user:u.name,task:t?t.title:'Unknown',date:e.date,hours:e.hours,activity:e.activity};
    });
  }
  const SC2={todo:'#94a3b8',in_progress:'#1AA6B7',review:'#f59e0b',done:'#22c55e',blocked:'#ef4444','Not Started':'#94a3b8','In Progress - On Track':'#1AA6B7','Completed':'#22c55e'};
  const cols=r.basedOn==='projects'?['title','status','start','due','owner','contractValue','progress','risk']:
             r.basedOn==='tasks'?['title','status','priority','assignee','project','due']:
             ['user','task','date','hours','activity'];
  const colLabels={title:'Title',status:'Status',start:'Start date',due:'Due date',owner:'Owner',
    contractValue:'Contract Value, $',progress:'Progress',risk:'Project risk',
    priority:'Priority',assignee:'Assignee',project:'Project',hours:'Hours',
    user:'User',task:'Task',date:'Date',activity:'Activity'};
  el.innerHTML=`
  <div style="padding:12px 20px;border-bottom:1px solid var(--border2);display:flex;align-items:center;gap:12px;font-size:12px;color:var(--text3)">
    <button class="btn ghost" style="font-size:11px" onclick="showReports()">← Reports</button>
    <span>Updated at ${new Date().toLocaleTimeString('en-GB',{hour:'2-digit',minute:'2-digit'})}</span>
  </div>
  <div style="padding:0 20px 20px;overflow-x:auto">
    <table class="rpt-data-table">
      <thead><tr>${cols.map(c=>`<th>${colLabels[c]||c}</th>`).join('')}</tr></thead>
      <tbody>
        ${rows.slice(0,30).map((row,i)=>`<tr>
          ${cols.map(c=>{
            const v=row[c];
            if(c==='status') return `<td><span class="pill" style="background:${(SC2[v]||'#94a3b8')}22;color:${SC2[v]||'#94a3b8'};border:1px solid ${(SC2[v]||'#94a3b8')}44;font-size:10px">${v||'—'}</span></td>`;
            if(c==='progress') return `<td><div style="display:flex;align-items:center;gap:6px"><div style="flex:1;height:5px;background:var(--border2);border-radius:3px;overflow:hidden"><div style="height:100%;width:${v||0}%;background:var(--accent)"></div></div><span style="font-size:11px;color:var(--text3);width:28px">${v||0}%</span></div></td>`;
            if(c==='risk') return `<td style="font-size:11px;color:${v?'#ef4444':'#22c55e'}">${v?'At Risk':'Low'}</td>`;
            if(c==='contractValue') return `<td style="font-size:12px">${v?'$'+v.toLocaleString():'—'}</td>`;
            if(c==='start'||c==='due'||c==='date') return `<td style="font-size:11px;color:var(--text3)">${v?new Date(v).toLocaleDateString('en-GB',{day:'2-digit',month:'short',year:'numeric'}):'—'}</td>`;
            return `<td style="font-size:12px">${v!==null&&v!==undefined?v:'—'}</td>`;
          }).join('')}
        </tr>`).join('')}
      </tbody>
    </table>
  </div>`;
}""",
    "Replace showReports + add full reports implementation"
)

# ── 5. Add Reports CSS ────────────────────────────────────────────────────────
rp(
    ".stream-time{font-size:11px;color:var(--text3)}",
    """.stream-time{font-size:11px;color:var(--text3)}
/* Reports */
.rpt-template-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px}
.rpt-template-card{background:var(--surface);border:1px solid var(--border2);border-radius:10px;padding:14px 12px;cursor:pointer;transition:.15s;text-align:center}
.rpt-template-card:hover{border-color:var(--accent);box-shadow:0 2px 10px rgba(26,166,183,.1)}
.rpt-tmpl-icon{font-size:22px;margin-bottom:6px}
.rpt-tmpl-label{font-size:11px;font-weight:600;color:var(--text);margin-bottom:3px}
.rpt-tmpl-desc{font-size:10px;color:var(--text3)}
.rpt-list-header{display:flex;align-items:center;gap:16px;padding:8px 0;border-bottom:2px solid var(--border2);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--text3)}
.rpt-list-header > div,.rpt-list-row > div{flex:1;min-width:80px}
.rpt-list-row{display:flex;align-items:flex-start;gap:16px;padding:14px 0;border-bottom:1px solid var(--border2);cursor:pointer;transition:.1s}
.rpt-list-row:hover{background:var(--surface);margin:0 -8px;padding-left:8px;padding-right:8px;border-radius:8px}
.rpt-sharing-badge{font-size:10px;padding:2px 8px;border-radius:8px;font-weight:600}
.rpt-sharing-badge.shared{background:#22c55e22;color:#22c55e}
.rpt-sharing-badge.private{background:#94a3b822;color:#94a3b8}
.rpt-type-opt{padding:7px 10px;border-radius:7px;font-size:12px;cursor:pointer;color:var(--text2);transition:.15s}
.rpt-type-opt:hover{background:var(--abg)}
.rpt-type-opt.on{background:var(--abg);color:var(--accent);font-weight:600;border-left:3px solid var(--accent);padding-left:7px}
.rpt-filter-exp{transition:.2s}
.rpt-filter-exp.open{transform:rotate(90deg);display:inline-block}
.rpt-data-table{width:100%;border-collapse:collapse;margin-top:12px;font-size:12px}
.rpt-data-table th{text-align:left;padding:8px 12px;font-size:11px;font-weight:700;color:var(--text3);border-bottom:2px solid var(--border2);text-transform:uppercase;letter-spacing:.4px;white-space:nowrap}
.rpt-data-table td{padding:10px 12px;border-bottom:1px solid var(--border2);vertical-align:middle;color:var(--text)}
.rpt-data-table tr:hover td{background:var(--surface)}""",
    "Add Reports CSS"
)

# ── Safe write ────────────────────────────────────────────────────────────────
tmp = src + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(tmp, src)
print(f"\nDone — {orig} -> {len(content)} chars ({len(content)-orig:+d})")
