from __future__ import annotations
import argparse, json

def _box(b):
    if len(b)!=4: raise ValueError("box must contain x1,y1,x2,y2")
    x1,y1,x2,y2=map(float,b)
    if x2<=x1 or y2<=y1: raise ValueError("invalid box")
    return x1,y1,x2,y2

def relations(a,b,near_ratio=1.5,align_tol=0.15):
    ax1,ay1,ax2,ay2=_box(a); bx1,by1,bx2,by2=_box(b)
    acx,acy=(ax1+ax2)/2,(ay1+ay2)/2
    bcx,bcy=(bx1+bx2)/2,(by1+by2)/2
    aw,ah=ax2-ax1,ay2-ay1; bw,bh=bx2-bx1,by2-by1
    out=[]
    if ax2 <= bx1: out.append("LEFT_OF")
    if bx2 <= ax1: out.append("RIGHT_OF")
    if ay2 <= by1: out.append("ABOVE")
    if by2 <= ay1: out.append("BELOW")
    if not (ax2 < bx1 or bx2 < ax1 or ay2 < by1 or by2 < ay1): out.append("OVERLAPS")
    if ax1>=bx1 and ay1>=by1 and ax2<=bx2 and ay2<=by2: out.append("INSIDE")
    dx,dy=abs(acx-bcx),abs(acy-bcy)
    scale=max((aw+bw)/2,(ah+bh)/2,1e-9)
    out.append("NEAR" if (dx*dx+dy*dy)**0.5 <= near_ratio*scale else "FAR")
    if dy <= align_tol*max(ah,bh): out.append("ALIGNED_HORIZONTAL")
    if dx <= align_tol*max(aw,bw): out.append("ALIGNED_VERTICAL")
    return out

def compare_relations(observed, reference):
    o=set(observed); r=set(reference)
    union=o|r
    return {
        "matched": sorted(o&r),
        "observed_only": sorted(o-r),
        "reference_only": sorted(r-o),
        "jaccard": 1.0 if not union else round(len(o&r)/len(union),6),
    }

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("derive"); a.add_argument("--a",nargs=4,type=float,required=True); a.add_argument("--b",nargs=4,type=float,required=True)
    c=sub.add_parser("compare"); c.add_argument("--observed",nargs="+",required=True); c.add_argument("--reference",nargs="+",required=True)
    ns=p.parse_args()
    out={"relations":relations(ns.a,ns.b)} if ns.cmd=="derive" else compare_relations(ns.observed,ns.reference)
    print(json.dumps(out,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
