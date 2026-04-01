#!/usr/bin/env python3
with open('/home/user/YCxDesign/team-nexus-v3.html','r') as f:
    html = f.read()

# 1. Add Operations workspace
old_ws = "  {id:'ws3',name:'Marketing',color:'#f59e4a',emoji:'📢',desc:'Campaigns, content and growth initiatives.',expanded:false},\n];"
new_ws = "  {id:'ws3',name:'Marketing',color:'#f59e4a',emoji:'📢',desc:'Campaigns, content and growth initiatives.',expanded:false},\n  {id:'ws4',name:'Operations',color:'#22c55e',emoji:'📊',desc:'Financial operations and resource planning.',expanded:false},\n];"
assert old_ws in html, "WORKSPACES anchor not found"
html = html.replace(old_ws, new_ws, 1)

# 2. Add financial projects after end of p3
old_proj_end = "    {id:'t13',title:'Stakeholder Review',status:'todo',priority:'low',assignee:5,duration:3,pred:'t12',start:rel(3),end:rel(6),dueDate:null,description:'Present concepts to stakeholders for feedback.',comments:[],history:[],custom:{}},\n   ]},\n];"

new_proj_end = """    {id:'t13',title:'Stakeholder Review',status:'todo',priority:'low',assignee:5,duration:3,pred:'t12',start:rel(3),end:rel(6),dueDate:null,description:'Present concepts to stakeholders for feedback.',comments:[],history:[],custom:{}},
   ]},
  // ── OPERATIONS / FINANCIAL PROJECTS ──
  {id:'p4',name:'Test Project A',desc:'Salesforce Services implementation and BI integration for enterprise client.',
   status:'active',priority:'high',emoji:'📊',color:'#1AA6B7',
   contractValue:110000,hourlyRate:150,
   lob:['SF Services','Business Intelligence'],
   dueDate:'2026-05-09',
   monthlyCosts:[
     {month:'2026-01',actual:45000,estimated:50000},
     {month:'2026-02',actual:38000,estimated:40000},
     {month:'2026-03',actual:22000,estimated:30000},
   ],
   locations:[{workspaceId:'ws4',folderId:null,isHome:true}],
   tasks:[
    {id:'ta1',title:'Requirements Analysis',status:'done',priority:'high',assignee:1,duration:10,pred:null,start:rel(-60),end:rel(-50),dueDate:null,description:'Define project scope and requirements.',comments:[],history:[{type:'status_change',from:'todo',to:'done',userId:1,time:rel(-50).toISOString()}],custom:{}},
    {id:'ta2',title:'Data Model Design',status:'done',priority:'high',assignee:6,duration:10,pred:'ta1',start:rel(-45),end:rel(-35),dueDate:null,description:'Design data architecture and field mappings.',comments:[],history:[{type:'status_change',from:'todo',to:'done',userId:6,time:rel(-35).toISOString()}],custom:{}},
    {id:'ta3',title:'Implementation',status:'in_progress',priority:'high',assignee:1,duration:40,pred:'ta2',start:rel(-20),end:rel(20),dueDate:null,description:'Build and configure Salesforce solution.',comments:[],history:[{type:'status_change',from:'todo',to:'in_progress',userId:1,time:rel(-20).toISOString()}],custom:{}},
    {id:'ta4',title:'UAT & Training',status:'todo',priority:'medium',assignee:6,duration:9,pred:'ta3',start:rel(21),end:rel(30),dueDate:null,description:'User acceptance testing and team training.',comments:[],history:[],custom:{}},
    {id:'ta5',title:'Go-Live & Support',status:'todo',priority:'high',assignee:1,duration:8,pred:'ta4',start:rel(31),end:rel(38),dueDate:null,description:'Production deployment and post-launch support.',comments:[],history:[],custom:{}},
   ]},
  {id:'p5',name:'Test Project B',desc:'SF Services delivery and custom development for mid-market client.',
   status:'active',priority:'medium',emoji:'💼',color:'#5AD2C9',
   contractValue:78000,hourlyRate:125,
   lob:['SF Services'],
   dueDate:'2026-04-26',
   monthlyCosts:[
     {month:'2026-01',actual:28000,estimated:30000},
     {month:'2026-02',actual:25000,estimated:28000},
     {month:'2026-03',actual:18000,estimated:20000},
   ],
   locations:[{workspaceId:'ws4',folderId:null,isHome:true}],
   tasks:[
    {id:'tb1',title:'Discovery Workshop',status:'done',priority:'high',assignee:2,duration:7,pred:null,start:rel(-45),end:rel(-38),dueDate:null,description:'Run discovery sessions with client.',comments:[],history:[{type:'status_change',from:'todo',to:'done',userId:2,time:rel(-38).toISOString()}],custom:{}},
    {id:'tb2',title:'Configuration & Custom Dev',status:'in_progress',priority:'high',assignee:2,duration:30,pred:'tb1',start:rel(-15),end:rel(15),dueDate:null,description:'Salesforce configuration and custom development.',comments:[],history:[{type:'status_change',from:'todo',to:'in_progress',userId:2,time:rel(-15).toISOString()}],custom:{}},
    {id:'tb3',title:'UAT & Deployment',status:'todo',priority:'high',assignee:1,duration:9,pred:'tb2',start:rel(16),end:rel(25),dueDate:null,description:'User acceptance testing and deployment.',comments:[],history:[],custom:{}},
   ]},
  {id:'p6',name:'Test Project C',desc:'SF Services and Data Science model integration.',
   status:'active',priority:'medium',emoji:'🔬',color:'#8b5cf6',
   contractValue:25000,hourlyRate:100,
   lob:['SF Services','Data Science'],
   dueDate:'2026-04-19',
   monthlyCosts:[
     {month:'2026-01',actual:8000,estimated:10000},
     {month:'2026-02',actual:9000,estimated:8000},
     {month:'2026-03',actual:5000,estimated:6000},
   ],
   locations:[{workspaceId:'ws4',folderId:null,isHome:true}],
   tasks:[
    {id:'tc1',title:'Scoping & Planning',status:'done',priority:'medium',assignee:6,duration:5,pred:null,start:rel(-30),end:rel(-25),dueDate:null,description:'Define project scope and deliverables.',comments:[],history:[{type:'status_change',from:'todo',to:'done',userId:6,time:rel(-25).toISOString()}],custom:{}},
    {id:'tc2',title:'ML Model Development',status:'in_progress',priority:'high',assignee:4,duration:22,pred:'tc1',start:rel(-10),end:rel(12),dueDate:null,description:'Build and validate ML models.',comments:[],history:[{type:'status_change',from:'todo',to:'in_progress',userId:4,time:rel(-10).toISOString()}],custom:{}},
    {id:'tc3',title:'Reporting & Handover',status:'todo',priority:'medium',assignee:6,duration:5,pred:'tc2',start:rel(13),end:rel(18),dueDate:null,description:'Final report and client handover.',comments:[],history:[],custom:{}},
   ]},
  {id:'p7',name:"Naveen's Test Project",desc:'Data Engineering pipeline build — internal initiative.',
   status:'active',priority:'low',emoji:'🔧',color:'#f59e4a',
   contractValue:0,hourlyRate:100,
   lob:['Data Engineering'],
   dueDate:'2026-04-11',
   monthlyCosts:[
     {month:'2026-01',actual:15000,estimated:15000},
     {month:'2026-02',actual:12000,estimated:12000},
     {month:'2026-03',actual:8000,estimated:10000},
   ],
   locations:[{workspaceId:'ws4',folderId:null,isHome:true}],
   tasks:[
    {id:'tn1',title:'Pipeline Architecture',status:'done',priority:'high',assignee:1,duration:7,pred:null,start:rel(-35),end:rel(-28),dueDate:null,description:'Design end-to-end pipeline architecture.',comments:[],history:[{type:'status_change',from:'todo',to:'done',userId:1,time:rel(-28).toISOString()}],custom:{}},
    {id:'tn2',title:'ETL Development',status:'in_progress',priority:'high',assignee:2,duration:30,pred:'tn1',start:rel(-20),end:rel(10),dueDate:null,description:'Build ETL pipelines and data transformations.',comments:[],history:[{type:'status_change',from:'todo',to:'in_progress',userId:2,time:rel(-20).toISOString()}],custom:{}},
   ]},
];"""

