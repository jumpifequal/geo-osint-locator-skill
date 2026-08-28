# 02 — Micro-Forensics
Before generic analysis, scan for signs, plaques, inscriptions, labels, route codes, monument boards, business names, coats of arms, flags, vehicle markings, distinctive façade details, unique objects.

Rank regions `VERY_HIGH | HIGH | MEDIUM | LOW`. Process VERY_HIGH/HIGH first.

For each high-value region perform all feasible passes:
1. CONTEXT_CROP
2. TIGHT_CROP
3. MAX_USEFUL_ZOOM
4. SECOND_PASS

Prefer `scripts/image_geometry.py`. Do not mark decisive text NOT_READABLE until feasible passes are exhausted.

Keep separate:
- `OBSERVED_CHARACTERS`
- `INFERRED_WORD`
- `SEARCH_HYPOTHESIS`

Use `?` for unknown characters. Retain up to 3 genuine alternative readings. Never report an inferred/search word as observed text.

Resizing/sharpening/contrast may aid inspection but cannot create new evidence.
