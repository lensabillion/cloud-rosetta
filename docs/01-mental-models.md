# Resource Ownership, Identity and Geography

Three questions need three answers: who administers a resource, where it runs, and which
identity can access it. Billing is a related fourth question. Drawing all four as one nested
hierarchy teaches the wrong model.

## Administrative Ownership

![Administrative relationships in AWS, Azure and Google Cloud](assets/architecture/hierarchy.svg)

The arrows in this drawing mean administrative parentage. They are not network connections.
Optional intermediate groups are labelled. Regions and zones do not belong in this tree.

| Provider | Workload administration | Related systems |
| --- | --- | --- |
| AWS | An account contains resources and IAM configuration; Organizations groups accounts | Organizations supports consolidated billing. Workforce access can come from Identity Center or another identity provider |
| Azure | Management groups organize subscriptions; resource groups contain resources deployed at resource-group scope | A subscription trusts an Entra tenant. Billing accounts and agreements form a separate billing hierarchy |
| Google Cloud | An organization can contain folders and projects; projects contain workload resources | Projects link to billing accounts. Directory administration and resource IAM are separate responsibilities |

Sources: [AWS Organizations](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html),
[AWS billing](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/consolidated-billing.html),
[Azure resource scopes](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview),
[Google hierarchy](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy).

## Network Membership and Location

![Network ownership and subnet location compared separately](assets/architecture/scope.svg)

An AWS VPC is regional and its subnets each occupy one Availability Zone. An Azure VNet and
its subnets are regional. A Google VPC is global and its subnets are regional. A Google project
owns network resources; it does not own geographic regions. A VPC does not own a zone.
[AWS subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html),
[Azure VNets](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview),
[Google VPCs](https://docs.cloud.google.com/vpc/docs/vpc).

A global network can connect regional resources; it does not make those resources global or
resilient to regional failure. Routing, firewall rules and authorization still apply.

## Grouping and Deletion

| Object | What deletion means |
| --- | --- |
| AWS Resource Group | Removes the group, not its member resources |
| AWS organizational unit | Accounts and child OUs must first be removed or moved |
| Azure resource group | Requests deletion of members; locks, dependencies and service behavior can prevent completion |
| Google folder | Must be empty before deletion; it does not recursively delete projects |
| Google project | Starts shutdown and a recovery period; some resources may not be recoverable. Project IDs cannot be reused |

Sources: [AWS resource groups](https://docs.aws.amazon.com/ARG/latest/userguide/deleting-resource-groups.html),
[AWS OUs](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_ous.html),
[Azure deletion](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/delete-resource-group),
[Google folders](https://docs.cloud.google.com/resource-manager/docs/creating-managing-folders),
[Google projects](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects).

## Failure Domains Are Not Guarantees

An Azure availability set separates fault and update domains within a datacenter; it is not a
multi-zone design. To tolerate a zone outage, place enough capacity in other zones and ensure
clients, data and dependencies can fail over. A single VM in a zone remains a single VM.
[Azure availability sets](https://learn.microsoft.com/en-us/azure/virtual-machines/availability-set-overview).

AWS AZ names can map differently across accounts. Use AZ IDs to align physical locations when
sharing resources. Do not replace “can differ” with “always differ.”
[AWS AZ IDs](https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html).

## Quotas and Names

Nesting depth, project-creation quotas and resource-name rules are service-specific. Check
current limits when designing an organization. S3 general-purpose bucket names, for example,
are unique within an AWS partition; not every S3 bucket type has identical naming rules.
[AWS Organizations quotas](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html),
[Azure management groups](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview),
[S3 naming](https://docs.aws.amazon.com/AmazonS3/latest/userguide/bucketnamingrules.html).

**Next:** [identity and access](02-identity.md) · [architecture atlas](architecture.md).

<!-- This document follows common-doc-guidelines.md. -->
