# Architecture

Geo OSINT Locator is a forensic verification pipeline for image geolocation.

Its governing rule is:

> **Ground claims only in visible evidence or executed verification. Similarity is not identity.**

## Visual doctrine

<p align="center">
  <img src="assets/slides/core-directive.png" alt="Deduction not prediction: core directive" width="92%">
</p>

Three rules govern the entire system: **visible evidence only**, **similarity is not identity**, and **text-derived candidates require independent physical corroboration**.

## 1. Ingestion and prior firewall

<p align="center">
  <img src="assets/slides/geographic-prior-firewall.png" alt="Geographic Prior Firewall" width="92%">
</p>

The diagram above makes the anti-anchoring rule explicit: conversation-history geography is blocked unless the same candidate can be independently generated from the current image.


Every image begins with a geographic reset.

```text
GEOGRAPHIC_PRIOR = GLOBAL
```

Conversation-history geography is forbidden as evidence unless the user explicitly bounds the current image.

The first-image counterfactual is mandatory:

> Would this candidate still be generated if this were the first image in the conversation?

If not, the candidate is `CONTEXT_ANCHORED` and cannot progress until current-image evidence independently supports it.

## 2. Micro-forensics

<p align="center">
  <img src="assets/slides/micro-forensics.png" alt="Micro-forensics and identifier fast-path" width="92%">
</p>

The visual fast-path separates what is actually readable from what is merely inferred, and emphasizes multi-scale inspection before declaring decisive text unreadable.


The image is scanned for compact, high-information regions:

- route codes;
- plaques;
- signs;
- business names;
- facade details;
- flags;
- road markings;
- distinctive infrastructure.

For small decisive regions, the skill uses multi-scale inspection:

```text
CONTEXT_CROP
→ TIGHT_CROP
→ MAX_USEFUL_ZOOM
→ SECOND_PASS
```

Observed characters, inferred words and search hypotheses remain separate.

## 3. Scene fingerprinting

If no unique identifier is available, the model extracts a macro fingerprint across independent layers:

- natural environment;
- built environment;
- architecture;
- road form;
- terrain;
- vegetation;
- skyline;
- water / coastline;
- settlement morphology;
- object configuration.

The goal is not to collect many clues. It is to identify the clues with the highest discriminative value.

## 4. Candidate ledger

The skill maintains a ledger of meaningful candidate hypotheses.

In ambiguous scenes, it attempts to create at least three non-filler hypotheses before aggressive elimination.

Candidate provenance must be one of:

- `IMAGE_DERIVED`
- `SEARCH_DERIVED`
- `USER_BOUNDED`
- `CONTEXT_ANCHORED`

Only the first three can become active candidates.

## 5. Chain of Verification (CoVE)

<p align="center">
  <img src="assets/slides/verification-pipeline.png" alt="End-to-end verification pipeline" width="92%">
</p>

The end-to-end view shows the five locked stages: ingestion/firewall, micro-forensics, hypothesis generation, falsification/verification, and the output contract.


A candidate should survive multiple independent evidence channels.

Possible channels include:

- facade geometry;
- skyline geometry;
- road layout;
- coastline / shoreline;
- object arrangement;
- mapped geometry;
- satellite structure;
- non-textual physical corroboration.

Two crops of the same sign are not two independent channels.

## 6. Spatial configuration and persistence

Identity often emerges from the joint geometry of multiple generic features.

Useful relations include:

```text
LEFT_OF
RIGHT_OF
ABOVE
BELOW
OVERLAPS
INSIDE
NEAR
FAR
ALIGNED_HORIZONTAL
ALIGNED_VERTICAL
```

Evidence is also weighted by persistence:

| Class | Weight | Examples |
|---|---:|---|
| STRUCTURAL | 1.00 | facade geometry, road alignment |
| SEMI_PERSISTENT | 0.75 | paint, vegetation form, signage |
| TRANSIENT | 0.40 | parked cars, temporary objects, weather |

## 7. Expected visibility and negative evidence

<p align="center">
  <img src="assets/slides/expected-visibility.png" alt="Expected visibility and negative evidence" width="92%">
</p>

Negative evidence only counts when a feature should physically be visible. Occlusion and out-of-frame states remain neutral instead of becoming false mismatches.


Absence is evidence only when the feature should physically be visible from the current viewpoint.

| Expected visibility | Feature absent | Result |
|---|---|---|
| `VISIBLE` | yes | `FAIL` / mismatch |
| `POSSIBLY_OCCLUDED` | yes | `ND` |
| `OUT_OF_FRAME` | yes | `ND` |
| `UNKNOWN` | yes | `ND` |

This avoids penalizing candidates for hidden or out-of-frame features.

