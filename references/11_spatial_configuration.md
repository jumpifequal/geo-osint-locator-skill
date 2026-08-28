# 11 — Spatial Configuration Verification

Use when individual features are not unique enough but their arrangement may be.

## Represent relations

Record coarse relations among stable features:

- `LEFT_OF`
- `RIGHT_OF`
- `ABOVE`
- `BELOW`
- `OVERLAPS`
- `INSIDE`
- `NEAR`
- `FAR`
- `ALIGNED_HORIZONTAL`
- `ALIGNED_VERTICAL`

Examples:
- relief `RIGHT_OF` portal
- rose window `ABOVE` portal
- annex `RIGHT_OF` façade
- mountain ridge `LEFT_BACKGROUND` of building

Use `scripts/spatial_relations.py` when bounding boxes can be approximated.

## Matching rule

A candidate gains spatial verification only when several relations are jointly preserved.

Do not count each relation as a fully independent CoVE channel if all relations derive from the same object pair. Treat the configuration as one physical-evidence channel unless it spans genuinely separate structures.

## Strong use cases

- churches and monuments with repeated architectural motifs;
- intersections and road geometry;
- neighbouring-building placement;
- skyline/object ordering;
- façade asymmetry.

Spatial configuration can be a killer check when the relation is candidate-specific and clearly visible.
