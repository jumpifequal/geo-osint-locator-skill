# 09 — Information Gain and Next-Test Priority

Use this module when more than one viable candidate remains or when deciding what to verify next.

## Goal

Choose the next observation or external check that is expected to eliminate the most uncertainty per unit cost.

Do not confuse evidence confidence with discriminative value. A clue can be certain but geographically generic.

## Discrimination class

Assign each usable clue or proposed test:

- `UNIQUE`: likely to isolate one candidate or tiny candidate set.
- `HIGH`: likely to eliminate most surviving candidates.
- `MEDIUM`: separates some candidates.
- `LOW`: weakly informative or common.

Evaluate discrimination relative to the current candidate set, not globally.

## Next-test ranking

For each proposed test estimate:

- `elimination_power`: 0–4
- `reliability`: 0–4
- `independence`: 0–4
- `execution_cost`: 1–4
- `availability`: `AVAILABLE | UNAVAILABLE`

Prefer tests with high elimination power, reliability, and independence, and low cost.

Use `scripts/evidence_rank.py` when several tests compete.

## Hard rules

- A cheap LOW-value test must not outrank a decisive HIGH/UNIQUE test merely because it is easy.
- Prefer the fastest falsifier of the current leader when its elimination value is comparable.
- Do not repeatedly test the same underlying physical feature.
- Stop adding tests once STRONG passes.
