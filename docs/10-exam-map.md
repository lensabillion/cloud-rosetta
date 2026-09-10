# The Exam Map

**Goal:** choose a current study path and use comparisons as supporting material.
This is a cross-cloud guide, not complete coverage of any certification syllabus. Exam tags
mean that a concept is relevant to the topic, not that a question will appear on an exam.
Use the official objectives to build your checklist.

<!-- BEGIN EXAMS. Generated from data/exams.yml by scripts/build.py -->

## Current Exams (18)

### AWS

| Code | Certification | Level | Verified |
| --- | --- | --- | --- |
| `CLF-C02` | [AWS Certified Cloud Practitioner](https://aws.amazon.com/certification/certified-cloud-practitioner/) | foundational | 2026-09-10 |
| `DVA-C02` | [AWS Certified Developer - Associate](https://aws.amazon.com/certification/certified-developer-associate/) | associate | 2026-09-10 |
| `SAA-C03` | [AWS Certified Solutions Architect - Associate](https://aws.amazon.com/certification/certified-solutions-architect-associate/) | associate | 2026-09-10 |
| `SOA-C03` | [AWS Certified CloudOps Engineer - Associate](https://aws.amazon.com/certification/certified-cloudops-engineer-associate/) | associate | 2026-09-10 |
| `SAP-C02` | [AWS Certified Solutions Architect - Professional](https://aws.amazon.com/certification/certified-solutions-architect-professional/) | professional | 2026-09-10 |
| `SCS-C03` | [AWS Certified Security - Specialty](https://aws.amazon.com/certification/certified-security-specialty/) | specialty | 2026-09-10 |

### Azure

| Code | Certification | Level | Verified |
| --- | --- | --- | --- |
| `AZ-900` | [Azure Fundamentals](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/) | foundational | 2026-09-10 |
| `DP-900` | [Azure Data Fundamentals](https://learn.microsoft.com/en-us/credentials/certifications/azure-data-fundamentals/) | foundational | 2026-09-10 |
| `AZ-104` | [Azure Administrator Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-administrator/) | associate | 2026-09-10 |
| `AZ-700` | [Azure Network Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-network-engineer-associate/) | associate | 2026-09-10 |
| `SC-300` | [Identity and Access Administrator Associate](https://learn.microsoft.com/en-us/credentials/certifications/identity-and-access-administrator/) | associate | 2026-09-10 |
| `AZ-305` | [Designing Microsoft Azure Infrastructure Solutions (exam toward Architect Expert)](https://learn.microsoft.com/en-us/credentials/certifications/exams/az-305/) | expert | 2026-09-10 |

### Google Cloud

| Code | Certification | Level | Verified |
| --- | --- | --- | --- |
| `CDL` | [Cloud Digital Leader](https://cloud.google.com/learn/certification/cloud-digital-leader) | foundational | 2026-09-10 |
| `GENAI-L` | [Google Cloud Generative AI Leader](https://cloud.google.com/learn/certification/generative-ai-leader) | foundational | 2026-09-10 |
| `ACE` | [Associate Cloud Engineer](https://cloud.google.com/learn/certification/cloud-engineer) | associate | 2026-09-10 |
| `ADP` | [Google Cloud Associate Data Practitioner](https://cloud.google.com/learn/certification/data-practitioner) | associate | 2026-09-10 |
| `PCA` | [Google Cloud Professional Cloud Architect](https://cloud.google.com/learn/certification/cloud-architect) | professional | 2026-09-10 |
| `PDE` | [Google Cloud Professional Data Engineer](https://cloud.google.com/learn/certification/data-engineer) | professional | 2026-09-10 |

## Retired (3)

Listed rather than deleted, because course material for them is still on sale.

| Code | Certification | Cloud | Note |
| --- | --- | --- | --- |
| `AZ-204` | [Azure Developer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/) | Azure | Certification and renewal assessment retired; the page carries a retirement banner. |
| `AZ-500` | [Azure Security Engineer Associate](https://learn.microsoft.com/en-us/credentials/certifications/azure-security-engineer/) | Azure | Certification and renewal assessment retired; the page carries a retirement banner. |
| `SCS-C02` | [AWS Certified Security - Specialty (SCS-C02)](https://aws.amazon.com/certification/certified-security-specialty/) | AWS | Exam version superseded by SCS-C03. The certification itself is current. |

<!-- END EXAMS -->

## Understand the Score and Renewal Rules

AWS's scaled passing scores are 700 for foundational exams, 720 for associate exams, and 750
for professional/specialty exams. A scaled score is not the percentage of questions answered
correctly. [AWS scoring policy](https://aws.amazon.com/certification/policies/after-testing/).

Google's foundational and associate certifications are valid for three years; professional
certifications are valid for two. Renewal options are credential-specific.
[Google certification policy](https://support.google.com/cloud-certification/answer/9750149?hl=en).

Microsoft role-based and specialty certifications generally require annual renewal; Fundamentals
credentials do not expire. Check the credential's page for its requirements, prerequisites, and
current exam format. [Microsoft expiration policy](https://learn.microsoft.com/en-us/credentials/support/certification-expiration-policy).
An exam retirement and a product retirement are separate events.

## Study the Decision, Not the Keyword

1. Read the current official objectives and mark unfamiliar domains.
2. Learn the [resource model](01-mental-models.md), [identity](02-identity.md), and
   [networking](03-networking.md) before memorizing service names.
3. For each scenario identify the required behavior: scope, access, data loss, recovery time,
   read capacity, or cost. Then compare the relevant service modes.
4. Explain why an alternative fails a stated constraint. Avoid rules such as “Multi-AZ is
   never readable”: [RDS deployment types differ](05-databases.md).
5. Practice the official exam interface and use the provider's current preparation resources.
   The [practice scenarios here](practice.md) build reasoning but do not predict your exam score.

## Format, Which Does Not Transfer

Practising on one vendor's question style does not prepare you for another's.

| | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Question types | Multiple choice, multiple response | Multiple choice, multiple select, case study, drag and drop, hot area, yes/no, sometimes interactive labs | Multiple choice, multiple select, case studies |
| Typical associate length | 130 minutes, 65 questions | AZ-104 allows 100 minutes | Two hours |
| Can you revisit answers? | Yes, flag and review | **Not always.** Some case study and lab sections lock once left | Yes |
| Result detail | Scaled score with section feedback | Scaled score with section feedback | Pass or fail only, no score published |

Two consequences worth planning around. **Azure sections can lock**, so read the on-screen
instructions before entering a case study; a habit built on AWS-style banks where anything can
be revisited will cost you. And **Microsoft role-based certifications renew annually**, free,
through an online assessment, where AWS and Google run multi-year cycles.

## Traps by Cloud

### AWS

- A security group has allow rules only. Blocking one address while broad allows remain needs a
  deny-capable control such as a network ACL.
- Network ACLs are stateless, so return traffic needs its own rule on ephemeral ports.
- **Read the RDS deployment type before answering a Multi-AZ question.** A Multi-AZ DB instance
  keeps an unreadable standby for failover; a Multi-AZ DB cluster has readable standbys. A read
  replica scales reads and does not fail over automatically. See [Databases](05-databases.md).
- An SCP never grants anything. It only limits what IAM may grant.
- Availability zone names are shuffled per account; use the AZ ID when physical identity matters.
- Gateway endpoints are free and serve only S3 and DynamoDB. Interface endpoints cost money and
  serve nearly everything.
- "Least operational overhead" usually selects the managed option even when a cheaper
  self-managed one exists.

### Azure

- RBAC inheritance is additive and downward. A grant at the subscription reaches every resource
  group beneath it.
- Entra roles are not Azure RBAC roles. A Global Administrator holds no resource access until
  they elevate to User Access Administrator at root scope.
- Azure Policy is not RBAC. Enforcing a required configuration is a Policy answer.
- An availability set is not an availability zone. Data centre level failure means zones.
- Service endpoint and private endpoint differ. On-premises access with a private address means
  private endpoint.
- Traffic Manager is DNS only. TLS termination or header routing at the edge means Front Door.
- Learn the redundancy acronyms literally: LRS, ZRS, GRS, GZRS, and the RA- prefix.
- Deleting a resource group deletes everything inside it.

### Google Cloud

- The VPC is global and subnets are regional. Nothing is zonal at the network level.
- Firewall rules belong to the network and select targets by network tag or service account.
- Basic roles, Owner, Editor and Viewer, are almost always wrong in a least-privilege scenario.
- IAM inheritance is additive and cannot be narrowed by a smaller grant lower down.
- Using a service account needs a role on the service account itself.
- Downloadable service account keys are the wrong answer wherever an alternative exists.
- Sustained use discounts apply automatically with no commitment, and have no AWS or Azure
  equivalent.
- Cloud Functions is now Cloud Run functions. Most study material has not caught up.

## Distractor Patterns Common to All Three

1. **The technically correct but costly option**, which works and ignores a stated cost limit.
2. **The self-managed option** where the question asks for least operational overhead.
3. **The right service at the wrong scope**, such as a regional answer to a global requirement.
4. **The superseded product**, still real and still sold, but not what is being asked for.
5. **The adjacent service with a similar name**, which is what
   [the decoder](09-confusing-terms.md) exists to defuse.

When two answers both look right, find the constraint word: cheapest, least operational
overhead, fastest to implement, minimum downtime, must survive a region failure. That word is
what is being tested, not the technology.

**Next:** [practice](practice.md) · [full comparison reference](README.md) ·
[chapter index](README.md).

<!-- This document follows common-doc-guidelines.md. -->
