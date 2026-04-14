#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

src = '/home/user/YCxDesign/team-nexus-v3.html'
content = open(src, encoding='utf-8').read()
orig = len(content)

def rp(old, new, label):
    global content
    assert old in content, f"ANCHOR NOT FOUND: {label}\n{repr(old[:120])}"
    content = content.replace(old, new, 1)
    print(f"  OK: {label}")

# ═══ CHUNK 5: Star functions + button in task detail panel ═══════════════════

rp(
    '// ═══════════════════════ TASK DETAIL ═══════════════════════\nfunction openTask(id){',
    '''// ═══════════════════════ TASK DETAIL ═══════════════════════
function toggleTaskStar(taskId,btn){
  STARRED_ITEMS.tasks[taskId]=!STARRED_ITEMS.tasks[taskId];
  if(btn){btn.textContent=STARRED_ITEMS.tasks[taskId]?'\u2605':'\u2606';
    btn.style.color=STARRED_ITEMS.tasks[taskId]?'#f59e0b':'var(--text3)';}
}
function toggleProjectStar(projId,btn){
  STARRED_ITEMS.projects[projId]=!STARRED_ITEMS.projects[projId];
  if(btn){btn.textContent=STARRED_ITEMS.projects[projId]?'\u2605':'\u2606';
    btn.style.color=STARRED_ITEMS.projects[projId]?'#f59e0b':'var(--text3)';}
}
function openTask(id){''',
    "Add toggleTaskStar + toggleProjectStar"
)

# Add star button inside the det-head, before close-btn
rp(
    '    <button class="close-btn" onclick="closeDetail()">✕</button>\n  </div>',
    '''    <button id="det-star-btn" onclick="toggleTaskStar(selTaskId,this)" style="background:none;border:none;cursor:pointer;font-size:18px;color:var(--text3);padding:0 2px;flex-shrink:0;line-height:1;align-self:flex-start;margin-top:2px" title="Star task">\u2606</button>
    <button class="close-btn" onclick="closeDetail()">✕</button>
  </div>''',
    "Add star to detail panel header"
)

# Sync star button state when panel opens — add after populateDetail call
rp(
    '    populateDetail(t);\n    document.getElementById(\'detail\').classList.add(\'open\');',
    '''    populateDetail(t);
    const sb=document.getElementById('det-star-btn');
    if(sb){sb.textContent=STARRED_ITEMS.tasks[id]?'\u2605':'\u2606';sb.style.color=STARRED_ITEMS.tasks[id]?'#f59e0b':'var(--text3)';}
    document.getElementById('detail').classList.add('open');''',
    "Sync star state on open"
)

# ═══ CHUNK 6: Customize Menu modal ═══════════════════════════════════════════
rp(
    "function showCustomizeMenu(){\n  showStub('Customize Menu','\u2699\ufe0f','Drag-and-drop sidebar customization coming in the next update.');\n}",
    r"""let HIDDEN_NAV={};
function showCustomizeMenu(){
  const navItems=[
    {key:'inbox',label:'Inbox',icon:'&#128229;'},
    {key:'mytasks',label:'My To-Do',icon:'&#10004;&#65039;'},
    {key:'timesheets',label:'Timesheets',icon:'&#9200;'},
    {key:'workload',label:'Workload',icon:'&#128101;'},
    {key:'created_by_me',label:'Created by me',icon:'&#9733;'},
    {key:'stream',label:'Stream',icon:'&#128172;'},
    {key:'starred',label:'Starred tasks',icon:'&#11088;'},
    {key:'dashboards',label:'Dashboards',icon:'&#128202;'},
    {key:'reports',label:'Reports',icon:'&#128203;'},
    {key:'calendars',label:'Calendars',icon:'&#128197;'},
    {key:'forms',label:'Forms',icon:'&#128221;'},
    {key:'settings',label:'Settings',icon:'&#9881;&#65039;'},
  ];
  const modal=document.createElement('div');
  modal.className='modal-overlay';
  modal.innerHTML=`<div class="modal" style="max-width:400px">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px">
      <div style="font-size:15px;font-weight:700">Customize sidebar menu</div>
      <button onclick="this.closest('.modal-overlay').remove()" style="background:none;border:none;font-size:20px;cursor:pointer;color:var(--text3)">&times;</button>
    </div>
    <div style="font-size:12px;color:var(--text3);margin-bottom:12px">Toggle items to show or hide them in your sidebar.</div>
    ${navItems.map(item=>`
      <div style="display:flex;align-items:center;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--border2)">
        <div style="display:flex;align-items:center;gap:8px;font-size:13px">
          <span style="font-size:15px">${item.icon}</span>
          <span>${item.label}</span>
        </div>
        <div class="toggle-sw${!HIDDEN_NAV[item.key]?' on':''}" onclick="HIDDEN_NAV['${item.key}']=!!HIDDEN_NAV['${item.key}']?false:true;this.classList.toggle('on')"></div>
      </div>`).join('')}
    <div style="margin-top:14px;display:flex;justify-content:flex-end;gap:8px">
      <button class="btn ghost" onclick="this.closest('.modal-overlay').remove()">Cancel</button>
      <button class="btn" onclick="this.closest('.modal-overlay').remove()">Save</button>
    </div>
  </div>`;
  document.body.appendChild(modal);
  modal.addEventListener('click',e=>{if(e.target===modal)modal.remove();});
}""",
    "Add Customize Menu modal"
)

