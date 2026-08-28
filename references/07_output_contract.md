# 07 — Output Contract

## 0. Prior firewall
For each new image, internally confirm:
- `GEOGRAPHIC_PRIOR = GLOBAL` unless current-image evidence narrows it;
- previous-test locations are `FORBIDDEN_PRIOR`;
- final candidates pass the first-image counterfactual.

When a context-anchor was detected during analysis, expose a one-line note:
`Prior firewall: context anchor detected and removed.`
Use this order.

## 0. Fast verdict
`#1 — Candidate/Area — confidence — score/100 — strongest independent evidence`
If no STRONG: `INDETERMINATE — [specific missing evidence]`

## 1. High-information evidence
| Region | Value | Inspection | Observed content | Status |

## 2. Text extraction
Observed characters; alternative readings; inferred word; search hypotheses; confidence.

## 3. Macro evidence
8–20 tagged clues.

## 4. Fingerprint
CRITICAL Must-haves; SUPPORTING Must-haves; Nice-to-have; Top 3 discriminants; ambiguities; 3 decisive missing observations.

## 5. Search execution
`ACTION — EXECUTED | NOT_EXECUTED | SKIPPED — RESULT/REASON`
List actual queries only when executed.

## 6. Candidate verification
| Candidate | Critical MH | Identifier | Independent CoVE | Killer | Expected-visibility failures | Spatial configuration | Major mismatch | Score | Status |

## 7. Active evidence loop
When invoked, report:
- highest-value disagreement;
- next test selected;
- why it outranked alternatives;
- result;
- candidate-set update.

## 8. Conclusion
Best supported identification/INDETERMINATE; 3 strongest independent proofs; strongest contrary evidence; remaining uncertainty; next decisive check if needed.

Before output verify: high-value regions first; feasible multi-scale inspection; observed characters separated from inference; no invented text; identifier fast-path when applicable; no premature candidates; decisive checks executed or accounted for; text-derived identity physically corroborated; no double counting; neutral states never PASS; rejected candidates never revived; exact place only via STRONG; insufficient evidence → INDETERMINATE.


## Minimal clarification state

When the clarification gate is triggered, replace the normal full report with one concise line:

`Mi manca un indizio discriminante. [single free-text question]`

Resume the normal output contract only after the user answers or the task terminates.


## Candidate competition report

When an exact-place candidate is proposed, include:
- `Holistic scene match: PASS | FAIL | ND`
- `Viewpoint compatibility: COMPATIBLE | INCOMPATIBLE | ND`
- `Nearest competitor: [candidate/status]`
- `Differential check: [result]`
- `Killer specificity: UNIQUE | DISCRIMINATIVE | GENERIC`

Do not output STRONG if these gates do not permit it.


## Ranked candidate table

Always include a ranked table of up to 3 viable candidates after the fast verdict.

| Rank | Candidate / Area | Confidence | Score | Strongest supporting evidence | Main weakness / unresolved check | Status |
|---|---|---:|---:|---|---|---|

Rules:
- show #1 plus up to two strongest surviving alternatives;
- preserve #2/#3 even when #1 is STRONG, if they remain genuinely viable;
- show REJECTED candidates when part of the top candidate ledger; exclude context-blocked candidates;
- do not invent filler candidates;
- if only one candidate survives, show one row;
- if no candidate survives, show `INDETERMINATE` instead of an empty table;
- ranking must follow the candidate scoring and tie-break rules;
- when a lower-ranked candidate could still plausibly be correct, state the single check that would allow it to overtake #1.

This table is mandatory whenever at least one viable candidate exists.


## Reranking transparency

When 2 or more viable candidates remain, the ranked table must reflect discriminative reranking.

Add when useful:
- `Discriminative density`
- `HIGH/UNIQUE clue count`

If #2 or #3 moved upward after reranking, state:
`Reranked upward due to higher discriminative evidence density.`

Do not expose internal arithmetic unless it helps explain an unexpected ordering.


## Final Decision Dashboard

This is the mandatory final block whenever at least one viable candidate remains.

Render this table:

| Rank | Candidate / Area | Confidence | Score | Discriminative Density | High-Value Clues | Holistic | Viewpoint | Competitor | Killer | Status |
|---:|---|---:|---:|---:|---:|---|---|---|---|---|
| #1 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| #2 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |
| #3 | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

