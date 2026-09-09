---
type: is
id: is-01m23d55dzmc9zps0vn8egxe3n
title: Create a first-principles learning route around one application
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
created_at: 2026-09-09T15:39:02.974Z
updated_at: 2026-09-09T23:14:09.835Z
---
### F05 · P1 · Give Beginners a Route Before the Reference

**Evidence:** `scripts/template.html:239` opens with a defensive comparison pitch, 84%, two
classification systems, three tabs, and 16 exam-code filters. Its main content starts with
compute because filenames are sorted alphabetically in `scripts/build.py:58`. It never links
to `docs/00-landscape.md`. That chapter's SaaS responsibility row also oversimplifies the
customer's role to “data only”; identity, access, and configuration still need explanation.
Source: [shared responsibility](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility).

**Fix/acceptance:** give the first screen three routes: **Start from zero**, **Translate from
my cloud**, and **Challenge my knowledge**. The first route teaches compute, storage, networking,
identity, availability, and cost through one small application. Expand terms before abbreviating
them; provide a glossary and a visible next step. A newcomer should explain where code runs,
where data lives, who can access it, and why a bill appears after a five-minute introduction.
Longer lessons, not a five-minute promise, provide mastery.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
