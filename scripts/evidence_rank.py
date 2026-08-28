from __future__ import annotations
import argparse, json

def score_test(elimination_power, reliability, independence, execution_cost, available=True):
    vals = {
        "elimination_power": elimination_power,
        "reliability": reliability,
        "independence": independence,
        "execution_cost": execution_cost,
    }
    if not all(isinstance(v, (int, float)) for v in vals.values()):
        raise TypeError("scores must be numeric")
    if not 0 <= elimination_power <= 4: raise ValueError("elimination_power must be 0..4")
    if not 0 <= reliability <= 4: raise ValueError("reliability must be 0..4")
    if not 0 <= independence <= 4: raise ValueError("independence must be 0..4")
    if not 1 <= execution_cost <= 4: raise ValueError("execution_cost must be 1..4")
    if not available:
        return float("-inf")
    # Elimination power dominates; reliability and independence break ties.
    return round((4*elimination_power + 2*reliability + independence) / execution_cost, 6)

def rank_tests(tests):
    ranked=[]
    for i,t in enumerate(tests):
        s=score_test(
            t["elimination_power"], t["reliability"],
            t["independence"], t["execution_cost"],
            t.get("available", True)
        )
        ranked.append({**t, "priority_score": s, "_index": i})
    ranked.sort(key=lambda x: (-x["priority_score"], -x["elimination_power"], -x["reliability"], -x["independence"], x["execution_cost"], x["_index"]))
    for r in ranked: r.pop("_index", None)
    return ranked

def main():
    p=argparse.ArgumentParser()
    p.add_argument("json_file", help="JSON array of proposed tests")
    ns=p.parse_args()
    with open(ns.json_file, encoding="utf-8") as f: tests=json.load(f)
    print(json.dumps(rank_tests(tests), ensure_ascii=False, indent=2))

if __name__=="__main__": main()
