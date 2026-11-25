from _draw import *
W,G="#fff",GREY
def rect(x,y,w,h,fill=W,dash=False):
    d=' stroke-dasharray="7 5"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#222" stroke-width="2"{d}/>'
# 1 parquet file
b=rect(60,30,560,400)
b+=text(340,52,"PAR1  (start marker)",13,fill="#444")
for i,y in enumerate([64,186]):
    b+=rect(80,y,520,110)+text(92,y+20,f"Row group {i+1}  (about 128 MB of rows)",14,bold=True,anchor="start")
    for j,n in enumerate(["segment_id","speed_kmh","event_time"]):
        b+=box(96+j*166,y+30,154,66,n,"pages, compressed",ts=15)
b+=rect(80,308,520,96,G)+text(340,332,"Footer",17,bold=True)
b+=text(340,356,"schema; for each row group and column:",14)+text(340,378,"min, max, null count, where it starts",14)
b+=text(340,422,"PAR1  (end marker)",13,fill="#444")
b+=arrow(760,356,606,356)+text(770,350,"a reader starts here,",15,bold=True,anchor="start")+text(770,372,"then fetches only the",15,bold=True,anchor="start")+text(770,394,"chunks it needs",15,bold=True,anchor="start")
b+=text(770,100,"one column chunk =",14,anchor="start",fill="#444")+text(770,120,"one column's values",14,anchor="start",fill="#444")+text(770,140,"for one row group",14,anchor="start",fill="#444")
b+=text(520,465,"The footer lets a reader skip whole row groups and columns without touching them.",15,italic=True)
svg('11-parquet-file.svg',485,b)

# 2 metadata levels
lv=[("Catalog","table name -> current metadata file","",G),
    ("Metadata file (.json)","schema, partition spec, list of snapshots","",W),
    ("Manifest list (one per snapshot)","one row per manifest + range of partition values","prune 1: skip manifests for other days",W),
    ("Manifest (.avro)","one row per data file + min/max of each column","prune 2: skip files that cannot hold segment 4471",W),
    ("Data files (.parquet)","the pings","prune 3: skip row groups and columns (footer)",G)]
b=''
for i,(t,s,n,f) in enumerate(lv):
    y=30+i*88
    b+=box(40,y,480,66,t,s,fill=f,ts=16)
    if i<4: b+=arrow(280,y+66,280,y+84)
    if n: b+=text(545,y+38,n,14,italic=True,anchor="start")
b+=text(520,490,"Query planning walks down this tree and discards most of it using metadata alone.",15,italic=True)
svg('11-metadata-levels.svg',510,b)

# 3 conflict
b=text(30,95,"Writer A",17,bold=True,anchor="start")+text(30,215,"Writer B",17,bold=True,anchor="start")
b+=box(150,60,170,66,"reads table","at snapshot 41",ts=16)+box(360,60,200,66,"swap 41 -> 42","succeeds",ts=16,fill=G)
b+=box(150,180,170,66,"reads table","at snapshot 41",ts=16)+box(590,180,180,66,"swap 41 -> 43","fails: now 42",ts=16,dash=True)
b+=box(800,180,210,66,"refresh, re-check","swap 42 -> 43: succeeds",ts=16,fill=G)
b+=arrow(320,93,356,93)+arrow(320,213,586,213)+arrow(770,213,796,213)
b+=arrow(130,300,1010,300)+text(570,328,"time",14,italic=True,fill="#444")
b+=text(520,375,"The loser does not redo its data files. It re-checks for a real conflict and commits on top.",15,italic=True)
svg('11-conflict.svg',395,b)

# 4 deletes
b=text(250,36,"Position delete",19,bold=True)+text(790,36,"Equality delete",19,bold=True)
b+=f'<line x1="520" y1="20" x2="520" y2="330" stroke="#222" stroke-width="1" stroke-dasharray="4 6"/>'
b+=text(60,80,"data file a.parquet",14,anchor="start",fill="#444")
b+=cells(60,90,["row 0","row 1","row 2","row 3","row 4"],80,50,[W,W,W,G,W],14)
b+=box(150,190,220,66,"Delete file","a.parquet, row 3",fill=G,ts=16)+arrow(340,190,340,144)
b+=text(250,290,"names the exact row: cheap to apply",14,italic=True)+text(250,312,"writer must first find the row",14,italic=True,fill="#444")
b+=box(600,80,170,56,"older file 1",ts=15)+box(600,150,170,56,"older file 2",ts=15)
b+=box(820,110,190,70,"Delete file","device_id = 81f3",fill=G,ts=16)+arrow(820,135,774,110)+arrow(820,155,774,176)
b+=text(790,290,"names a value: instant to write",14,italic=True)+text(790,312,"every reader must filter all older files",14,italic=True,fill="#444")
b+=text(520,365,"Position deletes move the cost to the writer. Equality deletes move it to every reader.",15,italic=True)
svg('11-deletes.svg',385,b)

# 5 maintenance
rows=[("Many small files, delete files","Compact","rewrite_data_files","Few large files, deletes applied"),
      ("Hundreds of old snapshots","Expire","expire_snapshots","Recent snapshots only; old files freed"),
      ("Files no snapshot points to","Clean","remove_orphan_files","Storage reclaimed")]
b=text(170,34,"Problem",17,bold=True)+text(520,34,"Job",17,bold=True)+text(860,34,"Result",17,bold=True)
for i,(p,j,proc,r) in enumerate(rows):
    y=50+i*92
    b+=box(20,y,300,70,p,ts=15)+arrow(320,y+35,396,y+35)+box(400,y,240,70,j,proc,fill=G,ts=17)+arrow(640,y+35,696,y+35)+box(700,y,320,70,r,ts=15)
b+=text(520,355,"An Iceberg table needs regular housekeeping. Each job is itself an ordinary commit.",15,italic=True)
svg('11-maintenance.svg',375,b)
