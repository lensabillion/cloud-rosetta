# Mental Models: How the Three Clouds Are Shaped

Read this before any service table. Service names are the easy part. The reason a competent
AWS engineer gets Google Cloud questions wrong is that the two clouds disagree about what
contains what, and about which things are global.

Verified against vendor documentation on 9 September 2026. Numeric quotas change; the
citations point at the pages that stay current.

## The Three Questions Every Cloud Answers Differently

1. **What is the isolation boundary?** The thing you put a workload inside so it cannot
   accidentally reach another workload.
2. **What is the billing boundary?** The thing an invoice is drawn around.
3. **What is the identity boundary?** The thing that holds users and decides who they are.

AWS answers "the account" to all three. Azure and Google Cloud split the answers across
different objects, and that split is the source of most cross-cloud confusion.

| Question | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Isolation boundary | Account | Subscription, loosely; resource group for lifecycle | Project |
| Billing boundary | Account, consolidated at the organization | Subscription | Billing account, linked to projects |
| Identity boundary | Account, or IAM Identity Center across the organization | Microsoft Entra ID tenant | Cloud Identity or Workspace domain, at the organization |

The line that matters: **in AWS these three collapse into one object, and in the other two
they do not.** An Azure tenant can hold many subscriptions, and a Google billing account can
pay for projects across several folders. Nothing in AWS behaves that way, because the account
is simultaneously the wall, the invoice, and the user directory.

## The Hierarchies Side by Side

```
AWS                     Azure                        Google Cloud
───                     ─────                        ────────────
Organization            Entra ID tenant              Organization
  └ Root                  └ Root management group      └ Folder
     └ OU                    └ Management group           └ Folder
        └ OU                    └ Subscription               └ Project
           └ Account               └ Resource group             └ Resource
              └ Resource              └ Resource
```

Verified structural limits:

| Limit | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Grouping levels | 5 levels of OUs below a root | 6 levels of management groups, excluding root and subscription levels | 10 levels of folders |
| Roots per hierarchy | Exactly 1 | Exactly 1 root management group per directory | 1 organization per domain |
| Children per parent | 2,000 OUs per organization | 10,000 management groups per directory | 300 direct child folders per parent |
| Default account or project count | 10 accounts, adjustable to 50,000 | Varies by agreement | Per-user project creation quota |

