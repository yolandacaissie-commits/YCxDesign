#!/usr/bin/env python3
with open('/home/user/YCxDesign/team-nexus-v3.html','r') as f:
    html = f.read()

fin_functions = r"""
// ═══════════════════════ FINANCIAL DASHBOARD ═══════════════════════

function showFinancialDashboard(){
  curView='financial';
  setTopbar('Financial Dashboard','Operations · Project financials & team utilisation',[
    `<button class="btn ghost" onclick="showWorkspace('ws4')"><svg viewBox="0 0 24 24" style="width:12px;height:12px;stroke:currentColor;stroke-width:2;fill:none;vertical-align:-1px;margin-right:5px"><polyline points="15 18 9 12 15 6"/></svg>Workspace</button>`
  ]);
  showView('financial');
  renderFinancialDashboard();
  renderNavWorkspaces();
  closeDetail();closeColPanel();closeNavIfMobile();
}

function makeLineChart(datasets,labels,w,h){
  const padL=44,padR=10,padT=12,padB=24;
  const W=w-padL-padR,H=h-padT-padB;
  const n=labels.length;
  if(n<2)return '';
  const allVals=datasets.flatMap(d=>d.values);
  const maxV=Math.max(...allVals,1);
  const xOf=i=>(padL+i*(W/(n-1))).toFixed(1);
  const yOf=v=>(padT+H*(1-v/maxV)).toFixed(1);
  let svg=`<svg viewBox="0 0 ${w} ${h}" style="width:100%;overflow:visible">`;
  [0,.25,.5,.75,1].forEach(f=>{
    const y=(padT+H*f).toFixed(1);
    const val=Math.round(maxV*(1-f));
    svg+=`<line x1="${padL}" y1="${y}" x2="${padL+W}" y2="${y}" stroke="var(--border2)" stroke-width="1"/>`;
    svg+=`<text x="${padL-4}" y="${(+y+4).toFixed(0)}" text-anchor="end" font-size="9" fill="var(--text3)">$${val>=1000?Math.round(val/1000)+'k':val}</text>`;
  });
  labels.forEach((l,i)=>{
    svg+=`<text x="${xOf(i)}" y="${h-2}" text-anchor="middle" font-size="9" fill="var(--text3)">${l}</text>`;
  });
  datasets.forEach(ds=>{
    const pts=ds.values.map((v,i)=>`${xOf(i)},${yOf(v)}`).join(' ');
    svg+=`<polyline points="${pts}" fill="none" stroke="${ds.color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>`;
    ds.values.forEach((v,i)=>{
      svg+=`<circle cx="${xOf(i)}" cy="${yOf(v)}" r="3" fill="${ds.color}" stroke="var(--surface)" stroke-width="1.5"/>`;
    });
  });
  svg+='</svg>';
  return svg;
}

function renderFinancialDashboard(){
  const el=document.getElementById('view-financial');
  const finP=PROJECTS.filter(p=>p.contractValue!==undefined);
  const MONTHS=['2026-01','2026-02','2026-03'];
  const MLABELS=['Jan','Feb','Mar'];
  const LOB_COLORS={'SF Services':'#1AA6B7','Business Intelligence':'#8b5cf6','Data Science':'#22c55e','Data Engineering':'#f59e4a'};
  const STATUS_COLORS={active:'#22c55e',on_hold:'#f59e4a',complete:'#1AA6B7',archived:'#94a3b8'};

  function fmt(n){return n>=1000000?'$'+(n/1000000).toFixed(1)+'M':n>=1000?'$'+(n/1000).toFixed(1)+'k':'$'+n;}
  function pct(n){return Math.round(n*100)+'%';}

  // Compute per-project stats
  const stats=finP.map(p=>{
    const actualCost=(p.monthlyCosts||[]).reduce((s,m)=>s+m.actual,0);
    const estCost=(p.monthlyCosts||[]).reduce((s,m)=>s+m.estimated,0);
    const hoursAvail=p.contractValue&&p.hourlyRate?Math.round(p.contractValue/p.hourlyRate):0;
    const hoursSpent=p.hourlyRate?Math.round(actualCost/p.hourlyRate):0;
    const util=p.contractValue>0?actualCost/p.contractValue:null;
    const done=p.tasks.filter(t=>t.status==='done').length;
    const progress=p.tasks.length?done/p.tasks.length:0;
    const thisMonth=p.monthlyCosts?.[p.monthlyCosts.length-1];
    return {p,actualCost,estCost,hoursAvail,hoursSpent,util,progress,done,thisMonth};
  });

  // ── KPI stats row ──
  const totalContract=finP.reduce((s,p)=>s+(p.contractValue||0),0);
  const totalActual=stats.reduce((s,r)=>s+r.actualCost,0);
  const totalHours=stats.reduce((s,r)=>s+r.hoursSpent,0);
  const avgUtil=stats.filter(r=>r.util!==null).reduce((s,r)=>s+r.util,0)/Math.max(1,stats.filter(r=>r.util!==null).length);

  let html=`<div class="fin-page">
  <div class="ws-bc" style="margin-bottom:16px"><span class="ws-bc-link" onclick="showHome()">Home</span> <span>›</span> <span class="ws-bc-link" onclick="showWorkspace('ws4')">Operations</span> <span>›</span> <span>Financial Dashboard</span></div>

  <div class="fin-stat-row">
    <div class="fin-stat"><div class="fin-stat-val">${fmt(totalContract)}</div><div class="fin-stat-lbl">Total Contract Value</div></div>
    <div class="fin-stat"><div class="fin-stat-val">${fmt(totalActual)}</div><div class="fin-stat-lbl">Actual Cost to Date</div></div>
    <div class="fin-stat"><div class="fin-stat-val">${totalHours.toLocaleString()}</div><div class="fin-stat-lbl">Total Hours Billed</div></div>
    <div class="fin-stat"><div class="fin-stat-val" style="color:${avgUtil>0.9?'#ef4444':avgUtil>0.75?'#f59e4a':'#22c55e'}">${pct(avgUtil)}</div><div class="fin-stat-lbl">Avg Contract Utilisation</div></div>
  </div>

  <!-- Section 1: Project Financials Overview -->
  <div class="fin-section">
    <div class="fin-section-title"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none"><rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M9 21V9"/></svg>Active Project Financials</div>
    <div style="overflow-x:auto;border:1px solid var(--border2);border-radius:12px">
    <table class="fin-table">
      <thead><tr>
        <th>Project</th><th>LOB</th><th>Contract Value</th><th>Actual Cost</th>
        <th>Hrs Available</th><th>Hrs Spent</th>
        <th style="min-width:120px">Contract Utilisation</th>
        <th>Progress</th><th>Status</th><th>Due</th>
      </tr></thead>
      <tbody>
      ${stats.map(({p,actualCost,hoursAvail,hoursSpent,util,progress,done})=>{
        const utilPct=util!==null?Math.round(util*100):null;
        const utilColor=util===null?'#94a3b8':util>0.95?'#ef4444':util>0.8?'#f59e4a':'#22c55e';
        const progPct=Math.round(progress*100);
        return `<tr onclick="openProject('${p.id}')" style="cursor:pointer">
          <td><span style="font-weight:600">${p.name}</span></td>
          <td>${(p.lob||[]).map(l=>`<span class="fin-lob-tag" style="background:${LOB_COLORS[l]||'#94a3b8'}22;color:${LOB_COLORS[l]||'#94a3b8'};border:1px solid ${LOB_COLORS[l]||'#94a3b8'}44">${l}</span>`).join('')}</td>
          <td>${p.contractValue>0?fmt(p.contractValue):'—'}</td>
          <td style="font-weight:600">${fmt(actualCost)}</td>
          <td>${hoursAvail>0?hoursAvail.toLocaleString()+' hrs':'—'}</td>
          <td>${hoursSpent.toLocaleString()} hrs</td>
          <td>
            ${utilPct!==null?`<div style="font-size:11px;font-weight:700;color:${utilColor};margin-bottom:3px">${utilPct}%</div>
            <div class="fin-util-bar"><div class="fin-util-fill" style="width:${Math.min(utilPct,100)}%;background:${utilColor}"></div></div>`:'<span style="color:var(--text3);font-size:11px">Internal</span>'}
          </td>
          <td>
            <div style="font-size:11px;font-weight:700;color:var(--accent);margin-bottom:3px">${progPct}%</div>
            <div class="fin-util-bar"><div class="fin-util-fill" style="width:${progPct}%;background:var(--accent)"></div></div>
          </td>
          <td><span class="fin-badge" style="background:${STATUS_COLORS[p.status]||'#94a3b8'}22;color:${STATUS_COLORS[p.status]||'#94a3b8'}">${p.status}</span></td>
          <td style="color:var(--text3);font-size:11px;white-space:nowrap">${p.dueDate||'—'}</td>
        </tr>`;
      }).join('')}
      </tbody>
    </table>
    </div>
  </div>`;

  // ── Section 2: This Month's Time Spent ──
  const thisMonthLabel=MLABELS[MLABELS.length-1]+' '+MONTHS[MONTHS.length-1].slice(0,4);
  html+=`
  <div class="fin-section">
    <div class="fin-section-title"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>This Month's Time Spent (${thisMonthLabel})</div>
    <div style="overflow-x:auto;border:1px solid var(--border2);border-radius:12px">
    <table class="fin-table">
      <thead><tr><th>Project</th><th>LOB</th><th>Actual Cost</th><th>Estimated</th><th>Variance</th><th>Hours</th></tr></thead>
      <tbody>
      ${stats.map(({p,thisMonth})=>{
        if(!thisMonth)return '';
        const hrs=p.hourlyRate?Math.round(thisMonth.actual/p.hourlyRate):0;
        const variance=thisMonth.actual-thisMonth.estimated;
        const varColor=variance>0?'#ef4444':'#22c55e';
        return `<tr onclick="openProject('${p.id}')" style="cursor:pointer">
          <td style="font-weight:600">${p.name}</td>
          <td>${(p.lob||[]).map(l=>`<span class="fin-lob-tag" style="background:${LOB_COLORS[l]||'#94a3b8'}22;color:${LOB_COLORS[l]||'#94a3b8'}">${l}</span>`).join('')}</td>
          <td style="font-weight:600">${fmt(thisMonth.actual)}</td>
          <td style="color:var(--text3)">${fmt(thisMonth.estimated)}</td>
          <td style="color:${varColor};font-weight:600">${variance>=0?'+':''}${fmt(Math.abs(variance))}</td>
          <td>${hrs} hrs</td>
        </tr>`;
      }).join('')}
      </tbody>
    </table>
    </div>
  </div>`;

  // ── Section 3: Charts grid — MoM line chart + Team Utilisation ──
  // Aggregate monthly totals across all projects
  const monthActual=MONTHS.map(m=>finP.reduce((s,p)=>{const mc=(p.monthlyCosts||[]).find(x=>x.month===m);return s+(mc?mc.actual:0);},0));
  const monthEst=MONTHS.map(m=>finP.reduce((s,p)=>{const mc=(p.monthlyCosts||[]).find(x=>x.month===m);return s+(mc?mc.estimated:0);},0));

  // Team utilisation from TIMESHEET_ENTRIES for latest month
  const latestMonth=MONTHS[MONTHS.length-1];
  const teamRows=USERS.slice(0,6).map(u=>{
    const entries=TIMESHEET_ENTRIES.filter(e=>e.userId===u.id&&e.date.startsWith(latestMonth));
    const hrs=entries.reduce((s,e)=>s+e.hours,0);
    const projs=[...new Set(entries.map(e=>{const p=PROJECTS.find(pr=>pr.tasks.some(t=>t.id===e.taskId));return p?p.name:null;}).filter(Boolean))];
    const stdHrs=8*20; // 20 working days
    const util=hrs/stdHrs;
    return {u,hrs,projs,util};
  }).filter(r=>r.hrs>0);

  const momChart=makeLineChart(
    [{values:monthActual,color:'#1AA6B7',label:'Actual'},{values:monthEst,color:'#94a3b8',label:'Estimated'}],
    MLABELS,460,180
  );

  html+=`
  <div class="fin-grid">
    <div class="fin-chart-box">
      <div class="fin-chart-title">Actual vs Estimated Cost — Month over Month</div>
      <div class="fin-legend">
        <div class="fin-legend-item"><div class="fin-legend-dot" style="background:#1AA6B7"></div>Actual</div>
        <div class="fin-legend-item"><div class="fin-legend-dot" style="background:#94a3b8"></div>Estimated</div>
      </div>
      ${momChart}
    </div>
    <div class="fin-chart-box">
      <div class="fin-chart-title">Team Utilisation — ${thisMonthLabel}</div>
      <table class="fin-table">
        <thead><tr><th>Member</th><th>Hours</th><th>Projects</th><th>Utilisation</th></tr></thead>
        <tbody>
        ${teamRows.map(({u,hrs,projs,util})=>`
          <tr>
            <td><div style="display:flex;align-items:center;gap:7px">
              <div style="width:24px;height:24px;border-radius:50%;background:${u.color};display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff;flex-shrink:0">${u.name.split(' ').map(n=>n[0]).join('').slice(0,2)}</div>
              <span style="font-size:12px">${u.name.split(' ')[0]}</span>
            </div></td>
            <td style="font-weight:600">${hrs}</td>
            <td style="font-size:11px;color:var(--text3)">${projs.join(', ')||'—'}</td>
            <td>
              <div style="font-size:11px;font-weight:700;color:${util>0.9?'#ef4444':util>0.6?'#f59e4a':'#22c55e'}">${Math.round(util*100)}%</div>
              <div class="fin-util-bar" style="min-width:60px"><div class="fin-util-fill" style="width:${Math.min(Math.round(util*100),100)}%;background:${util>0.9?'#ef4444':util>0.6?'#f59e4a':'#22c55e'}"></div></div>
            </td>
          </tr>`).join('')}
        ${teamRows.length===0?'<tr><td colspan="4" style="color:var(--text3);text-align:center;padding:16px">No timesheet entries for this period</td></tr>':''}
        </tbody>
      </table>
    </div>
  </div>`;

  // ── Section 4: Year Team Utilisation by month ──
  const allMonths=['01','02','03','04','05','06','07','08','09','10','11','12'];
  const allLabels=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const yearUsers=USERS.filter(u=>{
    return TIMESHEET_ENTRIES.some(e=>e.userId===u.id&&e.date.startsWith('2026'));
  });

  html+=`
  <div class="fin-section">
    <div class="fin-section-title"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/></svg>Team Utilisation — This Year (2026)</div>
    <div style="overflow-x:auto;border:1px solid var(--border2);border-radius:12px">
    <table class="fin-table">
      <thead><tr><th>Team Member</th>${allLabels.map(l=>`<th style="text-align:center">${l}</th>`).join('')}<th>Total Hrs</th></tr></thead>
      <tbody>
      ${yearUsers.map(u=>{
        const monthHrs=allMonths.map(m=>{
          return TIMESHEET_ENTRIES.filter(e=>e.userId===u.id&&e.date.startsWith('2026-'+m)).reduce((s,e)=>s+e.hours,0);
        });
        const total=monthHrs.reduce((a,b)=>a+b,0);
        return `<tr>
          <td><div style="display:flex;align-items:center;gap:7px">
            <div style="width:24px;height:24px;border-radius:50%;background:${u.color};display:flex;align-items:center;justify-content:center;font-size:10px;font-weight:700;color:#fff;flex-shrink:0">${u.name.split(' ').map(n=>n[0]).join('').slice(0,2)}</div>
            <span>${u.name}</span>
          </div></td>
          ${monthHrs.map(h=>`<td style="text-align:center;font-size:12px;color:${h>0?'var(--text)':'var(--text3)'};font-weight:${h>0?600:400}">${h>0?h:'—'}</td>`).join('')}
          <td style="font-weight:700;color:var(--accent)">${total}</td>
        </tr>`;
      }).join('')}
      </tbody>
    </table>
    </div>
  </div>`;

  // ── Section 5: Per-LOB cost charts ──
  const LOBS=['SF Services','Business Intelligence','Data Science','Data Engineering'];
  const LOB_C=['#1AA6B7','#8b5cf6','#22c55e','#f59e4a'];

  const lobCharts=LOBS.map((lob,li)=>{
    const lobProjects=finP.filter(p=>(p.lob||[]).includes(lob));
    const monthTotals=MONTHS.map(m=>lobProjects.reduce((s,p)=>{
      const mc=(p.monthlyCosts||[]).find(x=>x.month===m);
      return s+(mc?mc.actual:0);
    },0));
    const chart=makeLineChart([{values:monthTotals,color:LOB_C[li],label:lob}],MLABELS,280,140);
    const total=monthTotals.reduce((a,b)=>a+b,0);
    const projNames=lobProjects.map(p=>p.name).join(', ')||'No projects';
    return `<div class="fin-chart-box">
      <div class="fin-chart-title">${lob}</div>
      <div style="font-size:20px;font-weight:700;color:${LOB_C[li]};margin-bottom:2px">${fmt(total)}</div>
      <div style="font-size:11px;color:var(--text3);margin-bottom:10px">${lobProjects.length} project${lobProjects.length!==1?'s':''} · ${projNames}</div>
      ${chart}
    </div>`;
  });

  html+=`
  <div class="fin-section">
    <div class="fin-section-title"><svg viewBox="0 0 24 24" style="width:13px;height:13px;stroke:currentColor;stroke-width:1.75;fill:none"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>Cost by Line of Business — YTD</div>
    <div class="fin-lob-grid">${lobCharts.join('')}</div>
  </div>

  </div>`; // close fin-page

  el.innerHTML=html;
}
"""

# Insert before </script>
old_script_end = "// showHome() is called by loginAs() after authentication\n// Initial demo accounts are rendered by renderLoginDemos() above\n</script>"
new_script_end = fin_functions + "// showHome() is called by loginAs() after authentication\n// Initial demo accounts are rendered by renderLoginDemos() above\n</script>"
assert old_script_end in html, "script end anchor not found"
html = html.replace(old_script_end, new_script_end, 1)

with open('/home/user/YCxDesign/team-nexus-v3.html','w') as f:
    f.write(html)

print("JS2 done — financial dashboard functions added")
