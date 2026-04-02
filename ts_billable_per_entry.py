#!/usr/bin/env python3
content = open('/home/user/YCxDesign/team-nexus-v3.html').read()
orig_len = len(content)

# ── 1. Add global NON_BILL_ACTS + isEntryBillable after TASK_BILLABLE ──────────
old_tb = "let TASK_BILLABLE={}; // {taskId: false} means Non-Billable; default (undefined/true) = Billable"
new_tb = """let TASK_BILLABLE={}; // kept for compat; per-entry billable now lives on TIMESHEET_ENTRIES
const NON_BILL_ACTS=new Set(['DF Holiday','Leaves','Comp Off','HR Activities (Avengers)',
  'Training','Recruitment','Performance Reviews','All Hands Meeting',
  'Internal Meetings','Casual Catch Ups']);
function isEntryBillable(e){
  if(!e) return true;
  if(typeof e.billable==='boolean') return e.billable;
  return !NON_BILL_ACTS.has(e.activity);
}"""
assert old_tb in content, "ANCHOR 1 not found"
content = content.replace(old_tb, new_tb, 1)

# ── 2. Remove the Billable column (110px) from gridCols ───────────────────────
old_gc = "const gridCols=`2fr 110px repeat(7,1fr) 70px 100px`;"
new_gc = "const gridCols=`2fr repeat(7,1fr) 70px 100px`;"
assert old_gc in content, "ANCHOR 2 not found"
content = content.replace(old_gc, new_gc, 1)

# ── 3. Replace local billableBtn helper with nothing (globals handle it) ──────
old_bfn = """  function billableBtn(taskId){
    const isBillable=TASK_BILLABLE[taskId]!==false;
    return `<div style="display:flex;gap:4px;align-items:center">
      <button onclick="setTaskBillable('${taskId}',true)" style="flex:1;padding:3px 0;border-radius:5px 0 0 5px;font-size:10px;font-weight:700;cursor:pointer;border:1px solid ${isBillable?'var(--accent)':'var(--border2)'};background:${isBillable?'var(--accent)':'transparent'};color:${isBillable?'#fff':'var(--text3)'}">Billable</button>
      <button onclick="setTaskBillable('${taskId}',false)" style="flex:1;padding:3px 0;border-radius:0 5px 5px 0;font-size:10px;font-weight:700;cursor:pointer;border:1px solid ${!isBillable?'#ef4444':'var(--border2)'};border-left:none;background:${!isBillable?'#ef4444':'transparent'};color:${!isBillable?'#fff':'var(--text3)'}">Non-Bill</button>
    </div>`;
  }"""
assert old_bfn in content, "ANCHOR 3 not found"
content = content.replace(old_bfn, "", 1)

# ── 4. Remove Billable column header ─────────────────────────────────────────
old_bh = "\n        <div class=\"ts-head-cell\">Billable</div>"
assert old_bh in content, "ANCHOR 4 not found"
content = content.replace(old_bh, "", 1)

# ── 5. Remove per-row billable cell (old column) ──────────────────────────────
old_bc = "\n          <div class=\"ts-day-cell\" style=\"align-items:center;padding:4px 6px\">${billableBtn(t.id)}</div>"
assert old_bc in content, "ANCHOR 5 not found"
content = content.replace(old_bc, "", 1)

# ── 6. Add per-cell B/NB chip inside each day cell ───────────────────────────
old_cell = """return `<div class="ts-day-cell${isToday?' ts-today-cell':''}">
              <input class="ts-inp" type="number" min="0" max="24" step="0.5" placeholder="—"
                value="${e?e.hours:''}"
                onchange="saveTimeEntry('${t.id}','${dateStr}',this.value,this.nextElementSibling.value)">
              <select class="ts-act-sel" onchange="saveTimeEntry('${t.id}','${dateStr}',this.previousElementSibling.value,this.value)">
                ${actOpts(e)}
              </select>
            </div>`;"""
new_cell = """const bill=isEntryBillable(e);
            return `<div class="ts-day-cell${isToday?' ts-today-cell':''}">
              <input class="ts-inp" type="number" min="0" max="24" step="0.5" placeholder="—"
                value="${e?e.hours:''}"
                onchange="saveTimeEntry('${t.id}','${dateStr}',this.value,this.nextElementSibling.value)">
              <select class="ts-act-sel" onchange="saveTimeEntry('${t.id}','${dateStr}',this.previousElementSibling.value,this.value)">
                ${actOpts(e)}
              </select>
              ${e?`<span class="ts-bill-chip${bill?'':' nb'}"
                onclick="toggleEntryBillable('${t.id}','${dateStr}')"
                title="${bill?'Billable — click to mark non-billable':'Non-billable — click to mark billable'}"
              >${bill?'B':'NB'}</span>`:''}
            </div>`;"""
