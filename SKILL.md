---
name: geo-osint-locator
description: 'High-precision image geolocation and GeoGuessr/OSINT localisation from
  one user-provided photo. Auto-trigger for requests such as: ''GeoGuess'', ''GeoGuessr'',
  ''where was this image/photo taken?'', ''where is this?'', ''what place is this?'',
  ''identify this place/landmark/building/road/coastline'', ''geolocate this image'',
  ''locate this photo'', ''verify this location''; and in Italian: ''geoguess'', ''geoguessr'',
  ''dove è stata scattata questa immagine/foto?'', ''dove siamo?'', ''che posto è
  questo?'', ''identifica questo luogo/monumento/edificio/strada/costa'', ''geolocalizza
  questa immagine'', ''trova dove è stata scattata'', ''verifica questa località''.
  Also trigger for image-based place verification using signs, architecture, terrain,
  skylines, roads, maps, crop/zoom inspection, CoVE, killer checks, competitor falsification,
  viewpoint reconstruction, or evidence-scored ranking.'
metadata:
  author: Enrico Frumento
  version: '1.0'
---

# Geo OSINT Locator

Localise or narrow the place shown in one image. Accuracy and falsifiability outrank coverage. Prefer `INDETERMINATE` to a plausible false positive.

## Mandatory execution order

1. Read `references/01_evidence_policy.md`.
2. Read `references/14_geographic_prior_firewall.md` before generating any geographic candidate.
3. Scan for high-information regions.
4. For small decisive regions, read `references/02_micro_forensics.md`; use `scripts/image_geometry.py` when useful.
5. For readable/partial identifiers, read `references/03_identifier_search.md` and run the identifier fast-path before generic candidates.
6. Read `references/04_scene_fingerprint.md`.
7. Read `references/05_candidate_cove.md`.
8. Read `references/16_holistic_scene_match.md` when the image contains a broad scene, skyline, waterfront, road system, or multi-object configuration.
9. Read `references/17_nearest_competitor_falsification.md` before promoting any candidate to STRONG.
10. Read `references/18_viewpoint_reconstruction.md` whenever scene geometry, skyline, shoreline, road direction, or landmark placement can constrain camera position.
11. Read `references/19_killer_check_specificity.md` before accepting any killer check as decisive.
12. Read `references/06_scoring_termination.md` before scoring or exact-place identification.
13. Read `references/09_information_gain.md`
14. Read `references/20_discriminative_reranking.md` before final ranking whenever 2 or more viable candidates remain. when more than one viable candidate remains or when deciding the next verification.
15. Read `references/10_visibility_negative_evidence.md` before using absence as contradiction.
16. Read `references/11_spatial_configuration.md` when candidate/reference geometry can be compared.
17. Read `references/12_cross_view_persistence_bias.md` when maps, satellite, seasonal/transient clues, or search-result abundance could affect judgment.
18. Read `references/13_active_evidence_loop.md` whenever STRONG has not passed after the first verification round.
19. Read `references/15_minimal_user_clarification.md` only when the evidence loop is exhausted or materially stalled and a small amount of user context could unlock a decisive check.
20. Read `references/07_output_contract.md` before answering.
21. Read `references/08_runtime_map_tools.md` only when map/geocoding/Overpass/coordinate operations are useful.

Do not skip required references because the image appears easy.

## Input
- One user-provided image.
- Optional context: treat as hypothesis.
- Optional mode: `STRICT` or `EXPLORE`; default `STRICT`.

## Mode
`STRICT`: max 3 viable candidates; reject critical contradictions; return `INDETERMINATE` if STRONG does not pass.
`EXPLORE`: 3–10 hypotheses only when evidence supports them; every candidate needs a discriminating test and killer check; never add filler.

## Conversation-history isolation

Treat each new geolocation image as a fresh geographic task.

Previous test locations, prior successful regions, earlier user corrections, and recent candidate countries/regions are `FORBIDDEN_PRIOR` unless the user explicitly states that the new image belongs to the same place or bounded area.

Do not use conversational recency as geographic evidence.

Before promoting any candidate, ask:

`Would I generate this candidate if this were the first image in the conversation?`

If `NO`, mark it `CONTEXT_ANCHORED` and remove or demote it until image-grounded evidence independently supports it.

