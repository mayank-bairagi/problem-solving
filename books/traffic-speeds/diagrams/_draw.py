"""Tiny helpers for the book's greyscale SVG diagrams. Usage: see build_03.py."""
H='<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#222"/></marker></defs>'
GREY="#e6e6e6"
def svg(name,h,body):
    open(name,'w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1040 {h}" font-family="Helvetica, Arial, sans-serif">\n{H}\n<rect width="1040" height="{h}" fill="#fff"/>\n{body}\n</svg>\n')
def text(x,y,t,size=15,italic=False,bold=False,anchor="middle",fill="#111"):
    st=(' font-style="italic"' if italic else '')+(' font-weight="bold"' if bold else '')
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}"{st} fill="{fill}">{t}</text>'
def box(x,y,w,h,title,sub=None,fill="#fff",dash=False,ts=18):
    d=' stroke-dasharray="7 5"' if dash else ''
    s=f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#222" stroke-width="2"{d}/>'
    cy=y+h/2
    if sub:
        s+=text(x+w/2,cy-4,title,ts,bold=True)+text(x+w/2,cy+18,sub,14,fill="#444")
    else:
        s+=text(x+w/2,cy+6,title,ts,bold=True)
    return s
def arrow(x1,y1,x2,y2,dash=False):
    d=' stroke-dasharray="7 5"' if dash else ''
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#222" stroke-width="2"{d} marker-end="url(#a)"/>'
def cells(x,y,labels,w=70,h=56,fills=None,size=17):
    s=''
    for i,l in enumerate(labels):
        f=(fills[i] if fills else "#fff")
        s+=f'<rect x="{x+i*w}" y="{y}" width="{w}" height="{h}" fill="{f}" stroke="#222" stroke-width="2"/>'
        s+=text(x+i*w+w/2,y+h/2+6,l,size,bold=True)
    return s
def bar(x,y,w,h,fill=GREY):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="#222" stroke-width="2"/>'
