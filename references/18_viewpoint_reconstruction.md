# 18 — Viewpoint Reconstruction

Use when the image contains geometry that can constrain where the camera was located or which direction it faced.

## Reconstruct only what is supportable

Estimate:
- camera side relative to major scene features;
- approximate viewing direction;
- foreground-to-background ordering;
- left/right ordering of stable landmarks;
- shoreline, road, rail, ridge, or building-axis orientation;
- relative elevation when visible.

Use coarse states rather than false precision:

- `COMPATIBLE`
- `INCOMPATIBLE`
- `ND`

## Candidate test

For each leading candidate ask:

1. Is there a physically plausible camera position that reproduces the observed ordering?
2. Does the candidate require impossible reversal, occlusion, shoreline side, or object ordering?
3. Are major stable features expected on the observed side of the frame?
4. Does map or satellite geometry support the inferred viewing direction when available?

If the answer is materially incompatible, reject or apply MAJOR_MISMATCH.

## No precision hallucination

Do not invent exact bearings, focal lengths, heights, or coordinates from a single image unless they are actually derivable.

Use maps or geometry scripts only to test candidate compatibility, not to manufacture precision.

## STRONG requirement

When viewpoint geometry is materially observable, `INCOMPATIBLE` blocks STRONG.
