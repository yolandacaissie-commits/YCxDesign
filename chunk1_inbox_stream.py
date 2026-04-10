#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, tempfile

src = '/home/user/YCxDesign/team-nexus-v3.html'
content = open(src, encoding='utf-8').read()
orig = len(content)

def rp(old, new, label):
    global content
    assert old in content, f"ANCHOR NOT FOUND: {label}"
    content = content.replace(old, new, 1)
    print(f"  OK: {label}")

# ── 1. Add ACTIVITY_LOG + STARRED_ITEMS after TASK_BILLABLE ──────────────────
rp(
    "let TASK_BILLABLE={}; // kept for compat; per-entry billable now lives on TIMESHEET_ENTRIES",
    """let TASK_BILLABLE={}; // kept for compat; per-entry billable now lives on TIMESHEET_ENTRIES

// ── ACTIVITY LOG ─────────────────────────────────────────────────────────────
const _aln=Date.now();
let ACTIVITY_LOG=[
  {id:'al001',type:'task_assigned',fromUser:2,toUser:1,projId:'p1',taskId:'t7',
   msg:'Sarah Chen assigned you to <strong>"Launch &amp; Deploy"</strong>',
   projName:'Client Portal Redesign',ts:_aln-7*3600000,read:false},
  {id:'al002',type:'status_changed',fromUser:3,projId:'p2',taskId:'t8',
   msg:'Marcus Johnson changed <strong>"Performance Audit"</strong> to <em>In Progress</em>',
   projName:'Mobile App Refresh',ts:_aln-5*3600000,read:false},
  {id:'al003',type:'mention',fromUser:4,projId:'p1',taskId:'t2',
   msg:'Priya Nair mentioned you in <strong>"UI/UX Design Concepts"</strong>: <em>"@Yolanda can you review the mockups before EOD?"</em>',
   projName:'Client Portal Redesign',ts:_aln-3*3600000,read:false},
  {id:'al004',type:'task_ready',fromUser:null,projId:'p1',taskId:'t5',
   msg:'All predecessors complete \u2014 <strong>"Backend API Dev"</strong> is now ready to start',
   projName:'Client Portal Redesign',ts:_aln-2*3600000,read:false},
  {id:'al005',type:'ai_suggestion',fromUser:null,projId:'p3',taskId:null,
   msg:'Delta AI: 3 tasks in <strong>"Infrastructure Modernization"</strong> are approaching their deadlines. Consider adjusting timelines or reassigning.',
   projName:'Infrastructure Modernization',ts:_aln-90*60000,read:false},
  {id:'al006',type:'task_assigned',fromUser:5,toUser:1,projId:'p3',taskId:null,
   msg:'Dev Patel added you as a watcher on <strong>"Infrastructure Modernization"</strong>',
   projName:'Infrastructure Modernization',ts:_aln-60*60000,read:true},
  {id:'al007',type:'report_ready',fromUser:null,projId:null,taskId:null,
   msg:'Your <strong>"All Project Status Report"</strong> has finished generating and is ready for review',
   projName:null,ts:_aln-45*60000,read:true},
  {id:'al008',type:'comment',fromUser:6,projId:'p2',taskId:'t9',
   msg:'Ama Owusu commented on <strong>"Redesign Onboarding"</strong>: <em>"Updated the interaction flows \u2014 much cleaner now"</em>',
   projName:'Mobile App Refresh',ts:_aln-30*60000,read:true},
  {id:'al009',type:'project_created',fromUser:2,projId:'p8',taskId:null,
   msg:'Sarah Chen created a new project in <strong>Client Accounts</strong>',
   projName:'Client Accounts',ts:_aln-15*60000,read:true},
  {id:'al010',type:'task_created',fromUser:3,projId:'p1',taskId:null,
   msg:'Marcus Johnson added 3 new tasks to <strong>"Client Portal Redesign"</strong>',
   projName:'Client Portal Redesign',ts:_aln-5*60000,read:false},
  {id:'al011',type:'mention',fromUser:7,projId:'p4',taskId:null,
   msg:'Ankit Bhandari mentioned you: <em>"@Yolanda approval needed before we close the month"</em>',
   projName:'Q4 Financial Close',ts:_aln-2*60000,read:false},
  {id:'al012',type:'task_assigned',fromUser:8,toUser:1,projId:'p8',taskId:null,
   msg:'Raja Aishah assigned you to review the <strong>Aria Systems</strong> contract renewal',
   projName:'Client Accounts',ts:_aln-60000,read:false},
];
let STARRED_ITEMS={projects:{},folders:{},tasks:{}};""",
    "ACTIVITY_LOG + STARRED_ITEMS after TASK_BILLABLE"
)

