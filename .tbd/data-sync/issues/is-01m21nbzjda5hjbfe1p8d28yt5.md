---
type: is
id: is-01m21nbzjda5hjbfe1p8d28yt5
title: Self-test drills
kind: task
status: open
priority: 1
version: 2
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - guide
  - review-2026-09-09
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-08T23:24:06.092Z
updated_at: 2026-09-09T23:14:06.542Z
---
Recall drills and answer keys covering the mappings and traps.

## Notes

### F11 · P1 · Stop Flashcards From Teaching Unqualified Equivalence

**Evidence:** `scripts/surfaces.py:drills_tsv` emits a name-equivalence card even for `none`
rows. The answer lists service names without the divergence warning; the caveat is a separate
card. Studying the first card alone teaches the assumption the project warns against.

**Fix/acceptance:** put the grade, critical distinction, and source on every relevant answer.
Use scenario questions for non-equivalents; keep factual recall for names. Add worked answers,
wrong-answer reasoning, prerequisite links, and a no-account practice path. Publish the TSV
with import instructions. Extend existing bead `cloud-50j2` rather than duplicating it.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
