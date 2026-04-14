#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fix showDashboards() top-nav to list real dashboards + open them."""
import os

src = '/home/user/YCxDesign/team-nexus-v3.html'
content = open(src, encoding='utf-8').read()
orig = len(content)

def rp(old, new, label):
    global content
    assert old in content, f"ANCHOR NOT FOUND: {label}\n{repr(old[:120])}"
    content = content.replace(old, new, 1)
    print(f"  OK: {label}")

# ── 1. Replace showDashboards() with a real dashboard listing ────────────────
rp(
    """function showDashboards(){
  curView='stub';setTopbar('Dashboards','Visual KPI and overview',[]);showView('stub');closeNavIfMobile();
  document.getElementById('view-stub').innerHTML=`<div class="stub-view topo-bg">
    <div class="stub-icon">🔲</div><div class="stub-title">Dashboards</div>
    <div class="stub-sub">Build custom dashboards with charts, task lists and metrics. Select a workspace or view account-wide.</div>
    <div class="stub-ds-row">
      <div class="stub-ds-btn on">Entire account</div>
      ${WORKSPACES.map(ws=>`<div class="stub-ds-btn" onclick="this.parentElement.querySelectorAll('.stub-ds-btn').forEach(b=>b.classList.remove('on'));this.classList.add('on')">${ws.name}</div>`).join('')}
    </div>
  </div>`;
}""",
    r"""function showDashboards(filterWsId){
  curView='stub';
  setTopbar('Dashboards','All dashboards you have access to',[]);
  showView('stub');
  closeNavIfMobile();
  const dashTools=WORKSPACE_TOOLS.filter(t=>t.type==='dashboard');
  const filtered=filterWsId?dashTools.filter(t=>t.wsId===filterWsId):dashTools;
  document.getElementById('view-stub').innerHTML=`
    <div style="padding:20px 24px;max-width:900px;margin:0 auto">
      <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
        <div style="font-size:20px;font-weight:700">Dashboards</div>
        <button class="btn" onclick="showWsToolsMenu(WORKSPACES[0].id,event)" style="font-size:12px">+ New dashboard</button>
      </div>
      <!-- Workspace filter tabs -->
      <div style="display:flex;gap:8px;margin-bottom:20px;flex-wrap:wrap">
        <div class="stub-ds-btn${!filterWsId?' on':''}" onclick="showDashboards(null)">All workspaces</div>
        ${WORKSPACES.map(ws=>`<div class="stub-ds-btn${filterWsId===ws.id?' on':''}" onclick="showDashboards('${ws.id}')">${ws.name}</div>`).join('')}
      </div>
      <!-- Dashboard cards -->
      ${filtered.length===0?`<div style="text-align:center;padding:60px 20px;color:var(--text3)">
        <div style="font-size:40px;margin-bottom:12px">📊</div>
        <div style="font-size:15px;font-weight:600;margin-bottom:6px">No dashboards yet</div>
        <div style="font-size:13px">Add a dashboard from a workspace's Tools section in the sidebar.</div>
      </div>`:`
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px">
        ${filtered.map(t=>{
          const ws=WORKSPACES.find(w=>w.id===t.wsId)||{name:'Unknown'};
          const wsProjects=PROJECTS.filter(p=>(p.locations||[]).some(l=>l.workspaceId===t.wsId));
          const doneTasks=wsProjects.flatMap(p=>p.tasks).filter(t=>t.status==='done').length;
          const totalTasks=wsProjects.flatMap(p=>p.tasks).length;
          const pct=totalTasks?Math.round(doneTasks/totalTasks*100):0;
          return `<div onclick="openWsTool('${t.id}')" style="background:var(--surface);border:1px solid var(--border2);border-radius:14px;padding:18px;cursor:pointer;transition:.15s;position:relative" onmouseover="this.style.borderColor='var(--accent)';this.style.boxShadow='0 4px 16px rgba(26,166,183,.12)'" onmouseout="this.style.borderColor='var(--border2)';this.style.boxShadow='none'">
            <div style="display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px">
              <div style="width:36px;height:36px;border-radius:10px;background:rgba(26,166,183,.12);display:flex;align-items:center;justify-content:center;font-size:18px">📊</div>
              <span style="font-size:10px;padding:2px 8px;background:var(--abg);color:var(--accent);border-radius:8px;font-weight:600">${ws.name}</span>
            </div>
            <div style="font-size:14px;font-weight:700;margin-bottom:4px">${t.name}</div>
            <div style="font-size:12px;color:var(--text3);margin-bottom:12px">${wsProjects.length} projects &nbsp;·&nbsp; ${totalTasks} tasks</div>
            <div style="height:4px;background:var(--border2);border-radius:2px;overflow:hidden">
              <div style="height:100%;width:${pct}%;background:var(--accent);border-radius:2px"></div>
            </div>
            <div style="font-size:11px;color:var(--text3);margin-top:4px">${pct}% complete</div>
          </div>`;
        }).join('')}
      </div>`}
    </div>`;
}""",
    "Replace showDashboards with real dashboard listing"
)

# ── 2. Add stub-ds-btn CSS if not already polished ──────────────────────────
# Check if stub-ds-btn on-state is styled
if '.stub-ds-btn.on{' not in content and '.stub-ds-btn.on ' not in content:
    rp(
        '.dash-widget-row:last-child{border-bottom:none}',
        """.dash-widget-row:last-child{border-bottom:none}
.stub-ds-row{display:flex;gap:8px;margin-top:16px;flex-wrap:wrap;justify-content:center}
.stub-ds-btn{padding:6px 14px;border-radius:20px;font-size:12px;font-weight:600;cursor:pointer;background:var(--bg);border:1px solid var(--border2);color:var(--text2);transition:.15s}
.stub-ds-btn:hover{border-color:var(--accent);color:var(--accent)}
.stub-ds-btn.on{background:var(--accent);border-color:var(--accent);color:#fff}""",
        "Add stub-ds-btn CSS"
    )

# ── Safe write ────────────────────────────────────────────────────────────────
tmp = src + '.tmp'
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(content)
os.replace(tmp, src)
print(f"\nDone — {orig} -> {len(content)} chars ({len(content)-orig:+d})")