# ── 2. Wire nav items (Created by me, Stream, Starred tasks, Customize menu) ──
rp(
    '<div class="nav-item" style="font-size:12px"><span class="nav-icon"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>Created by me</div>',
    '<div class="nav-item" style="font-size:12px" onclick="showCreatedByMe()"><span class="nav-icon"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>Created by me</div>',
    "Wire Created by me"
)
rp(
    '<div class="nav-item" style="font-size:12px"><span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></span>Stream</div>',
    '<div class="nav-item" style="font-size:12px" onclick="showStream()"><span class="nav-icon"><svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg></span>Stream</div>',
    "Wire Stream"
)
rp(
    '<div class="nav-item" style="font-size:12px"><span class="nav-icon"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>Starred tasks</div>',
    '<div class="nav-item" style="font-size:12px" onclick="showStarred()"><span class="nav-icon"><svg viewBox="0 0 24 24"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></span>Starred tasks</div>',
    "Wire Starred tasks"
)
rp(
    '<div class="nav-item" style="font-size:12px" onclick="showSettings()"><span class="nav-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06-.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>Customize menu</div>',
    '<div class="nav-item" style="font-size:12px" onclick="showCustomizeMenu()"><span class="nav-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06-.06a2 2 0 0 1-2.83-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 2.83-2.83l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg></span>Customize menu</div>',
    "Wire Customize menu"
)

# ── 3. Add dedicated view divs ────────────────────────────────────────────────
rp(
    '<div id="view-stub" style="display:none;position:absolute;inset:0"></div>',
    '''<div id="view-inbox" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>
    <div id="view-stream" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>
    <div id="view-created-by-me" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>
    <div id="view-starred" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>
    <div id="view-stub" style="display:none;position:absolute;inset:0"></div>''',
    "Add view divs"
)

# ── 4. Update showView() ──────────────────────────────────────────────────────
rp(
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt'].forEach",
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt','inbox','stream','created-by-me','starred'].forEach",
    "Update showView list"
)

