# Progress Log

What has been done, in order, with the reasoning. Kept current as work lands rather than written
at the end. Requirements are numbered in [requirements.md](requirements.md); beads are tracked in
`tbd`.

## 2026-09-09

### Setup

Initialised a git repository and ran `tbd setup --auto --prefix=cloud` on the user's instruction,
which added the beads tracker, an agent skill, hooks, and `AGENTS.md`. Loaded
`common-doc-guidelines` from `tbd guidelines` and adopted it for every document here: Title Case
on H1 and H2, sparing em dashes, "and" rather than an ampersand in prose, sources cited, and
confidence calibrated rather than asserted.

### Scoping

Asked three questions before writing anything, because the answers changed the shape of the work:
delivery format, exam level, and emphasis. Answers: Markdown repository plus a published web
guide, foundational and associate level, and all four emphases.

### Research, and What It Changed

Four research passes, each of which changed a decision rather than merely informing one.

**Pain points.** Vendor exam guides plus published exam experiences. The finding that shaped
everything: the difficulty is not finding a service's equivalent but that near-equivalents behave
differently. Identity was named independently as the hardest area on two of the three exams.
Recorded in [research-pain-points.md](research-pain-points.md). Consequence: identity gets the
longest chapter, and every mapping needs a "where it breaks" note.

**Existing resources.** Surveyed five community projects and both vendor comparison pages using
the GitHub API. [CloudComparer](https://github.com/ilyas-it83/CloudComparer) has 1,505 stars and
was last pushed in August 2024 with 39 open issues.
[Cloud Product Mapping](https://github.com/milanm/Cloud-Product-Mapping) has 928 stars and its
README is three parallel category lists rather than a row-level mapping. Recorded in
[research-existing-resources.md](research-existing-resources.md). Consequence: the whole data
model, in particular the required `breaks_when` field.

**GitHub precedents.** Studied [og-aws](https://github.com/open-guides/og-aws), 36,453 stars, on
the user's suggestion. Its severity legend is defined by consequence rather than novelty, which
exposed a genuine gap: our `divergence` grade measured how far a mapping transfers and said
nothing about how badly the difference bites. Recorded in
[research-github-precedents.md](research-github-precedents.md). Consequence: adopted a second
`bite` axis using og-aws's own definitions, plus a `maturity` marker for superseded products.

The same sweep found that the best AWS certification study guide on GitHub has 120 stars and the
best Google Cloud one has four, against 36,453 for a practical AWS guide. The niche is unserved
rather than unwanted.

**Typography.** Google Fonts usage data. Roboto leads cumulative use at roughly 28 trillion
views; Inter is the current preference at 414 billion views in the year to May 2025 and growing
57%. Used both, which is the honest reading of the evidence, and documented the trade-off that
they are stylistic neighbours in [design-decisions.md](design-decisions.md).

### Facts Verified Against Vendor Documentation

Not recalled. Fetched, on this date.

| Fact | Source |
| --- | --- |
| AWS allows five levels of OUs below a root; default 10 accounts, raisable to 50,000; maximum 10 SCPs per entity | [AWS Organizations quotas](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_reference_limits.html) |
| Azure allows six levels of management groups excluding root and subscription; 10,000 per directory; the root cannot be moved or deleted; ARM caches the hierarchy for 30 minutes | [Management groups overview](https://learn.microsoft.com/en-us/azure/governance/management-groups/overview) |
| Google allows ten levels of folders and 300 direct children per parent | [Resource Manager limits](https://docs.cloud.google.com/resource-manager/docs/limits) |
| Cloud Functions is now Cloud Run functions, deployed as a Cloud Run service | [Version comparison](https://docs.cloud.google.com/functions/docs/concepts/version-comparison) |
| SysOps Administrator Associate became CloudOps Engineer Associate; SOA-C02 retired 29 September 2025, SOA-C03 launched the next day | [AWS coming soon](https://aws.amazon.com/certification/coming-soon/) |
| **AZ-204 and the Azure Developer Associate certification are retired** | [Credential page](https://learn.microsoft.com/en-us/credentials/certifications/azure-developer/) |
| AZ-104 is active, 100 minutes, renewed every 12 months | [Credential page](https://learn.microsoft.com/en-us/credentials/certifications/azure-administrator/) |
| Cloud infrastructure is a $129bn quarter growing 35%; AWS 28%, Azure 21%, Google 14% | [Synergy via Statista](https://www.statista.com/chart/18819/worldwide-market-share-of-leading-cloud-infrastructure-service-providers/) |
| 83% of enterprises run workloads on AWS, 79% on Azure, 89% use more than one provider | [Flexera 2026 State of the Cloud](https://www.flexera.com/blog/finops/flexera-2026-state-of-the-cloud-report-the-convergence-of-cloud-and-value/) |

The AZ-204 retirement was first seen in a search result, flagged as unverified, then confirmed
directly on Microsoft's own page, which carries a retirement banner and is marked `noindex`. The
draft was corrected before publication. This is the exact failure mode the freshness machinery
exists to catch.

### Built

**The dataset.** 38 mapping rows and 16 terminology collisions in YAML, one file per domain so
pull requests do not collide, with JSON Schema for both content types.

**The validator.** `scripts/validate.py` enforces the rule the project rests on: a row graded
`partial` or `none` with an empty `breaks_when` fails the build. It also checks id uniqueness,
staleness with a hard limit, and links to retired domains. It earned its keep on first run by
catching an Azure-only term claiming a collision with nobody, and two rows graded `exact` while
carrying caveats. The latter prompted a `shared_trap` field so `breaks_when` keeps its strict
meaning.

**The chapters.** Landscape, mental models, identity, networking, exam map, plus the decoder,
which is generated from the data so the prose cannot drift.

**The surfaces.** After the question of whether HTML was the right representation, the answer
from the research was that on GitHub it is not the primary one. `scripts/surfaces.py` now emits
the README's content block, a Mermaid hierarchy diagram that GitHub renders natively, a shareable
SVG poster, 157 flashcards as tab-separated text for Anki, and the dataset as JSON. All from the
same YAML.

### Feedback and Corrections

**"The most boring, most bare minimum HTML."** Fair. The first build was a competent utilitarian
layout, which under-read a brief that had asked for visual appeal and creativity twice. Rebuilt
around the Rosetta Stone idea: three vendor scripts held in a fixed column spine running the
length of the page, a stone palette, Roboto at display weight, and a visible fracture drawn
between columns wherever the translation fails, so the page's own structure breaks where the
mapping breaks.

### Open

- A study path rather than only a reference. The highest-starred guides all have a progression,
  and this does not yet.
- Storage, compute and database chapters in long form; the data exists, the prose does not.
- Drills chapter.
- Contributor credit file.

<!-- This document follows common-doc-guidelines.md. -->

## 2026-09-10

### Learning Experience Review

Completed the review begun on September 9 at baseline `2fc0c8e`. Inspected the generated site
at desktop and phone widths, the GitHub reading surfaces, content generators, and selected
claims against vendor documentation. The dataset validator passes, but this does not establish
factual correctness. Recorded 14 findings covering accuracy, beginner orientation, usability,
architecture, flashcards, sources, and reproducible publishing.

The [review](reviews/2026-09-09-learning-experience-review.md) contains evidence, acceptance
criteria, a GitHub-first learning proposal, and a participant-validation protocol. Created 12
implementation beads, extended three existing beads, and recorded dependencies. Added a
[three-provider network-scope diagram proposal](assets/network-scope-review.svg), visually
checked in the browser. Review task: `cloud-0apf`. Product fixes and learner testing remain open.
