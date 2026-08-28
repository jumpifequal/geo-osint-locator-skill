from __future__ import annotations
import argparse, json
from pathlib import Path
from PIL import Image

def clamp_box(box,w,h):
    x1,y1,x2,y2=box
    x1=max(0,min(w,int(round(x1)))); x2=max(0,min(w,int(round(x2))))
    y1=max(0,min(h,int(round(y1)))); y2=max(0,min(h,int(round(y2))))
    if x2<=x1 or y2<=y1: raise ValueError("Invalid or empty crop box")
    return x1,y1,x2,y2

def fractional_box_to_pixels(frac,w,h):
    if len(frac)!=4 or not all(0<=v<=1 for v in frac): raise ValueError("Fractional coordinates must contain four values in [0,1]")
    a,b,c,d=frac
    return clamp_box((a*w,b*h,c*w,d*h),w,h)

def crop_image(src,dst,box=None,frac=None,scale=1.0):
    if box is not None and frac is not None: raise ValueError("Specify either box or frac")
    if scale<=0: raise ValueError("scale must be > 0")
    img=Image.open(src).convert("RGB")
    if frac is not None: box=fractional_box_to_pixels(frac,*img.size)
    if box is None: box=(0,0,*img.size)
    box=clamp_box(box,*img.size); out=img.crop(box)
    if scale!=1.0: out=out.resize((max(1,round(out.width*scale)),max(1,round(out.height*scale))),Image.Resampling.LANCZOS)
    dst=Path(dst); dst.parent.mkdir(parents=True,exist_ok=True); out.save(dst)
    return {"source_size":list(img.size),"crop_box":list(box),"output_size":list(out.size),"output":str(dst)}

def tile_image(src,out_dir,rows=3,cols=3,overlap=0.05):
    if rows<1 or cols<1: raise ValueError("rows and cols must be >=1")
    if not 0<=overlap<0.5: raise ValueError("overlap must be in [0,0.5)")
    img=Image.open(src).convert("RGB"); w,h=img.size; out_dir=Path(out_dir); out_dir.mkdir(parents=True,exist_ok=True)
    cw,ch=w/cols,h/rows; px,py=cw*overlap,ch*overlap; rec=[]
    for r in range(rows):
        for c in range(cols):
            box=clamp_box((c*cw-px,r*ch-py,(c+1)*cw+px,(r+1)*ch+py),w,h)
            dst=out_dir/f"tile_r{r+1}_c{c+1}.jpg"; img.crop(box).save(dst,quality=95); rec.append({"tile":str(dst),"box":list(box)})
    return {"source_size":list(img.size),"tiles":rec}

def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest="cmd",required=True)
    a=s.add_parser("info"); a.add_argument("image")
    a=s.add_parser("crop"); a.add_argument("image"); a.add_argument("output"); g=a.add_mutually_exclusive_group(required=True); g.add_argument("--box",nargs=4,type=float); g.add_argument("--frac",nargs=4,type=float); a.add_argument("--scale",type=float,default=1)
    a=s.add_parser("tile"); a.add_argument("image"); a.add_argument("output_dir"); a.add_argument("--rows",type=int,default=3); a.add_argument("--cols",type=int,default=3); a.add_argument("--overlap",type=float,default=.05)
    n=p.parse_args()
    if n.cmd=="info":
        with Image.open(n.image) as im: out={"size":list(im.size),"mode":im.mode,"format":im.format}
    elif n.cmd=="crop": out=crop_image(n.image,n.output,box=n.box,frac=n.frac,scale=n.scale)
    else: out=tile_image(n.image,n.output_dir,n.rows,n.cols,n.overlap)
    print(json.dumps(out))
if __name__=="__main__": main()
