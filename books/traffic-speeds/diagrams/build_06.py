from _draw import *
W,G="#fff",GREY
# 1 plan
b=box(290,30,220,70,"Segments","where city = Pune: 20,000 rows",fill=G,ts=16)+arrow(400,100,400,146)
steps=[("Scan daily totals","last week only","7 billion rows"),("Join","keep Pune's roads","3.4 million rows"),("Sum per road","sum and count","20,000 rows"),("Sort","keep the worst 10","10 rows")]
for i,(t,s,n) in enumerate(steps):
    x=30+i*260
    b+=box(x,150,200,80,t,s)
    b+=text(x+100,262,n,16,bold=True)
    if i<3: b+=arrow(x+200,190,x+256,190)
b+=text(520,330,"The planner's aim: shrink the data as early as possible.",15,italic=True)
svg('06-plan.svg',355,b)

# 2 mpp
b=box(30,40,160,76,"Analyst","sends SQL")+arrow(190,78,396,78)
b+=box(400,40,240,76,"Coordinator","parses, plans, hands out work",fill=G)
xs=[110,410,710]
for i,x in enumerate(xs):
    b+=box(x,200,220,76,f"Worker {i+1}","scan, filter, join, sum")
    b+=arrow(520,116,x+110,196)
    b+=arrow(x+110,276,x+110,346)
b+=f'<line x1="334" y1="238" x2="406" y2="238" stroke="#222" stroke-width="2" marker-end="url(#a)" marker-start="url(#a)"/>'
b+=f'<line x1="634" y1="238" x2="706" y2="238" stroke="#222" stroke-width="2" marker-end="url(#a)" marker-start="url(#a)"/>'
b+=text(370,228,"rows",13,italic=True,fill="#444")+text(670,228,"rows",13,italic=True,fill="#444")
b+=bar(110,350,820,56)+text(520,384,"Lake: Parquet files in Iceberg tables",17,bold=True)
b+=text(760,150,"pieces of the plan",14,italic=True,fill="#444")+text(370,318,"each reads its share of files",14,italic=True,fill="#444")
b+=text(520,440,"Many machines work on one query at once. Data flows between them in memory.",15,italic=True)
svg('06-mpp.svg',460,b)

# 3 storage vs compute
b=text(250,36,"Warehouse",19,bold=True)+text(250,58,"storage and compute together",14,fill="#444")
b+=text(790,36,"Query engine on a lake",19,bold=True)+text(790,58,"storage and compute apart",14,fill="#444")
b+=f'<line x1="520" y1="20" x2="520" y2="380" stroke="#222" stroke-width="1" stroke-dasharray="4 6"/>'
for i,x in enumerate([30,190,350]):
    b+=box(x,90,140,90,f"Node {i+1}","CPU + own disks",ts=16)
b+=box(150,270,200,60,"Files to load",ts=16,fill=G)+arrow(250,270,250,184)+text(262,232,"load step",14,italic=True,anchor="start",fill="#444")
b+=text(250,365,"Data is copied in. The engine owns it.",15)
for i,(x,n) in enumerate([(545,"Trino"),(705,"Spark"),(865,"Flink")]):
    b+=box(x,90,140,90,n,"CPU only",ts=16)+arrow(x+70,180,x+70,266)
b+=bar(545,270,460,60)+text(775,306,"Object storage: one copy",17,bold=True)
b+=text(790,365,"Data stays put. Engines come and go.",15)
svg('06-storage-compute.svg',390,b)

# 4 cost bars
rows=[(900,"A year of raw pings, no filter","1,300 TB scanned","about $6,500"),
      (130,"One week of raw pings, two columns","about 4 TB scanned","about $20"),
      (16,"One week of daily totals","about 50 GB scanned","about 25 cents")]
b=''
for i,(w,t,scan,cost) in enumerate(rows):
    y=40+i*105
    b+=text(40,y,t,17,bold=True,anchor="start")+bar(40,y+12,w,40)
    if w<800: b+=text(40+w+16,y+38,scan+"  =  "+cost,15,anchor="start")
    else: b+=text(490,y+38,scan+"  =  "+cost,15)
b+=text(520,365,"The same question three ways, at $5 per TB scanned. Bars are not to scale.",15,italic=True)
svg('06-cost.svg',385,b)

# 5 chooser
rows=[("Fits on one machine","up to roughly 100 GB touched","DuckDB","one process, no cluster"),
      ("Ad-hoc over the lake, now and then","a few queries a day","Athena","no cluster, pay per scan"),
      ("Ad-hoc over the lake, all day","many analysts, steady use","Trino","your own cluster"),
      ("Dashboards, many users","same tables, sub-second","Warehouse","load a curated copy"),
      ("Hours-long transformation","terabytes shuffled","Spark","see Chapter 5")]
b=text(260,34,"If the work is...",18,bold=True)+text(800,34,"...reach for",18,bold=True)
for i,(a,a2,t,t2) in enumerate(rows):
    y=52+i*76
    b+=box(40,y,440,62,a,a2,ts=16)+arrow(480,y+31,616,y+31)+box(620,y,360,62,t,t2,fill=G,ts=17)
svg('06-chooser.svg',445,b)
