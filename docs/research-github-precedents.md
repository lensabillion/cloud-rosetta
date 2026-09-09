# What the Successful Guides Do, and What We Are Adopting

Surveyed 9 September 2026 using the GitHub API. Star and staleness figures are from that date.
This document exists to copy what works. Everything in the "Adopted" sections is now in the
schema, the validator, or the site.

## The Reference Case: og-aws

[open-guides/og-aws](https://github.com/open-guides/og-aws), "Amazon Web Services, a practical
guide."

| | |
| --- | --- |
| Stars | 36,453 |
| Forks | 3,882 |
| Open issues | 159 |
| Last push | 2024-08-16 |
| Licence | CC BY 4.0 |
| Shape | One 382 KB `README.md`, plus a 31 KB `AUTHORS.md` |

It is the most-starred cloud guide of its kind by two orders of magnitude over anything aimed at
certifications, and almost everything it does well is worth stealing.

### Adopted: A Severity Legend Defined by Consequence

og-aws opens with a legend, before any content, and each marker is defined by **what it will
cost you**, not by how unusual it is:

> - 🔹 Important or often overlooked tip
> - ❗ "Serious" gotcha (used where risks or time or resource costs are significant: critical
>   security risks, mistakes with significant financial cost, or poor architectural choices that
>   are fundamentally difficult to correct)
> - 🔸 "Regular" gotcha, limitation, or quirk (used where consequences are things not working,
>   breaking, or not scaling gracefully)

This exposed a real gap in our model. Our `divergence` grade says **how far a mapping
transfers**. It says nothing about **how badly the difference bites**. Those are independent:
"Google's Archive class is online" is a total divergence with mild consequences, while "an SCP
never grants anything" is a subtle difference that will lock an organisation out of its own
account.

**Adopted as a second axis, `bite`, using og-aws's own definitions.** A row now carries both,
so a reader can filter to "differences that will actually hurt me" rather than merely
"differences".

### Adopted: Date the Volatile Claims Inline

og-aws writes "(As of Jul 2018)" directly into gotchas that depend on current behaviour. That
instinct is right and it is the thing every stale resource lacks.

**Already in the model** as a required `verified` date per row, rendered on the page, and
enforced by the validator. og-aws validates the decision; we go further by failing the build
when a row ages out rather than leaving a date to be read.

### Adopted: A Maturity Marker

og-aws carries a product maturity table with launch dates and entries such as
"❗Nearly obsolete". This directly serves the biggest complaint from candidates, which is
studying a product that has been superseded.

**Adopted as an optional `maturity` field** on a provider entry, with `legacy` and `superseded`
values, rendered as a visible badge. Distinct from `formerly`, which records renames.

### Adopted: Ask for Help Early and Credit Loudly

The call for contributions sits at line 110 of the README, above the content, and `AUTHORS.md`
runs to 31 KB. Recognition is a large part of why a community guide accumulates contributors.

**Adopted:** a contribution call above the fold in the README, and contributor credit as a
first-class file rather than a link to the GitHub graph.

### Deliberately Not Adopted: One Enormous File

og-aws keeps everything in a single 382 KB README. That is superb for reading, searching and
being found, and terrible for contribution, because every concurrent pull request collides. It
is the same structural problem that left
[CloudComparer](https://github.com/ilyas-it83/CloudComparer) with 39 open issues on one 177 KB
YAML file.

Our split is one YAML file per domain for editing, generated into one canonical reading surface.
That keeps og-aws's reading experience without its merge conflicts.

### The Warning in the Numbers

og-aws was last pushed in August 2024 and carries 159 open issues. **The single most successful
resource in this category is itself two years stale.** Community guides do not fail from lack of
interest; they fail because nothing in them makes ageing visible or actionable. That is the
weakness the freshness machinery in this project exists to fix.

## The Gap: Nobody Serves Certifications on GitHub

A sweep of the certification study-guide niche, sorted by stars:

| Query | Best result | Stars | Last push |
| --- | --- | --- | --- |
| AWS certification study guide | [aandr26/AWS-SAP-C01-Study-Guide](https://github.com/aandr26/AWS-SAP-C01-Study-Guide) | 120 | 2025-05-02 |
| Azure AZ-104 study | [Iamrushabhshahh AZ-104 hub](https://github.com/Iamrushabhshahh/Microsoft-Azure-Administrator-AZ-104-Exam-Dump-Question-With-Solution) | 86 | 2025-05-28 |
| Google Cloud certification study guide | [chuya59 GenAI study guide](https://github.com/chuya59/Study-Guide-for-Google-Cloud-GenAI-Certification) | 4 | 2026-04-10 |
| Multicloud awesome list | [mahomedalid/awesome-multicloud](https://github.com/mahomedalid/awesome-multicloud) | 0 | 2022-02-28 |

Set that against the format's ceiling:

| Repository | Stars |
| --- | --- |
| [sindresorhus/awesome](https://github.com/sindresorhus/awesome) | 504,272 |
| [jwasham/coding-interview-university](https://github.com/jwasham/coding-interview-university) | 360,598 |
| [donnemartin/system-design-primer](https://github.com/donnemartin/system-design-primer) | 368,811 |
| [trimstray/the-book-of-secret-knowledge](https://github.com/trimstray/the-book-of-secret-knowledge) | 242,724 |
| [open-guides/og-aws](https://github.com/open-guides/og-aws) | 36,453 |

The best AWS certification guide on GitHub has **120 stars**. The best Google Cloud one has
**four**. Meanwhile a practical AWS guide has 36,453 and a study plan for software engineering
interviews has 360,598.

The conclusion is not that people do not want this. It is that the people who want it are
buying courses instead, because nothing good exists in the open. **The niche is unserved rather
than unwanted**, which is the best position to build from.

### What the Giants Have in Common

Looking across the five highest-starred entries above, four traits recur and all four are cheap
to adopt:

1. **You can use them in the first minute.** No install, no account, no build. The value is in
   the README or one click away.
2. **They are opinionated.** system-design-primer and og-aws both tell you what to do, not
   merely what exists. Neutral catalogues do not accumulate stars; judgement does.
3. **They have a progression.** coding-interview-university is a plan, not a pile. There is an
   order and a sense of finishing something.
4. **They make contributing obvious.** A visible legend, a clear schema, a stated scope, and
   credit for contributors.

Traits 1, 2 and 4 are in place. **Trait 3 is the outstanding gap**: this project is currently a
reference, not a path. A study plan built from the same dataset is the next thing to add.

## Summary of Changes Made From This Research

| Learning | Source | Change |
| --- | --- | --- |
| Grade severity by consequence, not by novelty | og-aws legend | New `bite` axis: serious, regular, tip |
| Mark superseded products | og-aws maturity table | New optional `maturity` field with a rendered badge |
| Date volatile claims | og-aws "(As of Jul 2018)" | Already present as `verified`, now also enforced |
| Credit contributors loudly | og-aws `AUTHORS.md` | Contributor file and an above-the-fold call to help |
| One file does not scale for contribution | og-aws 159 issues, CloudComparer 39 | Keeping per-domain YAML, generating one reading surface |
| Give readers a path, not only a reference | coding-interview-university | Study plan generated from the dataset, still to build |

<!-- This document follows common-doc-guidelines.md. -->
