# What Candidates Actually Find Painful

This document records what people who sit AWS, Azure, and Google Cloud exams report as the
hardest parts. It exists to aim the rest of the guide: chapters get depth in proportion to
the pain recorded here, not in proportion to how much there is to say.

## Method and Confidence

Findings come from vendor exam guides, vendor documentation, and published exam-experience
write-ups gathered in September 2026. Sources are cited inline. Treat these as *reported*
difficulty rather than measured difficulty. No vendor publishes per-question failure rates,
so nothing here is a controlled result, and self-selected write-ups skew toward people who
passed and then blogged about it.

Where a claim is only weakly supported, it is marked ⚠️.

## Pain Point 1: Several Answers Are Technically Correct

The dominant complaint across all three vendors. Questions rarely test whether a service
exists. They test which of four workable services best fits a stated constraint.

- AWS scenario questions require deciding which service or architecture is *most
  appropriate*, rather than recalling a definition. Candidates report that the useful skill
  was practicing the reasoning behind an answer rather than memorizing questions, and
  learning to eliminate options that look technically possible but miss a stated
  requirement. See [Educative's SAA write-up](https://www.educative.io/blog/how-to-pass-aws-solutions-architect-exam).
- Google's Associate Cloud Engineer shifts candidates into a decision-engineering mindset,
  where several solutions are technically valid but only one matches the stated operational
  priority, so correctness is contextual rather than absolute. A recurring difficulty is
  balancing cost, scalability, operational overhead, latency, and security against each
  other. See [Exam-Labs on ACE difficulty](https://www.exam-labs.com/blog/assessing-the-difficulty-of-the-google-associate-cloud-engineer-certification-exam).

**Consequence for this guide:** every mapping table needs a column for *where the mapping
breaks down*, and every chapter needs the constraint keywords that select between near-
equivalent services. A table of equivalents alone actively misleads.

## Pain Point 2: The Clouds Are Shaped Differently, Not Just Named Differently

Engineers who know one cloud well assume the second is a renaming exercise. It is not.

Services are similar, not identical: virtual machine products across the three clouds differ
in pricing models, image handling, and networking even though all three run virtual
machines. Azure calls its network a VNet while AWS and Google both say VPC, yet the
implementations differ. See
[Lucidchart's cloud terminology glossary](https://www.lucidchart.com/blog/cloud-terminology-glossary)
and [Microsoft's own Google Cloud to Azure comparison](https://learn.microsoft.com/en-us/azure/architecture/gcp-professional/services).

The structural differences that cause the most wrong answers:

- Google's VPC is a global resource with regional subnets. AWS VPCs are regional with zonal
  subnets. Someone carrying AWS habits into a Google exam will place subnets in zones.
- The isolation boundary is an account in AWS, a subscription in Azure, and a project in
  Google Cloud. These are not interchangeable, and billing, quota, and IAM scope attach to
  them differently.

**Consequence for this guide:** the mental-models chapter comes first and is not optional.
Service tables mean little before the scoping model is clear.

## Pain Point 3: The Same Word Means Different Things

The highest-value section of this guide, and the one no vendor writes because each vendor
only documents its own vocabulary.

Confirmed collisions worth teaching:

- **Role.** An AWS IAM role is an assumable identity with its own credentials. An Azure or
  Google role is a named set of permissions granted to a separate principal. Same word,
  different category of thing.
- **Resource group.** In Azure this is a mandatory lifecycle and deployment container that
  every resource lives in. In AWS a resource group is an optional, tag-driven view over
  resources. The Azure one is load-bearing; the AWS one is a convenience.
- **Policy.** In AWS a policy is a permissions document. Azure Policy is a governance and
  compliance engine that is separate from Azure RBAC. In Google Cloud, "policy" means either
  an IAM allow policy or an organization policy constraint.
- **ASG.** An AWS Auto Scaling Group and an Azure Application Security Group share an
  acronym and nothing else.
- **Container.** In Azure Blob Storage a container is a bucket-like grouping of blobs, not
  an OCI container image.

Azure candidates specifically report misjudging RBAC scope inheritance and confusing NSG
rule evaluation with firewall behavior as recurring mistakes. See
[TheServerSide's AZ-104 study guide](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Free-Azure-Administrator-Questions-and-Answers-AZ-104-Study-Guide).

**Consequence for this guide:** the decoder is a first-class chapter, alphabetical, with a
"false friend" marker on any term that means different things per cloud.

## Pain Point 4: Study Material Goes Stale Faster Than Candidates Notice

Vendors rename and retire aggressively, and third-party courses lag. Verified renames as of
September 2026:

| Was | Is now | Note |
| --- | --- | --- |
| Cloud Functions (2nd gen) | Cloud Run functions | Deployed as a Cloud Run service; manageable through the Cloud Run Admin API |
| Cloud Functions (1st gen) | Cloud Run functions (1st gen) | Original version, kept but re-prefixed |
| AWS Certified SysOps Administrator, Associate (SOA-C02) | AWS Certified CloudOps Engineer, Associate (SOA-C03) | SOA-C02 last sat 29 September 2025; SOA-C03 launched 30 September 2025 |

Sources: [Cloud Run functions version comparison](https://docs.cloud.google.com/functions/docs/concepts/version-comparison),
[AWS Certification coming soon](https://aws.amazon.com/certification/coming-soon/).

Retirements confirmed in the same pass: AWS Certified Advanced Networking, Specialty retires
31 December 2026. The Azure DP-203 data engineering exam has been retired. Microsoft Certified:
Azure Developer Associate, the AZ-204 credential, is retired: its Microsoft Learn page carries a
retirement banner covering both the certification and its renewal assessment, and the page is
marked `noindex`. This one is worth dwelling on, because a large amount of third-party AZ-204
course material is still on sale.

**Consequence for this guide:** every chapter carries a "verified on" date, and the exam
chapter links to vendor pages rather than restating volatile details.

## Pain Point 5: Format Shock, Especially on Azure

Format differs enough between vendors that practice on one does not transfer.

- AWS associate exams are multiple choice and multiple response. The Solutions Architect
  Associate allows 130 minutes for 65 questions, roughly two minutes each, which candidates
  note disadvantages non-native English speakers given the reading load.
- Azure AZ-104 mixes multiple choice, multiple select, case study, drag and drop, hot area,
  and yes/no items. Reported splits put roughly 40% at traditional multiple choice and the
  rest scenario-based or interactive. Candidates report losing time on case studies. ⚠️ The
  40/60 split comes from a third-party practice provider, not Microsoft.
- Azure exams lean operational and configuration-focused, whereas the AWS Solutions Architect
  Associate leans toward architecture and design.

Sources: [Whizlabs AZ-104 guide](https://www.whizlabs.com/blog/az-104-microsoft-azure-administrator-certification/),
[TheServerSide AZ-104 study guide](https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/Free-Azure-Administrator-Questions-and-Answers-AZ-104-Study-Guide).

**Consequence for this guide:** the exam chapter documents format per exam, and drills
imitate the vendor's own question shape rather than one generic shape.

## Pain Point 6: Identity Is Where People Fail

Named independently for two of the three vendors.

- Google: configuring IAM permissions and service accounts correctly, particularly edge
  cases, is reported as the hardest part of the Associate Cloud Engineer exam.
- Azure: misjudging RBAC scope inheritance is a recurring mistake on AZ-104.

**Consequence for this guide:** identity gets the longest chapter and the most drills.

## Ranking Used to Allocate Depth

1. Identity and access
2. Networking, including the security-boundary vocabulary
3. Terminology collisions, as a standalone decoder
4. Resource hierarchy and scoping
5. Storage and database selection under constraints
6. Everything else

<!-- This document follows common-doc-guidelines.md. -->
