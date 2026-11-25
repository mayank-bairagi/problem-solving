from _draw import *
W,G="#fff",GREY
def line(x1,y1,x2,y2,dash=False,w=2):
    d=' stroke-dasharray="6 5"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="{w}"{d}/>'
# 1 silence
rows=[("The request was lost on the way","req"),("The other node crashed, or is very slow","dead"),("It did the work, but the reply was lost","reply")]
b=''
for i,(t,k) in enumerate(rows):
    y=40+i*115
    b+=box(40,y,150,70,"Sender")
    b+=box(470,y,170,70,"Receiver",fill=G if k=="dead" else W,dash=(k=="dead"))
    if k=="req":
        b+=arrow(190,y+25,320,y+25)+text(338,y+32,"X",20,bold=True)
    else:
        b+=arrow(190,y+25,466,y+25)
    if k=="reply":
        b+=arrow(470,y+50,342,y+50)+text(324,y+57,"X",20,bold=True)
    b+=text(680,y+41,t,15,anchor="start")
b+=text(520,400,"From the sender's side, all three look exactly the same: silence.",15,italic=True)
svg('08-silence.svg',420,b)

# 2 clocks
b=text(30,95,"Server A",17,bold=True,anchor="start")+text(30,115,"clock 2 s fast",13,anchor="start",fill="#444")
b+=text(30,215,"Server B",17,bold=True,anchor="start")+text(30,235,"clock correct",13,anchor="start",fill="#444")
b+=box(190,65,270,70,"writes: road CLOSED","stamped 10:00:02",ts=16)
b+=box(430,185,270,70,"writes: road OPEN","stamped 10:00:01",ts=16)
b+=arrow(150,310,760,310)+text(455,338,"real time",14,italic=True,fill="#444")
b+=line(325,135,325,310,dash=True,w=1)+line(565,255,565,310,dash=True,w=1)
b+=text(325,300,"",1)+text(335,300,"10:00:00",13,anchor="start",fill="#444")+text(575,300,"10:00:01",13,anchor="start",fill="#444")
b+=box(800,125,210,80,"Database keeps","CLOSED (highest stamp)",fill=G,ts=16)
b+=arrow(460,100,796,150)+arrow(700,220,796,180)
b+=text(520,385,"OPEN was written later, but lost, because the other server's clock was ahead.",15,italic=True)
svg('08-clocks.svg',405,b)

# 3 fencing
b=text(30,95,"Job A",17,bold=True,anchor="start")+text(30,205,"Job B",17,bold=True,anchor="start")+text(30,325,"Storage",17,bold=True,anchor="start")
b+=box(130,60,200,66,"gets the lease","token 33",ts=16)+bar(340,70,450,46)+text(565,99,"paused (frozen for 40 s, lease expires)",14,italic=True)
b+=box(810,60,200,66,"wakes up, writes","token 33",ts=16)
b+=box(380,170,200,66,"gets the lease","token 34",ts=16)+box(600,170,180,66,"writes","token 34",ts=16)
b+=arrow(690,236,690,286)+arrow(910,126,910,286)
b+=box(600,290,180,66,"accepted","34 is newest",ts=16)+box(800,290,220,66,"REJECTED","33 is older than 34",fill=G,ts=16)
b+=text(520,410,"The storage remembers the highest token it has seen and refuses anything older.",15,italic=True)
svg('08-fencing.svg',430,b)

# 4 quorum
b=f'<rect x="40" y="100" width="470" height="150" rx="10" fill="none" stroke="#222" stroke-width="2" stroke-dasharray="7 5"/>'
b+=f'<rect x="620" y="100" width="320" height="150" rx="10" fill="none" stroke="#222" stroke-width="2" stroke-dasharray="7 5"/>'
for i,x in enumerate([60,210,360]): b+=box(x,145,130,60,f"Node {i+1}","leader" if i==1 else None,fill=G if i==1 else W,ts=16)
for i,x in enumerate([640,790]): b+=box(x,145,130,60,f"Node {i+4}",ts=16)
b+=line(565,60,565,290,dash=True)+text(565,45,"network cut",15,bold=True)
b+=text(275,85,"3 of 5: a majority",16,bold=True)+text(780,85,"2 of 5: a minority",16,bold=True)
b+=text(275,280,"elects a leader and keeps working",15)+text(780,280,"refuses to decide anything",15)
b+=text(520,345,"Any two majorities share at least one node, so two leaders can never both be elected.",15,italic=True)
svg('08-quorum.svg',365,b)

# 5 consistency map
b=text(260,36,"Must have one right answer",18,bold=True)+text(780,36,"Close enough is fine",18,bold=True)
L=["Which snapshot is current","Who leads partition 0","Who holds the compaction lease","Was this jam report saved"]
R=["Live speed on a road","Typical speeds","Analyst query results","Dashboards and metrics"]
for i,(l,r) in enumerate(zip(L,R)):
    y=56+i*64
    b+=box(40,y,440,50,l,fill=G,ts=16)+box(560,y,440,50,r,ts=16)
b+=text(260,335,"cost: slower, and may refuse during a network cut",14,italic=True,fill="#444")
b+=text(780,335,"cheap, fast, always answers, briefly stale",14,italic=True,fill="#444")
b+=text(520,380,"Pay for strong guarantees only where a wrong answer does damage.",15,italic=True)
svg('08-consistency-map.svg',400,b)
