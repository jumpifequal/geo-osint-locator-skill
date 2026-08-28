# 04 — Scene Inventory and Fingerprint
If identifier fast-path did not produce STRONG, extract 8–20 macro clues.

Natural: coast/sea, terrain, mountains/hills, plains, vegetation, horizon, apparent climate, reliable light/shadows.
Built: road geometry/width/curvature/slope, paving, sidewalks, walls, barriers, rail, bridges, guard rails, lamps, signs, street furniture.
Architecture: volumes, geometry, symmetry, façade/openings, roof, materials, towers/domes/stairs, adjacent structures/relative placement.

Avoid unsupported style labels.

Output:
`[CERTAIN|PROBABLE|UNCERTAIN] — feature — geographic value`

Priority:
1 unique readable identifier
2 discriminative partial identifier
3 unique symbol/code
4 unique structural geometry
5 infrastructure standard
6 geographically specific natural feature
7 distinctive material/layout
8 generic resemblance

Tie-break:
`uniqueness → geographic specificity → observability → independence → reliability → input order`

Build:
- 3–8 Must-haves, each CRITICAL or SUPPORTING
- 3–8 Nice-to-haves
- 2–4 ambiguities
- exactly 3 decisive missing observations
