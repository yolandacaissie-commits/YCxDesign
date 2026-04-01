#!/usr/bin/env python3
"""Chunk 1: Add users, custom fields, workspace, folders, 6 account projects."""
with open('/home/user/YCxDesign/team-nexus-v3.html', 'r') as f:
    html = f.read()

# ── 1. Add 3 new users ──
old_users_end = "  {id:6,name:'Yolanda Caissie', email:'yolanda.c@decisionfoundry.com', color:'#1AA6B7',role:'admin'},\n];"
new_users_end = """  {id:6,name:'Yolanda Caissie',            email:'yolanda.c@decisionfoundry.com', color:'#1AA6B7',role:'admin'},
  {id:7,name:'Ankit Bhandari',              email:'ankit.b@decisionfoundry.com',   color:'#3b82f6',role:'regular'},
  {id:8,name:'Raja Aishah Bin Raja AbdulRashid',email:'raja.a@decisionfoundry.com',color:'#8b5cf6',role:'regular'},
  {id:9,name:'Jomal Andrews',               email:'jomal.a@decisionfoundry.com',   color:'#22c55e',role:'regular'},
];"""
assert old_users_end in html
html = html.replace(old_users_end, new_users_end, 1)

# ── 2. Add custom fields ──
PRODUCTS = ['Adverity','AgentForce','Audit','Azure','Camptag',
'Churn Prediction/Retention','CLTV (Customer Lifetime Value)',
'CPQ (Configure, Price, Quote)','DataBricks','Data Cloud','DBT',
'Data Strategy Consulting','Experience Cloud','Marketing Cloud',
'MCI (Marketing Cloud Intelligence)','Memosight',
'MMM (Marketing Mix Modeling)','MTA (Multi-Touch Attribution)',
'Mulesoft','NinjaCat','Pardot/Marketing Cloud Engagement',
'Power BI','Sales Cloud','Service Cloud','SF CRM',
'SFMC (Sales Marketing Cloud)','Sigma','Snowflake','Supermetrics','Tableau']
products_js = str(PRODUCTS).replace('"',"'").replace("'", "'")

old_cfs = """let CUSTOM_FIELDS=[
  {id:'cf1',name:'Story Points',type:'number',desc:'Effort estimate in story points'},
  {id:'cf2',name:'Sprint',type:'select',options:['Sprint 1','Sprint 2','Sprint 3'],desc:'Which sprint this belongs to'},
  {id:'cf3',name:'Review URL',type:'url',desc:'Link to design or PR review'},
];"""

new_cfs = f"""let CUSTOM_FIELDS=[
  {{id:'cf1',name:'Story Points',type:'number',options:[],desc:'Effort estimate in story points',visible:true}},
  {{id:'cf2',name:'Sprint',type:'select',options:['Sprint 1','Sprint 2','Sprint 3'],desc:'Which sprint this belongs to',visible:true}},
  {{id:'cf3',name:'Review URL',type:'url',options:[],desc:'Link to design or PR review',visible:true}},
  // ── Account Management fields ──
  {{id:'cf_client',name:'Client',type:'text',options:[],desc:'Client company name',visible:true}},
  {{id:'cf_acct_owner',name:'Account Owner',type:'assignee',options:[],desc:'Primary account owner',visible:true}},
  {{id:'cf_acct_health',name:'Account Health',type:'select',options:['Healthy','At Risk','Critical','Unknown'],desc:'Overall account health',visible:true}},
  {{id:'cf_delivery_status',name:'Delivery Status',type:'select',options:['Not Started','In Progress - On Track','In Progress - At Risk','In Progress - Behind','On Hold','Complete'],desc:'Current delivery status',visible:true}},
  {{id:'cf_upsell',name:'Upsell / Cross Sell',type:'text',options:[],desc:'Upsell and cross-sell opportunities',visible:true}},
  {{id:'cf_products',name:'Products',type:'multiselect',options:{products_js},desc:'Products and services delivered',visible:true}},
];"""

assert old_cfs in html
html = html.replace(old_cfs, new_cfs, 1)

