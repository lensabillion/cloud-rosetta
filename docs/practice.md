# Practice Architectural Decisions

For each scenario, state the constraint, choose an option, and explain what changes when the
constraint changes. These are learning exercises, not real exam questions or a score predictor.

## An Unreadable Standby

An RDS Multi-AZ **DB instance** serves a photo application. Reporting queries need to move off
the writer. Can they use the existing standby?

**Answer:** no. That deployment's standby is not a client read endpoint. Evaluate a read replica
or a supported DB cluster configuration. Preserve the application's availability requirement.
A Multi-AZ DB cluster has readable standbys, so “all Multi-AZ standbys are unreadable” is wrong.
[Deployment modes and sources](05-databases.md).

## A Private Address That Does Not Work

An on-premises client resolves an Azure service hostname to its public address, even after a
private endpoint was created. Does adding a broader RBAC grant fix the network path?

**Answer:** no. Inspect DNS resolution and forwarding, routes, endpoint approval and traffic
controls. Authorization matters after reachability is established. Creating the endpoint alone
does not guarantee public access is disabled. [Private access](03-networking.md).

## A Smaller Role Does Not Remove Access

A principal inherits a broad Azure or Google allow grant. You assign a narrower role on a child
resource. Have you reduced the inherited permission?

**Answer:** no. The child allow grant does not subtract the parent grant. Change the relevant
assignment or evaluate applicable deny and condition controls. Check other grants before
concluding what the principal can do. [Identity](02-identity.md).

## One Region Is Not a Recovery Plan

A web application has two instances in different zones but one unreplicated database. Is the
application now resilient to every zone failure?

**Answer:** no. The database remains a dependency that can prevent useful service. Define the
failure scope, data-loss objective and recovery time, then examine every dependency. Multi-zone
resilience also does not establish recovery after a region-wide outage.
[Architecture assumptions](architecture.md).

## One Product Name Can Hide a New Operating Mode

A design review claims that every AWS NAT gateway requires its own public subnet and one
customer-managed gateway per Availability Zone. Is the statement current?

**Answer:** it describes the zonal public NAT pattern, not every mode. Regional NAT gateways
support different placement and expansion behavior. Their mode restrictions and expansion delay
still matter. [NAT modes and sources](03-networking.md).

## Import the Optional Flashcards

Download [the tab-separated deck](../dist/drills.tsv). In Anki, import it with fields mapped to
front, back and tags. Comparison answers include the grade, caveat and sources so a card does
not teach a false equivalence. Provider links establish where to investigate; they do not
replace reading the applicable conditions.

You can also practise without an account or flashcard application: cover the answer paragraph,
write a justification, and check it against the linked chapter and primary sources. Revisit
an answer when its source or required service configuration changes.

**Next:** [architecture atlas](architecture.md) · [exam map](10-exam-map.md).

<!-- This document follows common-doc-guidelines.md. -->
