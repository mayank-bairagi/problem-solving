from _draw import *
W,G="#fff",GREY
def line(x1,y1,x2,y2,dash=False,w=2):
    d=' stroke-dasharray="6 5"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="{w}"{d}/>'
def dot(x,y,r=7,fill="#222"):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="#222" stroke-width="2.5"/>'

# 1 pipeline
ys=[70,180,290]
b=text(105,40,"Kafka",17,bold=True)+text(325,40,"Read",17,bold=True)+text(710,40,"Window + average",17,bold=True)+text(955,40,"Write",17,bold=True)
for i,y in enumerate(ys):
    b+=box(30,y,150,70,f"Partition {i}","by device",fill=G)+arrow(180,y+35,246,y+35)+box(250,y,150,70,f"Reader {i}")
    b+=box(600,y,220,70,f"Worker {i}",["segments 4471, ...","segments 9002, ...","segments 1203, ..."][i])
    for y2 in ys: b+=arrow(400,y+35,596,y2+35)
    b+=arrow(820,y+35,886,215 if i!=1 else 215)
b+=box(890,180,130,70,"Serving DB")
b+=text(500,395,"key by segment_id",16,bold=True)
b+=text(520,430,"Whichever partition a ping came from, all pings for one road reach the same worker.",15,italic=True)
svg('04-pipeline.svg',450,b)

# 2 windows
X0,M=200,130
b=''
for i in range(7):
    x=X0+i*M; b+=line(x,50,x,330,dash=True,w=1)+text(x,355,f"08:1{i}",14,fill="#444")
b+=text(20,95,"Tumbling",17,bold=True,anchor="start")+text(20,115,"back to back",13,anchor="start",fill="#444")
for i in range(6): b+=bar(X0+i*M,72,M,36,G if i%2==0 else W)
b+=text(20,180,"Sliding",17,bold=True,anchor="start")+text(20,200,"3 min long,",13,anchor="start",fill="#444")+text(20,216,"new one each min",13,anchor="start",fill="#444")
for i in range(4): b+=bar(X0+i*M,150+i*20,3*M,14,G)
b+=text(20,280,"Session",17,bold=True,anchor="start")+text(20,300,"ends after a quiet gap",13,anchor="start",fill="#444")
for s,e in [(0.2,1.6),(2.8,3.4),(4.5,5.9)]: b+=bar(X0+s*M,262,(e-s)*M,36,G)
b+=text(X0+2.2*M,285,"gap",13,italic=True,fill="#444")+text(X0+3.65*M,285,"gap",13,italic=True,fill="#444")
b+=text(520,392,"Three ways to cut an endless stream into pieces you can finish.",15,italic=True)
svg('04-windows.svg',410,b)

# 3 two clocks
b=line(140,360,140,40)+line(140,360,960,360)
for i in range(5):
    x=140+190*i; y=340-70*i
    b+=line(x,360,x,368)+text(x,388,f"08:1{3+i}",14,fill="#444")
    b+=line(132,y,140,y)+text(124,y+5,f"08:1{3+i}",14,anchor="end",fill="#444")
b+=line(140,340,900,60,dash=True,w=1.5)
for t,d in [(0.2,.06),(0.6,.09),(1.1,.06),(1.6,.1),(2.0,.07),(2.6,.08),(3.1,.06),(3.6,.09)]:
    b+=dot(140+190*t,340-70*(t+d))
lx,ly=140+190*1.0,340-70*4.0
b+=line(lx,ly,lx,340-70*1.0,dash=True,w=1.5)+dot(lx,ly,9,W)
b+=text(lx+18,ly-8,"tunnel: happened at 08:14, arrived at 08:17",15,bold=True,anchor="start")
b+=text(lx+12,180,"3 minutes late",14,italic=True,anchor="start",fill="#444")
b+=text(760,150,"arrives instantly",13,italic=True,fill="#444")
b+=text(550,418,"event time: when the car was on the road",16)
b+=f'<text x="50" y="200" text-anchor="middle" font-size="16" fill="#111" transform="rotate(-90 50 200)">arrival time</text>'
svg('04-two-clocks.svg',435,b)

# 4 watermark
b=line(80,300,980,300)
for i,l in enumerate(["08:14:00","08:14:30","08:15:00","08:15:30","08:16:00"]):
    x=120+200*i; b+=line(x,300,x,308)+text(x,328,l,14,fill="#444")
b+=bar(120,190,400,50,G)+text(320,221,"window 08:14 to 08:15",16,bold=True)
b+=line(520,70,520,300,dash=True)+line(720,70,720,300,dash=True)
b+=text(520,40,"watermark",17,bold=True)+text(520,60,"\"nothing older is coming\"",14,fill="#444")
b+=text(720,40,"newest ping seen",17,bold=True)+text(720,60,"08:15:30",14,fill="#444")
b+=f'<line x1="528" y1="120" x2="712" y2="120" stroke="#222" stroke-width="2" marker-end="url(#a)" marker-start="url(#a)"/>'+text(620,110,"wait 30 s",15,bold=True)
b+=text(540,160,"window closes here:",14,anchor="start",italic=True)+text(540,178,"result is published",14,anchor="start",italic=True)
b+=dot(387,268,8,W)+text(372,273,"a ping for 08:14:40 arriving now is late",14,anchor="end",italic=True)
b+=text(520,375,"The watermark trails the newest ping by a fixed wait. A window closes when the watermark passes its end.",15,italic=True)
svg('04-watermark.svg',395,b)

# 5 checkpoint
b=bar(80,170,880,44,W)+bar(380,170,380,44,G)
b+=text(230,198,"already counted",14,fill="#444")+text(570,198,"read again after restart",14,bold=True)+text(860,198,"not yet read",14,fill="#444")
b+=box(240,40,280,74,"Checkpoint","position 1000 + all sums and counts")+arrow(380,114,380,166)
b+=text(760,120,"CRASH",19,bold=True)+text(760,142,"at position 1500",14,fill="#444")+arrow(760,148,760,166)
b+=text(380,236,"1000",14,fill="#444")+text(760,236,"1500",14,fill="#444")
b+=f'<path d="M760,250 C760,310 380,310 380,254" fill="none" stroke="#222" stroke-width="2" marker-end="url(#a)"/>'
b+=text(570,330,"restart: load the checkpoint, go back to 1000",15,bold=True)
b+=text(520,385,"Position and state are saved together, so after a restart they always match.",15,italic=True)
svg('04-checkpoint.svg',405,b)
