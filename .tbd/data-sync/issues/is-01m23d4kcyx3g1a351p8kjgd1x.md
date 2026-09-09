---
type: is
id: is-01m23d4kcyx3g1a351p8kjgd1x
title: Correct IAM evaluation and directory administration mental models
kind: bug
status: open
priority: 1
version: 3
spec_path: docs/reviews/2026-09-09-learning-experience-review.md
labels:
  - review-2026-09-09
dependencies:
  - type: blocks
    target: is-01m21nbzjda5hjbfe1p8d28yt5
  - type: blocks
    target: is-01m23d63pp1symbz6jbbspb5t0
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-09T15:38:44.509Z
updated_at: 2026-09-09T23:14:09.671Z
---
### F01 · P1 · Teach Permission Evaluation Without False Universal Rules

**Evidence:** `data/mappings/identity.yml` (`iam.evaluation`, `iam.two-role-systems`) and
`docs/02-identity.md`. AWS is presented as a six-stage pipeline every grant must survive.
Google is described as having no separation between directory and resource administration.

AWS evaluation combines unions and intersections and depends on request context and principal.
A universal sequential rule teaches the wrong outcome for resource policies and boundaries.
Google documents separate Workspace/Cloud Identity super administrator and organization IAM
administrator responsibilities. Organization Administrator is not an AWS-root equivalent.
Sources: [AWS evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html),
[Google organization administration](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization).

**Fix/acceptance:** rewrite both mappings and prose together, distinguish identity administration
from resource authorization across all three providers, and add two worked permission decisions
with explicit account/principal assumptions. Regenerate all outputs. A technical reviewer must
be able to reproduce the decisions from the cited documentation.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
