from _draw import *
W,G="#fff",GREY
# 1 btree
b=box(370,30,300,56,"0-16M  |  16-33M  |  33-50M",fill=G,ts=16)
for i,x in enumerate([60,370,680]):
    b+=arrow(520,86,x+135,126)
    b+=box(x,130,270,56,"0-5M  |  5-10M  |  10-16M" if i==0 else "...",fill=G if i==0 else W,ts=16)
for i,x in enumerate([30,250,470]):
    b+=arrow(195,186,x+100,226)
    b+=box(x,230,200,56,"... 4470 | 4471 | 4472 ..." if i==0 else "...",fill=G if i==0 else W,ts=15)
b+=arrow(130,286,130,326)+box(30,330,380,56,"segment 4471: sum 9,120, count 240",ts=15)
b+=text(1010,63,"step 1",14,italic=True,anchor="end",fill="#444")+text(1010,263,"step 3",14,italic=True,anchor="end",fill="#444")
b+=text(1010,163,"step 2",14,italic=True,anchor="end",fill="#444")+text(1010,363,"step 4: the row",14,italic=True,anchor="end",fill="#444")
b+=text(520,425,"A few steps find one row among millions. Each step reads one small block.",15,italic=True)
svg('07-btree.svg',445,b)

# 2 LSM
b=text(40,80,"write",16,bold=True)+arrow(66,75,106,75)+box(110,40,240,70,"Table in memory","kept sorted",fill=G)
b+=arrow(230,110,230,206)+text(245,160,"when full: written out as one sorted file",14,italic=True,anchor="start",fill="#444")
for i,(x,t,s2) in enumerate([(150,"File 3","newest"),(330,"File 2",""),(510,"File 1","oldest")]):
    b+=box(x,210,160,70,t,s2 if s2 else None)
b+=arrow(670,245,786,245)+text(728,232,"merge",14,italic=True,fill="#444")
b+=box(790,210,220,70,"One bigger file","old versions dropped")
b+=text(410,320,"a read checks memory first, then files from newest to oldest",14,italic=True,fill="#444")
b+=text(520,375,"Writes only ever add. The tidying up happens later, in the background.",15,italic=True)
svg('07-lsm.svg',395,b)

# 3 replication
b=box(30,60,200,76,"App","writes")+arrow(230,98,396,98)
b+=box(400,60,240,76,"Primary","zone A",fill=G)+arrow(640,98,756,98)+box(760,60,250,76,"Standby","zone B, takes over on failure")
b+=text(698,86,"copy first,",13,italic=True,fill="#444")+text(698,124,"then confirm",13,italic=True,fill="#444")
b+=box(290,260,230,76,"Read replica 1")+box(600,260,230,76,"Read replica 2")
b+=arrow(480,136,410,256,dash=True)+arrow(560,136,700,256,dash=True)
b+=text(770,200,"copied a moment later",14,italic=True,anchor="start",fill="#444")
b+=box(30,260,170,76,"App","reads")+arrow(200,298,286,298)
b+=text(520,385,"One place accepts writes. Copies give safety (standby) and read capacity (replicas).",15,italic=True)
svg('07-replication.svg',405,b)

# 4 partitioning
b=box(20,160,250,84,"Lookup","segment 4471, last 5 minutes")+arrow(270,202,316,202)+box(320,160,190,84,"hash(segment_id)","picks one partition",fill=G)
rows=[("Partition 1","segments 1203, 7730, ...",W),("Partition 2","segment 4471:  08:10  08:11  08:12  08:13  08:14",G),("Partition 3","segments 9002, 3318, ...",W)]
for i,(t,s,f) in enumerate(rows):
    y=40+i*122
    b+=arrow(510,202,576,y+42,dash=(i!=1))+box(580,y,440,84,t,s,fill=f)
b+=text(520,415,"One lookup goes to one partition. A road's minutes sit together, in time order.",15,italic=True)
svg('07-partitioning.svg',435,b)

# 5 lost update
b=text(40,105,"Server A",17,bold=True,anchor="start")+text(40,225,"Server B",17,bold=True,anchor="start")
b+=box(190,70,170,60,"reads 7",ts=17)+box(590,70,170,60,"writes 8",ts=17,fill=G)
b+=box(390,190,170,60,"reads 7",ts=17)+box(790,190,170,60,"writes 8",ts=17,fill=G)
b+=arrow(150,300,1000,300)+text(575,330,"time",14,italic=True,fill="#444")
for x,v in [(275,"7"),(475,"7"),(675,"8"),(875,"8")]:
    b+=f'<line x1="{x}" y1="{135 if x in (275,675) else 255}" x2="{x}" y2="296" stroke="#222" stroke-width="1" stroke-dasharray="4 5"/>'
    b+=text(x,288,"",1)
b+=text(40,293,"counter:",15,anchor="start")
for x,v in [(275,"7"),(475,"7"),(675,"8"),(875,"8")]: b+=text(x+14,285,v,18,bold=True,anchor="start")
b+=text(520,375,"Two drivers reported a jam. The counter went from 7 to 8, not 9.",15,italic=True)
svg('07-lost-update.svg',395,b)