# ── 5. Replace showInbox() ────────────────────────────────────────────────────
rp(
    """function showInbox(){
  curView='stub';setTopbar('Inbox','Notifications and updates',[]);showView('stub');closeNavIfMobile();
  document.getElementById('view-stub').innerHTML=`<div class="stub-view topo-bg">
    <div class="stub-icon">🔔</div>
    <div class="stub-title">Inbox</div>
    <div class="stub-sub">All your task assignments, mentions, status changes and form submissions will appear here.</div>
  </div>`;
}""",
    """function timeSince(ts){
  const s=Math.floor((Date.now()-ts)/1000);
  if(s<60)return 'just now';if(s<3600)return Math.floor(s/60)+'m ago';
  if(s<86400)return Math.floor(s/3600)+'h ago';if(s<604800)return Math.floor(s/86400)+'d ago';
  return new Date(ts).toLocaleDateString('en-GB',{day:'numeric',month:'short'});
}
function showInbox(){
  curView='inbox';
  setTopbar('Inbox','Your notifications and updates',[
    `<button class="btn ghost" style="font-size:12px" onclick="markAllInboxRead()">Mark all read</button>`
  ]);
  showView('inbox');closeNavIfMobile();
  window._inboxFilter=window._inboxFilter||'all';
  renderInbox(window._inboxFilter);
}
function renderInbox(filter){
  window._inboxFilter=filter;
  const el=document.getElementById('view-inbox');
  const unread=ACTIVITY_LOG.filter(a=>!a.read).length;
  const TYPE_ICON={task_assigned:'👤',status_changed:'🔄',mention:'💬',task_ready:'✅',ai_suggestion:'⚡',report_ready:'📊',comment:'💬',project_created:'📁',task_created:'📋'};
  const TYPE_LABEL={task_assigned:'Assignment',status_changed:'Status Change',mention:'Mention',task_ready:'Task Ready',ai_suggestion:'AI Suggestion',report_ready:'Report Ready',comment:'Comment',project_created:'Project Created',task_created:'Task Added'};
  function uInit(uid){const u=USERS.find(u=>u.id===uid);return u?u.name.split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase():'?';}
  function uColor(uid){const u=USERS.find(u=>u.id===uid);return u?u.color:'#94a3b8';}
  const tabs=[{key:'all',label:'All'},{key:'unread',label:`Unread${unread?' ('+unread+')':''}`},{key:'task_assigned',label:'Assignments'},{key:'mention',label:'Mentions'},{key:'automation',label:'Automations'}];
  let items=[...ACTIVITY_LOG].sort((a,b)=>b.ts-a.ts);
  if(filter==='unread') items=items.filter(a=>!a.read);
  else if(filter==='automation') items=items.filter(a=>['task_ready','ai_suggestion','report_ready'].includes(a.type));
  else if(filter!=='all') items=items.filter(a=>a.type===filter);
  el.innerHTML=`
    <div class="inbox-header-bar">
      <div style="font-weight:700;font-size:17px">Inbox ${unread>0?`<span class="inbox-count-badge">${unread}</span>`:''}</div>
    </div>
    <div class="inbox-filter-tabs">
      ${tabs.map(t=>`<button class="inbox-tab${filter===t.key?' on':''}" onclick="renderInbox('${t.key}')">${t.label}</button>`).join('')}
    </div>
    <div class="inbox-list">
      ${items.length?items.map(a=>`
        <div class="inbox-card${a.read?'':' unread'}" onclick="markInboxRead('${a.id}')">
          <div class="inbox-av-wrap">
            ${a.fromUser?`<div class="inbox-av" style="background:${uColor(a.fromUser)}">${uInit(a.fromUser)}</div>`
              :`<div class="inbox-av sys">${TYPE_ICON[a.type]||'🔔'}</div>`}
          </div>
          <div class="inbox-body">
            <div class="inbox-msg">${a.msg}</div>
            <div class="inbox-meta">
              ${a.projName?`<span class="inbox-proj-chip">${a.projName}</span>`:''}
              <span class="inbox-time">${timeSince(a.ts)}</span>
              <span class="inbox-type-badge">${TYPE_LABEL[a.type]||a.type}</span>
            </div>
          </div>
          ${!a.read?'<div class="inbox-dot"></div>':''}
        </div>`).join('')
        :`<div class="inbox-empty"><div style="font-size:36px;margin-bottom:10px">🎉</div><div style="font-weight:600;margin-bottom:4px">You're all caught up!</div><div style="font-size:12px;color:var(--text3)">No notifications in this category</div></div>`}
    </div>`;
}
function markInboxRead(id){
  const a=ACTIVITY_LOG.find(a=>a.id===id);if(a)a.read=true;
  renderInbox(window._inboxFilter||'all');
  const b=document.querySelector('.nav-badge.firefly');
  const u=ACTIVITY_LOG.filter(x=>!x.read).length;
  if(b){b.textContent=u;b.style.display=u?'':'none';}
}
function markAllInboxRead(){
  ACTIVITY_LOG.forEach(a=>a.read=true);
  renderInbox(window._inboxFilter||'all');
  const b=document.querySelector('.nav-badge.firefly');if(b)b.style.display='none';
}""",
    "Replace showInbox"
)

