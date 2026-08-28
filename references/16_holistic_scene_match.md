# 16 — Holistic Scene Match

Use when the image contains multiple independent structures or a broad environmental layout.

## Principle

A candidate must explain the scene as a configuration, not as a collection of isolated compatible clues.

Represent the scene using independent layers when visible:

- foreground geometry;
- primary structure or landmark;
- secondary structures;
- skyline or horizon profile;
- water/road/rail alignment;
- terrain and elevation pattern;
- vegetation/land-use boundary;
- relative object ordering;
- large-scale orientation.

## Holistic completeness

For a candidate to receive a holistic PASS:

1. no major visible layer contradicts the candidate;
2. at least three independent scene layers are compatible when three are observable;
3. the relative arrangement of major elements is coherent;
4. the candidate does not rely on one visually salient feature while ignoring the rest of the frame.

If fewer than three independent layers are observable, use all available layers and downgrade confidence accordingly.

## Salient-feature dominance guard

A landmark-like feature cannot by itself authorize STRONG when the surrounding scene contains testable geometry.

If the landmark matches but the scene configuration remains unverified, status is at most `PLAUSIBLE`.

## Scene-level mismatch

Treat a contradiction in large-scale scene organization as `MAJOR_MISMATCH` even when individual objects look similar.
