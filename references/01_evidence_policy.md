# 01 — Evidence Policy
Visual certainty: `CERTAIN | PROBABLE | UNCERTAIN`.
Verification: `PASS | FAIL | ND | NOT_EXECUTED | SKIPPED`.
Text: `READABLE | PARTIAL | AMBIGUOUS | NOT_READABLE | NOT_EXECUTED`.

Rules:
1. Ground claims only in visible evidence, explicit user context, or actually executed verification.
2. User context is hypothesis, never ground truth.
3. Never invent letters, numbers, names, plates, symbols, brands, signs, architectural details, or geography.
4. Similarity alone is never identity.
5. ND/NOT_EXECUTED/SKIPPED never confirm.
6. CRITICAL FAIL rejects regardless of score.
7. Nice-to-have never rescues a rejected candidate.
8. Text-derived candidates require independent non-textual physical corroboration.
9. Never double-count one physical feature or one underlying source.
10. If evidence is insufficient, return `INDETERMINATE`.

Independent: inscription + façade; road layout + skyline.
Not independent: two crops of same sign; tower shape + silhouette; two sites reproducing same photo.
