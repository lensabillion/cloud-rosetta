---
type: is
id: is-01m23d5vvwqqtd5gjfyb04xrce
title: Complete GitHub reading paths and stable guide distribution
kind: task
status: open
priority: 1
version: 1
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - review-2026-09-09
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-09T15:39:25.947Z
updated_at: 2026-09-09T15:39:25.947Z
---
### F09 · P1 · Finish the GitHub Reading and Distribution Experience

**Evidence:** README's primary guide link targets a Claude artifact; no repository-controlled
publication workflow is present. “Read the chapters” goes to a directory mixing educational and
internal project records. `dist/` is committed, but downloads are not prominently linked.
The generated README often reduces a useful caveat to an empty opening sentence such as
“The classic RDS trap, and it transfers” (`scripts/surfaces.py:78`). Full mapping explanations
are not generated as dedicated Markdown reference chapters.

**Fix/acceptance:** add a curated chapter index, a beginner entry link above the fold, complete
Markdown mappings, and direct diagram/flashcard/download links. Use authored one-line takeaways
rather than first-sentence truncation. Separate reader content from project records in navigation.
If retaining the site, publish through a stable repository-controlled URL and smoke-test it.
A reader must complete the core learning journey entirely on GitHub without opening HTML.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
