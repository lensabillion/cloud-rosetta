---
type: is
id: is-01m23d513df18fs77zqqa7xxt1
title: Update Kubernetes and storage comparisons and audit exclusivity claims
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
created_at: 2026-09-09T15:38:58.540Z
updated_at: 2026-09-09T23:14:09.510Z
---
### F04 · P1 · Replace Unsupported Exclusivity Claims With Current Comparisons

**Evidence:** `cmp.kubernetes` in `data/mappings/compute.yml` says GKE Autopilot has no direct
counterpart; `sto.redundancy` in `data/mappings/storage.yml` says One Zone-IA is S3's only
single-zone option. Both claims are too categorical.

Compare operational responsibilities with [EKS Auto Mode](https://docs.aws.amazon.com/eks/latest/userguide/automode.html)
and [AKS Automatic](https://learn.microsoft.com/en-us/azure/aks/intro-aks-automatic);
these need not be identical to be relevant alternatives. Include S3 Express One Zone in the
[storage comparison](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html).

**Fix/acceptance:** revise these rows and the `exact/partial/none` rubric. Distinguish absent
capability from different implementation and partial parity. Audit “only,” “always,” “never,”
“no equivalent,” and product lifecycle claims, including the Fabric/Synapse wording. Capture
conditions, region/tier/version constraints, and direct evidence for each strong claim.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
