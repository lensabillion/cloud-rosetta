---
type: is
id: is-01m2j72qgnf55v5hat17y82ddr
title: "F3: Multi-AZ row omits the constraint that actually bites"
kind: bug
status: closed
priority: 1
version: 3
delegate: claude-code@lensas-macbook-air.local
labels:
  - review
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
hold: null
hold_until: null
created_at: 2026-09-15T09:41:28.212Z
updated_at: 2026-09-15T09:43:30.153Z
started_at: 2026-09-15T09:43:29.769Z
closed_at: 2026-09-15T09:43:30.153Z
close_reason: null
resolution: null
duplicate_of: null
---
db.ha-vs-readscale is accurate on replication but never says Multi-AZ DB clusters run only on NVMe-backed instance classes and only on MySQL and PostgreSQL. An architect designs for HA plus read scaling, then finds the engine unsupported. It also omits flow control, which throttles writes on the writer to contain replica lag. Source: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/multi-az-db-clusters-concepts.html
