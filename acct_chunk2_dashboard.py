#!/usr/bin/env python3
"""Chunk 2: Account Management Dashboard — HTML div, CSS, JS."""
with open('/home/user/YCxDesign/team-nexus-v3.html', 'r') as f:
    html = f.read()

# ── 1. Add view-account-mgmt div after view-financial ──
old_fin_div = '<div id="view-financial" style="display:none;position:absolute;inset:0;overflow-y:auto;padding:24px"></div>'
new_fin_div = '<div id="view-financial" style="display:none;position:absolute;inset:0;overflow-y:auto;padding:24px"></div>\n    <div id="view-account-mgmt" style="display:none;position:absolute;inset:0;overflow-y:auto;padding:24px"></div>'
assert old_fin_div in html
html = html.replace(old_fin_div, new_fin_div, 1)

# ── 2. Add view to showView list ──
old_sv = "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial']"
new_sv = "['welcome','home','projects','workspace','board','table','gantt','settings','forms','timesheet','stub','financial','account-mgmt']"
assert old_sv in html
html = html.replace(old_sv, new_sv, 1)

# ── 3. Add CSS ──
acct_css = """
/* ── ACCOUNT MANAGEMENT DASHBOARD ── */
.acct-page{max-width:1200px;margin:0 auto}
.acct-toolbar{display:flex;align-items:center;gap:10px;margin-bottom:16px;flex-wrap:wrap}
.acct-search{display:flex;align-items:center;gap:7px;background:var(--surface);border:1px solid var(--border2);border-radius:8px;padding:6px 12px;flex:1;max-width:280px}
.acct-search input{flex:1;border:none;background:transparent;font-size:12.5px;color:var(--text);outline:none}
.acct-filter-btn{display:flex;align-items:center;gap:5px;padding:5px 12px;border-radius:8px;font-size:12px;font-weight:600;border:1px solid var(--border2);background:var(--surface);color:var(--text2);cursor:pointer;transition:all .15s}
.acct-filter-btn:hover{border-color:var(--accent);color:var(--accent)}
.acct-filter-btn.active{background:var(--abg);border-color:var(--accent);color:var(--accent)}
.acct-table-wrap{background:var(--surface);border:1px solid var(--border2);border-radius:12px;overflow:hidden}
.acct-overview-title{font-size:13px;font-weight:700;color:var(--text);padding:14px 16px;border-bottom:1px solid var(--border2);display:flex;align-items:center;gap:6px}
.acct-overview-count{font-size:12px;font-weight:400;color:var(--text3);margin-left:2px}
.acct-table{width:100%;border-collapse:collapse;font-size:12.5px}
.acct-table th{text-align:left;padding:8px 12px;font-size:11px;font-weight:600;color:var(--text3);border-bottom:1px solid var(--border2);white-space:nowrap;cursor:pointer;user-select:none}
.acct-table th:hover{color:var(--text2)}
.acct-table td{padding:9px 12px;border-bottom:1px solid var(--border);vertical-align:middle}
.acct-table tr:last-child td{border-bottom:none}
.acct-table tbody tr{cursor:pointer;transition:background .1s}
.acct-table tbody tr:hover td{background:var(--surface2)}
.acct-health-badge{display:inline-block;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:700;letter-spacing:.2px}
.acct-status-badge{display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:6px;font-size:11px;font-weight:600;white-space:nowrap}
.acct-status-bar{width:4px;height:14px;border-radius:2px;flex-shrink:0}
.acct-product-tag{display:inline-block;padding:2px 7px;border-radius:6px;font-size:10px;font-weight:600;background:var(--abg);color:var(--accent);border:1px solid var(--accent);margin:1px 2px;white-space:nowrap}
.acct-owner-cell{display:flex;align-items:center;gap:7px}
.acct-av{width:24px;height:24px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:9px;font-weight:700;color:#fff;flex-shrink:0}
.acct-location{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:5px;font-size:11px;font-weight:500;background:var(--surface2);color:var(--text2);white-space:nowrap}
.acct-empty{padding:32px;text-align:center;color:var(--text3);font-size:13px}
"""
assert '</style>' in html
html = html.replace('</style>', acct_css + '</style>', 1)