# ── 6. Add showStream + showCreatedByMe + showStarred after showStub ──────────
rp(
    """function showStub(title,icon,desc){
  curView='stub';setTopbar(title,'',[]);showView('stub');closeNavIfMobile();
  document.getElementById('view-stub').innerHTML=`<div class="stub-view topo-bg">
    <div class="stub-icon">${icon}</div><div class="stub-title">${title}</div>
    <div class="stub-sub">${desc}</div>
  </div>`;
}""",
    """function showStub(title,icon,desc){
  curView='stub';setTopbar(title,'',[]);showView('stub');closeNavIfMobile();
  document.getElementById('view-stub').innerHTML=`<div class="stub-view topo-bg">
    <div class="stub-icon">${icon}</div><div class="stub-title">${title}</div>
    <div class="stub-sub">${desc}</div>
  </div>`;
}
function showStream(){
  curView='stream';setTopbar('Activity Stream','Everything happening across your workspaces',[]);
  showView('stream');closeNavIfMobile();renderStream();
}
function renderStream(){
  const el=document.getElementById('view-stream');
  const TYPE_ICON={task_assigned:'👤',status_changed:'🔄',mention:'💬',task_ready:'✅',ai_suggestion:'⚡',report_ready:'📊',comment:'💬',project_created:'📁',task_created:'📋'};
  function uInit(uid){const u=USERS.find(u=>u.id===uid);return u?u.name.split(' ').map(w=>w[0]).join('').slice(0,2).toUpperCase():'⚡';}
  function uColor(uid){const u=USERS.find(u=>u.id===uid);return u?u.color:'#94a3b8';}
  const sorted=[...ACTIVITY_LOG].sort((a,b)=>b.ts-a.ts);
  el.innerHTML=`<div class="stream-wrap">
    <div class="stream-feed">
      ${sorted.map((a,i)=>`
        <div class="stream-entry">
          <div class="stream-av-col">
            ${a.fromUser?`<div class="stream-av" style="background:${uColor(a.fromUser)}">${uInit(a.fromUser)}</div>`
              :`<div class="stream-av sys">${TYPE_ICON[a.type]||'🔔'}</div>`}
            ${i<sorted.length-1?'<div class="stream-line"></div>':''}
          </div>
          <div class="stream-body">
            <div class="stream-msg">${a.msg}</div>
            <div class="stream-meta">
              ${a.projName?`<span class="stream-proj-chip">${a.projName}</span>`:''}
              <span class="stream-time">${timeSince(a.ts)}</span>
            </div>
          </div>
        </div>`).join('')}
    </div>
  </div>`;
}
function showCreatedByMe(){
  curView='created-by-me';setTopbar('Created by Me','Tasks and projects you created',[]);
  showView('created-by-me');closeNavIfMobile();
  const el=document.getElementById('view-created-by-me');
  const me=USERS[0];
  const myTasks=PROJECTS.flatMap(p=>p.tasks.filter(t=>!t.createdBy||t.createdBy===me.id)
    .slice(0,4).map(t=>({...t,projName:p.name,projId:p.id,projColor:p.color||'var(--accent)'})));
  el.innerHTML=`<div style="padding:20px 24px;overflow-y:auto;height:100%">
    <div style="font-size:13px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.6px;margin-bottom:12px">Projects (${PROJECTS.length})</div>
    <div class="home-card" style="margin-bottom:20px">
      ${PROJECTS.slice(0,6).map(p=>`<div class="home-task-row" onclick="openProject('${p.id}')">
        <span style="width:10px;height:10px;border-radius:3px;background:${p.color||'var(--accent)'};flex-shrink:0;display:inline-block"></span>
        <span style="flex:1;font-weight:500">${p.name}</span>
        <span class="pill" style="background:#1AA6B722;color:var(--accent);border:1px solid #1AA6B744">${p.tasks.length} tasks</span>
      </div>`).join('')}
    </div>
    <div style="font-size:13px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.6px;margin-bottom:12px">Recent tasks (${myTasks.length})</div>
    <div class="home-card">
      ${myTasks.map(t=>`<div class="home-task-row" onclick="openProject('${t.projId}');setTimeout(()=>openTask('${t.id}'),200)">
        <span class="dot" style="background:${SC[t.status]||SC.todo}"></span>
        <span style="flex:1">${t.title}</span>
        <span style="font-size:11px;color:${t.projColor}">${t.projName}</span>
        <span class="pill" style="background:${SC[t.status]}22;color:${SC[t.status]};border:1px solid ${SC[t.status]}44;margin-left:6px">${SL[t.status]}</span>
      </div>`).join('')}
    </div>
  </div>`;
}
function showStarred(){
  curView='starred';setTopbar('Starred','Your starred items',[]);
  showView('starred');closeNavIfMobile();
  const el=document.getElementById('view-starred');
  const sProj=PROJECTS.filter(p=>STARRED_ITEMS.projects[p.id]);
  const sTasks=PROJECTS.flatMap(p=>p.tasks.filter(t=>STARRED_ITEMS.tasks[t.id]).map(t=>({...t,projName:p.name,projId:p.id})));
  if(!sProj.length&&!sTasks.length){
    el.innerHTML=`<div class="stub-view topo-bg"><div class="stub-icon">\u2B50</div>
      <div class="stub-title">No starred items yet</div>
      <div class="stub-sub">Star any task or project to quickly find it here. Click the \u2606 icon on any task or project.</div></div>`;
    return;
  }
  el.innerHTML=`<div style="padding:20px 24px;overflow-y:auto;height:100%">
    ${sProj.length?`<div style="font-size:13px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.6px;margin-bottom:12px">Starred projects</div>
    <div class="home-card" style="margin-bottom:20px">
      ${sProj.map(p=>`<div class="home-task-row" onclick="openProject('${p.id}')">
        <span style="width:10px;height:10px;border-radius:3px;background:${p.color||'var(--accent)'};flex-shrink:0;display:inline-block"></span>
        <span style="flex:1;font-weight:500">${p.name}</span>
        <button onclick="event.stopPropagation();delete STARRED_ITEMS.projects['${p.id}'];showStarred()" style="background:none;border:none;cursor:pointer;color:#f59e0b;font-size:17px">\u2605</button>
      </div>`).join('')}</div>`:''}
    ${sTasks.length?`<div style="font-size:13px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.6px;margin-bottom:12px">Starred tasks</div>
    <div class="home-card">
      ${sTasks.map(t=>`<div class="home-task-row" onclick="openProject('${t.projId}');setTimeout(()=>openTask('${t.id}'),200)">
        <span class="dot" style="background:${SC[t.status]||SC.todo}"></span>
        <span style="flex:1">${t.title}</span>
        <span style="font-size:11px;color:var(--text3)">${t.projName}</span>
        <button onclick="event.stopPropagation();delete STARRED_ITEMS.tasks['${t.id}'];showStarred()" style="background:none;border:none;cursor:pointer;color:#f59e0b;font-size:17px">\u2605</button>
      </div>`).join('')}</div>`:''}
  </div>`;
}
function showCustomizeMenu(){
  showStub('Customize Menu','⚙️','Drag-and-drop sidebar customization coming in the next update.');
}""",
    "Add showStream/showCreatedByMe/showStarred/showCustomizeMenu"
)

