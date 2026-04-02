#!/usr/bin/env python3
"""Fix timesheet totals + update activities + add billable + due date + task click."""
with open('/home/user/YCxDesign/team-nexus-v3.html', 'r') as f:
    html = f.read()

# ── 1. Add TASK_BILLABLE map after tsWeekOffset declaration ──
old_ts_state = "let tsWeekOffset=0, tsUserId=1;"
new_ts_state = """let tsWeekOffset=0, tsUserId=1;
let TASK_BILLABLE={}; // {taskId: false} means Non-Billable; default (undefined/true) = Billable"""
assert old_ts_state in html
html = html.replace(old_ts_state, new_ts_state, 1)

# ── 2. Fix saveTimeEntry — re-render after save so totals update ──
old_save = """function saveTimeEntry(taskId,date,hours,activity){
  const h=parseFloat(hours);
  if(isNaN(h)||h<=0){TIMESHEET_ENTRIES=TIMESHEET_ENTRIES.filter(e=>!(e.userId===tsUserId&&e.taskId===taskId&&e.date===date));return;}
  const ex=TIMESHEET_ENTRIES.find(e=>e.userId===tsUserId&&e.taskId===taskId&&e.date===date);
  if(ex){ex.hours=h;ex.activity=activity||'Development';}
  else TIMESHEET_ENTRIES.push({id:'te'+Date.now(),userId:tsUserId,taskId,date,hours:h,activity:activity||'Development'});
}"""
new_save = """function saveTimeEntry(taskId,date,hours,activity){
  const h=parseFloat(hours);
  if(isNaN(h)||h<=0){
    TIMESHEET_ENTRIES=TIMESHEET_ENTRIES.filter(e=>!(e.userId===tsUserId&&e.taskId===taskId&&e.date===date));
    renderTimesheets();return;
  }
  const ex=TIMESHEET_ENTRIES.find(e=>e.userId===tsUserId&&e.taskId===taskId&&e.date===date);
  if(ex){ex.hours=h;ex.activity=activity||'Development Work';}
  else TIMESHEET_ENTRIES.push({id:'te'+Date.now(),userId:tsUserId,taskId,date,hours:h,activity:activity||'Development Work'});
  renderTimesheets();
}

function setTaskBillable(taskId,val){
  TASK_BILLABLE[taskId]=val;
  renderTimesheets();
}

function openTaskFromTimesheet(projId,taskId){
  curProjectId=projId;
  openTask(taskId);
}"""
assert old_save in html
html = html.replace(old_save, new_save, 1)

# ── 3. Rewrite renderTimesheets with new columns + activity list ──
ACTIVITIES = [
  ('All Hands Meeting',       'All Hands'),
  ('Audit',                   'Audit'),
  ('Backend Activities',      'Backend'),
  ('Casual Catch Ups',        'Catch Up'),
  ('Client Meeting / Communications', 'Client Mtg'),
  ('Comp Off',                'Comp Off'),
  ('Consultation',            'Consult'),
  ('Development Work',        'Dev Work'),
  ('DF Holiday',              'Holiday'),
  ('HR Activities (Avengers)','HR'),
  ('Internal Meetings',       'Internal Mtg'),
  ('Leaves',                  'Leave'),
  ('Performance Reviews',     'Perf Review'),
  ('Process Compliance',      'Process'),
  ('Project Management',      'PM'),
  ('Recruitment',             'Recruit'),
  ('Training',                'Training'),
  ('Unassigned',              'Unassigned'),
]

