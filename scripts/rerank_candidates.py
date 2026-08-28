from __future__ import annotations
import argparse, json

DISC = {"LOW":1.0,"MEDIUM":2.0,"HIGH":3.0,"UNIQUE":4.0}
QUAL = {"UNCERTAIN":0.30,"PROBABLE":0.70,"CERTAIN":1.00}
PERS = {"TRANSIENT":0.40,"SEMI_PERSISTENT":0.75,"STRUCTURAL":1.00}

def clue_contribution(clue):
    if not isinstance(clue, dict):
        raise TypeError("clue must be an object")
    d=clue.get("discrimination"); q=clue.get("quality"); p=clue.get("persistence","STRUCTURAL")
    if d not in DISC: raise ValueError("invalid discrimination")
    if q not in QUAL: raise ValueError("invalid quality")
    if p not in PERS: raise ValueError("invalid persistence")
    if clue.get("duplicate", False):
        return 0.0
    return DISC[d]*QUAL[q]*PERS[p]

def metrics(candidate):
    clues=candidate.get("positive_clues",[])
    if not isinstance(clues,list): raise TypeError("positive_clues must be a list")
    vals=[clue_contribution(c) for c in clues]
    high=sum(1 for c in clues if not c.get("duplicate",False) and c.get("discrimination") in {"HIGH","UNIQUE"})
    return {
        "density": round(sum(vals)/max(1,len([c for c in clues if not c.get("duplicate",False)])),6),
        "high_value_count": high,
        "contribution_sum": round(sum(vals),6),
    }

def rerank(candidates):
    if not isinstance(candidates,list): raise TypeError("candidates must be a list")
    rows=[]
    for i,c in enumerate(candidates):
        m=metrics(c)
        row={**c, **m, "_i":i}
        rows.append(row)

    def gate_rank(c):
        return {
            "ACTIVE":3,
            "PLAUSIBLE":2,
            "WEAK":1,
            "REJECTED":0,
        }.get(c.get("status","ACTIVE"), 0)

    def competitor_rank(c):
        return {
            "REJECTED":3,
            "WEAKER":2,
            "NO_SERIOUS_COMPETITOR_FOUND":2,
            "SURVIVES_SIMILARLY":1,
            "UNTESTED":0,
        }.get(c.get("competitor_status","UNTESTED"), 0)

    def holistic_rank(c):
        return {"PASS":2,"ND":1,"FAIL":0}.get(c.get("holistic_state","ND"),0)

    rows.sort(key=lambda c:(
        -gate_rank(c),
        -competitor_rank(c),
        -holistic_rank(c),
        -c["density"],
        -c["high_value_count"],
        -float(c.get("score",0)),
        c["_i"],
    ))
    for n,r in enumerate(rows,1):
        r["rerank_position"]=n
        r.pop("_i",None)
    return rows

def main():
    p=argparse.ArgumentParser()
    p.add_argument("json_file")
    ns=p.parse_args()
    with open(ns.json_file,encoding="utf-8") as f:
        data=json.load(f)
    print(json.dumps(rerank(data),ensure_ascii=False,indent=2))

if __name__=="__main__": main()
