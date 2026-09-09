---
type: is
id: is-01m23d59g6bprkxfbtht6srgw3
title: Generate a complete UTF-8 standards-mode HTML document
kind: bug
status: open
priority: 1
version: 1
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - review-2026-09-09
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-09T15:39:07.142Z
updated_at: 2026-09-09T15:39:07.142Z
---
### F06 · P1 · Emit a Complete HTML Document

**Evidence:** both `scripts/template.html:1` and `site/index.html:1` start with a title and omit
a doctype, UTF-8 declaration, viewport metadata, and `html lang`. Ordinary HTTP browsing
confirmed `document.characterSet = windows-1252` and `document.compatMode = BackCompat`.
The literal generated symbols are corrupted; numeric entities in the legend survive.

**Fix/acceptance:** generate a standalone standards-mode document with UTF-8, English language,
responsive viewport, head/body, and a useful description. Confirm correct symbols over ordinary
HTTP without special host headers. Verify phone rendering on an actual mobile browser as well
as desktop viewport resizing.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