old_render = """function renderTimesheets(){
  const monday=getMondayOf(tsWeekOffset);
  const days=[0,1,2,3,4,5,6].map(i=>addDays(monday,i));
  const user=USERS.find(u=>u.id===tsUserId)||USERS[0];
  const myTasks=PROJECTS.flatMap(p=>p.tasks.filter(t=>t.assignee===tsUserId).map(t=>({...t,projName:p.name,projId:p.id})));
  const cols=8+1; // task col + 7 days + total
  const gridCols=`2fr repeat(7,1fr) 70px`;
  const el=document.getElementById('view-timesheet');

  const weekLabel=`${fmtDay(days[0])} – ${fmtDay(days[6])} ${monday.getFullYear()}`;

  function getEntry(taskId,date){return TIMESHEET_ENTRIES.find(e=>e.userId===tsUserId&&e.taskId===taskId&&e.date===fmtDate(date));}
  function rowTotal(taskId){return days.reduce((s,d)=>{const e=getEntry(taskId,d);return s+(e?e.hours:0);},0);}
  function colTotal(dayIdx){return myTasks.reduce((s,t)=>{const e=getEntry(t.id,days[dayIdx]);return s+(e?e.hours:0);},0);}
  const grandTotal=myTasks.reduce((s,t)=>s+rowTotal(t.id),0);

  el.innerHTML=`
    <div class="ts-header">
      <button class="btn ghost" onclick="tsWeekOffset--;renderTimesheets()">‹ Prev</button>
      <div class="ts-week-label">${weekLabel}</div>
      <button class="btn ghost" onclick="tsWeekOffset++;renderTimesheets()">Next ›</button>
      ${USERS[0].role==='admin'?`
        <select class="ts-user-sel" onchange="tsUserId=parseInt(this.value);renderTimesheets()">
          ${USERS.map(u=>`<option value="${u.id}"${u.id===tsUserId?' selected':''}>${u.name}</option>`).join('')}
        </select>`:''}
    </div>
    <div class="ts-table">
      <div class="ts-head-row" style="grid-template-columns:${gridCols}">
        <div class="ts-head-cell" style="text-align:left;padding-left:14px">Task</div>
        ${days.map(d=>`<div class="ts-head-cell">${fmtDay(d)}</div>`).join('')}
        <div class="ts-head-cell">Total</div>
      </div>
      ${myTasks.length?myTasks.map(t=>`
        <div class="ts-data-row" style="grid-template-columns:${gridCols}">
          <div class="ts-task-cell">
            <div class="ts-task-name">${t.title}</div>
            <div class="ts-task-proj">${t.projName}</div>
          </div>
          ${days.map((d,di)=>{
            const e=getEntry(t.id,d);
            const dateStr=fmtDate(d);
            return `<div class="ts-day-cell">
              <input class="ts-inp" type="number" min="0" max="24" step="0.5" placeholder="—"
                value="${e?e.hours:''}"
                onchange="saveTimeEntry('${t.id}','${dateStr}',this.value,this.nextElementSibling.value)">
              <select class="ts-act-sel" onchange="saveTimeEntry('${t.id}','${dateStr}',this.previousElementSibling.value,this.value)">
                <option value="Development"${e?.activity==='Development'?' selected':''}>Dev</option>
                <option value="Design"${e?.activity==='Design'?' selected':''}>Design</option>
                <option value="Review"${e?.activity==='Review'?' selected':''}>Review</option>
                <option value="Planning"${e?.activity==='Planning'?' selected':''}>Plan</option>
                <option value="Testing"${e?.activity==='Testing'?' selected':''}>Test</option>
                <option value="Meeting"${e?.activity==='Meeting'?' selected':''}>Meet</option>
              </select>
            </div>`;
          }).join('')}
          <div class="ts-row-total">${rowTotal(t.id)||'—'}</div>
        </div>`).join(''):`<div style="padding:20px;color:var(--text3);font-size:13px;text-align:center">No tasks assigned to ${user.name} this week.</div>`}
      <div class="ts-totals-row" style="grid-template-columns:${gridCols}">
        <div class="ts-grand" style="text-align:left;padding-left:14px">Daily totals</div>
        ${days.map((_,di)=>`<div class="ts-grand">${colTotal(di)||'—'}</div>`).join('')}
        <div class="ts-grand" style="color:var(--accent)">${grandTotal||'—'}</div>
      </div>
    </div>
    <div style="font-size:11px;color:var(--text3);margin-top:8px">Hours logged this week: <strong>${grandTotal}h</strong> across ${myTasks.length} tasks</div>`;
}"""

