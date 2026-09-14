# Architecture Review — 14 September 2026

Reviewed by Codex against the merged guide at `227e99d` and the changes on
`codex/reference-architectures`. This is an editorial and diagram review, not an independent
certification, deployment validation or load test.

## Findings and Resolutions

| Finding | Reader impact | Resolution |
| --- | --- | --- |
| The atlas explains concepts but stops before deployment and operational decisions | Readers cannot trace ingress, private access and database recovery as one system | Added three sourced [deployment views](../reference-architectures.md), numbered flows and failure behavior |
| Azure inbound Private Link and outbound integration need separate depiction | A reader could assume an inbound private endpoint supplies outbound connectivity | Drew separate endpoint and delegated integration subnet paths; managed services remain outside the VNet |
| Global network/ingress scope can imply global application availability | A regional database or application outage could be overlooked | Google design names regional dependencies and explicitly limits recovery scope |
| A database standby may be mistaken for an application read endpoint | Readers could route requests to an unavailable target | AWS design routes both app pools to the writer and labels the standby non-readable; Google text states the same limitation for its HA standby |
| Architecture chapter contents links could switch readers to the home page | Long chapters become difficult to navigate | Scoped heading identifiers, route to the owning chapter, preserve browser history |
| README referenced an absent architecture audit | Readers could not inspect the claimed audit evidence | Added this report and extended Markdown link validation to the root README |
| Unsupported disclosure markup was visible in practice answers | Learners saw HTML tags in the identity and database chapters | Used supported Markdown for answer labels |
| Diagram labels could overlap after title wrapping | Relationships become ambiguous | Position details below wrapped titles; visually review the new diagrams and adjust flows and captions |

## Evidence and Scope

The [reference architecture chapter](../reference-architectures.md) places primary vendor
sources beside each design. Reviewed requirements include ALB zone/subnet placement, RDS
instance standby behavior, Azure App Service inbound/outbound network paths, Azure SQL zone
redundancy, Google regional instance groups, private services access and Cloud SQL HA.
The designs include selected controls and omit other paths explicitly; omitted components
must be designed before implementation.

The merged atlas and mapping corrections are retained. This follow-up does not re-verify
every service feature, certification detail or archived research statement. Recorded dates
in the data are not advanced by this review. Source availability and regional/tier support
can change; recheck the linked documentation for a real deployment.

## Verification

Automated checks cover data validation, root/chapter Markdown destinations, generated-output
consistency, malformed input, standalone SVG accessibility references and unique HTML targets.
Browser review covers the three new diagrams, chapter navigation and narrow-screen layout.
No cloud resources are provisioned. Recovery times, throughput, security effectiveness and
costs therefore remain workload-specific and unmeasured.

Follow-up learner studies and remaining editorial work stay in tbd. This report records the
specific improvements above rather than asserting that every aspect of the guide is complete.

<!-- This document follows common-doc-guidelines.md. -->
