#!/usr/bin/env python3
"""Chunk 3: Wire Account Management button in Operations workspace + AI routing."""
with open('/home/user/YCxDesign/team-nexus-v3.html', 'r') as f:
    html = f.read()

# ── 1. Add Account Management button to Operations (ws4) toolbar ──
# The Operations workspace already has a Financial Dashboard button.
# Find that conditional and add another button for Account Management
# when wsId === 'ws5' (Client Accounts workspace).
old_fin_btn = """${wsId==='ws4'?`<div class="ws-tool-btn" onclick="showFinancialDashboard()" style="color:var(--accent);font-weight:600"><span class="nav-icon" style="width:16px;height:16px"><svg viewBox="0 0 24 24" style="width:14px;height:14px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><rect x="2" y="3" width="6" height="8" rx="1"/><rect x="10" y="3" width="6" height="5" rx="1"/><rect x="18" y="3" width="4" height="11" rx="1"/><line x1="2" y1="17" x2="22" y2="17"/></svg></span>Financial Dashboard</div>`:''}"""
new_fin_btn = """${wsId==='ws4'?`<div class="ws-tool-btn" onclick="showFinancialDashboard()" style="color:var(--accent);font-weight:600"><span class="nav-icon" style="width:16px;height:16px"><svg viewBox="0 0 24 24" style="width:14px;height:14px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><rect x="2" y="3" width="6" height="8" rx="1"/><rect x="10" y="3" width="6" height="5" rx="1"/><rect x="18" y="3" width="4" height="11" rx="1"/><line x1="2" y1="17" x2="22" y2="17"/></svg></span>Financial Dashboard</div>`:''}
      ${wsId==='ws5'?`<div class="ws-tool-btn" onclick="showAccountDashboard()" style="color:var(--accent);font-weight:600"><span class="nav-icon" style="width:16px;height:16px"><svg viewBox="0 0 24 24" style="width:14px;height:14px;stroke:currentColor;stroke-width:1.75;fill:none;stroke-linecap:round;stroke-linejoin:round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg></span>Account Management</div>`:''}"""
assert old_fin_btn in html, 'financial dashboard button anchor not found'
html = html.replace(old_fin_btn, new_fin_btn, 1)

# ── 2. Add AI routing for account management ──
old_ai_fin = "{match:/financial|finance|dashboard|operations|ops|revenue|cost/i, reply:\"Taking you to the Financial Dashboard in Operations.\", action:()=>showFinancialDashboard()}"
new_ai_fin = "{match:/financial|finance|dashboard|operations|ops|revenue|cost/i, reply:\"Taking you to the Financial Dashboard in Operations.\", action:()=>showFinancialDashboard()},\n    {match:/account.?management|client.?account|account.?dashboard|accounts|health/i, reply:\"Opening the Account Management Dashboard.\", action:()=>showAccountDashboard()}"
assert old_ai_fin in html, 'AI fin routing anchor not found'
html = html.replace(old_ai_fin, new_ai_fin, 1)

# ── 3. Add Account Management to welcome screen quick actions ──
old_welcome_action = "  else if(action==='financial'){\n    const ws=WORKSPACES.find(w=>w.name==='Operations');\n    if(ws)showWorkspace(ws.id); else showHome();\n  }\n  else{showHome();}"
new_welcome_action = "  else if(action==='financial'){\n    const ws=WORKSPACES.find(w=>w.name==='Operations');\n    if(ws)showWorkspace(ws.id); else showHome();\n  }\n  else if(action==='accounts'){showAccountDashboard();}\n  else{showHome();}"
assert old_welcome_action in html, f'welcome action anchor not found'
html = html.replace(old_welcome_action, new_welcome_action, 1)

# ── 4. Add Account Management card to welcome screen HTML ──
old_welcome_cards = """onclick="welcomeAction('financial')">"""
new_welcome_cards = """onclick="welcomeAction('financial')">"""
# Find the welcome action card for financial and add accounts card after it
# Look for the financial card's closing div and insert after
old_welcome_fin_card = """<div class="welcome-action" onclick="welcomeAction('financial')">
              <div style="font-size:22px;margin-bottom:6px">💰</div>
              <div style="font-size:14px;font-weight:700;color:#CFF7F2">Financial Dashboard</div>
              <div style="font-size:12px;color:rgba(207,247,242,.6);margin-top:3px">Review operations & financials</div>
            </div>"""
new_welcome_fin_card = """<div class="welcome-action" onclick="welcomeAction('financial')">
              <div style="font-size:22px;margin-bottom:6px">💰</div>
              <div style="font-size:14px;font-weight:700;color:#CFF7F2">Financial Dashboard</div>
              <div style="font-size:12px;color:rgba(207,247,242,.6);margin-top:3px">Review operations & financials</div>
            </div>
            <div class="welcome-action" onclick="welcomeAction('accounts')">
              <div style="font-size:22px;margin-bottom:6px">🏢</div>
              <div style="font-size:14px;font-weight:700;color:#CFF7F2">Account Management</div>
              <div style="font-size:12px;color:rgba(207,247,242,.6);margin-top:3px">View client accounts & health</div>
            </div>"""
if old_welcome_fin_card in html:
    html = html.replace(old_welcome_fin_card, new_welcome_fin_card, 1)
    print('Welcome card added')
else:
    print('Welcome card anchor not found — skipping (non-critical)')

with open('/home/user/YCxDesign/team-nexus-v3.html', 'w') as f:
    f.write(html)
print('Chunk 3 done')
