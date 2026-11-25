from _draw import *
W,G="#fff",GREY
def rect(x,y,w,h,fill=W,dash=False,rx=8):
    d=' stroke-dasharray="7 5"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="#222" stroke-width="2"{d}/>'
# 1 architecture
b=box(30,40,260,90,"Driver","plans the job, schedules tasks",fill=G)
b+=box(400,50,220,70,"Cluster manager","YARN / Kubernetes",ts=16)
b+=f'<line x1="294" y1="85" x2="396" y2="85" stroke="#222" stroke-width="2" marker-end="url(#a)" marker-start="url(#a)"/>'
b+=text(345,75,"ask for executors",12,italic=True,fill="#444")
for i,x in enumerate([40,370,700]):
    b+=rect(x,220,300,120)+text(x+150,243,f"Executor {i+1}",16,bold=True)
    b+=box(x+14,256,84,68,"task",ts=14)+box(x+108,256,84,68,"task",ts=14)+box(x+202,256,84,68,"cache",ts=14,fill=G)
    b+=arrow(160,130,x+150,216)
b+=text(700,160,"tasks out, results and status back",14,italic=True,fill="#444")
b+=text(520,385,"One driver decides. Executors run tasks, keep cached data, and hold shuffle output.",15,italic=True)
svg('13-architecture.svg',405,b)

# 2 plan
st=[("Your query","SQL or DataFrame"),("Logical plan","what to compute"),("Optimised plan","filters pushed, columns cut"),("Physical plan","join type, shuffles"),("Generated code","one tight loop per stage")]
b=''
for i,(t,s) in enumerate(st):
    x=14+i*205
    b+=box(x,70,185,84,t,s,fill=G if i in (2,3) else W,ts=16)
    if i<4: b+=arrow(x+185,112,x+201,112)
b+=f'<path d="M219,170 L219,182 L814,182 L814,170" fill="none" stroke="#222" stroke-width="2"/>'+text(516,206,"Catalyst optimiser",15,bold=True)
b+=text(926,206,"Tungsten",15,bold=True)
b+=text(520,265,"Because Spark sees the whole query, it can rewrite it. A UDF is a black box it cannot see into.",15,italic=True)
svg('13-plan.svg',285,b)

# 3 shuffle
b=text(190,36,"Stage 1: map tasks",17,bold=True)+text(830,36,"Stage 2: reduce tasks",17,bold=True)
for i in range(3):
    y=60+i*100
    b+=box(30,y,130,64,f"Map {i+1}",ts=16)+arrow(160,y+32,196,y+32)
    b+=cells(200,y+6,["for R0","for R1","for R2"],100,52,[W,G,W],14)
    b+=arrow(504,y+32,746,192)
    b+=box(750,y,250,64,f"Reduce {i}","fetches its slice from every map" if i==1 else None,fill=G if i==1 else W,ts=16)
b+=text(350,375,"each map task writes one file, sorted by target reducer",14,italic=True,fill="#444")
b+=text(520,415,"Shuffle = write to local disk, fetch over the network, merge. It is the costly step.",15,italic=True)
svg('13-shuffle.svg',435,b)

# 4 AQE
b=text(30,82,"Planned",17,bold=True,anchor="start")+text(30,222,"After AQE",17,bold=True,anchor="start")
x=170; before=[(40,"5 MB"),(40,"8 MB"),(40,"3 MB"),(150,"70 MB"),(420,"900 MB"),(40,"6 MB")]
for w,l in before:
    b+=f'<rect x="{x}" y="55" width="{w}" height="50" fill="{G if w>400 else W}" stroke="#222" stroke-width="2"/>'
    b+=text(x+w/2,126,l,13,fill="#444"); x+=w+10
x=170; after=[(140,"22 MB (merged)",W),(150,"70 MB",W),(136,"300 MB",G),(136,"300 MB",G),(136,"300 MB",G),(40,"6 MB",W)]
for w,l,f in after:
    b+=f'<rect x="{x}" y="195" width="{w}" height="50" fill="{f}" stroke="#222" stroke-width="2"/>'
    b+=text(x+w/2,266,l,13,fill="#444"); x+=w+10
b+=text(520,325,"After a shuffle, Spark knows the real sizes. It merges tiny partitions and splits a skewed one.",15,italic=True)
svg('13-aqe.svg',345,b)

# 5 memory
b=rect(30,40,980,250,rx=0)+text(520,30,"Executor container (what the cluster manager grants)",15,bold=True)
b+=rect(50,70,170,200,W,rx=0)+text(135,160,"Overhead",17,bold=True)+text(135,184,"outside the JVM heap",13,fill="#444")+text(135,204,"native, network buffers",13,fill="#444")
b+=rect(240,70,750,200,W,dash=True,rx=0)+text(615,92,"JVM heap (spark.executor.memory)",14,bold=True)
b+=rect(260,110,480,140,G,rx=0)+text(500,132,"Unified region (about 60%)",15,bold=True)
b+=rect(275,150,200,84,W,rx=0)+text(375,186,"Execution",16,bold=True)+text(375,208,"shuffles, joins, sorts",13,fill="#444")
b+=rect(525,150,200,84,W,rx=0)+text(625,186,"Storage",16,bold=True)+text(625,208,"cached data",13,fill="#444")
b+=f'<line x1="479" y1="192" x2="521" y2="192" stroke="#222" stroke-width="2" marker-end="url(#a)" marker-start="url(#a)"/>'
b+=rect(760,110,210,140,W,rx=0)+text(865,172,"User memory",16,bold=True)+text(865,196,"your objects, UDF data",13,fill="#444")
b+=text(520,330,"Execution and storage borrow from each other. Execution spills to disk when it runs out.",15,italic=True)
svg('13-memory.svg',350,b)