assert old_proj_end in html, "PROJECTS end anchor not found"
html = html.replace(old_proj_end, new_proj_end, 1)

# 3. Add timesheet entries for operations projects
old_ts = "  {id:'te5',userId:2,taskId:'t3',date:'2026-03-25',hours:3,activity:'Planning'},\n];"
new_ts = """  {id:'te5',userId:2,taskId:'t3',date:'2026-03-25',hours:3,activity:'Planning'},
  {id:'te6',userId:1,taskId:'ta3',date:'2026-03-10',hours:8,activity:'Development'},
  {id:'te7',userId:1,taskId:'ta3',date:'2026-03-17',hours:7.5,activity:'Development'},
  {id:'te8',userId:1,taskId:'ta3',date:'2026-03-24',hours:6,activity:'Development'},
  {id:'te9',userId:2,taskId:'tb2',date:'2026-03-11',hours:6,activity:'Configuration'},
  {id:'te10',userId:2,taskId:'tb2',date:'2026-03-18',hours:7,activity:'Configuration'},
  {id:'te11',userId:2,taskId:'tb2',date:'2026-03-25',hours:5,activity:'Testing'},
  {id:'te12',userId:6,taskId:'tc2',date:'2026-03-12',hours:5,activity:'ML Development'},
  {id:'te13',userId:6,taskId:'tn2',date:'2026-03-19',hours:8,activity:'Pipeline Dev'},
  {id:'te14',userId:4,taskId:'tc2',date:'2026-03-13',hours:6,activity:'ML Development'},
  {id:'te15',userId:1,taskId:'ta3',date:'2026-02-14',hours:8,activity:'Development'},
  {id:'te16',userId:2,taskId:'tb2',date:'2026-02-12',hours:7,activity:'Configuration'},
  {id:'te17',userId:6,taskId:'tc2',date:'2026-02-20',hours:6,activity:'Analysis'},
  {id:'te18',userId:2,taskId:'tn2',date:'2026-02-25',hours:8,activity:'Pipeline Dev'},
];"""

assert old_ts in html, "TIMESHEET_ENTRIES anchor not found"
html = html.replace(old_ts, new_ts, 1)

with open('/home/user/YCxDesign/team-nexus-v3.html','w') as f:
    f.write(html)

print("Chunk 1 done — data added")
