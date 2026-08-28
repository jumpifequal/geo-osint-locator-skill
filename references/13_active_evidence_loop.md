# 13 — Active Evidence Acquisition Loop

Use whenever the first verification round does not produce STRONG.

## Loop

1. Re-run the geographic prior firewall; block any candidate that acquired support only from conversation history.
2. Rank surviving candidates.
3. Identify the highest-value disagreement among them.
4. Enumerate feasible checks that could resolve that disagreement.
5. Rank the checks using `references/09_information_gain.md`.
6. Execute only the best available check.
7. Update PASS/FAIL/ND states, candidates, score, and expected visibility.
8. Apply killer/rejection gates.
9. If STRONG passes, stop.
10. If no check has meaningful elimination value, stop and return the best supported macro-area or `INDETERMINATE`.
11. Otherwise repeat from step 1.

## Loop guardrails

- Maximum default loop depth: 6 decisive checks after initial candidate generation.
- Exceed 6 only when the user explicitly asks for exhaustive investigation or the next check is exceptionally decisive and cheap.
- Do not repeat a check against the same underlying evidence.
- Do not broaden the web search when a narrower candidate-specific falsifier is available.
- Do not keep searching merely to increase confidence after STRONG passes.
- Record every executed, unavailable, or skipped decisive action in the output.

## Termination states

- `STRONG`: exact place permitted.
- `EXHAUSTED`: useful checks exhausted; return macro-area or INDETERMINATE.
- `TIED`: candidates remain equivalent after available high-value checks.


## Clarification transition

When useful checks are exhausted but one user-known clue could plausibly resolve the remaining ambiguity, transition once to `references/15_minimal_user_clarification.md`.

Do not ask the user while a better image/tool/search check remains executable.
