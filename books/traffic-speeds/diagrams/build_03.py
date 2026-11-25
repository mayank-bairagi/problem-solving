from _draw import *
W,G="#fff",GREY
# 1 row vs column
rows=[["A","4471","38","08:14"],["B","4471","41","08:14"],["C","9002","72","08:14"],["D","4471","35","08:15"]]
b=text(200,40,"Row layout",19,bold=True)+text(200,62,"one ping after another",14,fill="#444")
for i,r in enumerate(rows): b+=cells(30,90+i*48,r,85,48,[W,W,G,W],16)
b+=text(735,40,"Column layout",19,bold=True)+text(735,62,"one field after another",14,fill="#444")
names=["device","segment","speed","time"]
for i,n in enumerate(names):
    b+=text(640,90+i*48+30,n,15,anchor="end",bold=(n=="speed"))
    b+=cells(650,90+i*48,[r[i] for r in rows],85,48,[G]*4 if n=="speed" else None,16)
b+=text(200,315,"speed is scattered:",15)+text(200,337,"read everything to find it",15)
b+=text(820,315,"speed is one strip:",15)+text(820,337,"read only that",15)
b+=text(520,395,"Question: \"what is the average speed?\"  Grey = the bytes that question needs.",15,italic=True)
svg('03-row-vs-column.svg',420,b)

# 2 funnel
steps=[(960,"All pings, one year","1,300 TB",""),
       (420,"Only 12 November","3.5 TB","skipped the rest by: partitioning by day"),
       (150,"Only files that can contain segment 4471","about 35 GB","skipped the rest by: min/max stats per file"),
       (40,"Only the columns segment_id and speed","about 5 GB","skipped the rest by: column layout")]
b=''
for i,(w,t,size,how) in enumerate(steps):
    y=30+i*100
    b+=text(40,y,t+":  "+size,17,bold=True,anchor="start")
    b+=bar(40,y+12,w,40)
    if how: b+=text(40+w+16,y+38,how,14,italic=True,anchor="start",fill="#444")
b+=text(520,430,"A good layout answers a query by not reading. (Sizes are illustrative.)",15,italic=True)
svg('03-skip-funnel.svg',450,b)

# 3 iceberg tree
b=box(400,20,240,70,"Catalog","table pings: use snapshot 42",fill=G)
b+=arrow(520,90,520,136)+box(400,140,240,70,"Snapshot 42","the table at one moment")
b+=arrow(470,210,300,256)+arrow(570,210,740,256)
b+=box(160,260,280,70,"Manifest","files for 12 Nov + their stats")+box(600,260,280,70,"Manifest","files for 13 Nov + their stats")
for x,n in [(110,"a.parquet"),(310,"b.parquet"),(560,"c.parquet"),(760,"d.parquet")]:
    b+=box(x,380,170,56,n,ts=16)
b+=arrow(250,330,200,376)+arrow(350,330,390,376)+arrow(700,330,650,376)+arrow(790,330,840,376)
b+=text(30,60,"one pointer",14,italic=True,anchor="start",fill="#444")
b+=text(30,180,"metadata",14,italic=True,anchor="start",fill="#444")+text(30,300,"metadata",14,italic=True,anchor="start",fill="#444")
b+=text(30,468,"data",14,italic=True,anchor="start",fill="#444")
b+=text(560,468,"Everything below the catalog is a file that is never modified after it is written.",15,italic=True)
svg('03-iceberg-tree.svg',490,b)

# 4 atomic commit
b=box(400,20,240,64,"Catalog pointer",fill=G)
b+=box(120,170,220,70,"Snapshot 41","files A, B")+box(700,170,220,70,"Snapshot 42","files A, B, C")
b+=arrow(430,84,290,166,dash=True)+arrow(610,84,750,166)
b+=text(300,118,"before",15,italic=True)+text(800,118,"after: one atomic swap",15,italic=True)
b+=box(280,330,140,60,"A")+box(450,330,140,60,"B")+box(740,330,140,60,"C","new",fill=G)
b+=arrow(215,240,310,326)+arrow(265,240,480,326)+arrow(760,240,400,326)+arrow(790,240,570,326)+arrow(850,240,830,326)
b+=text(125,290,"a query that started",14,italic=True,fill="#444")+text(125,308,"on 41 finishes on 41",14,italic=True,fill="#444")
b+=text(520,430,"File C exists before the swap, but no reader can see it until the pointer moves.",15,italic=True)
svg('03-atomic-commit.svg',450,b)

# 5 cow vs mor
b=text(250,36,"Copy-on-write",19,bold=True)+text(790,36,"Merge-on-read",19,bold=True)
b+=f'<line x1="520" y1="20" x2="520" y2="330" stroke="#222" stroke-width="1" stroke-dasharray="4 6"/>'
b+=box(40,90,190,80,"File A","1,000,000 pings")+arrow(230,130,286,130)+box(290,90,200,80,"File A (new)","999,990 pings",fill=G)
b+=text(260,215,"Rewrite the whole file without the 10 pings.",15)
b+=text(260,255,"slow to write, fast to read",16,bold=True)
b+=box(560,60,190,70,"File A","untouched")+box(560,150,190,70,"Delete file","10 ping ids",fill=G)
b+=arrow(750,95,826,125)+arrow(750,185,826,150)+box(830,100,180,76,"Reader","A minus the 10")
b+=text(790,255,"fast to write, slower to read",16,bold=True)
b+=text(790,285,"Add a tiny file. Every reader subtracts.",15)
b+=text(520,375,"Either way, old files are never edited. Compaction later folds delete files in.",15,italic=True)
svg('03-cow-vs-mor.svg',400,b)
