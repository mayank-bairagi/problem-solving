from _draw import *
W,G="#fff",GREY
# 1 pure function
b=box(40,70,260,90,"Pings for 12 Nov","input: never changes",fill=G)+arrow(300,115,386,115)
b+=box(390,70,240,90,"Nightly job","reads, computes, nothing else")+arrow(630,115,716,115)
b+=box(720,70,280,90,"Daily totals for 12 Nov","output: replaced as a whole")
b+=f'<path d="M860,165 C860,250 510,250 510,168" fill="none" stroke="#222" stroke-width="2" stroke-dasharray="7 5" marker-end="url(#a)"/>'
b+=text(685,262,"run it again: same input, same output",15,bold=True)
b+=text(520,315,"Output = f(input). Nothing else is touched, so a re-run cannot make things worse.",15,italic=True)
svg('05-pure-function.svg',335,b)

# 2 stages
ys=[80,190,300]; y2=[135,245]
b=text(350,40,"Stage 1: runs where the data is",17,bold=True)+text(740,40,"Stage 2: after regrouping",17,bold=True)
for i,y in enumerate(ys):
    b+=box(30,y,150,70,f"File chunk {i+1}","pings",fill=G)+arrow(180,y+35,236,y+35)
    b+=box(240,y,220,70,f"Task 1.{i+1}","keep 3 columns, pre-add")
    for yy in y2: b+=arrow(460,y+35,636,yy+35)
for i,yy in enumerate(y2):
    b+=box(640,yy,200,70,f"Task 2.{i+1}","final sum and count")+arrow(840,yy+35,886,yy+35)+box(890,yy,130,70,"Output","file",ts=16)
b+=text(550,400,"shuffle",16,bold=True)
b+=text(105,420,"35 billion pings in",14,italic=True,fill="#444")
b+=text(550,420,"about 1 billion partial totals cross the network",14,italic=True,fill="#444")
b+=text(520,460,"Adding up early, before the shuffle, is what keeps the expensive step small.",15,italic=True)
svg('05-stages.svg',480,b)

# 3 joins
b=text(250,36,"Broadcast join",19,bold=True)+text(790,36,"Shuffle join",19,bold=True)
b+=f'<line x1="520" y1="20" x2="520" y2="350" stroke="#222" stroke-width="1" stroke-dasharray="4 6"/>'
b+=box(170,60,160,56,"Cities","2,000 rows",ts=16)
for i,x in enumerate([20,180,340]):
    b+=arrow(250,116,x+70,166)+box(x,170,140,90,f"Worker {i+1}","big chunk + copy",ts=16)
b+=text(250,300,"The small table is copied to every worker.",15)+text(250,324,"The big table does not move.",15,bold=True)
for i,y in enumerate([80,190]):
    b+=box(545,y,120,70,"Totals",f"chunk {i+1}",ts=16)+box(895,y,120,70,"Segments",f"chunk {i+1}",ts=16,fill=G)
    b+=box(710,y,140,70,f"Partition {i}","same keys meet",ts=16)
for y in [115,225]:
    for yy in [115,225]:
        b+=arrow(665,y,706,yy)+arrow(895,y,854,yy)
b+=text(790,300,"Both tables are regrouped by the join key.",15)+text(790,324,"Both tables move.",15,bold=True)
b+=text(520,385,"If one side is small, copy it. If both are big, regroup both.",15,italic=True)
svg('05-joins.svg',405,b)

# 4 retry
b=''
for i in range(5):
    x=40+i*198
    if i==2: b+=box(x,50,170,76,"Task 3","FAILED",fill=G,dash=True)
    else: b+=box(x,50,170,76,f"Task {i+1}","done, kept")
b+=arrow(521,126,521,186)+box(436,190,170,76,"Task 3","retried elsewhere",fill=G)
b+=text(700,222,"only this piece is redone",15,bold=True,anchor="start")
b+=text(520,315,"Safe because the input cannot change and a task does nothing except produce its output.",15,italic=True)
svg('05-retry.svg',335,b)

# 5 two-level
b=text(150,36,"Raw pings",18,bold=True)+text(150,56,"3.5 TB per day",14,fill="#444")
b+=text(520,36,"Daily totals",18,bold=True)+text(520,56,"per road, per hour: small",14,fill="#444")
b+=text(880,36,"Typical speeds",18,bold=True)+text(880,56,"per road, per hour of week",14,fill="#444")
days=["...","9 Nov","10 Nov","11 Nov","12 Nov"]
for i,d in enumerate(days):
    y=80+i*58; hot=i>=2
    b+=box(50,y,200,46,d,ts=16,fill=G if hot else W)+box(420,y,200,46,d,ts=16,fill=G if hot else W)
    if i>0: b+=arrow(250,y+23,416,y+23,dash=not hot)
    b+=arrow(620,y+23,766,215)
b+=box(770,170,220,90,"Add up","the last 56 days")
b+=text(335,395,"grey: recomputed every night (late pings may have changed them)",14,italic=True,fill="#444")
b+=text(880,300,"rebuilt from the small table",14,italic=True,fill="#444")
b+=text(520,430,"Heavy work touches three days. The eight-week view is rebuilt from small daily totals.",15,italic=True)
svg('05-two-level.svg',450,b)