# ── 4. Add showAccountDashboard + renderAccountDashboard JS ──
DASHBOARD_JS = r"""
// ═══════════════════ ACCOUNT MANAGEMENT DASHBOARD ═══════════════════

function showAccountDashboard(){
  curView='account-mgmt';
  setTopbar('Account Management','Client accounts · delivery tracking & health',[
    `<button class="btn ghost" onclick="showWorkspace('ws5')"><svg viewBox="0 0 24 24" style="width:12px;height:12px;stroke:currentColor;stroke-width:2;fill:none;vertical-align:-1px;margin-right:5px"><polyline points="15 18 9 12 15 6"/></svg>Client Accounts</button>`
  ]);
  showView('account-mgmt');
  renderAccountDashboard('','','');
  renderNavWorkspaces();closeDetail();closeColPanel();closeNavIfMobile();
}

function renderAccountDashboard(searchQ, healthFilter, statusFilter){
  const el=document.getElementById('view-account-mgmt');
  const acctProjects=PROJECTS.filter(p=>p.custom&&p.custom.cf_client!==undefined);

  const HEALTH_COLORS={
    'Healthy': {bg:'#dcfce7',color:'#15803d'},
    'At Risk':  {bg:'#fef9c3',color:'#a16207'},
    'Critical': {bg:'#fee2e2',color:'#dc2626'},
    'Unknown':  {bg:'var(--surface2)',color:'var(--text3)'},
  };
  const STATUS_COLORS={
    'In Progress - On Track': {bar:'#22c55e', bg:'#dcfce722', color:'#15803d'},
    'In Progress - At Risk':  {bar:'#f59e4a', bg:'#fef9c322', color:'#a16207'},
    'In Progress - Behind':   {bar:'#ef4444', bg:'#fee2e222', color:'#dc2626'},
    'On Hold':                {bar:'#f59e4a', bg:'#fef9c322', color:'#a16207'},
    'Not Started':            {bar:'#94a3b8', bg:'var(--surface2)', color:'var(--text3)'},
    'Complete':               {bar:'#1AA6B7', bg:'var(--abg)', color:'var(--accent)'},
  };

  function getLocation(p){
    const homeLoc=p.locations?.find(l=>l.isHome)||p.locations?.[0];
    if(!homeLoc)return'—';
    if(homeLoc.folderId){
      const fl=FOLDERS.find(f=>f.id===homeLoc.folderId);
      return fl?fl.name:'—';
    }
    const ws=WORKSPACES.find(w=>w.id===homeLoc.workspaceId);
    return ws?ws.name:'—';
  }

  // Filter
  let rows=acctProjects.filter(p=>{
    if(searchQ){
      const q=searchQ.toLowerCase();
      const match=p.name.toLowerCase().includes(q)||(p.custom.cf_client||'').toLowerCase().includes(q);
      if(!match)return false;
    }
    if(healthFilter&&p.custom.cf_acct_health!==healthFilter)return false;
    if(statusFilter&&p.custom.cf_delivery_status!==statusFilter)return false;
    return true;
  });

  // KPI strip
  const totalAccts=acctProjects.length;
  const healthyCnt=acctProjects.filter(p=>p.custom.cf_acct_health==='Healthy').length;
  const atRiskCnt=acctProjects.filter(p=>p.custom.cf_acct_health==='At Risk').length;
  const criticalCnt=acctProjects.filter(p=>p.custom.cf_acct_health==='Critical').length;

  let out=`<div class="acct-page">
    <div class="ws-bc" style="margin-bottom:14px"><span class="ws-bc-link" onclick="showHome()">Home</span> <span>›</span> <span class="ws-bc-link" onclick="showWorkspace('ws5')">Client Accounts</span> <span>›</span> <span>Account Management</span></div>
    <div class="fin-stat-row">
      <div class="fin-stat"><div class="fin-stat-val">${totalAccts}</div><div class="fin-stat-lbl">Total Accounts</div></div>
      <div class="fin-stat"><div class="fin-stat-val" style="color:#15803d">${healthyCnt}</div><div class="fin-stat-lbl">Healthy</div></div>
      <div class="fin-stat"><div class="fin-stat-val" style="color:#a16207">${atRiskCnt}</div><div class="fin-stat-lbl">At Risk</div></div>
      <div class="fin-stat"><div class="fin-stat-val" style="color:#dc2626">${criticalCnt}</div><div class="fin-stat-lbl">Critical</div></div>
    </div>
    <div class="acct-toolbar">
      <div class="acct-search">
        <svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:var(--text3);stroke-width:2;fill:none;flex-shrink:0"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <input id="acct-search-inp" placeholder="Search accounts or clients…" value="${searchQ}" oninput="renderAccountDashboard(this.value,document.getElementById('acct-health-sel').value,document.getElementById('acct-status-sel').value)">
      </div>
      <select id="acct-health-sel" class="acct-filter-btn" onchange="renderAccountDashboard(document.getElementById('acct-search-inp').value,this.value,document.getElementById('acct-status-sel').value)" style="appearance:none;padding-right:24px;background-image:url('data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22><path d=%22M6 9l6 6 6-6%22 stroke=%22%2394a3b8%22 stroke-width=%222%22 fill=%22none%22/></svg>');background-repeat:no-repeat;background-position:right 6px center;background-size:14px">
        <option value="">All health</option>
        <option value="Healthy" ${healthFilter==='Healthy'?'selected':''}>Healthy</option>
        <option value="At Risk" ${healthFilter==='At Risk'?'selected':''}>At Risk</option>
        <option value="Critical" ${healthFilter==='Critical'?'selected':''}>Critical</option>
      </select>
      <select id="acct-status-sel" class="acct-filter-btn" onchange="renderAccountDashboard(document.getElementById('acct-search-inp').value,document.getElementById('acct-health-sel').value,this.value)" style="appearance:none;padding-right:24px;background-image:url('data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 24 24%22><path d=%22M6 9l6 6 6-6%22 stroke=%22%2394a3b8%22 stroke-width=%222%22 fill=%22none%22/></svg>');background-repeat:no-repeat;background-position:right 6px center;background-size:14px">
        <option value="">All statuses</option>
        <option value="Not Started" ${statusFilter==='Not Started'?'selected':''}>Not Started</option>
        <option value="In Progress - On Track" ${statusFilter==='In Progress - On Track'?'selected':''}>In Progress - On Track</option>
        <option value="In Progress - At Risk" ${statusFilter==='In Progress - At Risk'?'selected':''}>In Progress - At Risk</option>
        <option value="On Hold" ${statusFilter==='On Hold'?'selected':''}>On Hold</option>
        <option value="Complete" ${statusFilter==='Complete'?'selected':''}>Complete</option>
      </select>
    </div>
    <div class="acct-table-wrap">
      <div class="acct-overview-title">
        <svg viewBox="0 0 24 24" style="width:14px;height:14px;stroke:currentColor;stroke-width:1.75;fill:none"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>
        Account Management Overview
        <span class="acct-overview-count">(${rows.length}${rows.length!==totalAccts?' of '+totalAccts:''})</span>
      </div>
      <div style="overflow-x:auto">
      <table class="acct-table">
        <thead><tr>
          <th>Name</th>
          <th>Location</th>
          <th>Client</th>
          <th>Account Owner</th>
          <th>Account Health</th>
          <th>Status</th>
          <th>Upsell / Cross Sell Opportunities</th>
          <th>Products</th>
        </tr></thead>
        <tbody>
        ${rows.length?rows.map(p=>{
          const c=p.custom||{};
          const health=c.cf_acct_health||'Unknown';
          const hc=HEALTH_COLORS[health]||HEALTH_COLORS['Unknown'];
          const status=c.cf_delivery_status||'Not Started';
          const sc=STATUS_COLORS[status]||STATUS_COLORS['Not Started'];
          const owner=USERS.find(u=>u.id===c.cf_acct_owner);
          const products=Array.isArray(c.cf_products)?c.cf_products:(c.cf_products?[c.cf_products]:[]);
          const loc=getLocation(p);
          return `<tr onclick="openProject('${p.id}')">
            <td>
              <div style="display:flex;align-items:center;gap:6px">
                <svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:var(--text3);stroke-width:1.75;fill:none;flex-shrink:0"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                <span style="font-weight:600;color:var(--text)">${p.name}</span>
              </div>
            </td>
            <td><span class="acct-location">${loc}</span></td>
            <td style="color:var(--text2)">${c.cf_client||'—'}</td>
            <td>
              ${owner?`<div class="acct-owner-cell">
                <div class="acct-av" style="background:${owner.color}">${ini(owner.name)}</div>
                <span style="color:var(--text2);white-space:nowrap">${owner.name}</span>
              </div>`:'<span style="color:var(--text3)">—</span>'}
            </td>
            <td><span class="acct-health-badge" style="background:${hc.bg};color:${hc.color}">${health}</span></td>
            <td>
              <span class="acct-status-badge" style="background:${sc.bg};color:${sc.color}">
                <span class="acct-status-bar" style="background:${sc.bar}"></span>
                ${status}
              </span>
            </td>
            <td style="color:var(--text3);font-size:12px;max-width:220px">${c.cf_upsell||''}</td>
            <td style="min-width:160px">${products.map(pr=>`<span class="acct-product-tag">${pr}</span>`).join('')}</td>
          </tr>`;
        }).join(''):`<tr><td colspan="8" class="acct-empty">No accounts match the current filters.</td></tr>`}
        </tbody>
      </table>
      </div>
    </div>
  </div>`;

  el.innerHTML=out;
}
"""

anchor = '// showHome() is called by loginAs() after authentication'
assert anchor in html
html = html.replace(anchor, DASHBOARD_JS + anchor, 1)

with open('/home/user/YCxDesign/team-nexus-v3.html', 'w') as f:
    f.write(html)
print('Chunk 2 done')
