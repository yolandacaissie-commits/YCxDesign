#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build out the Workload view — team capacity grid with per-user task bars."""
import os

src = '/home/user/YCxDesign/team-nexus-v3.html'
content = open(src, encoding='utf-8').read()
orig = len(content)

def rp(old, new, label):
    global content
    assert old in content, f"ANCHOR NOT FOUND: {label}\n{repr(old[:120])}"
    content = content.replace(old, new, 1)
    print(f"  OK: {label}")

# ── 1. Replace the Workload nav-more-panel item onclick ───────────────────────
rp(
    """<div class="nav-item" style="font-size:12px" onclick="showStub('Workload','👥','See team capacity across all workspaces.')">""",
    """<div class="nav-item" style="font-size:12px" onclick="showWorkload()">""",
    "Wire Workload nav item"
)

# ── 2. Add view-workload div after view-stub ──────────────────────────────────
rp(
    '<div id="view-stub"',
    '<div id="view-workload" style="display:none;position:absolute;inset:0;overflow-y:auto"></div>\n      <div id="view-stub"',
    "Add view-workload div"
)

# ── 3. Add 'workload' to showView list ───────────────────────────────────────
rp(
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt','inbox','stream','created-by-me','starred','dashboard','reports','report-viewer','calendar'].forEach(",
    "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt','inbox','stream','created-by-me','starred','dashboard','reports','report-viewer','calendar','workload'].forEach(",
    "Add workload to showView list"
)

