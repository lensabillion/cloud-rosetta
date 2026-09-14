# Cloud Foundations

AWS, Microsoft Azure and Google Cloud provide computing services that you configure and use
through consoles, APIs and automation. This guide compares architectural behavior. It does not
assume a certification or prior experience.

## Start With One Application

Imagine a photo-sharing application. A person uploads a photo, adds a caption, and later views it.
The architecture has six decisions:

| Decision | What the application needs |
| --- | --- |
| Compute | Run the code that checks an upload and responds to requests |
| Storage | Keep the photo as an object; query captions and ownership as database records |
| Networking | Decide which endpoints are public and how services reach each other |
| Identity | Authenticate people and give the application narrowly scoped permissions |
| Availability | Decide what should keep working after a machine, zone or region fails |
| Cost | Estimate usage, storage, requests, replicas and data transfer; set budgets and alerts |

These are requirements, not a claim that every application needs the same products. The
[architecture atlas](architecture.md) draws a logical request flow and three provider-specific
implementations. They are alternatives, not a requirement to deploy to all three clouds.

## What You Still Manage

A managed service reduces some operational work; it does not remove responsibility for data,
access or configuration. In SaaS, customers still control user access, data handling and
available application settings. IaaS generally also leaves the guest operating system and
application stack to the customer. The exact division depends on the service.
[AWS shared responsibility](https://aws.amazon.com/compliance/shared-responsibility-model/),
[Azure shared responsibility](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility),
[Google shared responsibility](https://docs.cloud.google.com/architecture/framework/security/shared-responsibility-shared-fate).

![Responsibilities retained across cloud service models](assets/architecture/responsibility.svg)

## Vocabulary for the Next Chapter

| Term | Meaning |
| --- | --- |
| Region | A geographic service location. Availability, supported features and prices depend on the region |
| Zone | A failure domain within a region. Resilience requires distribution and recovery, not just selecting a zone |
| Egress | Outbound data transfer. Charges depend on source, destination, service and allowances |
| Managed service | A service whose provider operates some infrastructure or software layers for you |
| Elasticity | Adjusting capacity to demand, within configured and available limits |
| Availability | Whether a service can successfully serve requests when needed |
| Durability | Whether stored data remains intact; different from immediate accessibility |
| RTO / RPO | Recovery time objective and recovery point objective: target recovery time and tolerable data-loss window |

Treat pricing, quotas and service availability as design inputs to check, not constants to
memorize. A cheaper storage rate may be outweighed by retrieval or transfer costs. A replicated
database can still replicate an accidental deletion.

## Learn the Provider Boundaries

An AWS account, an Azure subscription and a Google project are useful starting points for
resource administration, but they are not interchangeable billing and identity systems.
[Resource models](01-mental-models.md) explain those differences before the service catalogue.

## Choose a Reading Route

- New to cloud: [resource models](01-mental-models.md), [identity](02-identity.md), then
  [networking](03-networking.md).
- Already know one provider: use the [decoder](09-confusing-terms.md) and
  [architecture atlas](architecture.md) to test which assumptions transfer.
- Studying for an exam: use the [exam map](10-exam-map.md) to find official objectives.

Market-share estimates and adoption surveys are not architecture requirements. Earlier research
notes retain their historical context; they are not evidence that a provider is the best choice
for this application.

<!-- This document follows common-doc-guidelines.md. -->