# ── 3. Add ws5 (Client Accounts workspace) ──
old_ws = "  {id:'ws4',name:'Operations',color:'#22c55e',emoji:'📊',desc:'Financial operations and resource planning.',expanded:false},\n];"
new_ws = "  {id:'ws4',name:'Operations',color:'#22c55e',emoji:'📊',desc:'Financial operations and resource planning.',expanded:false},\n  {id:'ws5',name:'Client Accounts',color:'#3b82f6',emoji:'🏢',desc:'Active client accounts and delivery tracking.',expanded:false},\n];"
assert old_ws in html
html = html.replace(old_ws, new_ws, 1)

# ── 4. Add phase folders for ws5 ──
old_folders = "  {id:'fl3',name:'Brand',workspaceId:'ws2',parentFolderId:null,emoji:'🎨',color:'#8b5cf6'},\n];"
new_folders = """  {id:'fl3',name:'Brand',workspaceId:'ws2',parentFolderId:null,emoji:'🎨',color:'#8b5cf6'},
  {id:'fl4',name:'0. Pipeline',workspaceId:'ws5',parentFolderId:null,emoji:'📋',color:'#94a3b8'},
  {id:'fl5',name:'3. Execution',workspaceId:'ws5',parentFolderId:null,emoji:'⚡',color:'#22c55e'},
  {id:'fl6',name:'4. On Hold',workspaceId:'ws5',parentFolderId:null,emoji:'⏸',color:'#f59e4a'},
];"""
assert old_folders in html
html = html.replace(old_folders, new_folders, 1)

# ── 5. Add 6 account projects (p.custom at project level) ──
# Insert after the last financial project (p7 - Naveen's Test Project)
old_proj_end = """  {id:'p7',name:"Naveen's Test Project",desc:'Data Engineering pipeline build — internal initiative.',
   status:'active',priority:'low',emoji:'🔧',color:'#f59e4a',
   contractValue:0,hourlyRate:100,
   lob:['Data Engineering'],
   dueDate:'2026-04-11',
   monthlyCosts:[
     {month:'2026-01',actual:15000,estimated:15000},
     {month:'2026-02',actual:12000,estimated:12000},
     {month:'2026-03',actual:8000,estimated:10000},
   ],
   views:['table'],visibleColumns:['pred','duration','startDate','dueDate','status','assignee'],sortField:'startDate',sortDir:'asc',filterRules:[],groupBy:null,locations:[{workspaceId:'ws4',folderId:null,isHome:true}],
   tasks:[
    {id:'tn1',title:'Pipeline Architecture',status:'done',priority:'high',assignee:1,duration:7,pred:null,start:rel(-35),end:rel(-28),dueDate:null,description:'Design end-to-end pipeline architecture.',comments:[],history:[{type:'status_change',from:'todo',to:'done',userId:1,time:rel(-28).toISOString()}],custom:{}},
    {id:'tn2',title:'ETL Development',status:'in_progress',priority:'high',assignee:2,duration:30,pred:'tn1',start:rel(-20),end:rel(10),dueDate:null,description:'Build ETL pipelines and data transformations.',comments:[],history:[{type:'status_change',from:'todo',to:'in_progress',userId:2,time:rel(-20).toISOString()}],custom:{}},
   ]},
];"""

