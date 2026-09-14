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

## Use Current Exam Instructions

Question types, timing, review restrictions and renewal paths depend on the exact credential.
Use the linked official exam guide and the on-screen instructions. Google labels such as
`ACE` and `PCA` in this project are convenient abbreviations, not a promise of official exam codes.

Technical scenarios in this guide are original learning exercises. Product availability,
service retirement and exam retirement are separate facts. Avoid rules that select a service
from one word while ignoring the stated constraints.

**Next:** [practice](practice.md) · [full comparison reference](README.md) ·
[chapter index](README.md).

<!-- This document follows common-doc-guidelines.md. -->