assert old_cell in content, "ANCHOR 6 not found"
content = content.replace(old_cell, new_cell, 1)

# ── 7. Remove empty billable grand cell in totals row ────────────────────────
old_gr = """        <div class="ts-grand" style="text-align:left;padding-left:14px;font-weight:700">Daily totals</div>
        <div class="ts-grand"></div>
        ${days.map"""
new_gr = """        <div class="ts-grand" style="text-align:left;padding-left:14px;font-weight:700">Daily totals</div>
        ${days.map"""
assert old_gr in content, "ANCHOR 7 not found"
content = content.replace(old_gr, new_gr, 1)

# ── 8. Update footer billable totals to use per-entry ────────────────────────
old_foot = """      &nbsp;·&nbsp; Billable: <strong style="color:var(--accent)">${myTasks.filter(t=>TASK_BILLABLE[t.id]!==false).reduce((s,t)=>s+rowTotal(t.id),0)}h</strong>
      &nbsp;·&nbsp; Non-billable: <strong>${myTasks.filter(t=>TASK_BILLABLE[t.id]===false).reduce((s,t)=>s+rowTotal(t.id),0)}h</strong>"""
new_foot = """      &nbsp;·&nbsp; Billable: <strong style="color:var(--accent)">${TIMESHEET_ENTRIES.filter(e=>e.userId===tsUserId&&days.some(d=>fmtDate(d)===e.date)&&isEntryBillable(e)).reduce((s,e)=>s+e.hours,0)}h</strong>
      &nbsp;·&nbsp; Non-billable: <strong>${TIMESHEET_ENTRIES.filter(e=>e.userId===tsUserId&&days.some(d=>fmtDate(d)===e.date)&&!isEntryBillable(e)).reduce((s,e)=>s+e.hours,0)}h</strong>"""
assert old_foot in content, "ANCHOR 8 not found"
content = content.replace(old_foot, new_foot, 1)

# ── 9. Update saveTimeEntry to store billable per entry ───────────────────────
old_save = """  const ex=TIMESHEET_ENTRIES.find(e=>e.userId===tsUserId&&e.taskId===taskId&&e.date===date);
  if(ex){ex.hours=h;ex.activity=activity||'Development Work';}
  else TIMESHEET_ENTRIES.push({id:'te'+Date.now(),userId:tsUserId,taskId,date,hours:h,activity:activity||'Development Work'});"""
new_save = """  const act=activity||'Development Work';
  const ex=TIMESHEET_ENTRIES.find(e=>e.userId===tsUserId&&e.taskId===taskId&&e.date===date);
  if(ex){ex.hours=h;ex.activity=act;if(typeof ex.billable!=='boolean')ex.billable=!NON_BILL_ACTS.has(act);}
  else TIMESHEET_ENTRIES.push({id:'te'+Date.now(),userId:tsUserId,taskId,date,hours:h,activity:act,billable:!NON_BILL_ACTS.has(act)});"""
assert old_save in content, "ANCHOR 9 not found"
content = content.replace(old_save, new_save, 1)

# ── 10. Add toggleEntryBillable global function ───────────────────────────────
old_stb = """function setTaskBillable(taskId,val){
  TASK_BILLABLE[taskId]=val;
  renderTimesheets();
}"""
new_stb = """function setTaskBillable(taskId,val){
  TASK_BILLABLE[taskId]=val;
  renderTimesheets();
}
function toggleEntryBillable(taskId,date){
  const e=TIMESHEET_ENTRIES.find(e=>e.userId===tsUserId&&e.taskId===taskId&&e.date===date);
  if(e) e.billable=!isEntryBillable(e);
  renderTimesheets();
}"""
assert old_stb in content, "ANCHOR 10 not found"
content = content.replace(old_stb, new_stb, 1)

# ── 11. Add .ts-bill-chip CSS ─────────────────────────────────────────────────
old_today_css = ".ts-today-cell{background:var(--abg);border-radius:6px}"
new_today_css = """.ts-today-cell{background:var(--abg);border-radius:6px}
.ts-bill-chip{display:inline-flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;padding:1px 5px;border-radius:3px;cursor:pointer;background:var(--accent);color:#fff;letter-spacing:.3px;user-select:none;margin-top:2px;align-self:center}
.ts-bill-chip.nb{background:#ef4444}
.ts-bill-chip:hover{opacity:.8}"""
assert old_today_css in content, "ANCHOR 11 not found"
content = content.replace(old_today_css, new_today_css, 1)

open('/home/user/YCxDesign/team-nexus-v3.html','w').write(content)
print(f"Done — {orig_len} → {len(content)} chars ({len(content)-orig_len:+d})")
