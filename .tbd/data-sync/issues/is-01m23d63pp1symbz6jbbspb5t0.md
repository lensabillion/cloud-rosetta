---
type: is
id: is-01m23d63pp1symbz6jbbspb5t0
title: Replace mixed hierarchy drawings with precise architecture diagrams
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
created_at: 2026-09-09T15:39:33.973Z
updated_at: 2026-09-09T23:14:09.852Z
---
### F10 · P1 · Draw Separate Ownership, Location, and Traffic Models

**Evidence:** `HIERARCHY_SVG` in `scripts/build.py` and `mermaid_hierarchy()` in
`scripts/surfaces.py` imply one containment chain. AWS places an availability zone inside a VPC;
Google places a region inside a project. Administrative ownership, geographic scope, and network
membership are different relationships, not one tree. Google subnets' network membership is
also clearer in Mermaid than in the SVG, so the two diagrams teach different detail.

**Fix/acceptance:** use separate diagrams for resource ownership, network geography, and request
flow. Show AWS subnets belonging to a VPC and located in one AZ; never imply a VPC owns an AZ.
Show a Google global VPC with regional subnets. Sources:
[AWS subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html),
[Google VPC scope](https://docs.cloud.google.com/vpc/docs/vpc),
[Azure network and zone scope](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview).
Apply the diagram standard below and make SVG and Markdown explain the same relationships.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