new_proj_end = """  {id:'p7',name:"Naveen's Test Project",desc:'Data Engineering pipeline build — internal initiative.',
   status:'active',priority:'low',emoji:'🔧',color:'#f59e4a',
   contractValue:0,hourlyRate:100,
   lob:['Data Engineering'],
   dueDate:'2026-04-11',
   monthlyCosts:[
     {month:'2026-01',actual:15000,estimated:15000},
     {month:'2026-02',actual:12000,estimated:12000},
     {month:'2026-03',actual:8000,estimated:10000},
   ],
   views:['table'],visibleColumns:['pred','duration','startDate','dueDate','status','assignee'],sortField:'startDate',sortDir:'asc',filterRules:[],groupBy:null,locations:[{workspaceId:'ws4',folderId:null,isHome:true}],
   tasks:[
    {id:'tn1',title:'Pipeline Architecture',status:'done',priority:'high',assignee:1,duration:7,pred:null,start:rel(-35),end:rel(-28),dueDate:null,description:'Design end-to-end pipeline architecture.',comments:[],history:[{type:'status_change',from:'todo',to:'done',userId:1,time:rel(-28).toISOString()}],custom:{}},
    {id:'tn2',title:'ETL Development',status:'in_progress',priority:'high',assignee:2,duration:30,pred:'tn1',start:rel(-20),end:rel(10),dueDate:null,description:'Build ETL pipelines and data transformations.',comments:[],history:[{type:'status_change',from:'todo',to:'in_progress',userId:2,time:rel(-20).toISOString()}],custom:{}},
   ]},
  // ── CLIENT ACCOUNT PROJECTS ──
  {id:'p8',name:'TBC - Addressable Media LLC',desc:'MCI implementation for Addressable Media.',
   status:'on_hold',priority:'medium',emoji:'🏢',color:'#f59e4a',
   views:['table'],visibleColumns:['pred','duration','startDate','dueDate','status','assignee'],sortField:'startDate',sortDir:'asc',filterRules:[],groupBy:null,
   custom:{cf_client:'Addressable Media Inc',cf_acct_owner:7,cf_acct_health:'Healthy',cf_delivery_status:'On Hold',cf_upsell:'',cf_products:['MCI (Marketing Cloud Intelligence)']},
   locations:[{workspaceId:'ws5',folderId:'fl6',isHome:true}],
   tasks:[
    {id:'tp8_1',title:'Project Scoping',status:'done',priority:'high',assignee:7,duration:5,pred:null,start:rel(-60),end:rel(-55),dueDate:null,description:'Define project scope.',comments:[],history:[],custom:{}},
    {id:'tp8_2',title:'Implementation',status:'todo',priority:'high',assignee:7,duration:20,pred:'tp8_1',start:rel(5),end:rel(25),dueDate:rel(25).toISOString().slice(0,10),description:'MCI implementation.',comments:[],history:[],custom:{}},
   ]},
  {id:'p9',name:'25I001 Aria Systems - Salesforce',desc:'Salesforce and BI delivery for Aria Systems.',
   status:'active',priority:'high',emoji:'🏢',color:'#1AA6B7',
   views:['table'],visibleColumns:['pred','duration','startDate','dueDate','status','assignee'],sortField:'startDate',sortDir:'asc',filterRules:[],groupBy:null,
   custom:{cf_client:'Aria Systems',cf_acct_owner:8,cf_acct_health:'Healthy',cf_delivery_status:'In Progress - On Track',cf_upsell:'Chatting about MTA, Reporting, Salesforce A/B testing',cf_products:['Sales Cloud','MTA (Multi-Touch Attribution)']},
   locations:[{workspaceId:'ws5',folderId:'fl5',isHome:true}],
   tasks:[
    {id:'tp9_1',title:'Discovery',status:'done',priority:'high',assignee:8,duration:7,pred:null,start:rel(-45),end:rel(-38),dueDate:null,description:'Client discovery sessions.',comments:[],history:[],custom:{}},
    {id:'tp9_2',title:'SF Configuration',status:'in_progress',priority:'high',assignee:8,duration:30,pred:'tp9_1',start:rel(-15),end:rel(15),dueDate:rel(15).toISOString().slice(0,10),description:'Salesforce configuration.',comments:[],history:[],custom:{}},
    {id:'tp9_3',title:'BI Integration',status:'todo',priority:'medium',assignee:2,duration:14,pred:'tp9_2',start:rel(16),end:rel(30),dueDate:rel(30).toISOString().slice(0,10),description:'BI dashboard integration.',comments:[],history:[],custom:{}},
   ]},
  {id:'p10',name:'26C010 Aria Systems - AgentForce',desc:'AgentForce and Data Cloud delivery for Aria Systems.',
   status:'active',priority:'high',emoji:'🏢',color:'#8b5cf6',
   views:['table'],visibleColumns:['pred','duration','startDate','dueDate','status','assignee'],sortField:'startDate',sortDir:'asc',filterRules:[],groupBy:null,
   custom:{cf_client:'Aria Systems',cf_acct_owner:6,cf_acct_health:'Healthy',cf_delivery_status:'In Progress - On Track',cf_upsell:'',cf_products:['AgentForce','Data Cloud']},
   locations:[{workspaceId:'ws5',folderId:'fl5',isHome:true}],
   tasks:[
    {id:'tp10_1',title:'Platform Setup',status:'done',priority:'high',assignee:6,duration:7,pred:null,start:rel(-30),end:rel(-23),dueDate:null,description:'AgentForce platform setup.',comments:[],history:[],custom:{}},
    {id:'tp10_2',title:'Agent Development',status:'in_progress',priority:'high',assignee:6,duration:21,pred:'tp10_1',start:rel(-10),end:rel(11),dueDate:rel(11).toISOString().slice(0,10),description:'Build AI agents.',comments:[],history:[],custom:{}},
   ]},
  {id:'p11',name:'Axos Bank',desc:'Pipeline opportunity — Axos Bank.',
   status:'active',priority:'low',emoji:'🏦',color:'#94a3b8',
   views:['table'],visibleColumns:['pred','duration','startDate','dueDate','status','assignee'],sortField:'startDate',sortDir:'asc',filterRules:[],groupBy:null,
   custom:{cf_client:'Axos Bank',cf_acct_owner:7,cf_acct_health:'Healthy',cf_delivery_status:'Not Started',cf_upsell:'',cf_products:[]},
   locations:[{workspaceId:'ws5',folderId:'fl4',isHome:true}],
   tasks:[
    {id:'tp11_1',title:'Initial Discovery Call',status:'todo',priority:'medium',assignee:7,duration:2,pred:null,start:rel(7),end:rel(9),dueDate:rel(9).toISOString().slice(0,10),description:'Introductory discovery call.',comments:[],history:[],custom:{}},
   ]},
  {id:'p12',name:'25L036 BAL - MCI',desc:'MCI implementation for BAL.',
   status:'active',priority:'medium',emoji:'🏢',color:'#22c55e',
   views:['table'],visibleColumns:['pred','duration','startDate','dueDate','status','assignee'],sortField:'startDate',sortDir:'asc',filterRules:[],groupBy:null,
   custom:{cf_client:'BAL',cf_acct_owner:9,cf_acct_health:'Healthy',cf_delivery_status:'In Progress - On Track',cf_upsell:'',cf_products:['MCI (Marketing Cloud Intelligence)']},
   locations:[{workspaceId:'ws5',folderId:'fl5',isHome:true}],
   tasks:[
    {id:'tp12_1',title:'MCI Setup',status:'done',priority:'high',assignee:9,duration:10,pred:null,start:rel(-40),end:rel(-30),dueDate:null,description:'MCI platform setup.',comments:[],history:[],custom:{}},
    {id:'tp12_2',title:'Dashboard Build',status:'in_progress',priority:'high',assignee:9,duration:14,pred:'tp12_1',start:rel(-5),end:rel(9),dueDate:rel(9).toISOString().slice(0,10),description:'Build MCI dashboards.',comments:[],history:[],custom:{}},
   ]},
  {id:'p13',name:'25B017 Belardi Wong - MCI',desc:'MCI delivery for Belardi Wong — at risk.',
   status:'active',priority:'high',emoji:'🏢',color:'#ef4444',
   views:['table'],visibleColumns:['pred','duration','startDate','dueDate','status','assignee'],sortField:'startDate',sortDir:'asc',filterRules:[],groupBy:null,
   custom:{cf_client:'Belardi Wong',cf_acct_owner:8,cf_acct_health:'At Risk',cf_delivery_status:'In Progress - On Track',cf_upsell:'',cf_products:['MCI (Marketing Cloud Intelligence)','Sales Cloud']},
   locations:[{workspaceId:'ws5',folderId:'fl5',isHome:true}],
   tasks:[
    {id:'tp13_1',title:'MCI Implementation',status:'in_progress',priority:'critical',assignee:8,duration:21,pred:null,start:rel(-20),end:rel(1),dueDate:rel(1).toISOString().slice(0,10),description:'MCI implementation — overdue risk.',comments:[],history:[],custom:{}},
    {id:'tp13_2',title:'Sales Cloud Integration',status:'todo',priority:'high',assignee:2,duration:10,pred:'tp13_1',start:rel(2),end:rel(12),dueDate:rel(12).toISOString().slice(0,10),description:'Sales Cloud integration.',comments:[],history:[],custom:{}},
   ]},
];"""

assert old_proj_end in html, 'project end anchor not found'
html = html.replace(old_proj_end, new_proj_end, 1)

with open('/home/user/YCxDesign/team-nexus-v3.html', 'w') as f:
    f.write(html)
print('Chunk 1 done')
