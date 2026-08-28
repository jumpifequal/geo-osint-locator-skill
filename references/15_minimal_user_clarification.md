# 15 — Minimal User Clarification Gate

Use only when:
- STRONG has not passed;
- the active evidence loop has no remaining high-value executable check, or all such checks are unavailable;
- and one small piece of user-provided context could materially reduce uncertainty.

Do not use this gate merely because the task is difficult.

## Objective

Ask the smallest possible free-text question with the highest expected information gain.

## Question-selection rule

Prefer a question that separates the largest number of surviving hypotheses.

Rank candidate questions by:
1. expected elimination power;
2. likelihood the user actually knows the answer;
3. neutrality;
4. brevity.

Ask only one question at a time.

## Allowed question classes

Prefer one of:
- current country or broad macro-area;
- whether the scene was near sea/lake/river/mountains;
- remembered institution, park, road, monument, village, or district name;
- approximate travel context, when volunteered/known;
- whether the user has another photo of the same place from a different viewpoint;
- partial remembered text/signage.

## Forbidden questions

Do not ask:
- a list of many questions at once;
- leading questions such as `Era forse in Liguria?`;
- questions whose answer is already visible;
- private/sensitive information unrelated to geolocation;
- questions that encode a current candidate as if it were evidence;
- exact coordinates unless the user already has them and volunteers them.

## Free-text requirement

Ask naturally in one short sentence.

Good:
`Ricordi almeno il paese o una macro-area?`

Good:
`Hai un'altra foto dello stesso posto, anche da un'altra angolazione?`

Bad:
`Rispondi S/N: Italia? Francia? Svizzera?`

Bad:
`Compila: paese, regione, città, strada, data, ora.`

## After the answer

Treat the answer as:
- `USER_BOUNDED` if the user explicitly bounds the CURRENT image;
- otherwise as a hypothesis requiring verification.

Do not let the answer bypass the Geographic Prior Firewall, CoVE, killer checks, or STRONG gate.

If the answer adds no useful evidence, return `INDETERMINATE` or the best supported macro-area.

## No-answer fallback

If the user says they do not know:
- do not ask another question unless a distinctly different, high-information question exists;
- default to one total clarification question;
- then terminate with the best-supported uncertainty state.

## Output behavior

When invoking this gate, do not dump the whole internal analysis first.

Return:
`Mi manca un indizio discriminante. [single minimal free-text question]`
