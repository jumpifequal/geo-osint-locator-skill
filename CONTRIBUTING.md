# Contributing

Contributions should preserve the skill's central invariant:

> Accuracy and falsifiability outrank coverage.

## Before changing execution logic

1. Identify the behavioral invariant being changed.
2. Explain the failure mode the change addresses.
3. Avoid benchmark-specific hard-coding.
4. Keep current-image evidence separate from conversational priors.
5. Do not weaken STRONG-gate conditions merely to increase exact-place answer rate.
6. Preserve candidate-ledger auditability.
7. Preserve deterministic dashboard layout unless the output contract is intentionally versioned.

## Script changes

For Python changes:

```bash
python tools/validate_repo.py
```

Any new deterministic helper should include a small executable regression check in the repository validator or CI.

## Documentation changes

Documentation may explain the architecture in simpler language, but must not contradict `SKILL.md` or the numbered reference modules.

When in doubt, the skill package is canonical.
