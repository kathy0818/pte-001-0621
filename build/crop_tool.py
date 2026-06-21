import fitz, numpy as np, os, sys
from PIL import Image
SRC="/home/user/pte-001-0621"

def ink_bbox(arr):
    """bbox of meaningful ink: dark text OR colored pixels (excludes white card + gray bands)."""
    rgb=arr[:,:,:3].astype(np.int16)
    mx=rgb.max(2); mn=rgb.min(2)
    val=rgb.mean(2)
    sat=mx-mn
    ink=(val<150)&((sat>18)|(val<120))   # colored OR dark, but not uniform light gray
    # require some density to ignore stray pixels
    rows=np.where(ink.sum(1)>3)[0]; cols=np.where(ink.sum(0)>3)[0]
    if len(rows)==0 or len(cols)==0: return None
    return cols.min(),rows.min(),cols.max(),rows.max()

def render_crop(pdf, page_idx, dpi=350, pad=14, outpath=None):
    doc=fitz.open(os.path.join(SRC,pdf))
    pg=doc[page_idx]
    pix=pg.get_pixmap(dpi=dpi)
    arr=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)[:,:,:3]
    bb=ink_bbox(arr)
    if bb is None:
        crop=arr
    else:
        x0,y0,x1,y1=bb
        x0=max(0,x0-pad); y0=max(0,y0-pad); x1=min(arr.shape[1],x1+pad); y1=min(arr.shape[0],y1+pad)
        crop=arr[y0:y1,x0:x1]
    if outpath:
        Image.fromarray(crop).save(outpath)
    return crop.shape[1],crop.shape[0]

if __name__=="__main__":
    pdf=sys.argv[1]; idx=int(sys.argv[2]); dpi=int(sys.argv[3]) if len(sys.argv)>3 else 350
    out=sys.argv[4] if len(sys.argv)>4 else f"{SRC}/build/crop/test.png"
    w,h=render_crop(pdf,idx,dpi,outpath=out)
    print(f"{pdf} p{idx+1} -> {out}  ({w}x{h})")
