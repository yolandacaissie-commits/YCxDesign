#!/usr/bin/env python3
with open('/home/user/YCxDesign/team-nexus-v3.html','r') as f:
    html = f.read()

# 1. Update showView() to include 'financial'
old_sv = "['welcome','home','projects','workspace','kanban','table','gantt','settings','forms','timesheet','stub'].forEach(n=>{"
new_sv = "['welcome','home','projects','workspace','kanban','table','gantt','settings','forms','timesheet','stub','financial'].forEach(n=>{"
assert old_sv in html, "showView anchor not found"
html = html.replace(old_sv, new_sv, 1)

# 2. Add Financial Dashboard button to Operations workspace toolbar
old_toolbar_end = "</span>Workspace Settings</div>\n    </div>\n    ${folders.length?"
new_toolbar_end = """</span>Workspace Settings</div>
      ${wsId==='ws4'?`<div class="ws-tool-btn" onclick="showFinancialDashboard()" style="color:var(--accent);font-weight:600"><span class="nav-icon" style="width:16px;height:16px"><svg viewBox="0 0 24 24" style="width:14px;height:14px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><rect x="2" y="3" width="6" height="8" rx="1"/><rect x="10" y="3" width="6" height="5" rx="1"/><rect x="18" y="3" width="4" height="11" rx="1"/><line x1="2" y1="17" x2="22" y2="17"/></svg></span>Financial Dashboard</div>`:''}
    </div>
    ${folders.length?"""
assert old_toolbar_end in html, "toolbar end anchor not found"
html = html.replace(old_toolbar_end, new_toolbar_end, 1)

# 3. Update AI routing for financial
old_ai = "action:()=>{const ws=WORKSPACES.find(w=>w.name==='Operations');if(ws)showWorkspace(ws.id);else showHome();}}"
new_ai = "action:()=>showFinancialDashboard()}"
assert old_ai in html, "AI routing anchor not found"
html = html.replace(old_ai, new_ai, 1)

with open('/home/user/YCxDesign/team-nexus-v3.html','w') as f:
    f.write(html)

print("JS1 done — showView + toolbar + AI routing updated")
