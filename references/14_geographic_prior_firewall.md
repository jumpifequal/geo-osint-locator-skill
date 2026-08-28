# 14 — Geographic Prior Firewall

Use this module before generating geographic candidates for every new image.

## Default prior

Set:

`GEOGRAPHIC_PRIOR = GLOBAL`

unless the CURRENT image itself contains evidence that narrows geography.

The following are never geographic evidence by themselves:

- places identified in previous tests;
- recent successful countries/regions;
- user corrections from earlier images;
- previous assistant guesses;
- the fact that several earlier photos came from one region;
- search popularity or documentation density.

Classify all such context as:

`FORBIDDEN_PRIOR`

unless the user explicitly states that the CURRENT image belongs to the same bounded location set.

## Candidate provenance

Every candidate must have a provenance label:

- `IMAGE_DERIVED`: generated from current-image evidence.
- `SEARCH_DERIVED`: generated from a search based on current-image evidence.
- `USER_BOUNDED`: allowed only when the user explicitly bounds the current image geographically.
- `CONTEXT_ANCHORED`: candidate depends materially on previous-conversation geography.

`CONTEXT_ANCHORED` candidates must not be ranked or searched further until they acquire independent current-image support.

Use `scripts/prior_guard.py` to validate structured candidate records when practical.

## First-image counterfactual

Before promoting a candidate ask:

`Would I generate this candidate if this were the first image in the conversation?`

If `NO`:
- mark `CONTEXT_ANCHORED`;
- remove it from the active candidate set, or
- demote it to an unscored note until current-image evidence independently supports it.

## Weak-signal diversity gate

When:
- there is no readable unique identifier;
- there is no unique mapped object;
- and the current image does not strongly constrain country/region,

do not jump directly to a locality.

First generate at least 3 geographically distinct macro-hypotheses that explain the visible evidence.

Example:
`Western/Central European historic park`
`Northern Italian/French landscaped estate`
`Central European manor/cemetery sculpture setting`

These are hypothesis classes, not candidate locations.

Only convert a macro-hypothesis into a specific candidate after obtaining a candidate-generating clue.

## Iconography and style guard

Do not let uncertain iconography or broad architectural/art-historical style create a precise geographic prior.

Use:
`object interpretation → period/material/function → environment type → macro distribution → candidate generation`

not:
`object resembles X → familiar region → local candidate`.

## Search neutrality

Search queries must be derived from CURRENT-image evidence.

Before geography is supported, avoid inserting:
- previous region names;
- previous country names;
- nearby towns from prior tests.

Search broad-to-specific using object, material, iconography, landscape, and structural relations.

## Scoring rule

Conversation-history geography contributes:

`0 points`

to:
- Must-have;
- Nice-to-have;
- CoVE;
- killer checks;
- tie-breaks.

A candidate cannot become STRONG if any required support depends on `FORBIDDEN_PRIOR`.

## Debug check

Before final output confirm:

- no current candidate exists only because of earlier-test geography;
- no search query inherited a previous place name without current-image support;
- no candidate received a ranking advantage from conversational recency;
- weak-signal cases considered geographically distinct macro-hypotheses;
- the first-image counterfactual passes for the final candidate.
