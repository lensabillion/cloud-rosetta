---
type: is
id: is-01m23d5q1ffg33r07p9jm5nckt
title: Fix decoder filters and add stable links and recoverable search
kind: bug
status: open
priority: 2
version: 1
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - review-2026-09-09
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-09T15:39:21.007Z
updated_at: 2026-09-09T15:39:21.007Z
---
### F08 · P2 · Make Search, Filters, and Links Predictable

**Evidence:** the decoder leaves “Only what misleads” and “Only what hurts” visible. Clicking
changes their pressed state but leaves 16/16 terms; `apply()` filters decoder content by search
only. Search/filter/view state is absent from the URL, mapping articles lack stable IDs, related
term references are plain text, and there is no clear-all action.

**Fix/acceptance:** hide irrelevant filters or implement term-specific severity filters; show
active filters with a clear-all action. Add stable row/term anchors and URL state with reload
and Back support. Link related concepts. Make search coverage explicit and include provider
notes. A copied link must open the same explanation and filters; an empty result must offer a
one-step recovery.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
