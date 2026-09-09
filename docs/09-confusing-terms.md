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
| AWS | compute | Auto Scaling group. A pool of identical instances scaled by policy. |
| Azure | networking | Application security group. A named group of network interfaces that NSG rules can reference instead of listing addresses. |

**Why it costs marks.** One acronym, two services, different domains entirely, and both are common enough that the abbreviation gets used unqualified in study notes and team chat. Expand it every time.

See also: Security group.

*Verified 2026-09-09.*

## Availability set

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | no equivalent | No such construct. Spreading across datacentres means using several Availability Zones, and placement groups solve a different problem. |
| Azure | intra-datacentre placement | A grouping using fault domains and update domains inside a single datacentre, protecting against rack failure and host patching. |
| Google Cloud | no equivalent | No such construct. Spread placement policies exist for physical separation, but the failure domain you design against is the zone. |

**Why it costs marks.** It sounds like an availability zone and is not one. An availability set does not protect against a datacentre outage; an availability zone does. AWS and Google have no equivalent construct, so there is nothing to translate it to. Any question naming a datacentre-level failure wants zones, and the availability set is a deliberately placed wrong answer.

See also: Availability zone, Fault domain.

*Verified 2026-09-09.*

## Container

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | compute packaging | An OCI container image or running container. The storage equivalent is a bucket. |
| Azure | storage grouping | In Blob Storage, a grouping of blobs inside a storage account. Roughly what the other clouds call a bucket. |
| Google Cloud | compute packaging | An OCI container image or running container. The storage equivalent is a bucket. |

**Why it costs marks.** Azure uses the word for both meanings in the same portal. "Create a container" in a storage context means a blob grouping and has nothing to do with Docker, Kubernetes or Container Apps. Reading it as a compute object sends the whole answer wrong.

See also: Bucket, Storage account.

*Verified 2026-09-09.*

## Endpoint

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | private connectivity | A VPC endpoint. Gateway endpoints are free route table entries serving only S3 and DynamoDB; interface endpoints are billed network interfaces serving most services. |
| Azure | private connectivity, two variants | Two unrelated things. A service endpoint keeps traffic on the backbone while the service keeps its public IP. A private endpoint puts a private IP from your subnet in front of the service. |
| Google Cloud | private connectivity | Private Service Connect endpoints, plus Private Google Access as a separate subnet setting. |

**Why it costs marks.** The Azure pair is the worst naming collision in cloud networking. Service endpoint and private endpoint sound like synonyms and behave differently: only the private endpoint gives the service an address inside your network and only it works from on-premises over ExpressRoute or VPN.

See also: Private Link, Service endpoint.

*Verified 2026-09-09.*

## Policy

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | permissions document | A JSON document listing actions, resources and conditions, attached to an identity or a resource. |
| Azure | configuration governance engine | Azure Policy is a governance engine evaluating resource configuration at write time. It is not the permissions system. |
| Google Cloud | two different things | Either an IAM allow policy, which is a list of role bindings, or an organization policy, which is a configuration constraint. |

**Why it costs marks.** In AWS, policy is how permissions work. In Azure, permissions are RBAC and Azure Policy is a separate system answering a different question. A scenario about enforcing a required configuration is an Azure Policy answer and every RBAC option is a distractor. Google uses the word for both of its systems, so context decides.

See also: Role, Service control policy.

*Verified 2026-09-09.*

## Resource group

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | saved view | An optional, tag-driven query that produces a view over resources. It owns nothing. |
| Azure | ownership container | A mandatory lifecycle container. Every resource is in exactly one, and deleting the group deletes everything inside. |

**Why it costs marks.** Identical phrase, unrelated concepts, and one of them is destructive. Deleting an Azure resource group destroys every resource in it without a per-resource prompt. Deleting an AWS resource group destroys nothing. Google has no construct at this level at all.

See also: Stack, Project.

*Verified 2026-09-09.*

## Role

**Severity: high.** Same word, different category of object.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | identity | An assumable identity with its own temporary credentials issued by STS, and a trust policy naming who may assume it. |
| Azure | permission set | A named set of permissions, meaningless until assigned to a separate principal at a scope. |
| Google Cloud | permission set | A named collection of permissions, bound to a member at a resource node. |

**Why it costs marks.** An AWS role is a thing you become; the other two are lists of verbs pinned to somebody else. Different categories of object behind one word. The nearest AWS equivalent of an Azure or Google role is a managed policy, and the nearest Azure or Google equivalent of an AWS role is a service principal or service account.

See also: Policy, Service account, Principal.

*Verified 2026-09-09.*

## Account

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | boundary | The isolation, billing and identity boundary all at once. Identified by a 12-digit number. |
| Azure | overloaded | Usually means a sign-in identity. A storage account is something else entirely, and a billing account something else again. |
| Google Cloud | overloaded | Usually a user identity. A billing account is a separate payable object linked to projects. A service account is a machine identity. |

**Why it costs marks.** Only in AWS does "the account" name the thing workloads live in. Saying "put it in another account" is a clear instruction on AWS and an ambiguous one everywhere else. Azure's storage account is a resource, not an identity, despite the name.

See also: Project, Subscription, Service account.