Sources: [AWS Organizations quotas](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html),
[Azure management groups overview](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview),
[Google Cloud Resource Manager limits](https://docs.cloud.google.com/resource-manager/docs/limits).

Three facts from those pages that show up in questions:

- The **AWS default account quota is 10**, not unlimited. Candidates assume an organization
  starts unbounded. It does not, though the increase goes to 50,000.
- The **Azure root management group cannot be moved or deleted**, its ID equals the Entra
  tenant ID, and new subscriptions land in it by default. Nobody has access to it by default
  either. A Global Administrator must first elevate to User Access Administrator.
- Azure Resource Manager **caches the management group hierarchy for up to 30 minutes**, so a
  move can appear not to have happened.

## Grouping Objects Are Not Equivalent

The single most costly false friend in the entire subject.

| | AWS organizational unit | Azure resource group | Azure management group | Google folder |
| --- | --- | --- | --- | --- |
| Mandatory? | No | **Yes**, every resource is in exactly one | No | No |
| Holds | Accounts | Resources | Subscriptions and other management groups | Projects and other folders |
| Deleting it deletes contents? | No | **Yes** | No | Yes, with the projects inside |
| Move contents later? | Yes | Sometimes, and many resource types refuse | Yes | Yes |
| Sits above or below the billing boundary? | Above accounts | **Below** subscriptions | Above subscriptions | Above projects |

An Azure resource group is not an AWS OU. It sits on the other side of the billing boundary,
it is compulsory, and deleting it destroys everything inside. The closest AWS analogue to a
resource group is a CloudFormation stack, and that analogy is itself imperfect.

An **AWS resource group** exists and is a different thing again: an optional, tag-driven view
over resources. Two clouds, one phrase, two unrelated concepts, one of which is load-bearing.

## Global, Regional, Zonal

Where a resource lives decides what happens when infrastructure fails, and it is the highest
frequency trap in the whole subject.

| Resource | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Virtual network | **Regional** | **Regional** | **Global** |
| Subnet | **Zonal**, one AZ | **Regional** | **Regional** |
| Virtual machine | Zonal | Zonal | Zonal |
| Managed disk or volume | Zonal | Zonal | Zonal, or regional if replicated |
| Object storage bucket | Regional, global namespace | Regional, global namespace | Regional, dual-region, or multi-region; global namespace |
| Load balancer | Regional, except CloudFront and Global Accelerator | Regional, except Front Door and Traffic Manager | Regional or global, chosen at creation |
| IAM identities | Global | Global | Global |

The two rows to burn in:

- **A Google VPC is a global object.** One VPC spans every region. Subnets inside it are
  regional. A virtual machine in Tokyo and one in Frankfurt can sit in the same VPC and route
  to each other over Google's backbone without peering. Nothing in AWS or Azure works this way.
- **An AWS subnet lives in exactly one availability zone.** Azure subnets are regional and
  span the zones. This means "spread across zones" is a subnet-design problem in AWS and a
  resource-placement problem in Azure.

## Zones Are Not the Same Word

| Term | Cloud | What it is |
| --- | --- | --- |
| Availability Zone | AWS | One or more discrete data centres in a region, with independent power and cooling |
| Availability Zone | Azure | The same idea, but not enabled in every region, and opt-in per resource |
| Zone | Google Cloud | A deployment area within a region, named like `us-central1-a` |
| **Availability Set** | Azure only | A within-datacentre construct using fault domains and update domains. **Not a zone.** No AWS or Google equivalent |

The Azure availability set is the one that catches people. It protects against rack-level
failure and host patching inside a single datacentre. It does not protect against a datacentre
failing. An availability zone does. Choosing an availability set when the question says
"datacentre outage" is a wrong answer, and the distractor is deliberately placed.

AWS also **shuffles zone names per account**. The `us-east-1a` in one account is generally not
the same physical zone as `us-east-1a` in another. AWS exposes a stable AZ ID such as `use1-az1`
for when the physical identity matters.

## Naming and Uniqueness

| Thing | Uniqueness scope |
| --- | --- |
| S3 bucket name | Global, across every AWS customer |
| Azure storage account name | Global, and it becomes a DNS label |
| Google Cloud Storage bucket name | Global, across every Google customer |
| Google project ID | Global, permanent, and cannot be reused after deletion |
| AWS account ID | Global, 12 digits, assigned |
| Azure resource group name | Unique within its subscription only |

Google project IDs deserve a note. A project has a **name** you can change, an **ID** you
choose once and can never change or reuse, and a **number** Google assigns. Questions exploit
the difference between them.

## What Happens When You Delete the Container

| Action | Result |
| --- | --- |
| Close an AWS account | Enters a post-closure period before permanent closure; still counts against the organization quota until permanently closed |
| Delete an Azure resource group | Deletes every resource inside it, without a per-resource prompt |
| Delete a Google project | Enters a 30-day recovery window, then deletes; the project ID is never reusable |

The Azure behaviour is the one that surprises people who came from AWS, where no equivalent
container deletes its contents.

## Practical Consequences

- **Coming from AWS to Google Cloud:** stop thinking of the network as regional, and stop
  putting subnets in zones. Use projects the way you used accounts, and expect to create far
  more of them than you created accounts.
- **Coming from AWS to Azure:** every resource must go in a resource group, so decide the
  grouping before you deploy. Do not map a resource group to an OU; the levels do not line up.
- **Coming from Azure to AWS:** there is no resource group. Lifecycle grouping is done with
  tags, CloudFormation stacks, or separate accounts, and separate accounts are used far more
  freely than separate subscriptions.
- **Coming from Google Cloud anywhere:** your VPC is about to become regional, and cross-region
  traffic is about to need peering or a transit construct.

## Next

- [02-identity.md](02-identity.md) for who is allowed to do what, the area candidates report
  as hardest.
- [09-confusing-terms.md](09-confusing-terms.md) for the word-by-word decoder.

<!-- This document follows common-doc-guidelines.md. -->