## Tool discipline
Use native vision first. Do not default to OCR. For small text, crop/enlarge first with `scripts/image_geometry.py`, then visually inspect. OCR is last resort only if native inspection fails and OCR exists.

Use:
- `scripts/image_geometry.py`: crop, zoom, tile, dimensions.
- `scripts/geo_math.py`: distance, bearing, bbox.
- `scripts/evidence_rank.py`: deterministic next-test ranking by expected elimination value, reliability, independence, and execution cost.
- `scripts/spatial_relations.py`: derive and compare coarse geometric relations among visible features.
- `scripts/prior_guard.py`: validate candidate provenance and flag candidates supported only by conversation-history priors.
- `scripts/competitor_gate.py`: enforce nearest-competitor margin, holistic-match completeness, viewpoint compatibility, and killer-check specificity before STRONG.
- `scripts/rerank_candidates.py`: rerank viable candidates using discriminative density so several high-value local clues can outweigh many generic macro-clues.
- `scripts/map_lookup.py`: targeted Nominatim GET when outbound HTTP is allowed.
- `scripts/overpass_lookup.py`: targeted Overpass POST when outbound HTTP is allowed.

Never claim tool/network/map/reverse-image/street-level execution unless it actually happened. If unavailable, use `NOT_EXECUTED`.

## Exact-place lock
Only Section 06's STRONG gate authorises an exact-place answer. Text alone may create a candidate but cannot prove identity; text-derived candidates require independent non-textual physical corroboration.

## Evidence states
Use only `PASS | FAIL | ND | NOT_EXECUTED | SKIPPED`. `ND`, `NOT_EXECUTED`, and `SKIPPED` add zero affirmative evidence.


## Discriminative reranking

When 2 or more viable candidates remain, do not finalize ranking from raw score alone.

Before output:
- re-evaluate #1, #2, and #3 using `references/20_discriminative_reranking.md`;
- distinguish generic macro-clues from candidate-specific local clues;
- prefer candidates supported by a denser set of HIGH/UNIQUE discriminants when evidence quality is otherwise comparable;
- prevent many LOW/MEDIUM generic matches from overpowering fewer HIGH/UNIQUE local matches;
- explicitly review whether #2 or #3 is under-ranked before finalizing #1.

If reranking changes the order, use the reranked order in the user-visible table.


## Fixed terminal SVG template

The terminal SVG dashboard is visually deterministic.

Always render it through `scripts/dashboard_svg.py`.

Never improvise a new dashboard layout.

The fixed structure is:
- vertically stacked candidate cards;
- #1 candidate highlighted with blue outline;
- status badge at upper right;
- metric row in this order: Confidence, Score, High/unique clues, Holistic match;
- footer row: Competitor · Killer check · Viewpoint;
- optional final line: Decisive missing evidence.

Use the exact contract in `references/07_output_contract.md`.

## Terminal output invariant

For every normal geolocation result with at least one viable candidate, the response MUST end with the rendered Final Decision Dashboard SVG whenever SVG rendering is supported.

This is a hard output invariant:
- the SVG dashboard is the final visible block;
- do not place prose, notes, citations, questions, caveats, Markdown tables, headings, or follow-up offers after the SVG;
- complete all explanation, verification, citations, competitor analysis, and any textual table before the SVG;
- if SVG rendering is unsupported, fall back to the Markdown dashboard as the final visible block;
- if a minimal clarification question is required instead of a candidate result, the clarification-only contract may terminate without the dashboard;
- if no viable candidate survives and the result is INDETERMINATE, follow the INDETERMINATE/clarification contract rather than forcing an empty dashboard.

Before sending, perform a final serialization check:

`LAST_VISIBLE_BLOCK == FINAL_DECISION_DASHBOARD_SVG`

When SVG is unavailable:

`LAST_VISIBLE_BLOCK == FINAL_DECISION_DASHBOARD_TABLE`

If false, reorder the output before responding.

## Final decision dashboard

End every normal geolocation result with a compact `Final Decision Dashboard` whenever at least one viable candidate exists.

The dashboard is the final synthesis layer, not a replacement for the evidence analysis.

