from __future__ import annotations
import argparse, json

VALID = {"PASS", "FAIL", "ND", "NOT_EXECUTED", "SKIPPED"}
KILLER_SPECIFICITY = {"UNIQUE", "DISCRIMINATIVE", "GENERIC"}

def _state(value, field):
    if value not in VALID:
        raise ValueError(f"{field} must be one of {sorted(VALID)}")
    return value

def evaluate_strong_gate(record):
    if not isinstance(record, dict):
        raise TypeError("record must be an object")

    score = float(record.get("score", 0))
    critical_all_pass = bool(record.get("critical_all_pass", False))
    independent_cove_pass = int(record.get("independent_cove_pass", 0))
    killer_state = _state(record.get("killer_state", "ND"), "killer_state")
    killer_specificity = record.get("killer_specificity", "GENERIC")
    if killer_specificity not in KILLER_SPECIFICITY:
        raise ValueError("invalid killer_specificity")

    no_major_mismatch = bool(record.get("no_major_mismatch", False))
    holistic_state = _state(record.get("holistic_state", "ND"), "holistic_state")
    viewpoint_state = record.get("viewpoint_state", "ND")
    if viewpoint_state not in {"COMPATIBLE", "INCOMPATIBLE", "ND"}:
        raise ValueError("invalid viewpoint_state")

    competitor_status = record.get("competitor_status", "UNTESTED")
    if competitor_status not in {"REJECTED", "WEAKER", "NO_SERIOUS_COMPETITOR_FOUND", "SURVIVES_SIMILARLY", "UNTESTED"}:
        raise ValueError("invalid competitor_status")

    text_derived = bool(record.get("text_derived", False))
    independent_non_text_pass = bool(record.get("independent_non_text_pass", False))
    decisive_checks_accounted = bool(record.get("decisive_checks_accounted", False))

    reasons = []

    if score < 80: reasons.append("score below threshold")
    if not critical_all_pass: reasons.append("not all critical must-haves pass")
    if independent_cove_pass < 2: reasons.append("insufficient independent CoVE passes")
    if killer_state != "PASS": reasons.append("killer check not passed")
    if killer_specificity not in {"UNIQUE", "DISCRIMINATIVE"}:
        reasons.append("killer check is not competitor-discriminative")
    if not no_major_mismatch: reasons.append("unresolved major mismatch")
    if holistic_state != "PASS": reasons.append("holistic scene match not passed")
    if viewpoint_state == "INCOMPATIBLE": reasons.append("viewpoint incompatible")
    if competitor_status not in {"REJECTED", "WEAKER", "NO_SERIOUS_COMPETITOR_FOUND"}:
        reasons.append("nearest competitor not sufficiently falsified")
    if text_derived and not independent_non_text_pass:
        reasons.append("text-derived candidate lacks independent non-textual pass")
    if not decisive_checks_accounted:
        reasons.append("decisive checks not fully accounted")

    return {
        "strong": len(reasons) == 0,
        "status": "STRONG" if len(reasons) == 0 else "NOT_STRONG",
        "reasons": reasons,
    }

def main():
    p = argparse.ArgumentParser()
    p.add_argument("json_file")
    ns = p.parse_args()
    with open(ns.json_file, encoding="utf-8") as f:
        record = json.load(f)
    print(json.dumps(evaluate_strong_gate(record), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
