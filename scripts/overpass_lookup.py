from __future__ import annotations
import argparse,json,re,urllib.parse,urllib.request
ENDPOINT="https://overpass-api.de/api/interpreter"; SAFE=re.compile(r"^[A-Za-z0-9_:.-]+$")

def esc(v): return str(v).replace("\\","\\\\").replace('"','\\"')

def build_around_query(lat,lon,radius_m,key,value=None,limit=50):
    if not -90<=lat<=90 or not -180<=lon<=180: raise ValueError("invalid coordinates")
    if not 0<radius_m<=25000: raise ValueError("radius_m must be >0 and <=25000")
    if not SAFE.fullmatch(key): raise ValueError("unsafe tag key")
    if value is not None and len(str(value))>200: raise ValueError("tag value too long")
    if not 1<=int(limit)<=500: raise ValueError("limit must be 1..500")
    tag=f'["{esc(key)}"]' if value is None else f'["{esc(key)}"="{esc(value)}"]'
    return "[out:json][timeout:20];\n(\n  nwr(around:%d,%s,%s)%s;\n);\nout center tags %d;"%(int(radius_m),float(lat),float(lon),tag,int(limit))

def post_json(query,endpoint=ENDPOINT,user_agent="geo-osint-locator/1.0",timeout=30):
    if not query or not query.strip(): raise ValueError("empty query")
    if timeout<=0: raise ValueError("timeout must be >0")
    body=urllib.parse.urlencode({"data":query}).encode(); req=urllib.request.Request(endpoint,data=body,method="POST",headers={"User-Agent":user_agent,"Accept":"application/json","Content-Type":"application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req,timeout=timeout) as r: return json.loads(r.read().decode())

def main():
    p=argparse.ArgumentParser(); p.add_argument("--endpoint",default=ENDPOINT); p.add_argument("--user-agent",default="geo-osint-locator/1.0"); p.add_argument("--timeout",type=int,default=30); s=p.add_subparsers(dest="cmd",required=True)
    a=s.add_parser("around"); a.add_argument("lat",type=float); a.add_argument("lon",type=float); a.add_argument("radius_m",type=float); a.add_argument("key"); a.add_argument("--value"); a.add_argument("--limit",type=int,default=50)
    a=s.add_parser("raw"); a.add_argument("query")
    n=p.parse_args(); q=build_around_query(n.lat,n.lon,n.radius_m,n.key,n.value,n.limit) if n.cmd=="around" else n.query; print(json.dumps(post_json(q,n.endpoint,n.user_agent,n.timeout),ensure_ascii=False,indent=2))
if __name__=="__main__": main()
