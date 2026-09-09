# The Exam Map

Which certification is which, what each exam actually asks, and the traps that recur. Exam
codes and formats change more often than anything else in this guide, so this chapter links to
vendor pages rather than trying to be the record.

Facts marked **verified** were checked against the vendor's own page on 9 September 2026. Other
statements are general and should be confirmed on the exam guide before you book.

## Foundational and Associate at a Glance

| | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Entry level | Cloud Practitioner (CLF-C02) | Azure Fundamentals (AZ-900) | Cloud Digital Leader |
| Core architecture | Solutions Architect, Associate (SAA-C03) | Azure Administrator (AZ-104), then AZ-305 for design | Associate Cloud Engineer |
| Operations | CloudOps Engineer, Associate (SOA-C03) | Folded into AZ-104 | Folded into Associate Cloud Engineer |
| Development | Developer, Associate (DVA-C02) | **Retired.** AZ-204 is gone | Professional Cloud Developer |
| Data entry point | Data Engineer, Associate | Azure Data Fundamentals (DP-900) | Associate Data Practitioner |
| AI entry point | AI Practitioner | Azure AI Fundamentals (AI-900) | Generative AI Leader |

Two of those cells deserve attention.

**The AWS operations exam was renamed.** AWS Certified SysOps Administrator, Associate became
AWS Certified CloudOps Engineer, Associate. SOA-C02 could last be sat on 29 September 2025 and
SOA-C03 launched the next day. The new exam runs 130 minutes, 65 questions, at 150 USD, in
English, Japanese, Korean and Simplified Chinese, at a Pearson VUE centre or online proctored.
Verified on the [AWS coming soon page](https://aws.amazon.com/certification/coming-soon/).

**The Azure developer certification is retired.** Microsoft Certified: Azure Developer
Associate, the AZ-204 credential, carries a retirement banner on its own Microsoft Learn page
covering both the certification and its renewal assessment, and the page is marked `noindex`.
Verified on
[the credential page](https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/).
A great deal of AZ-204 course material is still on sale. The Azure data engineering exam DP-203
is also retired, with Microsoft's warehouse story having moved into Fabric.

## Scoring, Which Is Not Comparable

| | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Scale | 100 to 1000, scaled | 1 to 1000, scaled | Not published |
| Pass mark | 700 for foundational and associate | 700 | Not published |
| Result | Scaled score and section feedback | Scaled score and section feedback | Pass or fail only |

**700 out of 1000 is not 70%.** Both AWS and Microsoft use a scaled score, so the number of
questions you must answer correctly is not 70% and is not disclosed. Candidates routinely
misread this and either panic or coast. Google publishes no score at all: you are told you
passed or you did not.

Section feedback on AWS and Azure tells you which domains were weak. It does not tell you which
questions you got wrong, and AWS explicitly warns against reading too much into per-domain bars
on a small number of questions.

## Format, Which Does Not Transfer

| | AWS | Azure | Google Cloud |
| --- | --- | --- | --- |
| Question types | Multiple choice, multiple response | Multiple choice, multiple select, case study, drag and drop, hot area, yes/no, sometimes interactive labs | Multiple choice, multiple select, case studies |
| Typical associate length | 130 minutes, 65 questions | AZ-104 allows 100 minutes (verified) | Two hours |
| Can you go back? | Yes, flag and review | **Not always.** Some Azure case study and lab sections lock once left | Yes |
| Renewal | Three years | **12 months** on AZ-104, free online assessment (verified) | Two years for associate, three for professional |

Three consequences:

- **Azure's format is the outlier.** Roughly 40% of AZ-104 is traditional multiple choice and
  the rest is scenario-based or interactive, according to third-party practice providers. Treat
  that split as indicative rather than official; Microsoft does not publish it. What is
  official is that the exam may include interactive components, and candidates consistently
  report losing time on case studies.
- **Azure sections can lock.** Practising on AWS-style banks where you can revisit anything
  builds a habit that costs you on Azure. Read the on-screen instructions before entering a
  case study.
- **Microsoft certifications expire annually** and are renewed free by passing an online
  assessment on Microsoft Learn. AWS and Google run on multi-year cycles. This is an ongoing
  commitment people do not plan for.

## What Each Associate Exam Is Really Testing

Verified domain lists where the vendor publishes them.

**AWS Solutions Architect, Associate (SAA-C03)** rewards design judgement. Questions describe a
requirement and offer four workable services. The skill is eliminating options that are
technically possible but miss a stated constraint. Cost and operational overhead are the usual
tiebreakers.

**AWS CloudOps Engineer, Associate (SOA-C03)** covers monitoring and maintaining workloads,
implementing security controls and networking, business continuity procedures, and cost and
performance optimisation.

**Azure Administrator (AZ-104)** covers, in Microsoft's own words: manage Azure identities and
governance; implement and manage storage; deploy and manage Azure compute resources; implement
and manage virtual networking; monitor and maintain Azure resources. It leans operational and
configuration-focused where SAA-C03 leans architectural. Without portal or CLI experience the
scenario questions become guesswork.

**Google Associate Cloud Engineer** rewards a decision-engineering mindset: several solutions
are technically valid and only one matches the stated operational priority, so correctness is
contextual. Candidates report IAM permissions and service account edge cases as the hardest
part, and constant trade-offs between cost, scalability, operational overhead, latency and
security.

## Traps by Cloud

### AWS

- A security group cannot deny. Blocking one address needs a network ACL.
- Network ACLs are stateless. Return traffic needs its own rule.
- Multi-AZ is for failover and is not readable. A read replica is readable and does not fail
  over automatically. Both will be offered.
- An SCP never grants anything. It only limits.
- Availability zone names are shuffled per account.
- Gateway endpoints are free and serve only S3 and DynamoDB. Interface endpoints cost money and
  serve nearly everything.
- "Least operational overhead" almost always selects the managed or serverless option even when
  a cheaper self-managed one exists.

### Azure

- RBAC scope inheritance is additive and downward. A grant at the subscription applies to every
  resource group beneath it.
- Entra roles are not Azure RBAC roles. A Global Administrator has no resource access until they
  elevate.
- Azure Policy is not RBAC. Enforcing a configuration is a Policy answer.
- An availability set is not an availability zone. Datacentre-level failure means zones.
- Service endpoint and private endpoint are different. On-premises access means private
  endpoint.
- Traffic Manager is DNS only. TLS termination or header routing means Front Door.
- Learn the redundancy acronyms literally: LRS, ZRS, GRS, GZRS, and the RA- prefix.
- Deleting a resource group deletes everything in it.

### Google Cloud

- The VPC is global. Subnets are regional. Nothing is zonal at the network level.
- Firewall rules attach to the network and target by network tag or service account.
- Basic roles, Owner, Editor and Viewer, are almost always wrong in a least-privilege scenario.
- IAM inheritance is additive and cannot be narrowed lower down.
- Using a service account needs a role on the service account itself.
- Downloadable service account keys are the wrong answer wherever an alternative exists.
- Sustained use discounts apply automatically with no commitment. There is no AWS or Azure
  equivalent, and it is a free mark.
- Cloud Functions is now Cloud Run functions. Most study material has not caught up.

## Distractor Patterns Common to All Three

1. **The technically-correct-but-costly option.** Works, ignores a stated cost constraint.
2. **The self-managed option** where the question says "minimise operational overhead".
3. **The right service at the wrong scope**, such as a regional answer to a global requirement.
4. **The superseded product**, still real and still sold, but not what the question is after.
5. **The adjacent service with a similar name**, which is what the decoder chapter is for.

When two answers both look right, re-read the question for the constraint word: cheapest, least
operational overhead, fastest to implement, minimum downtime, must survive a region failure.
That word, not the technology, is what is being tested.

## Next

- [09-confusing-terms.md](09-confusing-terms.md) for the vocabulary these exams exploit.
- [research-pain-points.md](research-pain-points.md) for the evidence behind this chapter.

<!-- This document follows common-doc-guidelines.md. -->
