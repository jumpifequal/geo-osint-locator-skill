# 06 — Scoring and Termination
Scoring ranks surviving candidates only; it never overrides gates.

Score from 0:
- Must-have max 50, split equally: PASS full; ND/NOT_EXECUTED/SKIPPED 0; FAIL subtract allocation; CRITICAL FAIL rejects.
- Nice-to-have max 15, split equally: PASS full; otherwise 0.
- Independent CoVE max 25: first +10, second +10, additional +5 each, capped 25.
- Killer max 10: PASS +10; ND/NOT_EXECUTED/SKIPPED 0; FAIL rejects.
- MAJOR_MISMATCH -10 for identifier/Must-have geometry/layout/infrastructure/skyline/coastline/other discriminating contradiction.
- MINOR_MISMATCH -5 only for contextual discrepancy that does not independently falsify.
Never double-penalise one contradiction. Clamp 0–100.

Tie-break:
1 CRITICAL PASS count
2 independent CoVE PASS count
3 killer confirmation
4 identifier strength
5 fewer ND
6 fewer NOT_EXECUTED/SKIPPED
7 fewer mismatches
Still equal → `TIED`.

## Single exact-place STRONG gate
ALL must pass:
1. score ≥80
2. every CRITICAL Must-have PASS
3. ≥2 independent CoVE channels PASS
4. ≥1 killer PASS whose specificity is `UNIQUE` or `DISCRIMINATIVE`
5. no unresolved MAJOR_MISMATCH
6. every available decisive verification executed, or explicitly skipped without leaving identity materially unresolved
7. text-derived candidate has ≥1 independent non-textual physical PASS
8. holistic scene match = PASS when broad scene geometry is observable
9. viewpoint is not INCOMPATIBLE when viewpoint geometry is observable
10. nearest competitor is REJECTED, materially WEAKER, or no serious competitor is found after targeted search

Then output `STRONG — IDENTIFICATION SUFFICIENTLY VERIFIED` and stop broad exploration.

Otherwise:
PLAUSIBLE = 60–79, no rejection
WEAK = <60
REJECTED = rejection condition

Only STRONG may produce exact place. Else return supported macro-area or `INDETERMINATE`.


## Ranked alternatives visibility

After scoring and hard-gate evaluation:
1. sort all surviving candidates using the existing ranking and tie-break rules;
2. retain the top 3 at most for user-visible reporting;
3. never remove a surviving #2/#3 merely because #1 reaches STRONG;
4. do not permit a lower-ranked candidate to inherit STRONG status from the leader;
5. expose the decisive unresolved check for each non-leading candidate when useful.

Stopping broad exploration after STRONG means stop searching for new candidates; it does not mean hiding already-surviving alternatives.


## Final ordering rule

When 2 or more candidates survive, discriminative reranking is mandatory before the final visible ranking.

Raw numerical score is not the final ordering key when it conflicts with substantially stronger HIGH/UNIQUE evidence density.

Reranking never bypasses hard rejection or STRONG gates.

## Candidate-ledger preservation

Final ranking and final display are different operations.

After scoring:
1. preserve the top 3 genuinely considered non-firewall-blocked candidates in the candidate ledger;
2. assign each its final status;
3. render all ledger entries in the final dashboard, including REJECTED entries;
4. do not let STRONG termination erase already-considered alternatives.

This preserves auditability and exposes under-ranked correct candidates.
