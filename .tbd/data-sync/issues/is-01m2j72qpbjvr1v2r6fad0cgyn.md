---
type: is
id: is-01m2j72qpbjvr1v2r6fad0cgyn
title: "F4: gateway endpoint row gives consequence without mechanism"
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
created_at: 2026-09-15T09:41:28.395Z
updated_at: 2026-09-15T09:43:45.344Z
started_at: 2026-09-15T09:43:44.958Z
closed_at: 2026-09-15T09:43:45.344Z
close_reason: null
resolution: null
duplicate_of: null
---
net.private-service-access says gateway endpoints are unreachable over VPN, Direct Connect or peering but not why: traffic still uses the service public endpoint so there is no private address to route to. Also omits that the route is regional, so cross-region S3 traffic silently leaves via the internet gateway. Source: https://docs.aws.amazon.com/vpc/latest/privatelink/gateway-endpoints.html
