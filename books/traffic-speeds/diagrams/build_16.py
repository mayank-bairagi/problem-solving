from _draw import *
W,G="#fff",GREY
def rect(x,y,w,h,fill=W,dash=False,rx=8):
    d=' stroke-dasharray="7 5"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="#222" stroke-width="2"{d}/>'
def both(x1,y1,x2,y2):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="2" marker-end="url(#a)" marker-start="url(#a)"/>'
# 1 architecture
b=box(30,40,220,76,"DAG files","Python, kept in git",ts=17)+arrow(250,78,326,78)
b+=box(330,40,240,76,"DAG processor","parses the files",ts=17)+arrow(570,90,676,170)
b+=box(680,150,320,96,"Metadata database","DAGs, runs, task states",fill=G)
b+=box(330,170,240,76,"Scheduler","decides what runs next",fill=G,ts=17)+both(574,208,676,208)
b+=arrow(450,246,450,296)+box(330,300,240,76,"Executor","hands tasks to workers",ts=17)
b+=arrow(330,338,254,338)+box(30,300,220,76,"Workers","run the tasks",ts=17)
b+=box(680,300,320,76,"API server and web UI","people look, trigger, re-run",ts=17)+both(840,296,840,250)
b+=text(140,400,"report state back",13,italic=True,fill="#444")
b+=text(520,440,"Everything Airflow knows is in the database. The scheduler reads it and writes it in a loop.",15,italic=True)
svg('16-architecture.svg',460,b)

# 2 states
names=["scheduled","queued","running","success"]
b=''
for i,n in enumerate(names):
    x=30+i*250
    b+=box(x,50,220,64,n,fill=G if n=="success" else W,ts=18)
    if i<3: b+=arrow(x+220,82,x+246,82)
b+=text(140,36,"dependencies met",13,italic=True,fill="#444")+text(390,36,"waiting for a worker",13,italic=True,fill="#444")
b+=box(280,200,220,64,"up for retry","wait, then try again",ts=17)+box(780,200,220,64,"failed","no retries left",ts=17)
b+=arrow(600,114,430,196)+arrow(690,114,850,196)+arrow(280,232,140,118,dash=True)
b+=text(520,315,"Never started:  upstream failed (a parent failed)  ·  skipped (a branch not taken)",15)
b+=text(520,365,"A task instance moves through these states. Each change is a row update in the database.",15,italic=True)
svg('16-states.svg',385,b)

# 3 data interval
b=f'<line x1="60" y1="170" x2="1000" y2="170" stroke="#222" stroke-width="2" marker-end="url(#a)"/>'
for x,l in [(160,"12 Nov 00:00"),(520,"13 Nov 00:00"),(880,"14 Nov 00:00")]:
    b+=f'<line x1="{x}" y1="158" x2="{x}" y2="182" stroke="#222" stroke-width="2"/>'+text(x,206,l,14)
b+=bar(160,110,360,48,G)+text(340,140,"data interval: all of 12 Nov",16,bold=True)
b+=bar(520,110,360,48,W)+text(700,140,"next interval: 13 Nov",15,fill="#444")
b+=text(160,236,"logical date of the run",14,bold=True)
b+=arrow(520,300,520,216)+text(520,324,"the run for 12 Nov starts here,",15,bold=True)+text(520,346,"once its interval is over",15,bold=True)
b+=text(520,400,"A run is named after the start of the period it covers, and starts when that period ends.",15,italic=True)
svg('16-data-interval.svg',420,b)

# 4 backfill
days=["7 Nov","8 Nov","9 Nov","10 Nov","11 Nov","12 Nov","13 Nov","14 Nov"]
b=text(520,36,"Partitions of daily_totals, one per day",17,bold=True)
b+=cells(60,170,days,115,64,[W,W,W,G,G,G,W,W],16)
b+=box(330,50,380,64,"Backfill 10 to 12 Nov","one run per day, each with its own dates",ts=16)
for i in (3,4,5): b+=arrow(520,114,60+i*115+57,166)
b+=text(520,270,"each run replaces only its own day",15,bold=True)
b+=text(520,325,"Because a run overwrites one partition and nothing else, re-running is safe, in any order.",15,italic=True)
svg('16-backfill.svg',345,b)

# 5 sensors
b=text(30,86,"Sensor",17,bold=True,anchor="start")+text(30,108,"(poke mode)",14,anchor="start",fill="#444")
b+=bar(190,60,800,56,G)+text(590,94,"occupies a worker slot for the whole wait",16,bold=True)
b+=text(30,216,"Deferrable",17,bold=True,anchor="start")+text(30,238,"operator",14,anchor="start",fill="#444")
b+=bar(190,190,80,56,G)+text(230,224,"start",14,bold=True)
b+=f'<rect x="270" y="190" width="640" height="56" fill="#fff" stroke="#222" stroke-width="2" stroke-dasharray="7 5"/>'+text(590,224,"no worker: the triggerer watches",16)
b+=bar(910,190,80,56,G)+text(950,224,"finish",14,bold=True)
b+=f'<line x1="190" y1="290" x2="990" y2="290" stroke="#222" stroke-width="2" marker-end="url(#a)"/>'+text(590,316,"time spent waiting for the data to arrive",14,italic=True,fill="#444")
b+=text(520,370,"Waiting is not work. A deferred task frees its worker until the event arrives.",15,italic=True)
svg('16-sensors.svg',390,b)
