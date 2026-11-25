from _draw import *
W,G="#fff",GREY
def rect(x,y,w,h,fill=W,dash=False,rx=8):
    d=' stroke-dasharray="7 5"' if dash else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="#222" stroke-width="2"{d}/>'
# 1 stages
b=box(380,30,280,70,"Stage 0  [SINGLE]","final sort, keep 10, return rows",ts=16)
b+=box(380,150,280,70,"Stage 1  [HASH]","join, final sum per road",ts=16,fill=G)
b+=box(60,280,400,76,"Stage 2  [SOURCE]","scan daily_totals (7 days), partial sums",ts=16)
b+=box(580,280,400,76,"Stage 3  [SOURCE]","scan segments, keep city = Pune",ts=16)
b+=arrow(520,150,520,104)+arrow(260,280,440,224)+arrow(780,280,600,224)
b+=text(250,246,"rows hashed by segment_id",13,italic=True,fill="#444")+text(800,246,"small: sent to every worker",13,italic=True,fill="#444")
b+=text(690,70,"runs on the coordinator",13,italic=True,anchor="start",fill="#444")
b+=text(690,190,"runs on all workers",13,italic=True,anchor="start",fill="#444")
b+=text(520,400,"A query becomes a tree of stages. Data flows upward, in memory, between them.",15,italic=True)
svg('14-stages.svg',420,b)

# 2 dynamic filter
b=box(30,50,300,84,"Scan segments","city = Pune: 20,000 rows")+arrow(330,92,416,92)
b+=box(420,50,240,84,"Build side","collect the 20,000 ids",fill=G)
b+=arrow(660,92,746,92)+box(750,50,260,84,"Join","match ids")
b+=box(30,230,300,84,"Scan daily_totals","7 billion rows on paper")
b+=arrow(540,134,300,226,dash=True)+text(375,185,"\"only these ids\"",15,bold=True,anchor="end")
b+=arrow(330,272,790,138)
b+=text(180,340,"files and row groups without those ids are skipped",14,italic=True,fill="#444")
b+=text(520,395,"Dynamic filtering: the small side of a join becomes a filter on the big side's scan.",15,italic=True)
svg('14-dynamic-filter.svg',415,b)

# 3 resource groups
b=box(400,30,240,64,"All queries",fill=G)
gs=[("dashboards","20 at once, 40% memory"),("ad hoc","10 at once, queue of 50"),("scheduled","5 at once, 30% memory")]
for i,(t,s) in enumerate(gs):
    x=40+i*340
    b+=arrow(520,94,x+140,146)+box(x,150,280,76,t,s,ts=17)
b+=box(380,290,280,64,"11th ad hoc query","waits in the queue",dash=True,ts=16)+arrow(520,290,520,230)
b+=text(520,400,"Each group has its own limits, so one group's flood cannot starve the others.",15,italic=True)
svg('14-resource-groups.svg',420,b)

# 4 athena
b=box(30,150,170,84,"Analyst","sends SQL")+arrow(200,192,276,192)
b+=box(280,150,220,84,"Athena","no cluster to run",fill=G)
b+=box(600,40,400,76,"Glue catalog","table definitions, Iceberg pointers",ts=17)
b+=box(600,154,400,76,"S3: table data","billed per TB scanned",ts=17)
b+=box(600,268,400,76,"S3: results folder","every result is saved here",ts=17)
b+=arrow(500,170,596,90)+arrow(500,192,596,192)+arrow(500,214,596,296)
b+=text(390,270,"workgroup: caps bytes",13,italic=True,fill="#444")+text(390,288,"per query, tracks cost",13,italic=True,fill="#444")
b+=text(520,395,"You manage tables and queries. The service supplies the compute, per query.",15,italic=True)
svg('14-athena.svg',415,b)

# 5 redshift
b=box(380,30,280,70,"Leader node","plans, hands out work, returns results",fill=G,ts=16)
for i,x in enumerate([40,370,700]):
    b+=rect(x,170,300,150)+text(x+150,193,f"Compute node {i+1}",16,bold=True)
    b+=box(x+14,206,130,100,"Slice",f"totals + segments",ts=14)+box(x+156,206,130,100,"Slice","totals + segments",ts=14)
    b+=arrow(520,100,x+150,166)
b+=text(520,355,"Both tables use DISTKEY(segment_id): matching rows already sit in the same slice.",15,bold=True)
b+=text(520,395,"A join on the distribution key needs no data movement between nodes.",15,italic=True)
svg('14-redshift.svg',415,b)
