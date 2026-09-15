---
type: is
id: is-01m2j72qav1r03277q3jshvx6s
title: "F2: the most severe rows have the weakest evidence"
kind: bug
status: closed
priority: 0
version: 2
labels:
  - review
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
created_at: 2026-09-15T09:41:28.026Z
updated_at: 2026-09-15T09:43:29.605Z
closed_at: 2026-09-15T09:43:29.605Z
close_reason: null
resolution: null
duplicate_of: null
---
iam.role, hier.virtual-network-scope and hier.grouping-below are graded serious, carry one source each, and are the stalest rows in the set. Severity and sourcing are inversely correlated. Fix: re-verify each against vendor docs, add sources, refresh the verified date, and have validate.py require more evidence as bite rises.