# ── 7. Add CSS ────────────────────────────────────────────────────────────────
rp(
    ".ts-today-cell{background:var(--abg);border-radius:6px}",
    """.ts-today-cell{background:var(--abg);border-radius:6px}
/* Inbox */
.inbox-header-bar{padding:20px 20px 8px;display:flex;align-items:center;gap:10px}
.inbox-count-badge{display:inline-flex;align-items:center;justify-content:center;background:var(--accent);color:#fff;border-radius:10px;font-size:10px;font-weight:700;padding:1px 7px;vertical-align:middle;margin-left:4px}
.inbox-filter-tabs{display:flex;gap:4px;padding:8px 16px 12px;border-bottom:1px solid var(--border2);flex-wrap:wrap}
.inbox-tab{padding:5px 13px;border-radius:20px;font-size:12px;font-weight:500;cursor:pointer;border:1px solid transparent;background:transparent;color:var(--text2);transition:all .15s}
.inbox-tab:hover{background:var(--surface);border-color:var(--border2)}
.inbox-tab.on{background:var(--accent);color:#fff}
.inbox-list{overflow-y:auto;padding:8px 12px}
.inbox-card{display:flex;align-items:flex-start;gap:12px;padding:12px 14px;border-radius:10px;cursor:pointer;transition:background .15s;position:relative;margin-bottom:2px}
.inbox-card:hover{background:var(--surface)}
.inbox-card.unread{background:rgba(26,166,183,.06)}
.inbox-card.unread:hover{background:rgba(26,166,183,.1)}
.inbox-av{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;flex-shrink:0}
.inbox-av.sys{background:var(--surface);border:1px solid var(--border2);font-size:17px}
.inbox-av-wrap{flex-shrink:0}
.inbox-body{flex:1;min-width:0}
.inbox-msg{font-size:13px;line-height:1.5;color:var(--text);margin-bottom:5px}
.inbox-meta{display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.inbox-proj-chip{font-size:10px;padding:2px 7px;border-radius:10px;background:var(--abg);color:var(--accent);font-weight:600}
.inbox-time{font-size:11px;color:var(--text3)}
.inbox-type-badge{font-size:10px;padding:1px 6px;border-radius:8px;background:var(--surface);color:var(--text3);border:1px solid var(--border2)}
.inbox-dot{width:8px;height:8px;border-radius:50%;background:var(--accent);flex-shrink:0;margin-top:6px}
.inbox-empty{padding:60px 24px;text-align:center;color:var(--text3)}
/* Stream */
.stream-wrap{padding:20px 24px;overflow-y:auto;height:100%;box-sizing:border-box}
.stream-feed{max-width:660px;margin:0 auto}
.stream-entry{display:flex;gap:12px}
.stream-av-col{display:flex;flex-direction:column;align-items:center;flex-shrink:0}
.stream-av{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;color:#fff;flex-shrink:0}
.stream-av.sys{background:var(--surface);border:1px solid var(--border2);font-size:17px}
.stream-line{width:2px;background:var(--border2);flex:1;min-height:12px;margin-top:4px;border-radius:1px}
.stream-body{flex:1;background:var(--surface);border:1px solid var(--border2);border-radius:10px;padding:12px 14px;margin-bottom:12px;min-width:0}
.stream-msg{font-size:13px;line-height:1.5;color:var(--text)}
.stream-meta{display:flex;align-items:center;gap:8px;margin-top:6px;flex-wrap:wrap}
.stream-proj-chip{font-size:10px;padding:2px 7px;border-radius:10px;background:var(--abg);color:var(--accent);font-weight:600}
.stream-time{font-size:11px;color:var(--text3)}""",
    "Add Inbox + Stream CSS"
)

# ── Safe write via tempfile ───────────────────────────────────────────────────
tmp = src + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(tmp, src)
print(f"\nDone — {orig} -> {len(content)} chars ({len(content)-orig:+d})")
