---
type: is
id: is-01m23d5gqzb2mv6zn0dcjpkx1e
title: Make mobile reading and keyboard navigation accessible
kind: task
status: open
priority: 1
version: 2
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - review-2026-09-09
dependencies:
  - type: blocks
    target: is-01m21q38aap0qqv1ng8jsdwfsf
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-09T15:39:14.558Z
updated_at: 2026-09-09T23:14:09.842Z
---
### F07 · P1 · Make Mobile Reading and Keyboard Use Practical

**Evidence:** at 390 pixels wide the sticky filter/navigation block measured 384 pixels tall,
nearly half the tested viewport. The 16 exam codes wrap into multiple rows; labels and dates
use 10–11.5 pixel type. The hierarchy requires horizontal panning. Tabs lack panel relationships
and keyboard behavior; the result count has no live-region semantics and there is no skip link.

**Fix/acceptance:** keep a compact search/filter summary sticky; disclose advanced and exam
filters on demand. Use readable text and generous targets, preserve visible focus, provide a
skip link, associate tabs with panels, and announce count updates. Follow the
[W3C tab pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/). Verify 390-pixel reading,
200% zoom, keyboard-only navigation, both themes, and a screen-reader smoke test. Aim for
controls to consume at most about one-fifth of the phone viewport during normal reading.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
