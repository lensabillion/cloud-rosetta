# The Confusing Terms Decoder

Generated from `data/terms/`. Edit the YAML, not this file.

The hardest part of a second cloud is not that Compute Engine is called EC2. It is that
the same word denotes different kinds of thing depending on whose console you are in.
These have no row in a service comparison table, because they are not services.

**Severity** says how badly the word collides. `high` means the clouds use it for
different categories of object. `medium` means the same category behaving differently.
`low` means a naming difference worth knowing.

## Index

| Term | Severity | The collision in one line |
| --- | --- | --- |
| [ASG](#asg) | high | AWS compute vs Azure networking |
| [Availability set](#availability-set) | high | AWS no equivalent vs Azure intra-datacentre placement vs Google Cloud no equivalent |
| [Container](#container) | high | AWS compute packaging vs Azure storage grouping vs Google Cloud compute packaging |
| [Endpoint](#endpoint) | high | AWS private connectivity vs Azure private connectivity, two variants vs Google Cloud private connectivity |
| [Policy](#policy) | high | AWS permissions document vs Azure configuration governance engine vs Google Cloud two different things |
| [Resource group](#resource-group) | high | AWS saved view vs Azure ownership container |
| [Role](#role) | high | AWS identity vs Azure permission set vs Google Cloud permission set |
| [Account](#account) | medium | AWS boundary vs Azure overloaded vs Google Cloud overloaded |
| [Project](#project) | medium | AWS not applicable vs Azure not applicable vs Google Cloud isolation boundary |
| [Security group](#security-group) | medium | AWS instance firewall vs Azure subnet or instance firewall vs Google Cloud network firewall |
| [Service account](#service-account) | medium | AWS identity vs Azure identity vs Google Cloud identity and resource |
| [Tag](#tag) | medium | AWS metadata vs Azure metadata vs Google Cloud metadata and network selector |
| [Zone](#zone) | medium | AWS failure domain vs Azure failure domain vs Google Cloud failure domain |
| [Image](#image) | low | AWS VM template vs Azure VM template vs Google Cloud VM template |
| [Reserved instance](#reserved-instance) | low | AWS discount vs Azure discount vs Google Cloud discount |
| [Stack](#stack) | low | AWS deployment unit vs Azure deployment unit vs Google Cloud deployment unit |

## ASG

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [compute](https://docs.aws.amazon.com/autoscaling/ec2/userguide/auto-scaling-groups.html) | Auto Scaling group. A pool of EC2 instances that can scale together; mixed instance types and purchase options are supported. |
| Azure | [networking](https://learn.microsoft.com/en-us/azure/virtual-network/application-security-groups) | Application security group. A named group of network interfaces that NSG rules can reference instead of listing addresses. |

**Why the distinction matters.** One acronym, two services, different domains entirely, and both are common enough that the abbreviation gets used unqualified in study notes and team chat. Expand it every time.

See also: Security group.

*Verified 2026-09-14.*

## Availability set

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [no equivalent](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/placement-groups.html) | AWS does not use the Azure availability-set resource. Placement groups and multi-zone deployment address different placement and failure requirements. |
| Azure | [intra-datacentre placement](https://learn.microsoft.com/en-us/azure/virtual-machines/availability-set-overview) | A grouping using fault domains and update domains inside a single datacentre, protecting against rack failure and host patching. |
| Google Cloud | [no equivalent](https://docs.cloud.google.com/compute/docs/instances/define-instance-placement) | Google does not use the Azure availability-set resource. Placement policies and distribution across zones must be evaluated against the intended failure domain. |

**Why the distinction matters.** An availability set is not a multi-zone deployment. Surviving loss of a zone requires replicas in other zones and a functioning failover path. Merely placing all resources in one availability zone does not provide that protection.

See also: Availability zone, Fault domain.

*Verified 2026-09-14.*

## Container

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [compute packaging](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/Welcome.html) | An OCI container image or running container. The storage equivalent is a bucket. |
| Azure | [storage grouping](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) | In Blob Storage, a grouping of blobs inside a storage account. Roughly what the other clouds call a bucket. |
| Google Cloud | [compute packaging](https://docs.cloud.google.com/run/docs/container-contract) | An OCI container image or running container. The storage equivalent is a bucket. |

**Why the distinction matters.** Azure uses the word for both meanings in the same portal. "Create a container" in a storage context means a blob grouping and has nothing to do with Docker, Kubernetes or Container Apps. Reading it as a compute object sends the whole answer wrong.

See also: Bucket, Storage account.

*Verified 2026-09-09.*

## Endpoint

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [private connectivity](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html) | For VPC endpoints, gateway endpoints provide route-based S3 and DynamoDB access. Interface endpoints place endpoint interfaces in selected subnets for supported PrivateLink services. There are other endpoint types; identify the product and mode. |
| Azure | [private connectivity, two variants](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview) | Two unrelated things. A service endpoint keeps traffic on the backbone while the service keeps its public IP. A private endpoint puts a private IP from your subnet in front of the service. |
| Google Cloud | [private connectivity](https://docs.cloud.google.com/vpc/docs/private-service-connect) | Private Service Connect endpoints, plus Private Google Access as a separate subnet setting. |

**Why the distinction matters.** For the Azure service-endpoint/private-endpoint pair, only the private endpoint supplies a private address in the consumer VNet. Hybrid clients also need working routing and DNS. Endpoint connectivity does not itself grant permission or disable a service public endpoint.

See also: Private Link, Service endpoint.

*Verified 2026-09-14.*

## Policy

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [permissions document](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html) | A JSON document listing actions, resources and conditions, attached to an identity or a resource. |
| Azure | [configuration governance engine](https://learn.microsoft.com/en-us/azure/governance/policy/overview) | Azure Policy is a governance engine evaluating resource configuration at write time. It is not the permissions system. |
| Google Cloud | [two different things](https://docs.cloud.google.com/iam/docs/policies) | An IAM allow policy binds roles to principals. IAM deny policies and organization policies are separate controls; their scope and supported operations differ. |

**Why the distinction matters.** Specify the policy product and effect. An IAM permission grant, an IAM deny, and a resource-configuration constraint answer different questions. Governance controls do not substitute for application authorization.

See also: Role, Service control policy.

*Verified 2026-09-14.*

## Resource group

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [saved view](https://docs.aws.amazon.com/ARG/latest/userguide/welcome.html) | An optional, tag-driven query that produces a view over resources. It owns nothing. |
| Azure | [ownership container](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/delete-resource-group) | A lifecycle and management container for resources deployed at resource-group scope. Deletion requests removal of its contents; locks, dependencies and service behavior can block completion. Not every Azure resource type belongs to a resource group. |

**Why the distinction matters.** Deleting an AWS Resource Group removes the grouping, not its members. Azure resource-group deletion requests deletion of member resources, subject to locks and dependencies. Google projects are a different lifecycle boundary.

See also: Stack, Project.

*Verified 2026-09-14.*

## Role

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [identity](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) | An assumable identity with its own temporary credentials issued by STS, and a trust policy naming who may assume it. |
| Azure | [permission set](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions) | A named set of permissions, meaningless until assigned to a separate principal at a scope. |
| Google Cloud | [permission set](https://docs.cloud.google.com/iam/docs/roles-overview) | A named collection of permissions, bound to a member at a resource node. |

**Why the distinction matters.** An AWS role is a thing you become; the other two are lists of verbs pinned to somebody else. Different categories of object behind one word. The nearest AWS equivalent of an Azure or Google role is a managed policy, and the nearest Azure or Google equivalent of an AWS role is a service principal or service account.

See also: Policy, Service account, Principal.

*Verified 2026-09-09.*

## Account

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [boundary](https://docs.aws.amazon.com/accounts/latest/reference/welcome.html) | A resource and IAM administration boundary identified by a 12-digit number. Organizations supports consolidated billing; workforce identities can be federated across accounts. |
| Azure | [overloaded](https://learn.microsoft.com/en-us/azure/cost-management-billing/understand/view-all-accounts) | Usually means a sign-in identity. A storage account is something else entirely, and a billing account something else again. |
| Google Cloud | [overloaded](https://docs.cloud.google.com/billing/docs/concepts) | Usually a user identity. A billing account is a separate payable object linked to projects. A service account is a machine identity. |

**Why the distinction matters.** An AWS account holds workload resources and IAM configuration. In Azure and Google, qualify whether account means a person, workload identity, billing object or storage object. Identity, resource and payment boundaries are related but not identical.

See also: Project, Subscription, Service account.

*Verified 2026-09-14.*

## Project

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [not applicable](https://docs.aws.amazon.com/accounts/latest/reference/welcome.html) | An AWS account is the relevant workload administration boundary here; individual AWS services can also have objects named projects. |
| Azure | [not applicable](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/initial-subscriptions) | An Azure subscription is the relevant workload administration scope here; a project in another Azure product is not automatically that scope. |
| Google Cloud | [isolation boundary](https://docs.cloud.google.com/resource-manager/docs/creating-managing-projects) | A container for workload resources and API configuration. Organization, folder and billing resources exist outside projects. A project has a mutable name, an immutable unique ID and an assigned number. |

**Why the distinction matters.** Project name, ID and number are different identifiers. The ID cannot be reused after deletion. Choose project boundaries for access, quotas and operations rather than assuming they map exactly to another provider account.

See also: Account, Subscription.

*Verified 2026-09-14.*

## Security group

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [instance firewall](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html) | A stateful allow-only filter attached to a network interface. It cannot deny. |
| Azure | [subnet or instance firewall](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview) | Network security group, a stateful filter with allow and deny rules evaluated by priority, attachable to a subnet, a NIC, or both. |
| Google Cloud | [network firewall](https://docs.cloud.google.com/firewall/docs/firewalls) | No object by this name. VPC firewall rules do the job, attached to the network and targeted by tag or service account. |

**Why the distinction matters.** The AWS object cannot deny anything, which people consistently forget, and Azure's similarly named object can. In Entra ID, "security group" additionally means a directory group of users, a third unrelated sense.

See also: ASG, Network ACL, Firewall rule.

*Verified 2026-09-09.*

## Service account

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [identity](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) | Not the term used. The equivalent is an IAM role assumed by a service. |
| Azure | [identity](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview) | Not the term used. The equivalent is a service principal, or a managed identity that wraps one. |
| Google Cloud | [identity and resource](https://docs.cloud.google.com/iam/docs/service-account-permissions) | A workload identity that is also an IAM-managed resource. Permission to attach it differs from permission to generate access tokens and from the permissions used by the workload. |

**Why the distinction matters.** Service Account User supports attaching a Google service account; Token Creator supports credential generation. A grant to use the identity does not grant that identity permission to the application data. Check the intended authentication path.

See also: Role, Managed identity, Principal.

*Verified 2026-09-14.*

## Tag

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [metadata](https://docs.aws.amazon.com/tag-editor/latest/userguide/tagging.html) | A key-value label for billing, search and access control conditions. |
| Azure | [metadata](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/tag-resources) | A key-value label for billing and search, usable as a condition in Azure Policy. |
| Google Cloud | [metadata and network selector](https://docs.cloud.google.com/resource-manager/docs/tags/tags-overview) | Three distinct constructs: labels for resource metadata, network tags for firewall and route selection, and Resource Manager tags for governed key-value associations and supported policy conditions. |

**Why the distinction matters.** A network tag is metadata with operational effects: firewall rules and routes can select it. A Resource Manager tag is a different governed construct. Do not treat either as interchangeable with a billing label.

See also: Label, Firewall rule.

*Verified 2026-09-14.*

## Zone

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [failure domain](https://docs.aws.amazon.com/ram/latest/userguide/working-with-az-ids.html) | An Availability Zone consists of one or more datacenters. AZ names can map differently between accounts; AZ IDs identify the same physical zone across accounts. |
| Azure | [failure domain](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview) | Availability zone, the same idea, but not present in every region and opted into per resource. |
| Google Cloud | [failure domain](https://docs.cloud.google.com/compute/docs/regions-zones) | A deployment area within a region, named like us-central1-a. |

**Why the distinction matters.** Compare AWS AZ IDs when physical alignment between accounts matters; equal AZ names do not guarantee it. Region and service support determine how zones can be selected. A DNS zone is a different meaning of the word.

See also: Availability set, Region.

*Verified 2026-09-14.*

## Image

**Severity: low.** Mostly cosmetic, still worth knowing.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [VM template](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AMIs.html) | Amazon Machine Image, an AMI. Regional, and must be copied to be used in another region. |
| Azure | [VM template](https://learn.microsoft.com/en-us/azure/virtual-machines/azure-compute-gallery) | A managed image, or a version published in an Azure Compute Gallery for replication and versioning. |
| Google Cloud | [VM template](https://docs.cloud.google.com/compute/docs/images) | A custom image, which is a global resource usable from any region without copying. |

**Why the distinction matters.** Scope differs. Google images are global; AMIs are regional and need explicit copying, which is a step people forget in multi-region designs and which exam questions test directly.

See also: Snapshot.

*Verified 2026-09-09.*

## Reserved instance

**Severity: low.** Mostly cosmetic, still worth knowing.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [discount](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-reserved-instances.html) | An EC2 billing discount for matching usage. Regional Reserved Instances do not reserve capacity; zonal Reserved Instances include a capacity reservation. Savings Plans use a different commitment model. |
| Azure | [discount](https://learn.microsoft.com/en-us/azure/cost-management-billing/reservations/save-compute-costs-reservations) | A reservation, purchased for one or three years. |
| Google Cloud | [discount](https://docs.cloud.google.com/compute/docs/sustained-use-discounts) | Committed use discounts and capacity reservations are separate mechanisms. Sustained use discounts apply automatically only to eligible usage. |

**Why the distinction matters.** A discount is not necessarily guaranteed capacity. Verify reservation scope and eligible machine families, regions and purchase options. Google sustained use discounts are not a blanket reduction for every VM or for usage already receiving another incompatible discount.

See also: Spot.

*Verified 2026-09-14.*

## Stack

**Severity: low.** Mostly cosmetic, still worth knowing.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | [deployment unit](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html) | A CloudFormation stack, the set of resources created and deleted together from one template. |
| Azure | [deployment unit](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deployment-stacks) | An Azure deployment stack manages a set of resources deployed from Bicep or ARM templates. Its deletion and detach behavior is configurable. Azure Stack is a separate hybrid product family. |
| Google Cloud | [deployment unit](https://docs.cloud.google.com/infrastructure-manager/docs/overview) | Infrastructure Manager manages Terraform deployments. A deployment and its state are not a universal equivalent of an AWS CloudFormation stack. |

**Why the distinction matters.** Azure deployment stacks exist and must not be confused with Azure Stack. In every provider, check retain, detach, deletion protection and state ownership rather than assuming deleting a deployment always deletes every resource.

See also: Resource group.

*Verified 2026-09-14.*

<!-- Generated by scripts/build.py from data/terms/. Do not edit by hand. -->
