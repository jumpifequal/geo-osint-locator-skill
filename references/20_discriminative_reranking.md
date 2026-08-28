# 20 — Discriminative Reranking

Use whenever at least 2 viable candidates remain after initial scoring.

## Objective

Detect under-ranked candidates that explain more candidate-specific evidence than the current leader.

Raw match count is not enough.

A candidate supported by many generic clues can rank below a candidate supported by fewer but more discriminative clues.

## Evidence discrimination weight

Classify each positive clue:

- `UNIQUE` = 4
- `HIGH` = 3
- `MEDIUM` = 2
- `LOW` = 1

Classify evidence quality separately:

- `CERTAIN` = 1.00
- `PROBABLE` = 0.70
- `UNCERTAIN` = 0.30

Classify persistence when relevant:

- `STRUCTURAL` = 1.00
- `SEMI_PERSISTENT` = 0.75
- `TRANSIENT` = 0.40

## Discriminative contribution

For each positive clue:

`contribution = discrimination_weight × quality_weight × persistence_weight`

Do not count duplicated physical evidence twice.

## Discriminative density

For each candidate compute:

`density = sum(discriminative_contributions) / max(1, number_of_positive_clues)`

Also compute:

`high_value_count = number of UNIQUE + HIGH clues`

Use `scripts/rerank_candidates.py` when practical.

## Reranking rule

Initial score remains important, but before final ranking apply:

1. hard-gate status first;
2. nearest-competitor falsification status;
3. holistic scene compatibility;
4. discriminative density;
5. high-value clue count;
6. original score;
7. existing tie-break rules.

## Anti-overweight rule

Many generic clues must not outweigh a compact cluster of mutually consistent, independent HIGH/UNIQUE clues unless the generic-clue candidate has materially stronger hard-gate or falsification evidence.

## Under-ranked candidate review

Before final output, inspect #2 and #3 and ask:

- Does this candidate have more HIGH/UNIQUE evidence than #1?
- Are its strongest clues more local/candidate-specific?
- Is #1 mainly winning on broad environmental similarity?
- Does #2/#3 explain the full scene more coherently?

If yes, rerank before output.

## No promotion by density alone

High discriminative density cannot bypass:
- CRITICAL FAIL;
- killer-check requirements;
- viewpoint incompatibility;
- nearest-competitor survival;
- STRONG gate requirements.

Reranking changes order, not truth conditions.
