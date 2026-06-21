import fitz, numpy as np, os, sys
from PIL import Image
SRC="/home/user/pte-001-0621"
OUT=f"{SRC}/build/pages"; os.makedirs(OUT,exist_ok=True)

def card_columns(arr):
    rgb=arr[:,:,:3].astype(np.int16); h,w=rgb.shape[:2]
    val=rgb.mean(2); sat=rgb.max(2)-rgb.min(2)
    graybg=(val>120)&(val<150)&(sat<10)
    gf=graybg.mean(0); half=w//2
    left=[x for x in range(half) if gf[x]>0.4]
    right=[x for x in range(half,w) if gf[x]>0.4]
    lb=max(left) if left else None; rb=min(right) if right else None
    if lb is not None and rb is not None and (rb-lb) < 0.75*w:
        return lb,rb
    # case B: detect left sidebar (a left band whose bg differs). Heuristic: keep from where content really starts.
    return 0,w

def ink_rows(arr, x0, x1):
    rgb=arr[:,x0:x1,:3].astype(np.int16)
    val=rgb.mean(2); sat=rgb.max(2)-rgb.min(2)
    ink=(val<150)&((sat>18)|(val<120))
    rows=np.where(ink.sum(1)>3)[0]
    return (rows.min(),rows.max()) if len(rows) else (0,arr.shape[0])

def render(pdf, idx, dpi=300, target_w=1500, slice_h=1700, pad=16, tag=None):
    doc=fitz.open(os.path.join(SRC,pdf))
    pix=doc[idx].get_pixmap(dpi=dpi)
    arr=np.frombuffer(pix.samples,dtype=np.uint8).reshape(pix.height,pix.width,pix.n)[:,:,:3]
    x0,x1=card_columns(arr)
    y0,y1=ink_rows(arr,x0,x1)
    x0=max(0,x0-pad); x1=min(arr.shape[1],x1+pad)
    y0=max(0,y0-pad); y1=min(arr.shape[0],y1+pad)
    crop=arr[y0:y1,x0:x1]
    img=Image.fromarray(crop)
    if img.width>target_w:
        img=img.resize((target_w,int(img.height*target_w/img.width)),Image.LANCZOS)
    tag=tag or pdf.replace('.pdf','')
    base=f"{OUT}/{tag}_p{idx+1}"
    paths=[]
    H=img.height
    if H<=slice_h:
        p=f"{base}.png"; img.save(p); paths.append(p)
    else:
        n=(H+slice_h-1)//slice_h
        overlap=80
        for i in range(n):
            top=max(0,i*slice_h-(overlap if i>0 else 0)); bot=min(H,(i+1)*slice_h)
            sl=img.crop((0,top,img.width,bot)); p=f"{base}_s{i+1}.png"; sl.save(p); paths.append(p)
    for p in paths: print(p, Image.open(p).size)
    return paths

if __name__=="__main__":
    pdf=sys.argv[1]; idx=int(sys.argv[2])
    render(pdf,idx)
