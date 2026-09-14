# Cloud Rosetta

Learn how AWS, Azure and Google Cloud solve similar problems, and where the designs differ.
The guide combines foundations, sourced comparisons, architecture drawings and practice.

**[Open the guide](https://lensabillion.github.io/cloud-rosetta/)** ·
[Read the chapters](docs/README.md) · [Architecture atlas](docs/architecture.md)

## Start With Your Question

- New to cloud: follow a photo application's needs in [Cloud Foundations](docs/00-landscape.md).
- Moving between providers: read [resource models](docs/01-mental-models.md) and the
  [terminology decoder](docs/09-confusing-terms.md).
- Reviewing a design: inspect [architecture boundaries and assumptions](docs/architecture.md).
- Testing your understanding: use [practice scenarios](docs/practice.md).

A mapping describes a similar purpose, a material behavior difference, or a different object
or architecture. These grades apply to this curated dataset, not to a measured percentage of
all cloud services. Read each caveat before translating a design.

<!-- BEGIN GENERATED. Edit data/, then run: python scripts/build.py -->

## The Legend

Two independent axes, because they answer different questions. Severity wording follows
[og-aws](https://github.com/open-guides/og-aws), which defines it by consequence.

| | How far the mapping transfers | | How badly it bites |
| --- | --- | --- | --- |
| ✅ | Similar purpose; verify configuration. | ❗ | Serious. Security risk, real money, or hard to undo. |
| ⚠️ | Behaves differently in a way that changes answers. | 🔸 | Regular. It breaks, or it fails to scale. |
| ❌ | Different object or architecture; read the caveat. | 🔹 | Tip. Often overlooked, nothing breaks. |

Service lifecycle and exam coverage are separate; check official documentation.

## The 14 Differences That Will Actually Hurt You

Filtered to ❗ only. This is the table to read if you read nothing else.

| | Concept | AWS | Azure | Google Cloud |
| --- | --- | --- | --- | --- |
| ⚠️ | **High availability versus read scaling on a relational database** | [RDS Multi-AZ DB instance or DB cluster; read replica](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html) | [Zone-redundant configuration, versus geo-replica](https://learn.microsoft.com/en-us/azure/azure-sql/database/high-availability-sla) | [Regional instance, versus read replica](https://docs.cloud.google.com/sql/docs/mysql/high-availability) |
| ⚠️ | **The primary workload isolation boundary** | [Account](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_getting-started_concepts.html) | [Subscription](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/initial-subscriptions) | [Project](https://docs.cloud.google.com/resource-manager/docs/cloud-platform-resource-hierarchy) |
| ❌ | **Grouping container below the isolation boundary** | [Resource group](https://docs.aws.amazon.com/ARG/latest/userguide/welcome.html) | [Resource group](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/overview) | *none* |
| ❌ | **Scope of the virtual network object** | [VPC, regional](https://docs.aws.amazon.com/vpc/latest/userguide/what-is-amazon-vpc.html) | [Virtual network, regional](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview) | [VPC network, global](https://docs.cloud.google.com/vpc/docs/vpc) |
| ⚠️ | **Independent failure domain within a region** | [Availability Zone](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-regions-availability-zones.html) | [Availability zone](https://learn.microsoft.com/en-us/azure/reliability/availability-zones-overview) | [Zone](https://docs.cloud.google.com/compute/docs/regions-zones) |
| ⚠️ | **Organization-wide preventive guardrail** | [Service control policy](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html) | [Azure Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview) | [Organization policy constraint](https://docs.cloud.google.com/resource-manager/docs/organization-policy/overview) |
| ❌ | **The object called a "role"** | [IAM role](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles.html) | [Azure role definition](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-definitions) | [IAM role](https://docs.cloud.google.com/iam/docs/roles-overview) |
| ⚠️ | **Credentials for compute without stored secrets** | [IAM role via instance profile](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html) | [Managed identity](https://learn.microsoft.com/en-us/entra/identity/managed-identities-azure-resources/overview) | [Attached service account](https://docs.cloud.google.com/iam/docs/service-account-overview) |
| ❌ | **How a permission decision is reached** | [IAM policy evaluation by request context](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) | [Deny assignment, then additive union of role assignments](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview) | [Deny policy, then additive union of allow policy bindings](https://docs.cloud.google.com/iam/docs/deny-overview) |
| ⚠️ | **Administering the directory versus administering resources** | [IAM Identity Center administration and account IAM](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html) | [Microsoft Entra roles and Azure RBAC roles](https://learn.microsoft.com/en-us/azure/role-based-access-control/rbac-and-directory-admin-roles) | [Cloud Identity super administrator and organization IAM roles](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization) |
| ⚠️ | **Instance-level traffic filtering** | [Security group](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html) | [Network security group](https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview) | [VPC firewall rule](https://docs.cloud.google.com/firewall/docs/firewalls) |
| ❌ | **Reaching a managed service without traversing the internet** | [VPC endpoint, gateway or interface](https://docs.aws.amazon.com/vpc/latest/privatelink/concepts.html) | [Private endpoint, and separately service endpoint](https://learn.microsoft.com/en-us/azure/private-link/private-endpoint-overview) | [Private Service Connect, and separately Private Google Access](https://docs.cloud.google.com/vpc/docs/private-service-connect) |
| ❌ | **Archival storage and retrieval behavior** | [S3 Glacier Deep Archive](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html) | [Archive access tier](https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview) | [Archive storage class](https://docs.cloud.google.com/storage/docs/storage-classes) |
| ❌ | **Naming the replication and durability setting** | [Storage class, with zonal scope implied by the class](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html) | [LRS, ZRS, GRS, GZRS, RA-GRS](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy) | [Location type, region, dual-region or multi-region](https://docs.cloud.google.com/storage/docs/locations) |

<details>
<summary><b>Open for the conditions and caveats</b></summary>

- **High availability versus read scaling on a relational database.** In RDS, a Multi-AZ DB instance has a non-readable standby, while a Multi-AZ DB cluster has two readable standby instances with semisynchronous replication that also support failover. Ordinary RDS read replicas are a separate asynchronous replication mechanism; do not infer automatic failover from readability. Azure SQL Database zone redundancy and read scale-out depend on service tier; active geo-replication is a separate readable asynchronous copy. Cloud SQL for MySQL regional HA uses a standby for failover; a read replica serves reads separately. Specify the engine, deployment type, and failure scope before choosing.
- **The primary workload isolation boundary.** An AWS account is a resource and IAM administration boundary, but workforce identities can be federated and Organizations can consolidate charges. Azure subscriptions are resource and billing scopes associated with an Entra tenant. Google projects hold workload resources and link to a billing account. Resource ownership, identity administration and payment responsibility must be designed separately in every cloud.
- **Grouping container below the isolation boundary.** An Azure resource group is a lifecycle and management scope for resources deployed at resource-group scope. Deleting the group initiates deletion of its contents, subject to locks, dependencies, and service behavior. An AWS Resource Group is a grouping/query construct; deleting that group does not delete its member resources. Google projects and labels provide different grouping boundaries. Not every Azure resource type is deployed at resource-group scope.
- **Scope of the virtual network object.** A Google VPC is a global object spanning every region and carries no CIDR of its own; the subnets hold the ranges and are regional. One Google VPC can contain instances in Tokyo and Frankfurt that route to each other over Google's backbone with no peering. AWS and Azure networks are regional, so the same design needs peering or a transit construct. An AWS subnet additionally lives in exactly one availability zone, whereas Azure and Google subnets are regional and span zones.
- **Independent failure domain within a region.** An Azure availability set distributes VMs across fault and update domains; it does not provide protection from losing a whole datacenter. Zone resilience requires resources distributed across zones and a working failover design, not simply selecting one zone. AWS AZ names can map differently between accounts; use AZ IDs when physical alignment matters.
- **Organization-wide preventive guardrail.** An SCP restricts the permissions available to affected member-account principals and never grants access. SCPs do not restrict the management account or service-linked roles. Azure Policy and Google Organization Policy govern resource configuration; the supported effects and enforcement points differ. Check the applicable control, scope and exceptions rather than treating governance policy as a permission grant.
- **The object called a "role".** These are different categories of object. An AWS role is an identity you assume, with its own temporary credentials issued by STS and a trust policy naming who may assume it. An Azure or Google role is a named set of permissions that carries no credentials and does nothing until assigned to a separate principal at a scope. The nearest AWS equivalent of an Azure or Google role is a managed policy; the nearest Azure or Google equivalent of an AWS role is a service principal or service account.
- **Credentials for compute without stored secrets.** Azure system-assigned identities follow the resource lifecycle; user-assigned identities are independent. An EC2 role is attached through an instance profile; other AWS runtimes use their own role integration. In Google Cloud, permission to attach a service account (actAs) is distinct from permission to mint its credentials. Neither automatically grants the service account access to application data.
- **How a permission decision is reached.** AWS evaluates applicable grants and restrictions rather than requiring an allow at every stage of a universal pipeline. Identity-based grants are constrained by boundaries and applicable organization or session policies. Same-account resource-based grants can behave differently depending on whether they name a user, role, or role session; an applicable explicit deny still wins. Azure RBAC and Google IAM allow grants inherit down their resource hierarchies, but deny controls and conditions must also be considered. A narrower role at a child scope does not remove an inherited grant.
- **Administering the directory versus administering resources.** Directory administration and workload access are different responsibilities in all three ecosystems. An Azure Global Administrator does not automatically receive resource permissions: elevation grants User Access Administrator at root scope, from which resource access can be assigned. Google Workspace or Cloud Identity super administrators manage the directory; Organization Administrator manages organization IAM and is not an unrestricted workload superuser. AWS Identity Center administration likewise does not replace the permission sets and IAM roles used to access member-account resources.
- **Instance-level traffic filtering.** An AWS security group has allow rules, not explicit deny rules. If broad allow rules must remain while one address is blocked, use an appropriate deny-capable control, such as a network ACL, network firewall, or application-layer control where applicable. Azure NSGs and Google VPC firewall rules support allow and deny decisions with priorities. Google VPC firewall rules belong to the network and select targets; do not assume all three attach and evaluate identically.
- **Reaching a managed service without traversing the internet.** A private endpoint provides a private destination address for a supported service; routing, DNS, authorization and service configuration must still permit access. Azure service endpoints instead retain the service public address and do not extend to on-premises clients. AWS gateway endpoints provide route-based access to S3 and DynamoDB without an endpoint fee; they are not reachable through VPN, Direct Connect or peering. Interface endpoints use PrivateLink and have service-specific support and charges. Google Private Service Connect and Private Google Access are different mechanisms.
- **Archival storage and retrieval behavior.** Google Archive remains online with low-latency reads. S3 Glacier Deep Archive requires a restore before access; Glacier Instant Retrieval is a different class. Azure Archive needs rehydration before normal reads. Minimum storage durations, retrieval operations, early deletion and data transfer affect total cost, so the lowest storage rate does not establish the cheapest design.
- **Naming the replication and durability setting.** Azure configures redundancy on the storage account: LRS is local, ZRS spans zones, and geo-redundant options add asynchronous replication to a second region. Read-access variants expose the secondary. S3 storage classes include both One Zone-IA and Express One Zone as single-zone choices; other classes have different resilience and retrieval characteristics. Google Cloud Storage separates location type from storage class. Choose resilience and access behavior independently where the platform allows it.

</details>

## 7 Words That Mean Different Things

Severity `high` means the clouds use the word for **different categories of object**,
not merely for things that behave differently.

| Word | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Role** | *identity* | *permission set* | *permission set* |
| **Resource group** | *saved view* | *ownership container* | — |
| **Policy** | *permissions document* | *configuration governance engine* | *two different things* |
| **ASG** | *compute* | *networking* | — |
| **Container** | *compute packaging* | *storage grouping* | *compute packaging* |
| **Availability set** | *no equivalent* | *intra-datacentre placement* | *no equivalent* |
| **Endpoint** | *private connectivity* | *private connectivity, two variants* | *private connectivity* |

The full decoder, with what each one actually means and why it costs marks, is in
[docs/09-confusing-terms.md](docs/09-confusing-terms.md).

<!-- END GENERATED -->

## Downloads and Verification

[Flashcards](dist/drills.tsv) · [JSON dataset](dist/rosetta.json) · [Comparison poster](dist/poster.svg)

Structural validation checks data shape and source links; it does not establish factual
correctness. Each entry has a recorded check date. See the
[architecture audit](docs/reviews/2026-09-14-architecture-audit.md) for corrections, evidence and
remaining limits. Archived research and progress notes are historical records, not current
architecture guidance.

## Contributing

[How to contribute](CONTRIBUTING.md). Prefer a correction with a primary source and the affected
concept ID. Code is [MIT licensed](LICENSE); content is
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