# ═══ CHUNK 7a: Outlook → Coming Soon ════════════════════════════════════════
rp(
    """<button class="btn ghost" style="font-size:12px" onclick="alert('Outlook sync requires backend setup \u2014 coming soon!')">Connect</button>""",
    """<button class="btn ghost" style="font-size:12px;opacity:.6;cursor:not-allowed" disabled>Connect <span style="font-size:9px;background:#22c55e;color:#fff;border-radius:8px;padding:1px 6px;margin-left:4px;font-weight:700">Soon</span></button>""",
    "Outlook Coming Soon badge"
)

# ═══ CHUNK 7b: Schedule editor — replace alert with real editor modal ════════
rp(
    """function editSchedule(id){
  const s=WORK_SCHEDULES.find(x=>x.id===id);if(!s)return;
  alert('Schedule editor coming soon \u2014 will allow editing holidays, work days, and hours for "'+s.name+'"');
}""",
    r"""function editSchedule(id){
  const s=WORK_SCHEDULES.find(x=>x.id===id);if(!s)return;
  // Remove existing modal if re-opening
  const existMod=document.getElementById('sch-edit-modal');if(existMod)existMod.remove();
  const DAYS=['Su','Mo','Tu','We','Th','Fr','Sa'];
  const MONTH_NAMES=['January','February','March','April','May','June','July','August','September','October','November','December'];
  const year=new Date().getFullYear();
  function daysInMonth(y,m){return new Date(y,m+1,0).getDate();}
  function makeMonthCal(y,m){
    const first=new Date(y,m,1).getDay();
    const days=daysInMonth(y,m);
    let rows='<tr>';let col=0;
    for(let i=0;i<first;i++){rows+='<td></td>';col++;}
    for(let d=1;d<=days;d++){
      const ds=`${y}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      const hol=s.holidays?s.holidays.find(h=>h.date===ds):null;
      const dow=new Date(y,m,d).getDay();
      const isWeekend=!s.workDays.includes(dow);
      rows+=`<td class="sch-cal-day${hol?' sch-holiday':''}${isWeekend&&!hol?' sch-weekend':''}" onclick="addSchedException('${id}','${ds}',this)" title="${hol?hol.name:ds}">${d}</td>`;
      col++;
      if(col%7===0&&d<days)rows+='</tr><tr>';
    }
    rows+='</tr>';
    return `<div class="sch-month-block"><div class="sch-month-name">${MONTH_NAMES[m]}</div>
      <table class="sch-mini-cal"><thead><tr>${DAYS.map(d=>`<th>${d}</th>`).join('')}</tr></thead>
      <tbody>${rows}</tbody></table></div>`;
  }
  if(!s.holidays)s.holidays=[];
  const workDayCount=(()=>{let c=0;for(let m=0;m<12;m++){const days=daysInMonth(year,m);for(let d=1;d<=days;d++){const dow=new Date(year,m,d).getDay();const ds=`${year}-${String(m+1).padStart(2,'0')}-${String(d).padStart(2,'0')}`;if(s.workDays.includes(dow)&&!s.holidays.find(h=>h.date===ds))c++;}}return c;})();
  const modal=document.createElement('div');
  modal.id='sch-edit-modal';
  modal.className='modal-overlay';
  modal.innerHTML=`<div class="modal" style="max-width:900px;width:98vw;max-height:90vh;overflow-y:auto">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;position:sticky;top:0;background:var(--surface);padding:4px 0;z-index:1;border-bottom:1px solid var(--border2)">
      <div style="font-size:15px;font-weight:700">Work schedule: ${s.name}</div>
      <button onclick="this.closest('.modal-overlay').remove()" style="background:none;border:none;font-size:20px;cursor:pointer;color:var(--text3)">&times;</button>
    </div>
    <div class="sch-info-banner">
      Set up work schedules to avoid planning work on holidays or off days. Click any day to add an exception.
      <a href="#" onclick="return false" style="color:var(--accent);margin-left:6px">Got it!</a>
    </div>
    <div style="display:flex;gap:32px;margin:12px 0;flex-wrap:wrap;align-items:flex-start">
      <div>
        <div style="font-size:12px;font-weight:700;margin-bottom:6px;color:var(--text2)">Workweek</div>
        <div style="display:flex;gap:4px">
          ${DAYS.map((d,i)=>`<div class="sch-day-toggle${s.workDays.includes(i)?' on':''}" onclick="
            const idx=${i};const sch=WORK_SCHEDULES.find(x=>x.id==='${id}');
            if(sch.workDays.includes(idx))sch.workDays=sch.workDays.filter(x=>x!==idx);
            else sch.workDays.push(idx);
            this.classList.toggle('on')">${d}</div>`).join('')}
        </div>
      </div>
      <div>
        <div style="font-size:12px;font-weight:700;margin-bottom:6px;color:var(--text2)">Daily capacity</div>
        <div style="font-size:22px;font-weight:700;color:var(--accent)">${s.workHours?.hoursPerDay||8}h</div>
        <div style="font-size:11px;color:var(--text3)">${(s.workHours?.hoursPerDay||8)*5}h / week</div>
      </div>
      <div>
        <div style="font-size:12px;font-weight:700;margin-bottom:6px;color:var(--text2)">Year ${year}</div>
        <div style="font-size:13px;color:var(--text2)">Working days: <strong>${workDayCount}d</strong></div>
        <div style="font-size:13px;color:var(--text2)">Non-working days: <strong>${365-workDayCount}d</strong></div>
        ${s.holidays.length?`<div style="font-size:12px;color:var(--text3);margin-top:4px">
          <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:#1AA6B7;margin-right:4px"></span>
          Holidays: <strong>${s.holidays.length}d</strong></div>`:''}
      </div>
    </div>
    <div class="sch-cal-grid" id="sch-cal-grid-${id}">
      ${Array.from({length:12},(_,m)=>makeMonthCal(year,m)).join('')}
    </div>
    <div style="display:flex;justify-content:flex-end;gap:8px;margin-top:16px;padding-top:12px;border-top:1px solid var(--border2)">
      <button class="btn ghost" onclick="this.closest('.modal-overlay').remove()">Cancel</button>
      <button class="btn" onclick="this.closest('.modal-overlay').remove()">Save changes</button>
    </div>
  </div>`;
  document.body.appendChild(modal);
  modal.addEventListener('click',e=>{if(e.target===modal)modal.remove();});
}
function addSchedException(schedId,date,el){
  const s=WORK_SCHEDULES.find(x=>x.id===schedId);if(!s)return;
  if(!s.holidays)s.holidays=[];
  const existing=s.holidays.find(h=>h.date===date);
  const types=[
    {key:'holiday',label:'Public holiday'},
    {key:'nonwork',label:'Other non-working'},
    {key:'extra',label:'Extra workday'},
    {key:'capacity',label:'Capacity change'},
  ];
  // Remove any existing popup
  document.querySelectorAll('.sch-popup').forEach(p=>p.remove());
  const popup=document.createElement('div');
  popup.className='ptb-menu sch-popup';
  const rect=el.getBoundingClientRect();
  popup.style.cssText=`position:fixed;left:${Math.min(rect.right+4,window.innerWidth-200)}px;top:${rect.top}px;min-width:180px;z-index:9999`;
  popup.innerHTML=`<div style="padding:8px 12px;font-size:11px;font-weight:700;color:var(--text3);border-bottom:1px solid var(--border2)">${date}${existing?' \u2014 '+existing.name:''}</div>
    ${types.map(t=>`<div class="ptb-menu-item" onclick="
      const sch=WORK_SCHEDULES.find(x=>x.id==='${schedId}');
      if(!sch.holidays)sch.holidays=[];
      if('${t.key}'==='holiday'||'${t.key}'==='nonwork'){
        sch.holidays=sch.holidays.filter(h=>h.date!=='${date}');
        sch.holidays.push({name:'${t.label}',date:'${date}',type:'${t.key}'});
      } else if('${t.key}'==='extra'){
        sch.holidays=sch.holidays.filter(h=>h.date!=='${date}');
      }
      this.closest('.sch-popup').remove();
      editSchedule('${schedId}');">${t.label}</div>`).join('')}
    ${existing?`<div class="ptb-menu-item" style="color:#ef4444" onclick="
      const sch=WORK_SCHEDULES.find(x=>x.id==='${schedId}');
      if(sch.holidays)sch.holidays=sch.holidays.filter(h=>h.date!=='${date}');
      this.closest('.sch-popup').remove();
      editSchedule('${schedId}')">Remove exception</div>`:''}
  `;
  document.body.appendChild(popup);
  setTimeout(()=>document.addEventListener('click',function h(){popup.remove();document.removeEventListener('click',h);},{once:true}),10);
}""",
    "Replace editSchedule with full schedule editor"
)

