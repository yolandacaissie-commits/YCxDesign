#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate Delta_User_Stories.xlsx — user stories grouped by module."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb = Workbook()

# ── Styling helpers ──────────────────────────────────────────────────────────
HEADER_FILL = PatternFill(start_color="1AA6B7", end_color="1AA6B7", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFF", size=11, name="Calibri")
TITLE_FONT  = Font(bold=True, color="0B1320", size=14, name="Calibri")
SECTION_FILL= PatternFill(start_color="CFF7F2", end_color="CFF7F2", fill_type="solid")
SECTION_FONT= Font(bold=True, color="0B7285", size=11, name="Calibri")
BORDER = Border(
    left=Side(style='thin', color='D7DCE4'),
    right=Side(style='thin', color='D7DCE4'),
    top=Side(style='thin', color='D7DCE4'),
    bottom=Side(style='thin', color='D7DCE4'),
)
WRAP_ALIGN = Alignment(wrap_text=True, vertical='top', horizontal='left')
CENTER_ALIGN = Alignment(wrap_text=True, vertical='center', horizontal='center')

STATUS_FILLS = {
    'Implemented': PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid"),
    'Partial':     PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid"),
    'Coming Soon': PatternFill(start_color="E0E7FF", end_color="E0E7FF", fill_type="solid"),
    'Not Started': PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid"),
}
PRIORITY_FILLS = {
    'High':   PatternFill(start_color="FECACA", end_color="FECACA", fill_type="solid"),
    'Medium': PatternFill(start_color="FDE68A", end_color="FDE68A", fill_type="solid"),
    'Low':    PatternFill(start_color="E5E7EB", end_color="E5E7EB", fill_type="solid"),
}

# ═══════════════════════════════════════════════════════════════════════════════
# USER STORIES DATA
# Each row: (Module, Story ID, User Story, Acceptance Criteria, Priority, Status, Notes)
# ═══════════════════════════════════════════════════════════════════════════════

STORIES = [

# ────────────────────────── WORKSPACES ──────────────────────────
("Workspaces", "WS-01",
 "As a user, I want to organize projects into workspaces so that I can separate work by team, client, or department.",
 "• Multiple workspaces visible in left sidebar\n• Each workspace shows its own projects and folders\n• Workspaces can be expanded/collapsed\n• Color/icon indicators per workspace",
 "High", "Implemented",
 "PMO, My Work, Account Management, Operations, and Client workspaces seeded."),

("Workspaces", "WS-02",
 "As a user, I want a Workspace Settings page so that I can manage members, permissions, and metadata for that workspace.",
 "• Workspace settings panel accessible from sidebar\n• Member list with roles\n• Workspace description/name editable",
 "Medium", "Partial",
 "Settings exist at account level; per-workspace settings could be expanded."),

("Workspaces", "WS-03",
 "As a user, I want each workspace to have its own Tools section so that I can attach dashboards, calendars, and reports to it.",
 "• Tools section in sidebar under each workspace\n• '+' dropdown to add Whiteboard/Dashboard/Calendar/Report/Workload\n• Tools listed under the section with icons",
 "High", "Implemented",
 "WORKSPACE_TOOLS data structure backs this."),

# ────────────────────────── PROJECTS & FOLDERS ──────────────────────────
("Projects & Folders", "PF-01",
 "As a user, I want to create projects within a workspace so that I can track distinct bodies of work.",
 "• Create project from workspace nav\n• Project shows in sidebar under workspace\n• Each project has its own Board/Table/Gantt views",
 "High", "Implemented",
 "Project creation modal with name, dates, owner."),

("Projects & Folders", "PF-02",
 "As a user, I want to organize projects in folders so that I can group related projects.",
 "• Folders can contain multiple projects\n• Folders expandable/collapsible\n• Folders shown in workspace sidebar",
 "Medium", "Implemented",
 "Folder hierarchy in sidebar."),

("Projects & Folders", "PF-03",
 "As a user, I want each project to support multiple locations (workspaces) so that one project can show under more than one workspace.",
 "• Projects have a locations array\n• A project shows under each location's nav\n• Editing one shared project updates everywhere",
 "Medium", "Implemented",
 "PROJECTS[i].locations array."),

("Projects & Folders", "PF-04",
 "As a user, I want to assign a Line of Business (LOB) to a project so that I can group and report by LOB.",
 "• Project edit form has LOB multi-select\n• Dashboards aggregate by LOB",
 "Medium", "Implemented",
 "p.lob field used in dashboards donut chart."),

# ────────────────────────── TASK MANAGEMENT ──────────────────────────
("Task Management", "TM-01",
 "As a user, I want a Kanban Board view so that I can visualize tasks by status.",
 "• Columns for Todo, In Progress, Review, Done, Blocked\n• Drag-and-drop between columns\n• Task cards show title, assignee, priority, due date",
 "High", "Implemented",
 "Board view with status columns."),

("Task Management", "TM-02",
 "As a user, I want a Table view of tasks so that I can see/edit many tasks in a spreadsheet-style grid.",
 "• Sortable columns\n• Inline editing\n• Custom fields displayed\n• Filterable by status/assignee/priority",
 "High", "Implemented",
 "Table view with column controls."),

("Task Management", "TM-03",
 "As a user, I want a Gantt view so that I can see task timelines and dependencies.",
 "• Horizontal task bars across a time axis\n• Dependency arrows between tasks\n• Today line\n• Drag to reschedule",
 "High", "Implemented",
 "Gantt with dependency lines."),

("Task Management", "TM-04",
 "As a user, I want a task detail panel so that I can edit all task fields in one place.",
 "• Slide-out detail panel\n• Status, priority, assignee, dates, description\n• Custom fields, comments, attachments\n• Predecessors and locations",
 "High", "Implemented",
 "Detail panel toggle via star + close buttons."),

("Task Management", "TM-05",
 "As a user, I want to define custom fields on tasks so that I can capture project-specific data.",
 "• Custom field types: text, number, date, select, checkbox\n• Fields appear in detail panel and table view\n• Persisted to TASKS[i].custom",
 "Medium", "Implemented",
 "CUSTOM_FIELDS array drives this."),

("Task Management", "TM-06",
 "As a user, I want to star tasks so that I can find my priorities quickly.",
 "• Star button in task detail panel\n• Star state syncs to STARRED_ITEMS\n• Starred view shows all starred tasks",
 "Medium", "Implemented",
 "toggleTaskStar / toggleProjectStar functions."),

# ────────────────────────── INBOX ──────────────────────────
("Inbox", "IN-01",
 "As a user, I want a notification inbox so that I can see what's happening that needs my attention.",
 "• Inbox shows task assignments, @mentions, status changes, system automations, AI suggestions\n• Filter tabs (All, Unread, Mentions, Tasks)\n• Cards with avatar, message, timestamp",
 "High", "Implemented",
 "12 seed notification types: task_assigned, mention, status_changed, task_ready, ai_suggestion, comment, project_created, task_created, report_ready."),

("Inbox", "IN-02",
 "As a user, I want to mark notifications as read so that I can clear my inbox.",
 "• Click marks individual as read\n• 'Mark all as read' button\n• Unread badge count in nav",
 "Medium", "Implemented",
 "markInboxRead / markAllInboxRead."),

("Inbox", "IN-03",
 "As a user, I want notifications about system events (task ready, report ready) so I'm informed without watching the app.",
 "• Automation triggers create notifications\n• AI surfaces suggestions in the same feed",
 "Medium", "Implemented",
 "Seeded for demo; production would need server-side events."),

# ────────────────────────── STREAM ──────────────────────────
("Stream", "ST-01",
 "As a user, I want a global activity stream so that I can see everything happening across my workspaces.",
 "• Feed of all recent actions across all workspaces\n• Facebook-wall style with timeline connector\n• User avatars and action descriptions",
 "Medium", "Implemented",
 "renderStream uses ACTIVITY_LOG."),

# ────────────────────────── CREATED BY ME ──────────────────────────
("Created by Me", "CM-01",
 "As a user, I want to see all tasks and projects I created across all workspaces so I can track my contributions.",
 "• Combined view of tasks I created + projects I created\n• Grouped by type or workspace\n• Click to open the original item",
 "Medium", "Implemented",
 "showCreatedByMe filters by creator."),

# ────────────────────────── STARRED ──────────────────────────
("Starred", "SR-01",
 "As a user, I want a Starred view so I can quickly access my pinned tasks, projects, and folders.",
 "• Star toggle on tasks/projects/folders\n• Starred view lists all starred items\n• Grouped by type",
 "Medium", "Implemented",
 "STARRED_ITEMS map; star buttons in detail panel."),

# ────────────────────────── DASHBOARDS ──────────────────────────
("Dashboards", "DB-01",
 "As a user, I want to add a dashboard to a workspace so I can monitor that workspace's KPIs.",
 "• Add via workspace Tools '+' dropdown\n• Dashboard appears in workspace sidebar\n• Click opens dashboard canvas",
 "High", "Implemented",
 "WORKSPACE_TOOLS type='dashboard'."),

("Dashboards", "DB-02",
 "As a user, I want pre-built widgets (AI highlights, KPIs, donuts, task lists) so I don't have to build from scratch.",
 "• AI Highlights panel\n• Project Count, Task Progress, At Risk KPIs\n• Project Status donut, LOB donut\n• At Risk Projects table, My Work task list",
 "High", "Implemented",
 "Widgets render live from PROJECTS/TASKS."),

("Dashboards", "DB-03",
 "As a user, I want to add new widgets to a dashboard via a gallery so I can customize what I see.",
 "• 'Add widget' button opens modal\n• 11 widget templates with badges (Indicator/Donut/List/Table)\n• Click to add (stub — needs persistence)",
 "Medium", "Partial",
 "Modal exists; widget persistence to dashboard layout not yet stored."),

("Dashboards", "DB-04",
 "As a user, I want a global Dashboards view from the top nav so I can see all my dashboards in one place.",
 "• Top-nav Dashboards link\n• Workspace filter tabs\n• Cards show progress, task counts, click to open",
 "High", "Implemented",
 "Recently fixed — was a stub before."),

# ────────────────────────── REPORTS ──────────────────────────
("Reports", "RP-01",
 "As a user, I want a Reports library showing report templates and saved reports.",
 "• 8 out-of-the-box templates (Project Status, Task Progress, etc.)\n• Saved reports list with metadata\n• Click template to create new report",
 "High", "Implemented",
 "renderReportsHome with SAVED_REPORTS."),

("Reports", "RP-02",
 "As a user, I want a Create Report modal so I can build custom reports.",
 "• Pick report type, data source (workspace), layout (table/chart), filters\n• Group by selection\n• Save & open",
 "High", "Implemented",
 "openCreateReportModal — 3-column layout."),

("Reports", "RP-03",
 "As a user, I want a report viewer showing live data so the report stays current.",
 "• Live data table\n• Filters apply\n• Group by selected field\n• Re-runnable",
 "High", "Implemented",
 "renderReportViewer."),

("Reports", "RP-04",
 "As a user, I want reports attached to a workspace so I can see/share reports relevant to that workspace.",
 "• Reports added via workspace Tools menu\n• Workspace-scoped data source by default",
 "Medium", "Implemented",
 "WORKSPACE_TOOLS type='report'."),

# ────────────────────────── CALENDAR / ROADMAP ──────────────────────────
("Calendar", "CL-01",
 "As a user, I want a workspace-level roadmap (year view) so I can see projects across time.",
 "• Year timeline with horizontal project bars\n• Bars grouped by assignee\n• Quarterly labels, today line\n• Layer toggles",
 "High", "Implemented",
 "renderCalendar with year mode."),

("Calendar", "CL-02",
 "As a user, I want to add layers to the calendar so I can show/hide different projection types.",
 "• 'New Layer' modal with layer config\n• Toggle visibility per layer\n• Stored in calLayers state",
 "Medium", "Implemented",
 "openNewLayerModal."),

("Calendar", "CL-03",
 "As a user, I want a traditional month/week calendar view so I can see scheduled items by day.",
 "• Month grid view\n• Week view\n• Switchable from year view",
 "Low", "Not Started",
 "Year mode is the primary use case; month/week deferred."),

# ────────────────────────── WORKLOAD ──────────────────────────
("Workload", "WL-01",
 "As a manager, I want a team workload view so I can see who has too much or too little.",
 "• Per-user rows with task load bar (critical/high/normal)\n• Capacity gauge with % utilization\n• Green/yellow/red status colors",
 "High", "Implemented",
 "renderWorkload — accessible from More menu."),

("Workload", "WL-02",
 "As a manager, I want workload summary KPIs so I can spot issues at a glance.",
 "• Open tasks total\n• Critical priority count\n• Unassigned tasks count\n• Over-capacity headcount",
 "High", "Implemented",
 "KPIs at top of workload view."),

("Workload", "WL-03",
 "As a manager, I want to filter workload by workspace so I can focus on a specific team.",
 "• Workspace dropdown filter\n• Re-renders rows on change",
 "Medium", "Implemented",
 "Filter dropdown in workload view."),

("Workload", "WL-04",
 "As a manager, I want to see unassigned tasks in the workload view so I can route them.",
 "• Unassigned tasks listed below user rows\n• Click to open task and assign",
 "Medium", "Implemented",
 "Unassigned section."),

# ────────────────────────── TIMESHEETS ──────────────────────────
("Timesheets", "TS-01",
 "As a user, I want a weekly timesheet so I can log hours by task and day.",
 "• Week grid with days as columns\n• Tasks/activities as rows\n• Hours entry per cell",
 "High", "Implemented",
 "Timesheet table view."),

("Timesheets", "TS-02",
 "As a user, I want each entry to be independently billable or non-billable so each cell can be classified.",
 "• Per-cell B/NB toggle chip\n• Auto-classified based on activity type (e.g., DF Holiday, Training = NB)\n• Override per entry preserved",
 "High", "Implemented",
 "isEntryBillable + NON_BILL_ACTS set."),

("Timesheets", "TS-03",
 "As a user, I want timesheet submission and approval workflow so my time is reviewed.",
 "• Submit button per week\n• Status (draft/submitted/approved)\n• Approver view (manager)",
 "Medium", "Partial",
 "Status visible; full approval workflow needs server."),

# ────────────────────────── FORMS ──────────────────────────
("Forms", "FM-01",
 "As a user, I want to build a form to collect requests so submissions create tasks automatically.",
 "• Form builder with field types\n• Submissions create new tasks\n• Forms have shareable URLs",
 "Medium", "Implemented",
 "Forms section with builder."),

# ────────────────────────── SETTINGS ──────────────────────────
("Settings", "SE-01",
 "As a user, I want a Profile section so I can set my name, avatar, role.",
 "• Editable name, email, avatar color\n• Role display",
 "Medium", "Implemented",
 "Settings → Profile."),

("Settings", "SE-02",
 "As an admin, I want a Members section so I can invite and manage team members.",
 "• List of users with roles\n• Invite by email\n• Edit role / remove user",
 "High", "Implemented",
 "Settings → Members."),

("Settings", "SE-03",
 "As a user, I want notification preferences so I can control what hits my inbox.",
 "• Toggle channels (in-app, email)\n• Toggle event types",
 "Medium", "Implemented",
 "Settings → Notifications."),

("Settings", "SE-04",
 "As a user, I want Outlook calendar sync so my OOO/vacations sync automatically.",
 "• Connect button\n• OAuth flow\n• Calendar events pulled into the app",
 "Low", "Coming Soon",
 "Coming Soon badge — requires backend OAuth."),

("Settings", "SE-05",
 "As an admin, I want a Work Schedule editor so I can define workweeks, capacity, and holidays.",
 "• Year calendar grid (12 months)\n• Click any day to add an exception (holiday, non-working, extra workday, capacity)\n• Workweek day toggles\n• Working/non-working day counts",
 "High", "Implemented",
 "editSchedule + addSchedException."),

("Settings", "SE-06",
 "As an admin, I want a Billing section so I can see plans, invoices, and download receipts.",
 "• Plan card\n• Invoice history table\n• Download link per invoice",
 "Medium", "Implemented",
 "Billing page with Download link (stubbed PDF gen)."),

("Settings", "SE-07",
 "As an admin, I want to manage workspaces so I can create/rename/delete them.",
 "• Workspace list with edit buttons\n• Create new workspace modal",
 "Medium", "Implemented",
 "Settings → Workspaces."),

# ────────────────────────── CUSTOMIZE MENU ──────────────────────────
("Customize Menu", "CU-01",
 "As a user, I want to show/hide sidebar nav items so I can declutter my sidebar.",
 "• Modal with toggle per nav item\n• 12 items (Inbox, My To-Do, Timesheets, Workload, Created by me, Stream, Starred, Dashboards, Reports, Calendars, Forms, Settings)\n• Saved to HIDDEN_NAV map",
 "Low", "Implemented",
 "showCustomizeMenu modal."),

("Customize Menu", "CU-02",
 "As a user, I want to drag-reorder sidebar items so I can put my most-used items first.",
 "• Drag handles on each item\n• Order persisted",
 "Low", "Not Started",
 "Phase 2 enhancement."),

# ────────────────────────── ACCOUNT MANAGEMENT / FINANCIAL ──────────────────────────
("Account Management", "AM-01",
 "As an account manager, I want an Account Management view to see client-level metrics and projects.",
 "• Client list with health indicators\n• Drill into client to see their projects\n• Account health summary",
 "Medium", "Implemented",
 "Account Management workspace."),

("Financial / PMO", "FI-01",
 "As a PMO lead, I want a financial overview so I can track budgets and burn.",
 "• Budget vs actual per project\n• Burn rate charts\n• Revenue/cost summaries",
 "Medium", "Implemented",
 "Financial dashboard widget."),

# ────────────────────────── GLOBAL UI ──────────────────────────
("Global UI", "UI-01",
 "As a user, I want a consistent top bar so I always know where I am.",
 "• Page title, subtitle, action buttons\n• Workspace switcher\n• Search (future)",
 "High", "Implemented",
 "setTopbar function."),

("Global UI", "UI-02",
 "As a user, I want a mobile-responsive layout so I can use the app on tablet/phone.",
 "• Collapsible sidebar\n• Responsive grid breakpoints\n• Touch-friendly tap targets",
 "Medium", "Partial",
 "Basic responsive; could be tuned."),

("Global UI", "UI-03",
 "As a user, I want a welcome/onboarding screen on first load so I know where to start.",
 "• Welcome screen with quick actions\n• Tutorial pointers (future)",
 "Low", "Implemented",
 "view-welcome shown on initial load."),
]

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 1: All Stories (Master List)
# ═══════════════════════════════════════════════════════════════════════════════
ws = wb.active
ws.title = "User Stories"

# Title row
ws.merge_cells('A1:G1')
ws['A1'] = "Delta Project Management — User Stories"
ws['A1'].font = TITLE_FONT
ws['A1'].alignment = Alignment(horizontal='left', vertical='center')
ws.row_dimensions[1].height = 28

# Subtitle row
ws.merge_cells('A2:G2')
ws['A2'] = "Generated 2026-05-15 — covers all modules built in the Delta app"
ws['A2'].font = Font(italic=True, color="58637A", size=10)
ws.row_dimensions[2].height = 18

# Header row
HEADERS = ["Module", "Story ID", "User Story", "Acceptance Criteria", "Priority", "Status", "Notes"]
for i, h in enumerate(HEADERS, 1):
    c = ws.cell(row=4, column=i, value=h)
    c.fill = HEADER_FILL
    c.font = HEADER_FONT
    c.alignment = CENTER_ALIGN
    c.border = BORDER
ws.row_dimensions[4].height = 24

# Body
row = 5
for s in STORIES:
    module, sid, story, ac, prio, stat, notes = s
    cells = [
        (1, module), (2, sid), (3, story), (4, ac),
        (5, prio), (6, stat), (7, notes),
    ]
    for col, val in cells:
        c = ws.cell(row=row, column=col, value=val)
        c.alignment = WRAP_ALIGN
        c.border = BORDER
        c.font = Font(name="Calibri", size=10)
    # Status fill
    ws.cell(row=row, column=6).fill = STATUS_FILLS.get(stat, PatternFill())
    ws.cell(row=row, column=6).alignment = CENTER_ALIGN
    ws.cell(row=row, column=6).font = Font(bold=True, size=10)
    # Priority fill
    ws.cell(row=row, column=5).fill = PRIORITY_FILLS.get(prio, PatternFill())
    ws.cell(row=row, column=5).alignment = CENTER_ALIGN
    ws.cell(row=row, column=5).font = Font(bold=True, size=10)
    # Story ID center
    ws.cell(row=row, column=2).alignment = CENTER_ALIGN
    ws.cell(row=row, column=2).font = Font(bold=True, size=10, color="0B7285")
    row += 1

# Column widths
widths = {'A': 20, 'B': 10, 'C': 55, 'D': 55, 'E': 11, 'F': 14, 'G': 38}
for col, w in widths.items():
    ws.column_dimensions[col].width = w

# Auto row height — leave as auto; Excel handles wrap text
ws.freeze_panes = "A5"
ws.auto_filter.ref = f"A4:G{row-1}"

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 2: Summary by Module
# ═══════════════════════════════════════════════════════════════════════════════
ws2 = wb.create_sheet("Summary by Module")
ws2.merge_cells('A1:E1')
ws2['A1'] = "Coverage Summary by Module"
ws2['A1'].font = TITLE_FONT
ws2.row_dimensions[1].height = 28

# Aggregate
from collections import defaultdict
mod_stats = defaultdict(lambda: {'total': 0, 'Implemented': 0, 'Partial': 0, 'Coming Soon': 0, 'Not Started': 0})
for s in STORIES:
    module, _, _, _, _, stat, _ = s
    mod_stats[module]['total'] += 1
    mod_stats[module][stat] = mod_stats[module].get(stat, 0) + 1

headers2 = ["Module", "Total Stories", "Implemented", "Partial", "Coming Soon / Not Started"]
for i, h in enumerate(headers2, 1):
    c = ws2.cell(row=3, column=i, value=h)
    c.fill = HEADER_FILL
    c.font = HEADER_FONT
    c.alignment = CENTER_ALIGN
    c.border = BORDER
ws2.row_dimensions[3].height = 24

r = 4
for module, st in mod_stats.items():
    pending = st.get('Coming Soon', 0) + st.get('Not Started', 0)
    ws2.cell(row=r, column=1, value=module).alignment = WRAP_ALIGN
    ws2.cell(row=r, column=2, value=st['total']).alignment = CENTER_ALIGN
    ws2.cell(row=r, column=3, value=st.get('Implemented', 0)).alignment = CENTER_ALIGN
    ws2.cell(row=r, column=4, value=st.get('Partial', 0)).alignment = CENTER_ALIGN
    ws2.cell(row=r, column=5, value=pending).alignment = CENTER_ALIGN
    for col in range(1, 6):
        ws2.cell(row=r, column=col).border = BORDER
        ws2.cell(row=r, column=col).font = Font(name="Calibri", size=10)
    # Color the implemented count green-ish if equal to total
    if st.get('Implemented', 0) == st['total']:
        ws2.cell(row=r, column=3).fill = STATUS_FILLS['Implemented']
        ws2.cell(row=r, column=3).font = Font(bold=True, size=10)
    if pending > 0:
        ws2.cell(row=r, column=5).fill = STATUS_FILLS['Not Started']
        ws2.cell(row=r, column=5).font = Font(bold=True, size=10)
    r += 1

# Totals row
ws2.cell(row=r, column=1, value="TOTAL").font = Font(bold=True, size=11)
ws2.cell(row=r, column=2, value=sum(s['total'] for s in mod_stats.values()))
ws2.cell(row=r, column=3, value=sum(s.get('Implemented', 0) for s in mod_stats.values()))
ws2.cell(row=r, column=4, value=sum(s.get('Partial', 0) for s in mod_stats.values()))
ws2.cell(row=r, column=5, value=sum(s.get('Coming Soon', 0) + s.get('Not Started', 0) for s in mod_stats.values()))
for col in range(1, 6):
    cell = ws2.cell(row=r, column=col)
    cell.fill = SECTION_FILL
    cell.font = Font(bold=True, size=11, color="0B7285")
    cell.border = BORDER
    cell.alignment = CENTER_ALIGN if col > 1 else Alignment(horizontal='left', vertical='center')

widths2 = {'A': 26, 'B': 16, 'C': 16, 'D': 12, 'E': 26}
for col, w in widths2.items():
    ws2.column_dimensions[col].width = w
ws2.freeze_panes = "A4"

# ═══════════════════════════════════════════════════════════════════════════════
# SHEET 3: Legend
# ═══════════════════════════════════════════════════════════════════════════════
ws3 = wb.create_sheet("Legend")
ws3['A1'] = "Legend & Definitions"
ws3['A1'].font = TITLE_FONT

ws3['A3'] = "Status"
ws3['A3'].font = SECTION_FONT
ws3['A3'].fill = SECTION_FILL

legend_rows = [
    ("Implemented", "Feature is built and working in the current app.", STATUS_FILLS['Implemented']),
    ("Partial", "Feature is partially built — core works but enhancements are needed.", STATUS_FILLS['Partial']),
    ("Coming Soon", "Placeholder shown in UI; awaiting backend integration.", STATUS_FILLS['Coming Soon']),
    ("Not Started", "Identified but not yet built.", STATUS_FILLS['Not Started']),
]
r = 4
for label, desc, fill in legend_rows:
    ws3.cell(row=r, column=1, value=label).fill = fill
    ws3.cell(row=r, column=1).font = Font(bold=True, size=10)
    ws3.cell(row=r, column=1).alignment = CENTER_ALIGN
    ws3.cell(row=r, column=1).border = BORDER
    ws3.cell(row=r, column=2, value=desc).alignment = WRAP_ALIGN
    ws3.cell(row=r, column=2).border = BORDER
    r += 1

r += 2
ws3.cell(row=r, column=1, value="Priority").font = SECTION_FONT
ws3.cell(row=r, column=1).fill = SECTION_FILL
r += 1
prio_rows = [
    ("High", "Core functionality — required for usable product."),
    ("Medium", "Important but not blocking."),
    ("Low", "Nice-to-have or polish item."),
]
for label, desc in prio_rows:
    ws3.cell(row=r, column=1, value=label).fill = PRIORITY_FILLS[label]
    ws3.cell(row=r, column=1).font = Font(bold=True, size=10)
    ws3.cell(row=r, column=1).alignment = CENTER_ALIGN
    ws3.cell(row=r, column=1).border = BORDER
    ws3.cell(row=r, column=2, value=desc).alignment = WRAP_ALIGN
    ws3.cell(row=r, column=2).border = BORDER
    r += 1

ws3.column_dimensions['A'].width = 18
ws3.column_dimensions['B'].width = 70

# ── Save ─────────────────────────────────────────────────────────────────────
out = '/home/user/YCxDesign/Delta_User_Stories.xlsx'
wb.save(out)
print(f"Saved: {out}")
print(f"Total stories: {len(STORIES)}")
print(f"Modules: {len(mod_stats)}")
