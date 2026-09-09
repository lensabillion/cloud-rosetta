---
type: is
id: is-01m21q38fwbmtyyv6ax35v48y1
title: Link every claim to its original source
kind: task
status: open
priority: 1
version: 2
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - content
  - review-2026-09-09
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-08T23:54:17.467Z
updated_at: 2026-09-09T23:14:06.715Z
---
Standing requirement. Any figure, name, limit or claim carries a link to the vendor page or study it came from, in docs, data and the rendered site.

## Notes

### F12 · P1 · Make Verification Mean More Than a Date

**Evidence:** terminology sources are optional in `data/schema/term.schema.json` and the
Markdown decoder renderer drops sense URLs. Chapter facts are outside the dataset freshness
check. `verified` does not record which claim a source supports. The site cannot promise that
passing schema validation proves accuracy. The link-check job is advisory (`continue-on-error`).

**Fix/acceptance:** extend `cloud-wsfy` with required primary sources for substantive claims,
reviewer/date/conditions, a source-visible decoder, and a documented review cadence for chapters,
exam facts, and fast-changing product modes. Separate “schema passed,” “links reachable,” and
“claim reviewed.” Include a correction link from each concept. Require review of strong claims
before changing their verification date.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
