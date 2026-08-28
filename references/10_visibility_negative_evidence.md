# 10 — Expected Visibility and Negative Evidence

Absence is evidence only when the feature should be visible from the current viewpoint.

Before treating a missing feature as contradiction, assign:

- `VISIBLE`: the feature should appear in this field of view if present.
- `POSSIBLY_OCCLUDED`: vegetation, architecture, terrain, vehicles, or perspective may hide it.
- `OUT_OF_FRAME`: geometry indicates the feature is outside the captured view.
- `UNKNOWN`: viewpoint or feature placement is insufficiently known.

## Negative-evidence rule

Only:

`EXPECTED_VISIBILITY = VISIBLE` + `feature absent`

may generate `FAIL` or a mismatch penalty.

For `POSSIBLY_OCCLUDED`, `OUT_OF_FRAME`, or `UNKNOWN`, absence is `ND`.

## Examples

Valid negative evidence:
- candidate reference shows a second façade opening exactly inside a clearly visible wall region, but the image shows continuous masonry there.

Invalid negative evidence:
- a known bell tower is absent, but the photograph crops the roofline where the tower would sit.
- a side chapel is not visible from a frontal view where another building could occlude it.

This gate takes precedence over mismatch scoring.
