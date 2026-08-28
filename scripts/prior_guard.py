from __future__ import annotations
import argparse, json

ALLOWED_PROVENANCE = {"IMAGE_DERIVED", "SEARCH_DERIVED", "USER_BOUNDED", "CONTEXT_ANCHORED"}
FORBIDDEN_SUPPORT = {"PREVIOUS_TEST_LOCATION", "RECENT_SUCCESS_REGION", "EARLIER_USER_CORRECTION", "PREVIOUS_ASSISTANT_GUESS"}

def evaluate_candidate(candidate):
    if not isinstance(candidate, dict):
        raise TypeError("candidate must be an object")
    name = candidate.get("name")
    if not name:
        raise ValueError("candidate requires name")
    provenance = candidate.get("provenance")
    if provenance not in ALLOWED_PROVENANCE:
        raise ValueError("invalid provenance")
    supports = candidate.get("supports", [])
    if not isinstance(supports, list):
        raise TypeError("supports must be a list")
    current_image_support = bool(candidate.get("current_image_support", False))
    user_current_bound = bool(candidate.get("user_current_bound", False))

    forbidden = sorted({s for s in supports if s in FORBIDDEN_SUPPORT})

    blocked = False
    reasons = []

    if provenance == "CONTEXT_ANCHORED" and not current_image_support:
        blocked = True
        reasons.append("context-anchored candidate lacks independent current-image support")

    if forbidden and not current_image_support:
        blocked = True
        reasons.append("candidate relies on forbidden conversation-history support")

    if provenance == "USER_BOUNDED" and not user_current_bound:
        blocked = True
        reasons.append("USER_BOUNDED requires an explicit bound for the current image")

    return {
        "name": name,
        "allowed": not blocked,
        "status": "ACTIVE" if not blocked else "BLOCKED_CONTEXT_ANCHOR",
        "forbidden_support": forbidden,
        "reasons": reasons,
    }

def filter_candidates(candidates):
    if not isinstance(candidates, list):
        raise TypeError("input must be a list")
    reports = [evaluate_candidate(c) for c in candidates]
    allowed_names = [r["name"] for r in reports if r["allowed"]]
    blocked_names = [r["name"] for r in reports if not r["allowed"]]
    return {"allowed": allowed_names, "blocked": blocked_names, "reports": reports}

def main():
    p = argparse.ArgumentParser()
    p.add_argument("json_file", help="JSON array of candidate records")
    ns = p.parse_args()
    with open(ns.json_file, encoding="utf-8") as f:
        data = json.load(f)
    print(json.dumps(filter_candidates(data), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
