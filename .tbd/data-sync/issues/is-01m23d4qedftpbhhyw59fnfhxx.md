---
type: is
id: is-01m23d4qedftpbhhyw59fnfhxx
title: Distinguish RDS Multi-AZ instances, clusters, and read replicas
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
created_at: 2026-09-09T15:38:48.652Z
updated_at: 2026-09-09T23:14:09.677Z
---
### F02 · P1 · Scope the Multi-AZ Lesson to the Actual Deployment Type

**Evidence:** `data/mappings/databases.yml:26` and `docs/10-exam-map.md` say Multi-AZ standbys
are unreadable and contrast them universally with read replicas.

AWS distinguishes Multi-AZ **DB instances**, whose standby does not serve reads, from Multi-AZ
**DB clusters**, whose standby instances can serve reads and provide failover. The current
simplification obscures the very kind of useful expert distinction this guide should teach.
Source: [RDS deployment types](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html).

**Fix/acceptance:** separate instance, cluster, and read-replica cases; label engine/product
assumptions; explain availability versus read scaling using a failure diagram and a worked
scenario. Check Azure and Google behavior independently rather than copying the AWS mnemonic.


Review: docs/reviews/2026-09-09-learning-experience-review.md. Keep source and generated surfaces consistent.
