# Changelog

## 1.1

### Last-mile verification
- separated area identification from exact camera-point verification;
- added locality states: `AREA_NARROWED`, `CAMERA_POINT_VERIFIED`, and `HUMAN_REVIEW_REQUIRED`;
- exact-place `STRONG` now requires `CAMERA_POINT_VERIFIED`;
- added candidate-specific last-mile geometry checks using map, aerial, spatial-relation, and viewpoint evidence;
- extended nearest-competitor falsification to exact camera-point evidence.

### Satellite / aerial verification
- added explicit satellite/aerial comparison guidance;
- added ESRI / ArcGIS World Imagery for high-resolution local structural comparison;
- added Copernicus / Sentinel for medium-resolution spatial and temporal comparison;
- added NASA Worldview / Earthdata for broad environmental and temporal context;
- added provider-neutral source-selection rules based on spatial scale and temporal role;
- added anti-confirmation rules requiring predicted geometry before imagery inspection;
- added temporal-mismatch handling so transient scene differences do not become false rejections.

### Mandatory unresolved-case escalation
- added mandatory satellite/aerial escalation whenever no clear winner emerges;
- requires all available source classes to be checked or explicitly marked `NOT_EXECUTED`;
- forbids early stopping after the first confirming imagery source;
- reruns nearest-competitor comparison and discriminative reranking after satellite/aerial checks;
- blocks decisive termination when an available source class remains unchecked.

### Output and controls
- added per-source satellite status reporting: `PASS`, `FAIL`, `ND`, or `NOT_EXECUTED`;
- added locality state to the deterministic SVG dashboard without changing its canonical layout;
- preserved existing scoring, CoVE, candidate ledger, prior firewall, and discriminative reranking logic.

## 1.0

Initial public repository packaging of Geo OSINT Locator.

### Core
- high-precision single-image geolocation workflow;
- geographic prior firewall;
- micro-forensic scanning and identifier fast-path;
- scene fingerprinting;
- candidate ledger;
- Chain-of-Verification;
- active evidence acquisition loop;
- expected-visibility / negative-evidence guard;
- spatial-configuration verification;
- nearest-competitor falsification;
- viewpoint reconstruction;
- killer-check specificity;
- discriminative reranking;
- exact-place STRONG gate;
- deterministic final SVG dashboard.

### Runtime helpers
- image geometry;
- geographic math;
- evidence ranking;
- spatial relations;
- prior guard;
- competitor gate;
- reranking;
- Nominatim lookup;
- Overpass lookup;
- SVG dashboard rendering.

### Repository
- GitHub-ready README;
- architecture documentation;
- usage examples;
- runtime-tool documentation;
- output-contract documentation;
- GitHub Actions validation workflow.
