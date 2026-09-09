---
type: is
id: is-01m23d4w2vq300cn0nkw7f99jw
title: Correct exam facts and centralize certification lifecycle metadata
kind: bug
status: open
priority: 1
version: 2
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - review-2026-09-09
dependencies:
  - type: blocks
    target: is-01m21nbzjda5hjbfe1p8d28yt5
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-09T15:38:53.402Z
updated_at: 2026-09-09T23:14:09.506Z
---
### F03 · P1 · Correct Certification Facts and Track Exam Lifecycle Centrally

**Evidence:** `docs/10-exam-map.md` gives 700 as the AWS associate passing score and reverses
Google associate/professional validity periods. The site offers AZ-204 as an ordinary filter
while that chapter calls it retired. Exam metadata is just free-text tags.

AWS specifies 720 for associate exams; Google specifies three years for foundational/associate
and two for professional credentials. Sources: [AWS scoring policy](https://aws.amazon.com/certification/policies/after-testing/),
[Google certification policy](https://support.google.com/cloud-certification/answer/9750149?hl=en).

**Fix/acceptance:** add a sourced exam registry with full names, level, current/retired status,
verification date, and official links. Generate filters and exam tables from it; put retired
exam tags in an explicit historical view. Recheck every listed exam, including Microsoft's
retirements, against [its registry](https://learn.microsoft.com/en-za/credentials/support/credential-retirement).
Do not infer product retirement from exam retirement.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
