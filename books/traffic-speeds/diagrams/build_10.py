from _draw import *
W,G="#fff",GREY
def line(x1,y1,x2,y2,dash=False,w=2):
    d=' stroke-dasharray="6 5"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="{w}"{d}/>'
# 1 anatomy
b=text(30,36,"Topic: pings",18,bold=True,anchor="start")
for i in range(3):
    y=54+i*48
    b+=text(30,y+24,f"Partition {i}",15,anchor="start",bold=(i==0))+cells(160,y,[str(n) for n in range(8)],60,36,[G]*8 if i==0 else None,15)
    b+=text(660,y+24,f"leader: broker {i+1}, copies on the other two",14,anchor="start",fill="#444")
b+=arrow(130,95,130,236)+text(145,222,"partition 0 on broker 1's disk",14,italic=True,anchor="start",fill="#444")
for i,(t,s,f) in enumerate([("Segment 0","closed: .log .index .timeindex",W),("Segment 350000","closed",W),("Segment 700000","active: appends go here",G)]):
    b+=box(40+i*330,240,300,84,t,s,fill=f,ts=17)
b+=text(190,350,"deleted whole when retention passes",13,italic=True,fill="#444")
b+=text(520,400,"A partition is a directory of segment files. Only the last one is written to.",15,italic=True)
svg('10-anatomy.svg',420,b)

# 2 high watermark
rows=[("Leader",8),("Follower A",7),("Follower B",6)]
b=''
for i,(n,k) in enumerate(rows):
    y=70+i*80
    b+=text(30,y+33,n,17,bold=True,anchor="start")
    b+=cells(200,y,[str(j) for j in range(k)],70,52,[G if j<6 else W for j in range(k)],16)
    b+=text(200+k*70+16,y+33,f"log end: {k}",14,anchor="start",fill="#444")
b+=line(620,40,620,310,dash=True)+text(620,30,"high watermark = 6",16,bold=True)
b+=text(410,340,"grey: on every in-sync replica, so consumers may read it",14,italic=True,fill="#444")
b+=text(520,385,"The high watermark is the lowest log end among in-sync replicas. Offsets 6 and 7 are not yet safe.",15,italic=True)
svg('10-high-watermark.svg',405,b)

# 3 rebalance
b=text(250,36,"Eager (old default)",19,bold=True)+text(790,36,"Cooperative",19,bold=True)
b+=line(520,20,520,330,dash=True,w=1)
def grp(x0,spec):
    s=''
    for i,(name,ps) in enumerate(spec):
        y=70+i*80
        s+=text(x0,y+30,name,16,bold=True,anchor="start")
        if ps: s+=cells(x0+60,y,[p for p,_ in ps],80,46,[f for _,f in ps],15)
        else: s+=text(x0+60,y+30,"(new, waiting)",14,italic=True,anchor="start",fill="#444")
    return s
b+=grp(40,[("C1",[("P0",G),("P1",G),("P2",G)]),("C2",[("P3",G),("P4",G),("P5",G)]),("C3",None)])
b+=grp(570,[("C1",[("P0",W),("P1",W),("P2",G)]),("C2",[("P3",W),("P4",W),("P5",G)]),("C3",None)])
b+=text(250,315,"everyone gives up everything, then all is reassigned",14,italic=True,fill="#444")
b+=text(790,315,"only P2 and P5 are handed to C3",14,italic=True,fill="#444")
b+=text(520,375,"C3 joins the group. Grey = partitions not being processed during the rebalance.",15,italic=True)
svg('10-rebalance.svg',395,b)

# 4 transaction
b=box(30,150,190,84,"Input topic","pings")+arrow(220,192,296,192)
b+=box(300,150,210,84,"Your app","begin ... commit",fill=G)
b+=f'<rect x="580" y="50" width="270" height="290" rx="10" fill="none" stroke="#222" stroke-width="2" stroke-dasharray="7 5"/>'
b+=text(715,40,"one transaction: both or neither",15,bold=True)
b+=box(600,75,230,84,"Output topic","results",ts=17)+box(600,225,230,84,"Offsets topic","new input position",ts=17)
b+=arrow(510,175,596,125)+arrow(510,210,596,260)
b+=box(890,75,130,84,"Reader","read_committed",ts=16)+arrow(830,117,886,117)
b+=text(955,185,"sees results only",13,italic=True,fill="#444")+text(955,203,"after the commit",13,italic=True,fill="#444")
b+=text(520,385,"Read, process, write: the output and the new read position are committed as one unit.",15,italic=True)
svg('10-transaction.svg',405,b)

# 5 compaction
b=text(30,82,"Before",17,bold=True,anchor="start")+text(30,222,"After",17,bold=True,anchor="start")
before=["A=1","B=1","A=2","C=1","B=2","A=3","C=del"]
b+=cells(130,50,before,115,56,[W,W,W,W,G,G,G],17)
for i in range(7): b+=text(130+i*115+57,126,f"offset {i}",13,fill="#444")
b+=cells(130+4*115,190,["B=2","A=3","C=del"],115,56,[G,G,G],17)
for i in range(4,7): b+=text(130+i*115+57,266,f"offset {i}",13,fill="#444")
b+=text(360,224,"older values removed; offsets keep their numbers",14,italic=True,fill="#444")
b+=text(520,330,"Compaction keeps the latest value for each key. \"C=del\" is a tombstone: kept a while, then dropped.",15,italic=True)
svg('10-compaction.svg',350,b)
