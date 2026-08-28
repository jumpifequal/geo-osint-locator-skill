# Usage Examples

These examples demonstrate invocation patterns only. They are not location-answer templates.

## Direct GeoGuess request

```text
GeoGuess: where was this image taken?
```

Expected behavior:

- reset prior to global;
- inspect high-information regions;
- generate and verify candidates;
- preserve the top candidate ledger;
- return exact place only if STRONG passes.

## Italian direct request

```text
Dove è stata scattata questa foto?
```

The skill should trigger automatically.

## Landmark verification

```text
I think this is Building X. Can you verify the location from the image?
```

The user suggestion is treated as a hypothesis, not as ground truth.

The skill must still:

- verify physical geometry;
- test a serious alternative when one exists;
- reject the proposed identity if critical evidence fails.

## Ambiguous landscape

```text
Geolocate this landscape.
```

If no unique identifier exists, the skill should:

- build macro clues;
- generate multiple meaningful hypotheses;
- use discriminative reranking;
- preserve the candidate ledger;
- return a macro-area or INDETERMINATE if the exact-place gate does not pass.

## Minimal clarification

If image/tool evidence is exhausted and one user-known clue could unlock the case, ask one narrow question only.

Example shape:

```text
Mi manca un indizio discriminante. Ricordi almeno il paese o la macro-area?
```

Do not ask a questionnaire while a better executable check remains available.
