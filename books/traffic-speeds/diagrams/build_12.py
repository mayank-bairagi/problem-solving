from _draw import *
W,G="#fff",GREY
def rect(x,y,w,h,fill=W,dash=False):
    d=' stroke-dasharray="7 5"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#222" stroke-width="2"{d}/>'
# 1 runtime
b=box(30,30,170,76,"Client","submits the job")+arrow(200,68,376,68)
b+=box(380,30,280,76,"JobManager","schedules, coordinates checkpoints",fill=G)
for i,x in enumerate([40,370,700]):
    b+=rect(x,190,300,130)+text(x+150,212,f"TaskManager {i+1}",16,bold=True)
    b+=box(x+14,226,130,80,"Slot","read, key",ts=15)+box(x+156,226,130,80,"Slot","window, write",ts=15)
    b+=arrow(520,106,x+150,186)
b+=f'<rect x="40" y="370" width="960" height="50" fill="{G}" stroke="#222" stroke-width="2"/>'+text(520,401,"Durable storage (S3): checkpoints and savepoints",17,bold=True)
for x in [190,520,850]: b+=arrow(x,320,x,366,dash=True)
b+=text(520,455,"The JobManager directs. TaskManagers do the work in slots and hold the state.",15,italic=True)
svg('12-runtime.svg',475,b)

# 2 key groups
b=box(30,40,200,70,"key: segment 4471")+arrow(230,75,286,75)+box(290,40,230,70,"hash, then mod 8","8 = max parallelism",fill=G)+arrow(520,75,576,75)+box(580,40,200,70,"key group 5")
def row(y,label,groups):
    s=text(30,y+32,label,16,bold=True,anchor="start")
    s+=cells(240,y,[str(i) for i in range(8)],90,50,[G if i==5 else W for i in range(8)],16)
    for (a,bn,name) in groups:
        x1=240+a*90+4; x2=240+(bn+1)*90-4
        s+=f'<path d="M{x1},{y+60} L{x1},{y+70} L{x2},{y+70} L{x2},{y+60}" fill="none" stroke="#222" stroke-width="2"/>'
        s+=text((x1+x2)/2,y+90,name,14)
    return s
b+=row(150,"Parallelism 2",[(0,3,"subtask 0"),(4,7,"subtask 1")])
b+=row(280,"Parallelism 4",[(0,1,"subtask 0"),(2,3,"subtask 1"),(4,5,"subtask 2"),(6,7,"subtask 3")])
b+=text(520,420,"Rescaling moves whole key groups. A key's group never changes, so its state can follow it.",15,italic=True)
svg('12-key-groups.svg',440,b)

# 3 barriers
b=text(30,95,"Input A",17,bold=True,anchor="start")+text(30,205,"Input B",17,bold=True,anchor="start")
b+=cells(130,65,["a9","a8","a7"],80,50,[W,W,W],16)+text(250,140,"barrier already arrived: these wait",14,italic=True,fill="#444")
b+=cells(130,175,["b6","barrier","b5","b4"],80,50,[W,G,W,W],15)+text(290,250,"records before the barrier are still processed",14,italic=True,fill="#444")
b+=arrow(370,90,566,140)+arrow(450,200,566,170)
b+=box(570,110,280,90,"Operator","saves state once both barriers are in",ts=17)
b+=arrow(850,155,876,155)+box(880,120,145,70,"next","barrier forwarded",ts=15)
b+=arrow(710,200,710,286)+box(590,290,240,60,"Checkpoint storage",fill=G,ts=16)
b+=text(520,395,"Waiting for the barrier on every input means the saved state reflects exactly the records before it.",15,italic=True)
svg('12-barriers.svg',415,b)

# 4 watermark min
ws=[("Partition 0","watermark 08:15:00",W),("Partition 1","watermark 08:14:40",W),("Partition 2","08:02:00, silent for 12 min",G)]
b=''
for i,(t,s,f) in enumerate(ws):
    y=40+i*100
    b+=box(40,y,300,76,t,s,fill=f)+arrow(340,y+38,476,178)
b+=box(480,130,230,96,"Operator","takes the lowest")
b+=arrow(710,160,776,110)+arrow(710,196,776,246,dash=True)
b+=box(780,60,240,90,"08:02:00","windows cannot close",ts=18)
b+=box(780,210,240,90,"08:14:40","if partition 2 is marked idle",ts=18,dash=True)
b+=text(520,375,"An operator's watermark is the minimum of its inputs. One silent input holds everything back.",15,italic=True)
svg('12-watermark-min.svg',395,b)

# 5 2pc
steps=[("1. Write","into an open transaction",W),("2. Barrier arrives","flush, keep it open",W),("3. Checkpoint done","every operator has saved",G),("4. Commit","output becomes visible",W)]
b=''
for i,(t,s,f) in enumerate(steps):
    x=20+i*258
    b+=box(x,60,226,84,t,s,fill=f,ts=17)
    if i<3: b+=arrow(x+226,102,x+254,102)
b+=f'<path d="M20,170 L20,182 L504,182 L504,170" fill="none" stroke="#222" stroke-width="2"/>'+text(262,206,"crash here: abort the transaction, replay from the last checkpoint",14,italic=True)
b+=f'<path d="M536,170 L536,182 L1020,182 L1020,170" fill="none" stroke="#222" stroke-width="2"/>'+text(778,206,"crash here: on restart, finish the commit",14,italic=True)
b+=text(520,270,"Output is committed only once the checkpoint that covers it is safely stored.",15,italic=True)
svg('12-two-phase.svg',290,b)
