import fitz, os, sys
from PIL import Image
SRC="/home/user/pte-001-0621"; OUT=f"{SRC}/build/zoom"; os.makedirs(OUT,exist_ok=True)
MAXSIDE=1900
def zoom(pdf, idx, x0,y0,x1,y1, dpi=300, name=None):
    doc=fitz.open(os.path.join(SRC,pdf)); pg=doc[idx]; r=pg.rect
    clip=fitz.Rect(r.x0+x0*r.width, r.y0+y0*r.height, r.x0+x1*r.width, r.y0+y1*r.height)
    pix=pg.get_pixmap(dpi=dpi, clip=clip)
    img=Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
    if max(img.size)>MAXSIDE:
        s=MAXSIDE/max(img.size); img=img.resize((int(img.width*s),int(img.height*s)),Image.LANCZOS)
    name=name or f"{pdf.replace('.pdf','')}_p{idx+1}_z"
    p=f"{OUT}/{name}.png"; img.save(p); print(p, f"{img.width}x{img.height}")
    return p
if __name__=="__main__":
    a=sys.argv
    zoom(a[1],int(a[2]),float(a[3]),float(a[4]),float(a[5]),float(a[6]),int(a[7]) if len(a)>7 else 300, a[8] if len(a)>8 else None)
