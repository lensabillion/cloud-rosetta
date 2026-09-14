---
type: is
id: is-01m23d6b4svm19jzeq2svxrvzy
title: Make all generated-output drift checks deterministic
kind: bug
status: closed
priority: 2
version: 4
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - review-2026-09-09
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-09T15:39:41.592Z
updated_at: 2026-09-14T13:32:41.354Z
closed_at: 2026-09-14T13:32:41.354Z
close_reason: "PR #6, commit 3adfcdf: all generated surfaces checked in isolation; deterministic source-date metadata; stale, missing, unexpected and failed-build probes covered. Four regression tests pass. GitHub data and link checks passed September 14."
resolution: null
duplicate_of: null
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

## Notes

PR #6 implements isolated comparison of all eight generated outputs, catches stale/missing/unexpected files and child-build failure, and compares identical output under two clock dates. Four regression tests and local data/style checks pass; awaiting GitHub CI before closure.
