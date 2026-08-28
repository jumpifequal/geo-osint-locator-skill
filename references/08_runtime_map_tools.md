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
