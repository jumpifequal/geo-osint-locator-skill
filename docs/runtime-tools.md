# Runtime Tools

Geo OSINT Locator uses native visual reasoning first and deterministic helpers where repeatability matters.

## Image geometry

`scripts/image_geometry.py`

Use for:

- image dimensions;
- crop extraction;
- fractional bounding boxes;
- zoom;
- tiling.

Do not treat digital enlargement as new evidence. Enlargement improves inspection only.

## Geographic math

`scripts/geo_math.py`

Use for:

- Haversine distance;
- initial bearing;
- coordinate bounding boxes.

## Evidence ranking

`scripts/evidence_rank.py`

Ranks candidate verification actions by expected value.

The skill prefers checks with:

- high elimination power;
- high reliability;
- high independence;
- low execution cost.

## Spatial relations

`scripts/spatial_relations.py`

Derives coarse object relationships and supports spatial-configuration comparison.

## Prior guard

`scripts/prior_guard.py`

Checks candidate provenance and prevents conversation-history geography from silently entering scoring.

## Competitor gate

`scripts/competitor_gate.py`

Evaluates STRONG-gate conditions involving:

- score threshold;
- critical must-haves;
- independent CoVE passes;
- killer specificity;
- holistic match;
- viewpoint compatibility;
- nearest-competitor status;
- major mismatches;
- physical corroboration.

## Discriminative reranking

`scripts/rerank_candidates.py`

Reranks candidates using discriminative density and high-value clue count.

It changes candidate order only.

It does not bypass hard rejection or STRONG gates.

## Map lookup

`scripts/map_lookup.py`

Provides targeted Nominatim lookup when outbound HTTP is available.

A map/API result is evidence, not truth, and must be corroborated against the image.

## Overpass lookup

`scripts/overpass_lookup.py`

Provides targeted Overpass queries around known hypotheses.

Do not use it as bulk scraping.

## Dashboard renderer

`scripts/dashboard_svg.py`

Renders the canonical final candidate dashboard as SVG.

The renderer is intentionally deterministic: content changes, geometry does not.

## Tool-use truthfulness

The skill never treats:

```text
READ == EXECUTED
ANALYSED == EXECUTED
VISIBLE == VERIFIED
```

If an operation did not run, report `NOT_EXECUTED`.
