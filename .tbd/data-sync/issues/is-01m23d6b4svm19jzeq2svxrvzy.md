---
type: is
id: is-01m23d6b4svm19jzeq2svxrvzy
title: Make all generated-output drift checks deterministic
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - review-2026-09-09
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-09T15:39:41.592Z
updated_at: 2026-09-09T15:39:41.592Z
---
### F13 · P2 · Make Generated-Output Checks Reproducible

**Evidence:** `scripts/build.py` and `scripts/surfaces.py` insert today's date.
`.github/workflows/validate.yml` rebuilds and requires `site/` to be unchanged, including in a
weekly scheduled run. In an isolated copy, changing the date to September 10 changed the HTML
with unchanged data. The workflow also ignores drift in other committed generated outputs.

**Fix/acceptance:** separate content verification dates from build metadata; use deterministic
inputs for committed artifacts or exclude intentionally volatile metadata from comparisons.
Check all generated surfaces. The same source must pass drift checks on different days, while
an intentionally outdated output must fail. Freshness checks should still use real elapsed time.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
