from __future__ import annotations
import argparse,json,math
R=6371008.8

def valid(lat,lon):
    if not -90<=lat<=90: raise ValueError("invalid latitude")
    if not -180<=lon<=180: raise ValueError("invalid longitude")

def haversine_m(a,b,c,d):
    valid(a,b); valid(c,d); p1,p2=math.radians(a),math.radians(c); dp=math.radians(c-a); dl=math.radians(d-b)
    x=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(x))

def initial_bearing_deg(a,b,c,d):
    valid(a,b); valid(c,d); p1,p2=math.radians(a),math.radians(c); dl=math.radians(d-b)
    y=math.sin(dl)*math.cos(p2); x=math.cos(p1)*math.sin(p2)-math.sin(p1)*math.cos(p2)*math.cos(dl)
    return 0.0 if abs(x)<1e-15 and abs(y)<1e-15 else (math.degrees(math.atan2(y,x))+360)%360

def bbox(lat,lon,radius_m):
    valid(lat,lon)
    if radius_m<0: raise ValueError("radius_m must be >=0")
    dlat=math.degrees(radius_m/R); cl=abs(math.cos(math.radians(lat))); dlon=180.0 if cl<1e-9 else min(180,math.degrees(radius_m/(R*cl)))
    return [max(-90,lat-dlat),max(-180,lon-dlon),min(90,lat+dlat),min(180,lon+dlon)]

def main():
    p=argparse.ArgumentParser(); s=p.add_subparsers(dest="cmd",required=True)
    a=s.add_parser("distance"); [a.add_argument(x,type=float) for x in ("lat1","lon1","lat2","lon2")]
    a=s.add_parser("bearing"); [a.add_argument(x,type=float) for x in ("lat1","lon1","lat2","lon2")]
    a=s.add_parser("bbox"); a.add_argument("lat",type=float); a.add_argument("lon",type=float); a.add_argument("radius_m",type=float)
    n=p.parse_args()
    out={"meters":haversine_m(n.lat1,n.lon1,n.lat2,n.lon2)} if n.cmd=="distance" else {"degrees":initial_bearing_deg(n.lat1,n.lon1,n.lat2,n.lon2)} if n.cmd=="bearing" else {"south_west_north_east":bbox(n.lat,n.lon,n.radius_m)}
    print(json.dumps(out))
if __name__=="__main__": main()
