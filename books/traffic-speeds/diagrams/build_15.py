from _draw import *
W,G="#fff",GREY
def rect(x,y,w,h,fill=W,dash=False,rx=8):
    d=' stroke-dasharray="7 5"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="#222" stroke-width="2"{d}/>'
# 1 btree
b=box(380,30,280,64,"Root page","key ranges, pointers to child pages",ts=16)
for i,x in enumerate([60,400,740]):
    b+=box(x,140,240,60,"Inner page",ts=16,fill=G if i==1 else W)+arrow(520,94,x+120,136)
lv=["4301 - 4380","4381 - 4460","4461 - 4540","4541 - 4620"]
for i,l in enumerate(lv):
    x=30+i*250
    b+=box(x,250,220,64,"Leaf page",l,ts=15,fill=G if i==2 else W)
    if i<3: b+=f'<line x1="{x+222}" y1="282" x2="{x+248}" y2="282" stroke="#222" stroke-width="2" marker-end="url(#a)" marker-start="url(#a)"/>'
b+=arrow(480,200,180,246,dash=True)+arrow(520,200,400,246,dash=True)+arrow(560,200,640,246)+arrow(600,200,880,246,dash=True)
b+=box(480,380,320,70,"Table page (heap)","the full row for segment 4471",fill=G,ts=16)+arrow(640,314,640,376)
b+=text(660,350,"entry holds the row's address",13,italic=True,anchor="start",fill="#444")
b+=text(520,495,"Three or four page reads find one row among millions. Leaves are linked, so ranges are cheap.",15,italic=True)
svg('15-btree.svg',515,b)

# 2 mvcc
b=text(520,34,"Row for segment 4471: three versions on disk",17,bold=True)
b+=cells(60,56,["created by txn","ended by txn","jam_reports"],180,44,[G,G,G],15)
rows=[["100","105","6"],["105","110","7"],["110","-","8"]]
for i,r in enumerate(rows):
    b+=cells(60,100+i*56,r,180,56,[W,W,W],17)
b+=arrow(696,128,604,128)+text(704,123,"no running transaction can see it:",14,anchor="start")+text(704,143,"dead, vacuum may remove it",14,anchor="start",fill="#444")
b+=arrow(696,184,604,184)+text(704,179,"transaction 107 started before 110",14,bold=True,anchor="start")+text(704,199,"committed: it still reads this one",14,anchor="start",fill="#444")
b+=arrow(696,240,604,240)+text(704,235,"new transactions read this one",14,anchor="start")
b+=text(520,315,"An update writes a new version. Readers keep their snapshot, so readers and writers do not block.",15,italic=True)
svg('15-mvcc.svg',335,b)

# 3 replication
b=box(30,150,170,84,"App servers","many connections",ts=16)+arrow(200,192,246,192)
b+=box(250,150,180,84,"Connection pool","few real connections",fill=G,ts=16)+arrow(430,192,476,192)
b+=box(480,150,200,84,"Primary","zone A: all writes",ts=17)
b+=box(780,40,230,84,"Standby","zone B: takes over on failure",ts=17)
b+=box(780,260,230,84,"Read replica","serves reads, slightly behind",ts=17)
b+=arrow(680,170,776,100)+arrow(680,214,776,284,dash=True)
b+=text(700,112,"synchronous",14,bold=True,anchor="end")+text(700,290,"asynchronous",14,bold=True,anchor="end")
b+=text(700,130,"commit waits for it",12,italic=True,anchor="end",fill="#444")+text(700,308,"commit does not wait",12,italic=True,anchor="end",fill="#444")
b+=text(520,395,"The standby is for surviving a failure. Read replicas are for spreading read load.",15,italic=True)
svg('15-replication.svg',415,b)

# 4 dynamo keys
b=box(30,160,230,84,"Item","segment 4471, minute 08:14",ts=17)+arrow(260,202,316,202)
b+=box(320,160,180,84,"Hash","of the partition key",fill=G,ts=17)
ps=[("Partition 1","segment 1207: 08:13, 08:14"),("Partition 2","segment 4471: 08:12, 08:13, 08:14"),("Partition 3","segment 9020: 08:14")]
for i,(t,s) in enumerate(ps):
    y=40+i*120
    b+=box(600,y,410,84,t,s,fill=G if i==1 else W,ts=17)
    b+=arrow(500,202,596,y+42,dash=(i!=1))
b+=text(805,395,"inside a partition, items are kept sorted by sort key",14,italic=True,fill="#444")
b+=text(520,440,"The partition key decides where an item lives. The sort key decides its order there.",15,italic=True)
svg('15-dynamo-keys.svg',460,b)

# 5 gsi
b=rect(30,50,420,190)+text(240,76,"Table: jam_reports",17,bold=True)+text(240,98,"key: report_id",14,fill="#444")
b+=cells(50,112,["r-81","seg 4471","08:14"],127,36,[G,W,W],14)+cells(50,148,["r-82","seg 9020","08:14"],127,36,[G,W,W],14)+cells(50,184,["r-83","seg 4471","08:15"],127,36,[G,W,W],14)
b+=rect(590,50,420,190)+text(800,76,"Index: by_segment",17,bold=True)+text(800,98,"key: segment_id + reported_at",14,fill="#444")
b+=cells(610,112,["seg 4471","08:14","r-81"],127,36,[G,G,W],14)+cells(610,148,["seg 4471","08:15","r-83"],127,36,[G,G,W],14)+cells(610,184,["seg 9020","08:14","r-82"],127,36,[G,G,W],14)
b+=arrow(450,145,586,145,dash=True)+text(518,128,"copied after",13,italic=True,fill="#444")+text(518,166,"the write",13,italic=True,fill="#444")
b+=text(240,270,"get one report by its id",14,italic=True,fill="#444")+text(800,270,"all reports for a road, newest first",14,italic=True,fill="#444")
b+=text(520,325,"A global secondary index is a second copy of the data under a different key, slightly behind.",15,italic=True)
svg('15-gsi.svg',345,b)
