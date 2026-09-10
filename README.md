# Cloud Rosetta

**Every other cross-cloud comparison tells you what a service is called somewhere else.
This one tells you what breaks when you assume it works the same way.**

A reference for AWS, Azure, and Google Cloud, aimed at people sitting foundational and
associate certifications and at anyone who has to work in a second cloud. Every mapping is
graded by how far the equivalence can be trusted, and any mapping that is not exact has to say
what actually differs before it is allowed into the dataset.

**[Open the guide](https://claude.ai/code/artifact/0ce56412-64e7-4747-92bd-94e45cd97f4b)** ·
[Read the chapters](docs/) · [Browse the data](data/)

---

## 84% of Our Mappings Mislead if You Take Them at Face Value

| | Count |
| --- | --- |
| ✅ Transfer cleanly | 6 |
| ⚠️ Behave differently in a way that changes answers | 20 |
| ❌ Have no honest equivalent | 12 |

That ratio is the reason this project exists. A three-column table of service names is not
wrong, exactly. It is just quiet about the part that costs you the mark.

## Here Is What That Means in Practice

Every comparison on the internet will tell you these three are equivalent:

| AWS | Azure | Google Cloud |
| --- | --- | --- |
| Security group | Network security group | VPC firewall rule |

Here is the same row in this dataset:

> ⚠️ **Behaves differently**
>
> An AWS security group **cannot express a deny rule**. It allows only, so blocking one specific
> address is impossible and requires a network ACL instead. NSGs and Google firewall rules both
> support deny and evaluate by priority. Google rules attach to the VPC network rather than to
> an instance and select targets by network tag or service account, so an engineer arriving from
> AWS looks for a firewall on the machine and does not find one. Google also has implied rules
> that cannot be deleted: allow all egress, deny all ingress.

That paragraph is the product. The table above it is packaging.

## The Terms Are Worse Than the Services

The hardest part of a second cloud is not that Compute Engine is called EC2. It is that the same
word means different kinds of thing:

| Word | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| **Role** | An identity you assume, with its own temporary credentials | A set of permissions granted to somebody else | A set of permissions granted to somebody else |
| **Resource group** | An optional tag query that owns nothing | A mandatory container whose deletion destroys everything inside | Does not exist |
| **ASG** | Auto Scaling group | Application security group | Does not exist |
| **Container** | An OCI container | A grouping of blobs in storage, **and** an OCI container | An OCI container |

No comparison table can hold this, because these are not services and have no row. So they get
their own content type, their own schema, and their own view. 16 terms so far.

## What Makes This Different

| | Others | Here |
| --- | --- | --- |
| Service name equivalents | Yes | Yes |
| Says where the equivalence breaks | No | **Required by CI** |
| Terminology collisions | No | 16 entries and counting |
| Shows how old each fact is | No | Per-row `verified` date, rendered |
| Neutral between vendors | Vendor pages map only to themselves | No allegiance |

The middle row is enforced, not aspirational. `scripts/validate.py` fails the build if a row
graded `partial` or `none` has an empty `breaks_when`. That single rule is what stops this
decaying into another name table, which is what happened to every project we surveyed.
<!-- BEGIN GENERATED. Edit data/, then run: python scripts/build.py -->

## The Legend

Two independent axes, because they answer different questions. Severity wording follows
[og-aws](https://github.com/open-guides/og-aws), which defines it by consequence.

| | How far the mapping transfers | | How badly it bites |
| --- | --- | --- | --- |
| ✅ | Close equivalent. Learn it once. | ❗ | Serious. Security risk, real money, or hard to undo. |
| ⚠️ | Behaves differently in a way that changes answers. | 🔸 | Regular. It breaks, or it fails to scale. |
| ❌ | No honest equivalent. Do not translate. | 🔹 | Tip. Often overlooked, nothing breaks. |

⚑ marks a product its vendor has superseded. Do not learn it for a current exam.

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
| ❌ | **Cheapest archival storage tier** | [S3 Glacier Deep Archive](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html) | [Archive access tier](https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview) | [Archive storage class](https://docs.cloud.google.com/storage/docs/storage-classes) |
| ❌ | **Naming the replication and durability setting** | [Storage class, with zonal scope implied by the class](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html) | [LRS, ZRS, GRS, GZRS, RA-GRS](https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy) | [Location type, region, dual-region or multi-region](https://docs.cloud.google.com/storage/docs/locations) |

<details>
<summary><b>Open for what breaks in each of those, in one line</b></summary>

- **High availability versus read scaling on a relational database.** In RDS, a Multi-AZ DB instance has a non-readable standby, while a Multi-AZ DB cluster has two readable standby instances that also support failover.
- **The primary workload isolation boundary.** An AWS account is simultaneously the isolation boundary, the billing boundary and the identity boundary.
- **Grouping container below the isolation boundary.** An Azure resource group is a lifecycle and management scope for resources deployed at resource-group scope.
- **Scope of the virtual network object.** A Google VPC is a global object spanning every region and carries no CIDR of its own; the subnets hold the ranges and are regional.
- **Independent failure domain within a region.** Azure additionally has an availability set, which is not a zone.
- **Organization-wide preventive guardrail.** An SCP sets a ceiling on what IAM may grant and never grants anything itself; if the SCP allows an action and no IAM policy grants it, the answer is still no.
- **The object called a "role".** These are different categories of object.
- **Credentials for compute without stored secrets.** Azure splits this into system-assigned, which is bound to one resource and deleted with it, and user-assigned, which is a standalone resource that survives and can be shared; "must outlive the VM" or "shared by several apps" selects user-assigned.
- **How a permission decision is reached.** AWS evaluates applicable grants and restrictions rather than requiring an allow at every stage of a universal pipeline.
- **Administering the directory versus administering resources.** Directory administration and workload access are different responsibilities in all three ecosystems.
- **Instance-level traffic filtering.** An AWS security group has allow rules, not explicit deny rules.
- **Reaching a managed service without traversing the internet.** Azure's service endpoint and private endpoint sound like synonyms and are not.
- **Cheapest archival storage tier.** Retrieval behaviour differs fundamentally and decides questions.
- **Naming the replication and durability setting.** Azure configures redundancy on the storage account: LRS is local, ZRS spans zones, and geo-redundant options add asynchronous replication to a second region.

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

## Contributing

The data is plain YAML, one file per domain so pull requests do not collide. Adding a mapping
means adding one block:

```yaml
- id: net.firewall.instance          # stable, never renumbered
  concept: Instance-level traffic filtering
  divergence: partial                # exact | partial | none
  aws:
    name: Security group
    url: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html
  azure:
    name: Network security group
    url: https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview
  gcp:
    name: VPC firewall rule
    url: https://docs.cloud.google.com/firewall/docs/firewalls
  breaks_when: >                     # required unless divergence is exact
    An AWS security group cannot express a deny rule...
  exam_tags: [SAA-C03, AZ-104, ACE]
  verified: '2026-09-09'
```

Then:

```bash
python scripts/validate.py && python scripts/build.py
```

Corrections are the most valuable contribution here. If a row is wrong or a service was renamed,
open an issue and say so. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Repository

```
data/mappings/     Graded service equivalences, one file per domain
data/terms/        Words that mean different things per cloud
data/schema/       JSON Schema for both content types
docs/              Long-form chapters, plus the research behind the design
scripts/validate.py   Schema check and the breaks_when rule
scripts/build.py      Renders the site from the data
site/              Generated. Never edited by hand
```

Start with [docs/01-mental-models.md](docs/01-mental-models.md). Service tables mean little
before the scoping model is clear.

## A Word on Accuracy

All three vendors rename aggressively. Cloud Functions became Cloud Run functions, Azure AD
became Microsoft Entra ID, and the AWS SysOps Administrator Associate exam became CloudOps
Engineer with a new code. Most study material has not caught up.

So: every row carries the date it was last checked against vendor documentation, that date is
shown on the page, and rows that go too long without a recheck fail the build rather than
quietly ageing. Vendor links on every entry are the authority. If something here disagrees with
the vendor, the vendor is right and we have a bug.

## Licence

Code under [MIT](LICENSE). Content under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), so use it in your own study notes
freely with attribution.