## 8. Active evidence loop

<p align="center">
  <img src="assets/slides/active-evidence-loop.png" alt="Active Evidence Loop" width="92%">
</p>

The loop prioritizes the next check by expected elimination value rather than convenience: rerun the firewall, identify the highest-value disagreement, rank tests, execute the best one, and update candidate states.


When the first round does not produce STRONG:

```text
Re-run firewall
→ rank candidates
→ identify highest-value disagreement
→ enumerate feasible tests
→ rank tests
→ execute best test
→ update states
→ apply rejection gates
→ repeat
```

Default maximum depth: six decisive checks after initial candidate generation.

The goal is to maximize uncertainty reduction per unit execution cost.

## 9. Nearest-competitor falsification

<p align="center">
  <img src="assets/slides/competitor-falsification.png" alt="Nearest competitor falsification and killer check specificity" width="92%">
</p>

A killer check must separate the leader from its nearest competitor. Generic compatibility cannot authorize a STRONG result.


Before a candidate becomes STRONG, identify the strongest plausible alternative and run a differential test.

A valid differential check:

- predicts different outcomes for the two candidates;
- is observable or verifiable;
- has high elimination power;
- is independent of the evidence that originally generated the leader;
- is specific enough that both candidates should not pass for the same reason.

A numerical score margin alone is not sufficient.

## 10. Killer-check specificity

Killer checks are classified as:

- `UNIQUE`
- `DISCRIMINATIVE`
- `GENERIC`

Only `UNIQUE` or `DISCRIMINATIVE` killer checks can satisfy the STRONG gate.

A useful question is:

> Would the nearest competitor also plausibly pass this check?

If yes, it is not a decisive killer.

## 11. Viewpoint reconstruction

When geometry permits it, reconstruct:

- camera side;
- foreground/background order;
- left/right landmark ordering;
- shoreline / road / rail direction;
- relative elevation;
- structural axes.

A viewpoint may be:

- `COMPATIBLE`
- `INCOMPATIBLE`
- `ND`

`INCOMPATIBLE` blocks STRONG.

## 12. Search-abundance bias guard

Search-result abundance is not geographic evidence.

A frequently photographed location cannot outrank a poorly documented location merely because search engines expose it more often.

## 13. Discriminative reranking

<p align="center">
  <img src="assets/slides/discriminative-reranking.png" alt="Discriminative reranking" width="92%">
</p>

The reranker intentionally favors compact clusters of UNIQUE/HIGH, persistent clues over larger piles of generic matches, while preserving the candidate ledger for auditability.


For each positive clue:

```text
contribution =
discrimination_weight
× quality_weight
× persistence_weight
```

Discrimination:

```text
UNIQUE = 4
HIGH   = 3
MEDIUM = 2
LOW    = 1
```

Quality:

```text
CERTAIN   = 1.00
PROBABLE  = 0.70
UNCERTAIN = 0.30
```

The final ordering prioritizes:

1. hard-gate status;
2. nearest-competitor falsification;
3. holistic scene compatibility;
4. discriminative density;
5. HIGH / UNIQUE clue count;
6. original score;
7. remaining tie-break rules.

## 14. STRONG gate

<p align="center">
  <img src="assets/slides/strong-gate.png" alt="STRONG gate and minimal clarification" width="92%">
</p>

The STRONG gate is conjunctive: score alone is never sufficient. If the gate cannot close and no better executable check remains, the system falls back to one minimal discriminative question.


An exact-place answer is permitted only if **all** gate conditions pass:

1. score ≥ 80;
2. every critical must-have PASS;
3. at least two independent CoVE channels PASS;
4. at least one UNIQUE or DISCRIMINATIVE killer PASS;
5. no unresolved major mismatch;
6. decisive verification is executed or explicitly accounted for;
7. text-derived identity has independent non-textual physical corroboration;
8. holistic scene match PASS when broad geometry is observable;
9. viewpoint is not INCOMPATIBLE when geometry is observable;
10. nearest competitor is REJECTED, materially WEAKER, or absent after targeted search.

## 15. Output layer

<p align="center">
  <img src="assets/slides/output-dashboard.png" alt="Deterministic SVG output dashboard" width="92%">
</p>

The final dashboard exposes the top candidate ledger in a fixed layout. Rejected alternatives remain visible for auditability; content changes, layout does not.


The final answer exposes the ranked candidate ledger and ends with a deterministic SVG dashboard when rendering is supported.

The dashboard is only a visual ledger of already-computed evidence.

It must never become a new reasoning layer.


## Source presentation

The full technical slide deck is retained as a secondary deep-dive artifact. The main architecture diagrams are also embedded directly in the Markdown documentation, so readers do not need PowerPoint to understand the system.