Rules:
- maximum 3 rows;
- keep #2/#3 when they were genuinely considered, even if later rejected;
- keep the final discriminatively reranked order;
- `Confidence` is a concise calibrated label or percentage/range;
- `Score` is the existing candidate score;
- `Discriminative Density` comes from the reranking layer when available;
- `High-Value Clues` is the count of HIGH + UNIQUE non-duplicate clues;
- `Holistic` uses PASS/FAIL/ND;
- `Viewpoint` uses COMPATIBLE/INCOMPATIBLE/ND;
- `Competitor` summarizes nearest-competitor state;
- `Killer` reports killer specificity/result compactly;
- `Status` uses STRONG / PLAUSIBLE / WEAK or the equivalent allowed final state;
- show rejected candidates if they are in the top candidate ledger; never show context-blocked candidates;
- do not invent filler rows.

### Optional rendered SVG

When the runtime can render or attach SVG, show the SVG after all textual content so it becomes the final visible block.

Use `scripts/dashboard_svg.py` with structured candidate data.

The SVG must:
- contain the same candidate ordering and core values as the Markdown table;
- show at most 3 candidates;
- remain readable without color alone;
- include text labels for status;
- avoid maps, invented coordinates, or unsupported geographic claims;
- be treated as a visualization of already-computed evidence, never as new evidence.

If SVG rendering is unsupported, skip SVG silently and keep the Markdown table as the final visible block.

## Terminal SVG Rule

The rendered Final Decision Dashboard SVG MUST be the last visible content of every normal candidate-bearing geolocation response when SVG rendering is supported.

Hard constraints:
1. complete explanation, evidence, verification, citations, competitor analysis, and optional Markdown dashboard first;
2. render the SVG dashboard last;
3. stop output immediately after the SVG;
4. do not append a conclusion, note, question, CTA, citation paragraph, heading, or Markdown table after the SVG;
5. keep maximum 3 candidate-ledger rows;
6. preserve the final discriminatively reranked candidate order;
7. the SVG must mirror the final candidate data already established in the analysis.

Final pre-send assertion:

`LAST_VISIBLE_BLOCK == FINAL_DECISION_DASHBOARD_SVG`

Fallback when SVG cannot be rendered or attached:

`LAST_VISIBLE_BLOCK == FINAL_DECISION_DASHBOARD_TABLE`

Exceptions:
- clarification-only output;
- INDETERMINATE output with no viable candidate and no meaningful dashboard row.


## Three-row candidate ledger

The final dashboard represents the top candidate ledger, not only surviving candidates.

When 3 genuine hypotheses were considered, render exactly 3 candidate rows in both the Markdown dashboard and the terminal SVG.

Allowed row statuses include:
- `STRONG`
- `PLAUSIBLE`
- `WEAK`
- `REJECTED`

Do not suppress a row because it is `REJECTED`; showing a rejected #2/#3 helps expose whether the correct answer was discovered but under-ranked.

Exclude:
- `CONTEXT_ANCHORED`
- firewall-blocked candidates
- artificial filler candidates

If fewer than 3 genuine hypotheses were ever available, render only those rows and visibly mark:
`INSUFFICIENT DISTINCT HYPOTHESES`

The SVG and Markdown candidate order must be identical.


## Fixed SVG Dashboard Contract

The final SVG dashboard has ONE canonical visual template. Do not redesign, restyle, reorder, or adapt the layout between runs.

Content may change. Layout must not.

### Candidate cards

Render up to 3 vertically stacked candidate cards in final ranked order.

For each candidate card, always show these elements in this exact order and hierarchy:

1. Candidate heading: `#rank — candidate / area`
2. Status badge aligned right: `STRONG | PLAUSIBLE | WEAK | REJECTED | INDETERMINATE`
3. Fixed four-column metric row:
   - `Confidence`
   - `Score`
   - `High/unique clues`
   - `Holistic match`
4. Fixed compact footer:
   - `Competitor: ... · Killer check: ... · Viewpoint: ...`

### Leader highlighting

Always highlight candidate #1 visually:
- blue outline;
- same white background as other cards;
- no ranking-dependent redesign beyond the highlight.

Other candidates:
- neutral light-gray outline;
- white background.

Status badges may use status-specific fill colors, but must keep the same badge geometry and right alignment.

### Final evidence line

When one decisive observation is still missing, place exactly one line below all cards:

`Decisive missing evidence: ...`

Do not insert explanatory prose inside the SVG beyond the fixed fields above.

### Deterministic rendering rule

Use `scripts/dashboard_svg.py` for the terminal SVG.

Do not hand-author an alternative SVG.

Do not:
- change to a table layout;
- switch to columns;
- move labels between runs;
- add/remove metrics ad hoc;
- change card geometry based on content;
- use a different visual style because of status or candidate count;
- add icons, charts, maps, bars, gauges, or decorative graphics.

If a field is unavailable, render `—` or the allowed neutral state (`ND` / `NOT_EXECUTED`) in its fixed slot.

The SVG is a visualization of already-computed evidence, not a new reasoning layer.
