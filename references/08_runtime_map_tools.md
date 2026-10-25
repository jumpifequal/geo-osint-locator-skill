# 08 — Runtime Map and Geometry Tools
Load only when coordinate/map/geocoding/OSM operations are useful.

`image_geometry.py`: deterministic crop, enlargement, tiling, dimensions, fractional boxes. Interpolation never creates evidence.
`geo_math.py`: haversine distance, initial bearing, coordinate bounding box.
`map_lookup.py`: targeted Nominatim GET. Commands: search QUERY; reverse LAT LON.
`overpass_lookup.py`: targeted Overpass POST around a known hypothesis.

HTTP rules:
- outbound HTTP must be allowed
- use descriptive User-Agent
- no bulk scraping
- use narrow, targeted queries
- reuse results in-task
- on failure report NOT_EXECUTED/tool failure, never fabricate
- map/API result is evidence, not truth; corroborate with image evidence


## Aerial imagery capability

When the runtime provides aerial/satellite imagery, use it as a last-mile corroboration channel.

Requirements:
- provider-agnostic;
- current candidate must already exist before the imagery check;
- verify predicted geometry rather than browse until a visual match appears;
- treat imagery as supporting evidence, not truth;
- if unavailable, use `NOT_EXECUTED`.

## Relational OSM verification

Use relational map queries when exact camera-point verification benefits from checking spatial relationships between visible features.

Prefer narrow, hypothesis-driven relations such as:
- `near`
- `within`
- `parallel`
- `crosses`
- `adjacent`
- `inside`
- directional side/orientation constraints

Do not use broad relation mining as a substitute for image-derived hypotheses.


## Satellite / aerial comparison sources

See `references/22_satellite_aerial_sources.md`.

When available, use:
- ESRI / ArcGIS World Imagery for high-resolution structural comparison;
- Copernicus Browser / Sentinel imagery for medium-resolution and temporal comparison;
- NASA Worldview / Earthdata imagery for broad environmental and temporal context.

Select the source according to feature scale.

Do not claim a satellite check was performed unless imagery was actually retrieved or viewed in the active runtime.
