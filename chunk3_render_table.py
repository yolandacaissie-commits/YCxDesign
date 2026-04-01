#!/usr/bin/env python3
"""Chunk 3: Rewrite renderTable with new columns + predecessor helpers."""
with open('/home/user/YCxDesign/team-nexus-v3.html', 'r') as f:
    html = f.read()

# ── Find the exact renderTable function to replace ──
# We'll replace from "function renderTable(){" to the end of the function
# (the closing brace), and also replace tblCell and cfInlineCell since we're
# reworking cells. We identify the block by its unique start/end.

import re

# Find start of renderTable
rt_start = html.index('function renderTable(){')
# Find the function after renderTable that we DON'T want to replace (tblCell)
rt_end = html.index('\nfunction tblCell(t,col,p){', rt_start)

old_render_table = html[rt_start:rt_end]

new_render_table = r"""function getPredDisplay(t,tasks){
  if(!t.pred)return '';
  const idx=tasks.findIndex(x=>x.id===t.pred);
  if(idx<0)return '';
  const rowNum=idx+1;
  const type=t.predType||'FS';
  const lag=t.predLag||0;
  return rowNum+type+(lag>0?'+'+lag:lag<0?String(lag):'');
}

function parsePredInput(str,tasks){
  if(!str||!str.trim())return{taskId:null,type:'FS',lag:0};
  const m=str.trim().match(/^(\d+)(FS|SS|FF|SF)?([+-]\d+)?$/i);
  if(!m)return null;
  const rowNum=parseInt(m[1]);
  if(rowNum<1||rowNum>tasks.length)return null;
  return{taskId:tasks[rowNum-1].id,type:m[2]?m[2].toUpperCase():'FS',lag:m[3]?parseInt(m[3]):0};
}

function savePredInput(taskId,inputEl){
  const p=getP();if(!p)return;
  const t=p.tasks.find(x=>x.id===taskId);if(!t)return;
  const parsed=parsePredInput(inputEl.value,p.tasks);
  if(parsed===null){inputEl.value=getPredDisplay(t,p.tasks);return;}
  t.pred=parsed.taskId;
  t.predType=parsed.type;
  t.predLag=parsed.lag;
  if(curView==='table')renderTable();
  if(curView==='gantt')renderGantt();
}

function getTaskSortVal(t,field,tasks){
  switch(field){
    case 'title':return(t.title||'').toLowerCase();
    case 'pred':{const idx=tasks.findIndex(x=>x.id===t.pred);return idx<0?99999:idx;}
    case 'duration':return t.duration||0;
    case 'startDate':return t.start?new Date(t.start).getTime():0;
    case 'dueDate':return t.dueDate?new Date(t.dueDate).getTime():99999999999;
    case 'status':{const ord={done:0,in_progress:1,review:2,todo:3,blocked:4};return ord[t.status]??5;}
    case 'priority':{const ord={critical:0,high:1,medium:2,low:3};return ord[t.priority]??4;}
    case 'assignee':return(USERS.find(u=>u.id===t.assignee)?.name||'zzz').toLowerCase();
    default:return 0;
  }
}

function applyFilterRule(t,rule,tasks){
  const{field,op,value}=rule;
  let v='';
  if(field==='title')v=(t.title||'').toLowerCase();
  else if(field==='status')v=t.status||'';
  else if(field==='priority')v=t.priority||'';
  else if(field==='assignee')v=USERS.find(u=>u.id===t.assignee)?.name||'';
  else if(field==='dueDate')v=t.dueDate||'';
  else if(field==='duration')v=t.duration??null;
  const lv=(value||'').toLowerCase();
  switch(op){
    case 'contains':return v.includes(lv);
    case 'does not contain':return !v.includes(lv);
    case 'is':return v===lv;
    case 'is not':return v!==lv;
    case 'is empty':return !v;
    case 'is not empty':return !!v;
    case '>':return Number(v)>Number(value);
    case '<':return Number(v)<Number(value);
    case 'after':return t.dueDate&&t.dueDate>value;
    case 'before':return t.dueDate&&t.dueDate<value;
    default:return true;
  }
}

function renderTable(){
  const p=getP();if(!p)return;
  const vc=p.visibleColumns||['pred','duration','startDate','dueDate','status','assignee'];
  const BUILTIN_COLS=[
    {key:'pred',     label:'Predecessors'},
    {key:'duration', label:'Duration'},
    {key:'startDate',label:'Start date'},
    {key:'dueDate',  label:'Due date'},
    {key:'status',   label:'Status'},
    {key:'priority', label:'Priority'},
    {key:'assignee', label:'Assignee'},
  ];
  const visCols=BUILTIN_COLS.filter(c=>vc.includes(c.key));
  const visCFs=CUSTOM_FIELDS.filter(cf=>vc.includes('cf_'+cf.id)||cf.visible!==false&&!vc.length);

  // Sort
  let tasks=[...p.tasks];
  const sf=p.sortField||'startDate',sd=p.sortDir||'asc';
  tasks.sort((a,b)=>{
    const va=getTaskSortVal(a,sf,p.tasks),vb=getTaskSortVal(b,sf,p.tasks);
    if(va<vb)return sd==='asc'?-1:1;
    if(va>vb)return sd==='asc'?1:-1;
    return 0;
  });

  // Filter
  if(p.filterRules&&p.filterRules.length)
    tasks=tasks.filter(t=>p.filterRules.every(r=>applyFilterRule(t,r,p.tasks)));

  // tbl-toolbar: just count
  document.getElementById('tbl-toolbar').innerHTML=
    `<span style="font-size:11.5px;color:var(--text3);padding:6px 0">${tasks.length} task${tasks.length!==1?'s':''}</span>`;

  // Column sort arrows
  const arr=k=>sf===k?(sd==='asc'?' ↑':' ↓'):'';

  // Header
  document.getElementById('tbl-head').innerHTML=`<tr>
    <th class="tbl-rn-th" style="width:32px;color:var(--text3);font-weight:400;font-size:11px"></th>
    <th style="cursor:pointer;min-width:180px" onclick="toggleTblSort('title')">Name${arr('title')}</th>
    ${visCols.map(c=>`<th style="cursor:pointer;white-space:nowrap" onclick="toggleTblSort('${c.key}')">${c.label}${arr(c.key)}</th>`).join('')}
    ${visCFs.map(cf=>`<th style="color:var(--accent);opacity:.85;white-space:nowrap">${cf.name}</th>`).join('')}
    <th class="th-plus" onclick="openFieldPanel(event)" title="Show/hide fields" style="cursor:pointer;text-align:center;width:36px;font-size:16px;color:var(--text3)">＋</th>
  </tr>`;

  // Group by
  const gb=p.groupBy;
  let rows='';
  if(gb){
    const groupMap={};
    tasks.forEach(t=>{
      let gk='';
      if(gb==='status')gk=t.status||'todo';
      else if(gb==='assignee')gk=USERS.find(u=>u.id===t.assignee)?.name||'Unassigned';
      else if(gb==='priority')gk=t.priority||'medium';
      else if(gb==='dueDate')gk=t.dueDate?t.dueDate.slice(0,7):'No date';
      else gk='Other';
      if(!groupMap[gk])groupMap[gk]=[];
      groupMap[gk].push(t);
    });
    Object.entries(groupMap).forEach(([gk,gTasks])=>{
      const colSpan=2+visCols.length+visCFs.length+1;
      rows+=`<tr><td colspan="${colSpan}" style="background:var(--surface2);padding:6px 12px;font-size:11px;font-weight:700;color:var(--text2);text-transform:uppercase;letter-spacing:.4px;border-bottom:1px solid var(--border2)">${gk} <span style="font-weight:400;opacity:.6">(${gTasks.length})</span></td></tr>`;
      gTasks.forEach(t=>{ rows+=renderTaskRow(t,p,visCols,visCFs,p.tasks); });
    });
  } else {
    tasks.forEach(t=>{ rows+=renderTaskRow(t,p,visCols,visCFs,p.tasks); });
  }
  document.getElementById('tbl-body').innerHTML=rows;
}

function renderTaskRow(t,p,visCols,visCFs,allTasks){
  const isSel=selTaskId===t.id;
  const rowNum=allTasks.findIndex(x=>x.id===t.id)+1;
  let row=`<tr class="${isSel?'row-sel':''}" id="trow-${t.id}" onmouseenter="this.querySelector('.open-detail-btn').style.opacity='1'" onmouseleave="this.querySelector('.open-detail-btn').style.opacity='0'">`;
  // Row number
  row+=`<td class="tbl-rn-td" style="color:var(--text3);font-size:11px;text-align:center;width:32px;user-select:none">${rowNum}</td>`;
  // Name cell
  row+=`<td><div class="title-cell" onclick="openTask('${t.id}')">
    <div class="open-detail-btn" style="opacity:0;transition:opacity .15s" title="Open details">
      <svg viewBox="0 0 24 24" style="width:11px;height:11px;stroke:currentColor;stroke-width:2;fill:none"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
    </div>
    <input value="${esc(t.title)}" style="font-weight:600;background:transparent;border:none;color:var(--text);font-size:13px;font-family:inherit;outline:none;flex:1;cursor:text;min-width:100px"
      onclick="event.stopPropagation()"
      onblur="inlineEdit('${t.id}','title',this.value)"
      onkeydown="if(event.key==='Enter')this.blur()">
  </div></td>`;
  // Builtin visible cols
  visCols.forEach(c=>{
    if(c.key==='pred'){
      const disp=getPredDisplay(t,allTasks);
      row+=`<td onclick="event.stopPropagation()"><div class="cell editable">
        <input value="${esc(disp)}" placeholder="e.g. 3FS+2"
          style="font-size:12px;color:var(--accent2);min-width:60px;font-weight:500"
          onblur="savePredInput('${t.id}',this)"
          onkeydown="if(event.key==='Enter')this.blur()">
      </div></td>`;
    } else if(c.key==='duration'){
      row+=`<td onclick="event.stopPropagation()"><div class="cell editable">
        <input type="number" value="${t.duration||''}" placeholder="—" min="0"
          style="width:55px;font-size:12px"
          onblur="inlineEdit('${t.id}','duration',this.value?parseInt(this.value):null)"
          onkeydown="if(event.key==='Enter')this.blur()">
        ${t.duration?'<span style="font-size:10px;color:var(--text3)">d</span>':''}
      </div></td>`;
    } else if(c.key==='startDate'){
      const dv=t.start?new Date(t.start).toISOString().slice(0,10):'';
      row+=`<td onclick="event.stopPropagation()"><div class="cell editable">
        <input type="date" value="${dv}"
          style="font-size:12px;color:var(--text2)"
          onchange="inlineEditStart('${t.id}',this.value)">
      </div></td>`;
    } else if(c.key==='dueDate'){
      const today=new Date().toISOString().slice(0,10);
      const overdue=t.dueDate&&t.dueDate<today&&t.status!=='done';
      row+=`<td onclick="event.stopPropagation()"><div class="cell editable">
        <input type="date" value="${t.dueDate||''}"
          style="font-size:12px;color:${overdue?'#ef4444':'var(--text2)'}"
          onchange="inlineEdit('${t.id}','dueDate',this.value||null)">
      </div></td>`;
    } else if(c.key==='status'){
      row+=`<td onclick="event.stopPropagation()"><div class="cell">
        <select style="background:transparent;border:none;color:${SC[t.status]};font-size:12px;font-weight:600;outline:none;cursor:pointer;font-family:inherit"
          onchange="inlineEdit('${t.id}','status',this.value)">
          ${Object.entries(SL).map(([v,l])=>`<option value="${v}" ${t.status===v?'selected':''} style="color:${SC[v]}">${l}</option>`).join('')}
        </select>
      </div></td>`;
    } else if(c.key==='priority'){
      row+=`<td onclick="event.stopPropagation()"><div class="cell">
        <select style="background:transparent;border:none;color:${PC[t.priority]};font-size:12px;font-weight:600;outline:none;cursor:pointer;font-family:inherit"
          onchange="inlineEdit('${t.id}','priority',this.value)">
          ${Object.entries(PL).map(([v,l])=>`<option value="${v}" ${t.priority===v?'selected':''} style="color:${PC[v]}">${l}</option>`).join('')}
        </select>
      </div></td>`;
    } else if(c.key==='assignee'){
      const u=USERS.find(x=>x.id===t.assignee);
      row+=`<td onclick="event.stopPropagation()"><div class="cell" style="gap:6px">
        ${u?`<div style="width:22px;height:22px;border-radius:50%;background:${u.color};display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;color:#fff;flex-shrink:0">${ini(u.name)}</div>`:''}
        <select style="background:transparent;border:none;color:var(--text);font-size:12px;outline:none;cursor:pointer;font-family:inherit"
          onchange="inlineEdit('${t.id}','assignee',this.value?parseInt(this.value):null)">
          <option value="">Unassigned</option>
          ${USERS.map(u2=>`<option value="${u2.id}" ${t.assignee===u2.id?'selected':''}>${u2.name}</option>`).join('')}
        </select>
      </div></td>`;
    } else {
      row+=`<td></td>`;
    }
  });
  // Custom field cells
  visCFs.forEach(cf=>{ row+=cfInlineCell(t,cf,false); });
  row+=`<td></td></tr>`;
  return row;
}

function inlineEditStart(taskId,val){
  const t=getP()?.tasks.find(x=>x.id===taskId);if(!t)return;
  t.start=val?new Date(val):null;
  if(curView==='table')renderTable();
  if(curView==='gantt')renderGantt();
}

function toggleTblSort(field){
  const p=getP();if(!p)return;
  if(p.sortField===field)p.sortDir=p.sortDir==='asc'?'desc':'asc';
  else{p.sortField=field;p.sortDir='asc';}
  renderProjToolbar();renderTable();
}

"""

assert old_render_table in html, 'renderTable block not found'
html = html.replace(old_render_table, new_render_table, 1)

with open('/home/user/YCxDesign/team-nexus-v3.html', 'w') as f:
    f.write(html)
print('Chunk 3 done')