# ═══ CHUNK 7c: Billing — improve download button ════════════════════════════
rp(
    """<td><button class="icon-btn" onclick="alert('PDF download requires backend integration')">⬇</button></td>""",
    '<td><a style="color:var(--accent);font-size:12px;font-weight:600;text-decoration:none;cursor:pointer" onclick="alert(\'Invoice download requires server-side PDF generation — coming soon!\')">Download</a></td>',
    "Fix billing download button"
)

# ═══ CHUNK 7d: Add schedule editor CSS ══════════════════════════════════════
rp(
    ".cal-today-line::before{content:'';position:absolute;top:-1px;left:-4px;width:10px;height:10px;border-radius:50%;background:#3b82f6}",
    """.cal-today-line::before{content:'';position:absolute;top:-1px;left:-4px;width:10px;height:10px;border-radius:50%;background:#3b82f6}
/* Schedule editor */
.sch-info-banner{background:rgba(26,166,183,.08);border:1px solid var(--accent);border-radius:8px;padding:10px 14px;font-size:12px;color:var(--text2);margin-bottom:14px}
.sch-cal-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:14px;margin-top:12px}
.sch-month-block{background:var(--surface);border:1px solid var(--border2);border-radius:10px;padding:10px}
.sch-month-name{font-size:12px;font-weight:700;margin-bottom:8px;text-align:center;color:var(--text2)}
.sch-mini-cal{width:100%;border-collapse:collapse;font-size:11px}
.sch-mini-cal th{padding:2px 3px;text-align:center;color:var(--text3);font-weight:600}
.sch-mini-cal td{padding:0;text-align:center;height:22px}
.sch-cal-day{width:22px;height:22px;border-radius:50%;cursor:pointer;display:inline-flex;align-items:center;justify-content:center;font-size:10px;margin:1px auto}
.sch-cal-day:hover{background:var(--abg);color:var(--accent)}
.sch-holiday{background:#1AA6B7!important;color:#fff!important;border-radius:50%;font-weight:700}
.sch-weekend{color:#ef4444;opacity:.7}
.sch-day-toggle{width:28px;height:28px;border-radius:50%;border:2px solid var(--border2);display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;cursor:pointer;transition:.15s;color:var(--text3);user-select:none}
.sch-day-toggle.on{background:var(--accent);border-color:var(--accent);color:#fff}""",
    "Add Schedule Editor CSS"
)

# ── Safe write ────────────────────────────────────────────────────────────────
tmp = src + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(tmp, src)
print(f"\nDone — {orig} -> {len(content)} chars ({len(content)-orig:+d})")
