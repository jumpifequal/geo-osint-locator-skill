# Output Contract

The skill separates reasoning, verification and presentation.

## Normal result

A normal geolocation result may include:

1. fast verdict;
2. high-information evidence;
3. text extraction;
4. macro evidence;
5. scene fingerprint;
6. executed search/tool actions;
7. candidate verification;
8. active evidence loop summary;
9. conclusion;
10. ranked candidate table;
11. terminal SVG dashboard.

## Candidate ledger

When three genuine hypotheses were considered, all three remain visible in the final ledger even if one later becomes `WEAK` or `REJECTED`.

Do not display:

- `CONTEXT_ANCHORED` candidates;
- firewall-blocked candidates;
- artificial filler candidates.

## Terminal SVG dashboard

The SVG is the final visible block whenever rendering is available.

Layout is deterministic:

```text
┌────────────────────────────────────────────────────────────┐
│ #1 — Candidate / Area                         [STATUS]      │
│ Confidence     Score     High/unique clues    Holistic     │
│ value          value     value                value         │
│ Competitor · Killer check · Viewpoint                      │
└────────────────────────────────────────────────────────────┘
```

Candidate #1 has a blue outline.

Other candidate cards use a neutral outline.

The fixed fields are:

- rank;
- candidate / area;
- status;
- Confidence;
- Score;
- High/unique clues;
- Holistic match;
- Competitor;
- Killer check;
- Viewpoint.

If one decisive observation is still missing, one final line may appear under the cards:

```text
Decisive missing evidence: ...
```

## Clarification-only state

If analysis is genuinely stalled and one small user-known clue can materially reduce uncertainty, the skill asks exactly one minimal free-text question.

Example form:

```text
Mi manca un indizio discriminante. [single free-text question]
```

The clarification state replaces the normal full report for that turn.

## Fallback

If SVG rendering is not available, the Markdown dashboard becomes the final visible block.

The dashboard must preserve the same candidate order and core values.
