# The Landscape: What These Three Things Are, and Where They Stand

Orientation, not comparison. Five minutes, and you can read every other chapter without looking
anything up.

Figures verified 9 September 2026. Every number links to its source.

## What a Cloud Provider Actually Sells

All three sell the same thing: **someone else's computers, rented by the minute.** The layers
below are named identically by all three vendors.

| Layer | You manage | They manage | Example |
| --- | --- | --- | --- |
| **Infrastructure as a service**, IaaS | The operating system and everything above | Hardware, virtualisation, network, power | A virtual machine |
| **Platform as a service**, PaaS | Your code and data | Everything below your code | A managed database |
| **Software as a service**, SaaS | Your data only | Everything | A hosted email product |

<!-- diagram: responsibility -->

All three publish this as a **shared responsibility model**
([AWS](https://aws.amazon.com/compliance/shared-responsibility-model/),
[Azure](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility),
[Google Cloud](https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate)).
Every foundational exam asks it: **the provider secures the cloud, you secure what you put in
it.** Patching the hypervisor is theirs. Leaving a bucket public is yours.

## The Three Providers in One Paragraph Each

**Amazon Web Services** launched in 2006 and is the oldest of the three. It has the widest
service catalogue and the most granular building blocks, which is both its strength and the
reason it feels overwhelming. Its design philosophy is small composable primitives you assemble
yourself. [Documentation](https://docs.aws.amazon.com/).

**Microsoft Azure** is built around Microsoft's existing enterprise relationships, so it
integrates tightly with Active Directory, Windows Server, Office and the licences companies
already hold. Its identity system, Microsoft Entra ID, is the same directory that signs people
into Microsoft 365, which is why Azure feels natural to organisations already inside that world
and strange to everyone else. [Documentation](https://learn.microsoft.com/en-us/azure/).

**Google Cloud** is the newest of the three at scale and exposes the infrastructure Google built
for itself. It is opinionated where the others are flexible, its network is global by default
rather than regional, and its data and machine learning products are the reason many
organisations choose it. [Documentation](https://docs.cloud.google.com/).

## Current State of the Market

Cloud infrastructure spending reached **129 billion US dollars in a single quarter**, growing
35% year on year, according to Synergy Research Group figures reported by
[Statista](https://www.statista.com/chart/18819/worldwide-market-share-of-leading-cloud-infrastructure-service-providers/).

Share of that market, for the first quarter of 2026:

| Provider | Share |
| --- | --- |
| Amazon Web Services | 28% |
| Microsoft Azure | 21% |
| Google Cloud | 14% |
| Everyone else combined | ~37% |

Take the shape, not the ranking. **The three together hold about 63%** of a market growing 35% a
year, with no fourth competitor close, so these three cover most of the industry. Later
reporting puts the combined share at 67% and Google at a record 15%, growing fastest of the
three, though those figures are secondary rather than from Synergy directly.

## Who Actually Uses Them

Market share measures money, not what is running where. From the
[Flexera 2026 State of the Cloud Report](https://www.flexera.com/blog/finops/flexera-2026-state-of-the-cloud-report-the-convergence-of-cloud-and-value/):

| Finding | Figure |
| --- | --- |
| Enterprises using cloud in some form | 94% |
| Running active workloads on AWS | 83% |
| Running active workloads on Azure | 79% |
| Using more than one provider | 89% |
| Using a hybrid model, cloud plus on-premises | 73% |
| Cloud spend wasted, on average | 32% |

⚠️ Flexera sells cost management software, so it has a commercial interest in the waste figure
being high and in multi-cloud complexity being real. The adoption numbers are broadly consistent
with other surveys; treat the 32% waste figure as directional.

Three consequences shape this guide. **AWS and Azure are nearly tied on usage**, 83% against
79%, despite a seven-point revenue gap. **89% use more than one provider**, which is the whole
reason this project exists. And **Google is a distant third by workload count** but concentrates
in data analytics and machine learning, where it is chosen deliberately rather than by default.

## Where Certifications Fit

Each vendor runs its own programme and none recognises the others. Passing an AWS exam gives you
nothing on Azure, and the concepts transfer far less cleanly than people expect.

| | Entry level | First serious credential |
| --- | --- | --- |
| AWS | [Cloud Practitioner, CLF-C02](https://aws.amazon.com/certification/certified-cloud-practitioner/) | [Solutions Architect Associate, SAA-C03](https://aws.amazon.com/certification/) |
| Azure | [Azure Fundamentals, AZ-900](https://learn.microsoft.com/en-us/credentials/certifications/azure-fundamentals/) | [Azure Administrator, AZ-104](https://learn.microsoft.com/en-us/credentials/certifications/azure-administrator/) |
| Google Cloud | [Cloud Digital Leader](https://cloud.google.com/learn/certification) | [Associate Cloud Engineer](https://cloud.google.com/learn/certification/cloud-engineer) |

Full detail, including which exams have been retired and how the scoring differs, is in
[10-exam-map.md](10-exam-map.md). The short warning: **the Azure developer certification AZ-204
is retired** and a great deal of course material for it is still on sale.

## The Vocabulary You Need Before Chapter One

Six words all three use identically. The rest of this guide is about the ones they do not.

| Term | Meaning |
| --- | --- |
| **Region** | A geographic area containing multiple data centres. You choose one, and it affects latency, price, and which laws apply |
| **Zone** | An isolated failure domain inside a region. Spreading across zones is how you survive a data centre outage |
| **Egress** | Data leaving the provider's network. All three charge for it, and it is the cost that surprises people |
| **Managed service** | Something the provider operates for you. Costs more per hour, costs less in staff time |
| **Elasticity** | Capacity that grows and shrinks with demand. The core economic argument for cloud |
| **Availability and durability** | Availability is whether you can reach your data now. Durability is whether it still exists. They are different numbers and exams test the difference |

## Where to Go Next

- **New to all of this:** [01-mental-models.md](01-mental-models.md), which explains why the
  three clouds are shaped differently before naming a single service.
- **Already know one cloud, learning a second:** skip to
  [09-confusing-terms.md](09-confusing-terms.md). The words will hurt you before the services do.
- **Preparing for a specific exam:** [10-exam-map.md](10-exam-map.md).
- **Want only the dangerous parts:** open the guide and filter to ❗.

<!-- This document follows common-doc-guidelines.md. -->