*Verified 2026-09-09.*

## Project

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | not applicable | Not a platform concept. The equivalent boundary is an account. |
| Azure | not applicable | Not a platform concept. The equivalent boundary is a subscription, or a resource group for lifecycle. |
| Google Cloud | isolation boundary | The mandatory container for all resources, with an immutable ID that can never be reused, plus a mutable name and an assigned number. |

**Why it costs marks.** Google projects are created far more freely than AWS accounts or Azure subscriptions, so the same word invites the wrong sense of weight. The ID, name and number are three different fields and questions exploit the difference; the ID is permanent and is not reusable even after the project is deleted.

See also: Account, Subscription.

*Verified 2026-09-09.*

## Security group

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | instance firewall | A stateful allow-only filter attached to a network interface. It cannot deny. |
| Azure | subnet or instance firewall | Network security group, a stateful filter with allow and deny rules evaluated by priority, attachable to a subnet, a NIC, or both. |
| Google Cloud | network firewall | No object by this name. VPC firewall rules do the job, attached to the network and targeted by tag or service account. |

**Why it costs marks.** The AWS object cannot deny anything, which people consistently forget, and Azure's similarly named object can. In Entra ID, "security group" additionally means a directory group of users, a third unrelated sense.

See also: ASG, Network ACL, Firewall rule.

*Verified 2026-09-09.*

## Service account

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | identity | Not the term used. The equivalent is an IAM role assumed by a service. |
| Azure | identity | Not the term used. The equivalent is a service principal, or a managed identity that wraps one. |
| Google Cloud | identity and resource | A machine identity that is simultaneously an identity and a resource. You grant it roles, and you grant others roles on it. |

**Why it costs marks.** The dual nature is the part candidates report failing. Using a Google service account requires a role on the service account itself, typically Service Account User, which is entirely separate from whatever permissions that service account holds.

See also: Role, Managed identity, Principal.

*Verified 2026-09-09.*

## Tag

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | metadata | A key-value label for billing, search and access control conditions. |
| Azure | metadata | A key-value label for billing and search, usable as a condition in Azure Policy. |
| Google Cloud | metadata and network selector | Two different things. Labels are key-value metadata for billing. Network tags are strings that select firewall rule targets and affect routing. Tags proper are a third, IAM-governed construct. |

**Why it costs marks.** A Google network tag is not metadata; it changes traffic behaviour by selecting which firewall rules apply. Treating it as a cosmetic label is how people accidentally expose or isolate an instance.

See also: Label, Firewall rule.

*Verified 2026-09-09.*

## Zone

**Severity: medium.** Same category, behaviour differs enough to matter.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | failure domain | Availability Zone, one or more discrete datacentres with independent power and cooling. Names are shuffled per account. |
| Azure | failure domain | Availability zone, the same idea, but not present in every region and opted into per resource. |
| Google Cloud | failure domain | A deployment area within a region, named like us-central1-a. |

**Why it costs marks.** Broadly the same concept, with two traps. AWS shuffles zone names per account, so us-east-1a is not the same physical place in two accounts; use the AZ ID such as use1-az1 when physical identity matters. Azure zones are not available in every region. The word also means a DNS zone in all three clouds.

See also: Availability set, Region.

*Verified 2026-09-09.*

## Image

**Severity: low.** Mostly cosmetic, still worth knowing.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | VM template | Amazon Machine Image, an AMI. Regional, and must be copied to be used in another region. |
| Azure | VM template | A managed image, or a version published in an Azure Compute Gallery for replication and versioning. |
| Google Cloud | VM template | A custom image, which is a global resource usable from any region without copying. |

**Why it costs marks.** Scope differs. Google images are global; AMIs are regional and need explicit copying, which is a step people forget in multi-region designs and which exam questions test directly.

See also: Snapshot.

*Verified 2026-09-09.*

## Reserved instance

**Severity: low.** Mostly cosmetic, still worth knowing.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | discount | A billing commitment for capacity. Savings Plans are the newer, more flexible commitment. |
| Azure | discount | A reservation, purchased for one or three years. |
| Google Cloud | discount | A committed use discount. Google also applies automatic sustained use discounts with no commitment, which the other two do not have. |

**Why it costs marks.** Google's sustained use discount applies automatically for running an instance a large part of the month, with nothing purchased. There is no AWS or Azure equivalent, and it is a free mark on Cloud Digital Leader and Associate Cloud Engineer.

See also: Spot.

*Verified 2026-09-09.*

## Stack

**Severity: low.** Mostly cosmetic, still worth knowing.

| Cloud | What it is | Meaning |
| --- | --- | --- |
| AWS | deployment unit | A CloudFormation stack, the set of resources created and deleted together from one template. |
| Azure | deployment unit | A deployment, from an ARM template or Bicep file. Azure Stack is an unrelated hybrid hardware product. |
| Google Cloud | deployment unit | A deployment, or a Terraform state in practice. |

**Why it costs marks.** Azure Stack is a distinct product line for on-premises hardware and has nothing to do with template deployments, so the word points at very different things depending on context.

See also: Resource group.

*Verified 2026-09-09.*

<!-- Generated by scripts/build.py from data/terms/. Do not edit by hand. -->
