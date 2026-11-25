from _draw import *
W,G="#fff",GREY
# 1 inside out
b=text(210,36,"Inside one database",18,bold=True)+text(740,36,"At Wayline",18,bold=True)
rows=[("Commit log","Kafka"),("Tables","Raw pings in Iceberg"),("Materialised views","Daily totals, typical speeds"),("Indexes and caches","Postgres and DynamoDB serving stores"),("The code that keeps views fresh","Flink and Spark jobs"),("Query planner","Trino and Athena")]
for i,(l,r) in enumerate(rows):
    y=54+i*58
    b+=box(40,y,340,46,l,ts=16)+text(430,y+30,"=",22,bold=True)+box(480,y,520,46,r,fill=G,ts=16)
b+=text(520,425,"The same parts as a database, taken out of the box and joined by a log.",15,italic=True)
svg('09-inside-out.svg',445,b)

# 2 DAG
b=box(20,70,170,76,"Day complete?","wait for the lake",ts=16)+arrow(190,108,216,108)
b+=box(220,70,190,76,"Daily totals","last 3 days",ts=16)+arrow(410,108,436,108)
b+=box(440,70,170,76,"Typical speeds","last 56 days",ts=16)+arrow(610,108,636,108)
b+=box(640,70,150,76,"Checks","block if wrong",fill=G,ts=16)+arrow(790,108,816,108)
b+=box(820,70,200,76,"Publish","switch readers over",ts=16)
b+=box(330,230,220,76,"Compare with stream","same hours, both paths",ts=16)
b+=arrow(340,146,420,226)+arrow(550,250,680,150)
b+=box(820,230,200,76,"Tidy up","compact, expire snapshots",ts=16)+arrow(920,146,920,226)
b+=text(520,360,"Each box is a task for one named day. A task runs only after the ones before it succeed.",15,italic=True)
svg('09-dag.svg',380,b)

# 3 reconcile
b=box(30,50,340,84,"Stream path","road 4471, 08:00 to 09:00: 1,420 pings",ts=17)
b+=box(30,200,340,84,"Batch path","same road, same hour: 1,436 pings",ts=17)
b+=box(450,125,150,84,"Compare","differ by 1.1%",fill=G,ts=17)
b+=arrow(370,92,446,150)+arrow(370,242,446,186)
b+=box(690,50,320,84,"Within 2%","expected: late pings",ts=17)+box(690,200,320,84,"Beyond 2%","alert: something is broken",ts=17,dash=True)
b+=arrow(600,150,686,92)+arrow(600,186,686,242,dash=True)
b+=text(520,340,"Two independent paths computing the same thing are a free cross-check.",15,italic=True)
svg('09-reconcile.svg',360,b)

# 4 counts
items=[("Received","by ingest","34,560 M"),("In the log","Kafka","34,560 M"),("In the lake","Iceberg","34,548 M"),("Daily totals","sum of counts","34,548 M")]
b=''
for i,(t,s,n) in enumerate(items):
    x=20+i*260
    b+=box(x,60,220,80,t,s)+text(x+110,172,n,18,bold=True)
    if i<3: b+=arrow(x+220,100,x+256,100)
b+=text(650,205,"12 M duplicates removed",14,italic=True,fill="#444")
b+=text(520,265,"If the counts at each stage cannot be explained, something was lost or counted twice.",15,italic=True)
svg('09-counts.svg',285,b)

# 5 side by side
b=box(30,130,220,90,"Raw pings","never changed",fill=G)
b+=box(400,50,280,80,"Typical speeds v1","average")+box(400,220,280,80,"Typical speeds v2","median (new logic)",dash=True)
b+=arrow(250,160,396,95)+arrow(250,190,396,255)
b+=box(830,130,180,90,"Readers")
b+=arrow(680,95,826,160)+arrow(680,255,826,190,dash=True)
b+=text(770,105,"most, for now",14,italic=True,fill="#444")+text(770,255,"a few, then more",14,italic=True,fill="#444")
b+=text(520,355,"New logic is a new view built from the same raw data. Readers move across gradually.",15,italic=True)
svg('09-side-by-side.svg',375,b)
