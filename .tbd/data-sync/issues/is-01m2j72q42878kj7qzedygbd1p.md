---
type: is
id: is-01m2j72q42878kj7qzedygbd1p
title: "F1: eight rows assert behaviour with no source"
kind: bug
status: closed
priority: 0
version: 3
delegate: claude-code@lensas-macbook-air.local
labels:
  - review
dependencies: []
parent_id: is-01m21nbcbvadjeap7gvmks7ems
hold: null
hold_until: null
created_at: 2026-09-15T09:41:27.807Z
updated_at: 2026-09-15T09:43:29.598Z
started_at: 2026-09-15T09:41:40.862Z
closed_at: 2026-09-15T09:43:29.598Z
close_reason: null
resolution: null
duplicate_of: null
---
cmp.autoscale, cmp.spot, db.managed-relational, db.key-value, db.streaming, net.firewall.subnet, net.peering, sto.object carry a breaks_when or shared_trap claim with an empty sources list. The project rule is that every behavioural claim links to vendor documentation. Three of these are graded none, the boldest claim the schema allows, on no evidence. Fix: add vendor sources, then make validate.py require a source wherever a claim exists.