new_render = r"""function renderTimesheets(){
  const monday=getMondayOf(tsWeekOffset);
  const days=[0,1,2,3,4,5,6].map(i=>addDays(monday,i));
  const user=USERS.find(u=>u.id===tsUserId)||USERS[0];
  const myTasks=PROJECTS.flatMap(p=>p.tasks.filter(t=>t.assignee===tsUserId).map(t=>({...t,projName:p.name,projColor:p.color||'#1AA6B7',projId:p.id})));
  const gridCols=`2fr 110px repeat(7,1fr) 70px 100px`;
  const el=document.getElementById('view-timesheet');
  const todayStr=fmtDate(new Date());

  const weekLabel=`${fmtDay(days[0])} \u2013 ${fmtDay(days[6])} ${monday.getFullYear()}`;

  function getEntry(taskId,date){
    return TIMESHEET_ENTRIES.find(e=>e.userId===tsUserId&&e.taskId===taskId&&e.date===fmtDate(date));
  }
  function rowTotal(taskId){
    return days.reduce((s,d)=>{const e=getEntry(taskId,d);return s+(e?e.hours:0);},0);
  }
  function colTotal(dayIdx){
    return myTasks.reduce((s,t)=>{const e=getEntry(t.id,days[dayIdx]);return s+(e?e.hours:0);},0);
  }
  const grandTotal=myTasks.reduce((s,t)=>s+rowTotal(t.id),0);

  const ACT_OPTIONS=[
    ['All Hands Meeting','All Hands'],['Audit','Audit'],['Backend Activities','Backend'],
    ['Casual Catch Ups','Catch Up'],['Client Meeting / Communications','Client Mtg'],
    ['Comp Off','Comp Off'],['Consultation','Consult'],['Development Work','Dev Work'],
    ['DF Holiday','Holiday'],['HR Activities (Avengers)','HR'],
    ['Internal Meetings','Internal Mtg'],['Leaves','Leave'],
    ['Performance Reviews','Perf Review'],['Process Compliance','Process'],
    ['Project Management','PM'],['Recruitment','Recruit'],
    ['Training','Training'],['Unassigned','Unassigned'],
  ];

  function actOpts(e){
    return ACT_OPTIONS.map(([v,l])=>`<option value="${v}"${e?.activity===v?' selected':''}>${l}</option>`).join('');
  }

  function billableBtn(taskId){
    const isBillable=TASK_BILLABLE[taskId]!==false;
    return `<div style="display:flex;gap:4px;align-items:center">
      <button onclick="setTaskBillable('${taskId}',true)" style="flex:1;padding:3px 0;border-radius:5px 0 0 5px;font-size:10px;font-weight:700;cursor:pointer;border:1px solid ${isBillable?'var(--accent)':'var(--border2)'};background:${isBillable?'var(--accent)':'transparent'};color:${isBillable?'#fff':'var(--text3)'}">Billable</button>
      <button onclick="setTaskBillable('${taskId}',false)" style="flex:1;padding:3px 0;border-radius:0 5px 5px 0;font-size:10px;font-weight:700;cursor:pointer;border:1px solid ${!isBillable?'#ef4444':'var(--border2)'};border-left:none;background:${!isBillable?'#ef4444':'transparent'};color:${!isBillable?'#fff':'var(--text3)'}">Non-Bill</button>
    </div>`;
  }

  el.innerHTML=`
    <div class="ts-header">
      <button class="btn ghost" onclick="tsWeekOffset--;renderTimesheets()">‹ Prev</button>
      <div class="ts-week-label">${weekLabel}</div>
      <button class="btn ghost" onclick="tsWeekOffset++;renderTimesheets()">Next ›</button>
      ${USERS[0].role==='admin'?`
        <select class="ts-user-sel" onchange="tsUserId=parseInt(this.value);renderTimesheets()">
          ${USERS.map(u=>`<option value="${u.id}"${u.id===tsUserId?' selected':''}>${u.name}</option>`).join('')}
        </select>`:''}
    </div>
    <div class="ts-table">
      <div class="ts-head-row" style="grid-template-columns:${gridCols}">
        <div class="ts-head-cell" style="text-align:left;padding-left:14px">Task</div>
        <div class="ts-head-cell">Billable</div>
        ${days.map(d=>{
          const ds=fmtDate(d);
          return `<div class="ts-head-cell${ds===todayStr?' ts-today-head':''}">${fmtDay(d)}</div>`;
        }).join('')}
        <div class="ts-head-cell">Total</div>
        <div class="ts-head-cell">Due date</div>
      </div>
      ${myTasks.length?myTasks.map(t=>{
        const rTotal=rowTotal(t.id);
        const today=new Date().toISOString().slice(0,10);
        const overdue=t.dueDate&&t.dueDate<today&&t.status!=='done';
        return `
        <div class="ts-data-row" style="grid-template-columns:${gridCols}">
          <div class="ts-task-cell">
            <div class="ts-task-name" onclick="openTaskFromTimesheet('${t.projId}','${t.id}')" style="cursor:pointer;color:var(--accent);text-decoration:underline;text-decoration-style:dotted">${t.title}</div>
            <div class="ts-task-proj" style="color:${t.projColor}">${t.projName}</div>
          </div>
          <div class="ts-day-cell" style="align-items:center;padding:4px 6px">${billableBtn(t.id)}</div>
          ${days.map((d,di)=>{
            const e=getEntry(t.id,d);
            const dateStr=fmtDate(d);
            const isToday=dateStr===todayStr;
            return `<div class="ts-day-cell${isToday?' ts-today-cell':''}">
              <input class="ts-inp" type="number" min="0" max="24" step="0.5" placeholder="—"
                value="${e?e.hours:''}"
                onchange="saveTimeEntry('${t.id}','${dateStr}',this.value,this.nextElementSibling.value)">
              <select class="ts-act-sel" onchange="saveTimeEntry('${t.id}','${dateStr}',this.previousElementSibling.value,this.value)">
                ${actOpts(e)}
              </select>
            </div>`;
          }).join('')}
          <div class="ts-row-total" style="color:${rTotal>0?'var(--accent)':'var(--text3)'}">${rTotal>0?rTotal+'h':'—'}</div>
          <div class="ts-day-cell" style="justify-content:center;font-size:11px;color:${overdue?'#ef4444':'var(--text3)'}">
            ${t.dueDate||'—'}
          </div>
        </div>`}).join(''):`<div style="padding:20px;color:var(--text3);font-size:13px;text-align:center">No tasks assigned to ${user.name} this week.</div>`}
      <div class="ts-totals-row" style="grid-template-columns:${gridCols}">
        <div class="ts-grand" style="text-align:left;padding-left:14px;font-weight:700">Daily totals</div>
        <div class="ts-grand"></div>
        ${days.map((_,di)=>{
          const ct=colTotal(di);
          return `<div class="ts-grand" style="color:${ct>0?'var(--accent)':'var(--text3)'};font-weight:${ct>0?700:400}">${ct>0?ct+'h':'—'}</div>`;
        }).join('')}
        <div class="ts-grand" style="color:var(--accent);font-weight:700">${grandTotal>0?grandTotal+'h':'—'}</div>
        <div class="ts-grand"></div>
      </div>
    </div>
    <div style="font-size:11px;color:var(--text3);margin-top:8px">
      Hours logged this week: <strong style="color:var(--accent)">${grandTotal}h</strong> across ${myTasks.length} task${myTasks.length!==1?'s':''}
      &nbsp;·&nbsp; Billable: <strong style="color:var(--accent)">${myTasks.filter(t=>TASK_BILLABLE[t.id]!==false).reduce((s,t)=>s+rowTotal(t.id),0)}h</strong>
      &nbsp;·&nbsp; Non-billable: <strong>${myTasks.filter(t=>TASK_BILLABLE[t.id]===false).reduce((s,t)=>s+rowTotal(t.id),0)}h</strong>
    </div>`;
}"""

assert old_render in html, 'renderTimesheets anchor not found'
html = html.replace(old_render, new_render, 1)

# ── 4. Add today highlight CSS ──
today_css = """
.ts-today-head{color:var(--accent);font-weight:700}
.ts-today-cell{background:var(--abg);border-radius:6px}
"""
html = html.replace('</style>', today_css + '</style>', 1)

with open('/home/user/YCxDesign/team-nexus-v3.html', 'w') as f:
    f.write(html)
print('Timesheet fix done')
