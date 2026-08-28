from __future__ import annotations
import argparse,json,urllib.parse,urllib.request
ENDPOINT="https://nominatim.openstreetmap.org"

def build_search_url(query,endpoint=ENDPOINT,limit=5,countrycodes=None):
    if not query or not query.strip(): raise ValueError("empty query")
    if not 1<=int(limit)<=50: raise ValueError("limit must be 1..50")
    p={"q":query.strip(),"format":"jsonv2","limit":int(limit),"addressdetails":1}
    if countrycodes: p["countrycodes"]=countrycodes
    return endpoint.rstrip("/")+"/search?"+urllib.parse.urlencode(p)

def build_reverse_url(lat,lon,endpoint=ENDPOINT,zoom=18):
    if not -90<=lat<=90 or not -180<=lon<=180: raise ValueError("invalid coordinates")
    if not 0<=int(zoom)<=18: raise ValueError("zoom must be 0..18")
    return endpoint.rstrip("/")+"/reverse?"+urllib.parse.urlencode({"lat":lat,"lon":lon,"format":"jsonv2","zoom":int(zoom),"addressdetails":1})

def get_json(url,user_agent,timeout=15):
    if not user_agent or not user_agent.strip(): raise ValueError("empty user-agent")
    if timeout<=0: raise ValueError("timeout must be >0")
    req=urllib.request.Request(url,headers={"User-Agent":user_agent,"Accept":"application/json"})
    with urllib.request.urlopen(req,timeout=timeout) as r: return json.loads(r.read().decode())

def main():
    p=argparse.ArgumentParser(); p.add_argument("--user-agent",required=True); p.add_argument("--endpoint",default=ENDPOINT); p.add_argument("--timeout",type=int,default=15); s=p.add_subparsers(dest="cmd",required=True)
    a=s.add_parser("search"); a.add_argument("query"); a.add_argument("--limit",type=int,default=5); a.add_argument("--countrycodes")
    a=s.add_parser("reverse"); a.add_argument("lat",type=float); a.add_argument("lon",type=float); a.add_argument("--zoom",type=int,default=18)
    n=p.parse_args(); url=build_search_url(n.query,n.endpoint,n.limit,n.countrycodes) if n.cmd=="search" else build_reverse_url(n.lat,n.lon,n.endpoint,n.zoom); print(json.dumps(get_json(url,n.user_agent,n.timeout),ensure_ascii=False,indent=2))
if __name__=="__main__": main()