Requirements:
- show at most 3 viable candidates;
- keep the discriminatively reranked order;
- use one row per candidate;
- expose comparable metrics rather than prose-only summaries;
- include the leader and surviving alternatives even when the leader is STRONG;
- include rejected hypotheses when they belong to the top 3 genuinely considered candidates; exclude context-blocked and filler candidates;
- if no viable candidate survives, output `INDETERMINATE` instead of an empty dashboard;
- provide the Markdown table before the SVG when useful for textual accessibility;
- when the runtime can render or attach SVG, generate and show a compact SVG dashboard using `scripts/dashboard_svg.py` as the final visible block;
- SVG is the preferred terminal dashboard when supported. Place all textual content before it.

Use the exact dashboard schema defined in `references/07_output_contract.md`.

## Three-candidate visibility invariant

For every normal geolocation task without a unique/direct identifier lock, generate at least 3 non-filler candidate hypotheses before final falsification.

Maintain a `candidate ledger` containing the best 3 genuinely considered hypotheses.

The final user-visible dashboard MUST show 3 rows whenever 3 non-filler hypotheses were actually considered, even if one or more later become `WEAK` or `REJECTED`.

Rules:
- never hide #2/#3 merely because #1 is much stronger;
- do not drop a candidate from the dashboard solely because its final status is `REJECTED`;
- candidates blocked as `CONTEXT_ANCHORED` or otherwise forbidden by the geographic-prior firewall must not appear;
- do not invent filler candidates just to reach 3 rows;
- when fewer than 3 genuine hypotheses can be formed from available evidence, show the smaller number and state `INSUFFICIENT DISTINCT HYPOTHESES` in the dashboard status area;
- direct unique-identifier cases may produce fewer than 3 if alternatives would be artificial.

The dashboard is a record of the top hypotheses considered, not only of the surviving hypotheses.

## Ranked candidate visibility

Always preserve viable alternatives in the user-visible result.

Return a ranked table with up to 3 total candidates:
- `#1`: current leader;
- `#2` and `#3`: strongest surviving alternatives, when they exist.

Do not hide a viable candidate merely because it scores below #1.

Do not create filler candidates. If fewer than 3 evidence-supported candidates survive, show only those that survive.

A `REJECTED` candidate may remain visible in the final dashboard as a considered hypothesis. `CONTEXT_ANCHORED` or firewall-blocked candidates must not appear.

When #1 is STRONG, still show any genuinely surviving #2/#3 alternatives, but clearly mark why they rank lower.

## Candidate competition guard

Do not promote a candidate to `STRONG` merely because it accumulates many compatible clues.

Before `STRONG`, require all of the following:
- the candidate matches the scene holistically, not just one landmark or one feature family;
- at least one serious competing hypothesis has been actively tested when a plausible competitor exists;
- the leading candidate survives a candidate-specific falsification that the nearest competitor would fail or explain materially worse;
- viewpoint/camera-side geometry is compatible when scene geometry is observable;
- the killer check is discriminative against the nearest competitor, not merely compatible with the leader.

If the nearest competitor remains comparably plausible, return `TIED`, `PLAUSIBLE`, or `INDETERMINATE`; do not inflate confidence.

## Minimal user clarification

Do not ask the user questions during normal geolocation if the image, tools, or active evidence loop can still produce a meaningful next test.

Only when analysis is stalled or exhausted may you ask one minimal free-text question, chosen to maximize expected information gain.

The question must:
- be answerable in natural language;
- request only information the user may reasonably know;
- avoid asking for details already visible in the image;
- avoid leading the user toward a candidate;
- avoid exposing internal candidate bias;
- request one compact clue, not a questionnaire.

Examples:
- `Sai almeno in quale paese o macro-area è stata scattata?`
- `Ricordi se era vicino a un lago, fiume o mare?`
- `Hai un'altra foto dello stesso posto, anche da un'angolazione diversa?`
- `Ricordi il nome del parco, strada, edificio o località, anche solo parzialmente?`

If the user does not know, continue with `INDETERMINATE` rather than inventing certainty.

## Runtime economy
Prefer bundled scripts over reconstructing geometry, coordinate maths, evidence-ranking arithmetic, spatial-relation logic, URL encoding, or Overpass boilerplate.

When STRONG has not passed, do not run every conceivable check. Select the next check with the highest expected elimination value, execute it, update the candidate set, and repeat. Stop broad exploration as soon as STRONG passes or no useful check remains.
