# Camera-Point Verification

## Purpose

Separate correct area identification from correct camera-point identification.

The workflow uses three explicit locality states:

- `AREA_NARROWED`
- `CAMERA_POINT_VERIFIED`
- `HUMAN_REVIEW_REQUIRED`

`STRONG` exact-place output is allowed only when the leader reaches `CAMERA_POINT_VERIFIED`.

## Last-mile pipeline

Use this sequence after the broader area is credibly narrowed:

```text
AREA_NARROWED
→ candidate camera point(s)
→ aerial/map geometry check
→ relational feature check
→ viewpoint reconstruction
→ nearest-competitor differential check
→ CAMERA_POINT_VERIFIED | unresolved
```

## Camera-point checks

Use only checks supported by current-image evidence and actually available tools.

Useful channels include:

- road / rail / shoreline alignment;
- relative object ordering;
- building-footprint geometry;
- intersection shape;
- bridge / track / path proximity;
- distance and side-of-feature relations;
- terrain and elevation consistency;
- aerial/satellite footprint corroboration;
- OSM feature relationships;
- camera-side compatibility;
- foreground/background ordering.

## Aerial imagery

Treat aerial imagery as a provider-agnostic capability.

Do not hard-code one vendor as mandatory.

Aerial imagery is supporting evidence, not ground truth.

If unavailable, mark the check `NOT_EXECUTED`.

## Relational OSM verification

Prefer queries that test relationships, not only object existence.

Examples of relation classes:

- feature A near feature B;
- road parallel to rail;
- building inside / adjacent to site boundary;
- path crossing water;
- viewpoint west/east/north/south of a structural feature;
- object within a constrained distance band from another mapped object.

The relation must be predicted from the image first, then tested.

Do not search relationally for arbitrary configurations until something matches.

## Verification rule

A candidate camera point may become `CAMERA_POINT_VERIFIED` only if:

1. the area is already supported;
2. no critical hard gate fails;
3. at least one candidate-specific geometric relation is verified;
4. viewpoint is not `INCOMPATIBLE`;
5. the nearest serious competitor is rejected or materially weaker on the same last-mile evidence;
6. no unresolved contradiction remains that could move the camera point materially.

A score margin alone is insufficient.

## Human-review gate

Set `HUMAN_REVIEW_REQUIRED` only when one of these is true:

- exact coordinates are explicitly requested and camera-point verification remains unresolved;
- the use case is high-stakes and exact location affects a real-world decision;
- available tools cannot execute the decisive last-mile check;
- contradictory geometry remains after the active evidence loop.

Do not use this state merely because confidence is imperfect.

If an area-level answer is sufficient, return `AREA_NARROWED` instead.

## Output semantics

- `AREA_NARROWED`: credible locality, exact camera point not verified.
- `CAMERA_POINT_VERIFIED`: last-mile verification succeeded.
- `HUMAN_REVIEW_REQUIRED`: automation cannot responsibly close exact-point uncertainty.

These states are orthogonal to candidate ranking and should not erase the candidate ledger.


## Satellite / aerial source policy

For last-mile verification, consult `references/22_satellite_aerial_sources.md`.

Use imagery sources according to required spatial scale and temporal role.

Preferred classes:
- high-resolution ESRI / ArcGIS World Imagery for local geometry and camera-point corroboration;
- Copernicus / Sentinel imagery for open medium-resolution spatial and temporal comparison;
- NASA Worldview / Earthdata for broad environmental and temporal context.

The candidate and predicted geometry must exist before imagery inspection.

Satellite/aerial imagery must never be used as an unconstrained similarity search.