# ── 4. Add showWorkload + renderWorkload functions ────────────────────────────
rp(
    "function showStream(){",
    r"""function showWorkload(wsId){
  curView='workload';
  setTopbar('Workload','Team capacity across all projects',[]);
  showView('workload');
  closeNavIfMobile();
  renderWorkload(wsId||null);
}
function renderWorkload(filterWsId){
  const el=document.getElementById('view-workload');
  // All tasks across all projects (optionally filtered by workspace)
  const allProjs=filterWsId
    ?PROJECTS.filter(p=>(p.locations||[]).some(l=>l.workspaceId===filterWsId))
    :PROJECTS;
  const allTasks=allProjs.flatMap(p=>p.tasks.map(t=>({...t,projName:p.name,projId:p.id})));
  const openTasks=allTasks.filter(t=>t.status!=='done');

  // Per-user stats
  const userRows=USERS.map(u=>{
    const mine=openTasks.filter(t=>t.assignee===u.id);
    const critical=mine.filter(t=>t.priority==='critical').length;
    const high=mine.filter(t=>t.priority==='high').length;
    const normal=mine.filter(t=>!['critical','high'].includes(t.priority)).length;
    const done=allTasks.filter(t=>t.assignee===u.id&&t.status==='done').length;
    const total=allTasks.filter(t=>t.assignee===u.id).length;
    // Capacity: assume 8h/day, 5d/week = 40h. Use task count as proxy (each task ~4h)
    const estHours=mine.length*4;
    const capHours=40;
    const utilPct=Math.min(Math.round(estHours/capHours*100),120);
    const capColor=utilPct>100?'#ef4444':utilPct>75?'#f59e0b':'#22c55e';
    return {u,mine,critical,high,normal,done,total,estHours,capHours,utilPct,capColor};
  });

  const SC2={todo:'#94a3b8',in_progress:'#1AA6B7',review:'#8b5cf6',done:'#22c55e',blocked:'#ef4444'};

  el.innerHTML=`
  <div style="padding:20px 24px;max-width:1100px;margin:0 auto">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;flex-wrap:wrap;gap:10px">
      <div style="font-size:18px;font-weight:700">Team Workload</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <select class="meta-sel" style="font-size:12px" onchange="renderWorkload(this.value||null)">
          <option value="">All workspaces</option>
          ${WORKSPACES.map(ws=>`<option value="${ws.id}"${filterWsId===ws.id?' selected':''}>${ws.name}</option>`).join('')}
        </select>
        <div style="font-size:12px;display:flex;align-items:center;gap:12px;padding:0 8px;background:var(--surface);border:1px solid var(--border2);border-radius:8px">
          <span style="display:flex;align-items:center;gap:4px"><span style="width:8px;height:8px;border-radius:50%;background:#22c55e;display:inline-block"></span>Under capacity</span>
          <span style="display:flex;align-items:center;gap:4px"><span style="width:8px;height:8px;border-radius:50%;background:#f59e0b;display:inline-block"></span>Near capacity</span>
          <span style="display:flex;align-items:center;gap:4px"><span style="width:8px;height:8px;border-radius:50%;background:#ef4444;display:inline-block"></span>Over capacity</span>
        </div>
      </div>
    </div>

    <!-- Summary KPIs -->
    <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;margin-bottom:24px">
      <div style="background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:14px;text-align:center">
        <div style="font-size:26px;font-weight:700;color:var(--accent)">${openTasks.length}</div>
        <div style="font-size:11px;color:var(--text3);margin-top:2px">Open tasks</div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:14px;text-align:center">
        <div style="font-size:26px;font-weight:700;color:#ef4444">${openTasks.filter(t=>t.priority==='critical').length}</div>
        <div style="font-size:11px;color:var(--text3);margin-top:2px">Critical priority</div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:14px;text-align:center">
        <div style="font-size:26px;font-weight:700;color:#f59e0b">${openTasks.filter(t=>!t.assignee).length}</div>
        <div style="font-size:11px;color:var(--text3);margin-top:2px">Unassigned</div>
      </div>
      <div style="background:var(--surface);border:1px solid var(--border2);border-radius:12px;padding:14px;text-align:center">
        <div style="font-size:26px;font-weight:700;color:#22c55e">${userRows.filter(r=>r.utilPct>100).length}</div>
        <div style="font-size:11px;color:var(--text3);margin-top:2px">Over capacity</div>
      </div>
    </div>

    <!-- Per-user rows -->
    <div style="background:var(--surface);border:1px solid var(--border2);border-radius:14px;overflow:hidden">
      <!-- Header -->
      <div style="display:grid;grid-template-columns:200px 1fr 120px 80px;gap:0;padding:10px 16px;background:var(--bg);border-bottom:1px solid var(--border2);font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.4px;color:var(--text3)">
        <div>Team member</div>
        <div>Task load</div>
        <div>Capacity</div>
        <div>Tasks</div>
      </div>
      ${userRows.map((r,ri)=>`
      <div style="display:grid;grid-template-columns:200px 1fr 120px 80px;gap:0;padding:14px 16px;border-bottom:${ri<userRows.length-1?'1px solid var(--border2)':'none'};align-items:center" onmouseover="this.style.background='var(--bg)'" onmouseout="this.style.background='transparent'">
        <!-- User info -->
        <div style="display:flex;align-items:center;gap:10px">
          <div style="width:34px;height:34px;border-radius:50%;background:${r.u.color};display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff;flex-shrink:0">${r.u.name.split(' ').map(w=>w[0]).join('').slice(0,2)}</div>
          <div>
            <div style="font-size:13px;font-weight:600">${r.u.name}</div>
            <div style="font-size:11px;color:var(--text3)">${r.u.role||'Team member'}</div>
          </div>
        </div>
        <!-- Task bar -->
        <div style="padding-right:16px">
          ${r.mine.length===0?`<div style="font-size:11px;color:var(--text3);font-style:italic">No open tasks</div>`:`
          <div style="display:flex;height:12px;border-radius:6px;overflow:hidden;background:var(--bg);border:1px solid var(--border2);margin-bottom:6px">
            ${r.critical?`<div style="flex:${r.critical};background:#ef4444;min-width:4px" title="${r.critical} critical"></div>`:''}
            ${r.high?`<div style="flex:${r.high};background:#f59e0b;min-width:4px" title="${r.high} high"></div>`:''}
            ${r.normal?`<div style="flex:${r.normal};background:#1AA6B7;min-width:4px" title="${r.normal} normal/low"></div>`:''}
          </div>
          <div style="display:flex;gap:8px;flex-wrap:wrap">
            ${r.critical?`<span style="font-size:10px;color:#ef4444;font-weight:600">${r.critical} critical</span>`:''}
            ${r.high?`<span style="font-size:10px;color:#f59e0b;font-weight:600">${r.high} high</span>`:''}
            ${r.normal?`<span style="font-size:10px;color:var(--text3)">${r.normal} normal</span>`:''}
          </div>`}
        </div>
        <!-- Capacity bar -->
        <div>
          <div style="display:flex;align-items:center;gap:6px;margin-bottom:4px">
            <div style="flex:1;height:6px;background:var(--border2);border-radius:3px;overflow:hidden">
              <div style="height:100%;width:${Math.min(r.utilPct,100)}%;background:${r.capColor};border-radius:3px;transition:width .4s"></div>
            </div>
            <span style="font-size:10px;font-weight:700;color:${r.capColor};min-width:30px;text-align:right">${r.utilPct}%</span>
          </div>
          <div style="font-size:10px;color:var(--text3)">~${r.estHours}h / ${r.capHours}h cap</div>
        </div>
        <!-- Task count -->
        <div style="text-align:center">
          <div style="font-size:20px;font-weight:700;color:${r.mine.length>0?'var(--text)':'var(--text3)'}">${r.mine.length}</div>
          <div style="font-size:10px;color:var(--text3)">${r.done} done</div>
        </div>
      </div>
      <!-- Expandable task list on click — show tasks below row on hover -->
      `).join('')}
    </div>

    <!-- Unassigned tasks section -->
    ${openTasks.filter(t=>!t.assignee).length?`
    <div style="margin-top:20px">
      <div style="font-size:13px;font-weight:700;margin-bottom:10px;color:var(--text2)">Unassigned tasks (${openTasks.filter(t=>!t.assignee).length})</div>
      <div style="background:var(--surface);border:1px solid var(--border2);border-radius:12px;overflow:hidden">
        ${openTasks.filter(t=>!t.assignee).slice(0,8).map((t,i,arr)=>`
        <div style="display:flex;align-items:center;gap:10px;padding:10px 14px;border-bottom:${i<arr.length-1?'1px solid var(--border2)':'none'};cursor:pointer" onclick="openProject('${t.projId}');setTimeout(()=>openTask('${t.id}'),200)">
          <span style="width:8px;height:8px;border-radius:50%;background:${SC2[t.status]||'#94a3b8'};flex-shrink:0"></span>
          <span style="flex:1;font-size:12px;font-weight:500">${t.title}</span>
          <span style="font-size:11px;color:var(--text3)">${t.projName}</span>
          <span style="font-size:10px;padding:2px 7px;border-radius:6px;background:${SC2[t.status]||'#94a3b8'}22;color:${SC2[t.status]||'#94a3b8'};font-weight:600">${SL[t.status]||t.status}</span>
        </div>`).join('')}
      </div>
    </div>`:''}
  </div>`;
}
function showStream(){""",
    "Add showWorkload + renderWorkload"
)

# ── Safe write ────────────────────────────────────────────────────────────────
tmp = src + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(tmp, src)
print(f"\nDone — {orig} -> {len(content)} chars ({len(content)-orig:+d})")
