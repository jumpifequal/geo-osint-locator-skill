# Satellite and Aerial Comparison Sources

## Purpose

Use satellite/aerial imagery as a candidate-specific verification channel for last-mile geolocation.

The objective is not to browse imagery until something looks similar.

The image must first produce a candidate and one or more predicted spatial relationships. Satellite/aerial imagery is then used to test those predictions.

## Preferred source order

### 1. ESRI / ArcGIS World Imagery

Preferred high-resolution visual comparison source when available.

Use for:
- building footprint comparison;
- courtyard and compound geometry;
- road / rail / shoreline alignment;
- object-to-structure relationships;
- candidate camera-point orientation;
- exact-site corroboration.

Treat it as a composite imagery source whose acquisition date and underlying provider may vary by location.

Do not assume the displayed image is current.

If acquisition date or source metadata is available, record it.

### 2. Copernicus Browser / Sentinel imagery

Use when temporal context or open satellite coverage is more important than very high spatial resolution.

Useful for:
- land-cover structure;
- coastline or river geometry;
- large road / rail patterns;
- vegetation and agricultural layout;
- change over time;
- cloud / snow / fire / flood context;
- cross-date comparison.

Do not use Sentinel-scale imagery as decisive evidence for small architectural details that fall below useful spatial resolution.

### 3. NASA Worldview / Earthdata imagery

Use as a complementary global source, especially for:
- broad terrain and environmental context;
- recent or historical environmental conditions;
- large-scale land-cover patterns;
- fires, floods, snow, smoke, dust, water conditions;
- temporal comparison.

Do not use coarse environmental imagery as an exact-building identity check.

## Source selection rule

Choose the imagery source based on the scale of the feature being tested.

- Building / courtyard / local road geometry -> prefer highest-resolution aerial/satellite imagery available.
- Area / terrain / coastline / agricultural pattern -> medium-resolution imagery may be sufficient.
- Environmental / temporal state -> use time-aware Earth-observation sources.

Do not select a source merely because it is familiar or visually attractive.

## Comparison protocol

Before opening satellite/aerial imagery:

1. state the candidate;
2. state the predicted geometry;
3. state what would falsify the candidate;
4. select the imagery source appropriate to the required spatial scale;
5. compare only the relevant geometry;
6. record PASS / FAIL / ND / NOT_EXECUTED.

Valid examples of predicted geometry:
- rectangular courtyard east of main building;
- road bends south of rail line;
- shoreline lies behind the visible structure;
- pylon stands west of railway;
- building cluster aligned along one road axis.

## Anti-confirmation guard

Satellite imagery must not become a free-form visual search channel.

Forbidden:
- scanning broad imagery until a convenient match appears;
- changing the predicted geometry after seeing the satellite image without recording the change;
- treating generic resemblance as identity;
- ignoring date/resolution mismatch;
- claiming exact-point verification when the imagery cannot resolve the relevant feature.

## Temporal mismatch

Satellite/aerial sources may be older or newer than the user image.

A mismatch involving:
- parked vehicles;
- seasonal vegetation;
- temporary structures;
- construction state;
- shadows;
- surface markings

must not automatically reject a candidate.

Structural geometry remains higher-value evidence.

## Evidence role

Satellite/aerial imagery is supporting evidence, not ground truth.

It may contribute to `CAMERA_POINT_VERIFIED` only when:
- the compared geometry was predicted before inspection;
- the relevant feature is resolvable at the source's spatial scale;
- the imagery is compatible with the candidate viewpoint;
- the nearest serious competitor does not pass the same test equally well.

## Runtime truthfulness

If the runtime cannot access or render the selected imagery source:
- mark the check `NOT_EXECUTED`;
- do not narrate a hypothetical satellite comparison;
- continue with other available evidence channels.

## Provider neutrality

The skill must not depend on one commercial provider.

ESRI / ArcGIS World Imagery is a preferred comparison source because it can expose high-resolution satellite and aerial imagery across many regions.

Copernicus and NASA sources provide complementary open Earth-observation coverage and temporal context.

If another provider is available in the active runtime, it may be used if it supports the same evidentiary role and the same comparison protocol.


## Mandatory multi-source escalation when no clear winner exists

If the standard verification pipeline does not produce a clearly dominant leader, satellite/aerial escalation is mandatory.

Trigger this escalation when ANY of the following is true:
- two or more candidates remain materially plausible;
- the nearest competitor is not `REJECTED` or clearly `WEAKER`;
- candidate ordering still depends mainly on generic clues;
- the leader has not reached `CAMERA_POINT_VERIFIED`;
- the score margin is insufficient to establish a decisive differential;
- the active evidence loop stalls without a candidate-specific winner.

When triggered, use **all available source classes**, not just one:

1. ESRI / ArcGIS World Imagery
2. Copernicus / Sentinel imagery
3. NASA Worldview / Earthdata imagery

For each source class:
- formulate the candidate-specific geometry to test before inspection;
- perform the comparison if technically available;
- record `PASS`, `FAIL`, `ND`, or `NOT_EXECUTED`;
- preserve source independence: one provider's result does not substitute for the others.

The escalation is complete only when every source class has either:
- been actually checked, or
- been explicitly marked `NOT_EXECUTED` with the technical reason.

Do not stop after the first confirming satellite source.

The objective is cross-source corroboration and competitor discrimination, not confirmation of the current leader.
