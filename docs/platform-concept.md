# Platform Concept

Turns the findings in [research-existing-resources.md](research-existing-resources.md) into
something buildable. Read that document first; every decision here traces to a gap named there.

## Working Name

**Cloud Rosetta.** It says what the thing does in two words. A GitHub search on 9 September 2026
found only dormant repositories using the name, the largest at three stars, so it is effectively
unclaimed. Change it freely; nothing in the build depends on it.

## The One-Line Pitch

> Every other cross-cloud comparison tells you what a service is called somewhere else.
> This one tells you what breaks when you assume it works the same way.

That sentence goes at the top of the README, because the README is where stars are won and lost.

## What It Is

Three things sharing one dataset:

1. **A graded mapping.** Service equivalences where every row states how far the equivalence
   can be trusted, and any row that is not a clean match must say what breaks.
2. **A terminology decoder.** The words that collide, treated as first-class content rather than
   footnotes, because they have no row in anybody else's schema.
3. **A study layer.** Filters by exam, and drills generated from the same rows, so the reference
   and the revision aid can never disagree.

## The Data Model Is the Product

Everything else is a rendering. A mapping row:

```yaml
- id: net.firewall.instance
  domain: networking
  concept: Instance-level traffic filtering
  divergence: partial          # exact | partial | none
  aws:
    name: Security group
    url: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html
  azure:
    name: Network security group
    url: https://learn.microsoft.com/en-us/azure/virtual-network/network-security-groups-overview
  gcp:
    name: VPC firewall rule
    url: https://docs.cloud.google.com/firewall/docs/firewalls
  breaks_when: >
    A security group cannot express a deny rule; it only allows. NSGs and Google
    firewall rules both support deny and evaluate by priority. Google rules attach
    to the network and select targets by tag or service account, not to the instance.
  exam_tags: [SAA-C03, AZ-104, ACE]
  verified: 2026-09-09
```

Three fields carry the whole differentiation:

- **`divergence`** makes the honesty machine-readable, so a reader can filter to *only the rows
  that lie*. That view does not exist anywhere else and is the single most useful screen in the
  project.
- **`breaks_when`** is **required whenever `divergence` is not `exact`**. Continuous integration
  rejects the row otherwise. This is what stops the project decaying into another name table,
  and it is a rule about contributions, not a nice intention.
- **`verified`** is rendered in the interface, and rows fade as they age. Staleness becomes
  visible instead of silent, which was weakness two.

A terminology entry is a separate type, because a false friend is not a service:

```yaml
- term: Role
  severity: high
  aws:
    meaning: An assumable identity with its own temporary credentials from STS.
    category: identity
  azure:
    meaning: A named set of permissions granted to a separate principal at a scope.
    category: permission set
  gcp:
    meaning: A named set of permissions bound to a member at a resource node.
    category: permission set
  why_it_hurts: >
    An AWS role is a thing you become. An Azure or Google role is a list of verbs
    pinned to somebody else. The nearest AWS equivalent of the other two is a
    managed policy.
```

## How It Addresses Each Weakness

| Weakness found | Fix in this platform |
| --- | --- |
| Maps names, not behaviour | `divergence` grade on every row; `breaks_when` required and enforced in CI; a "show only the mismatches" filter |
| Rots silently | `verified` date per row, rendered and visibly ageing; link checking in CI; a rename ledger for names stale courses still teach |
| No terminology layer | Terms are a separate content type with their own schema and view |
| Vendor pages are not neutral | Third-party, no vendor allegiance, and AWS to Azure is mapped as readily as anything to Google |

And each strength is carried forward rather than reinvented: YAML source of truth as
CloudComparer proved works, links to vendor pages on every entry as Cloud Product Mapping does,
and one shareable poster as Cloud Product Mapping proved travels, except generated from the data
so it cannot drift.

## What Makes It Visually Appealing and Usable

- **Divergence is the visual spine.** Colour and an icon on every row: ✅ exact, ⚠️ partial,
  ❌ none. A reader scanning the page sees where the danger is before reading a word.
- **Cloud colour is fixed everywhere.** One hue each for AWS, Azure, and Google Cloud, used
  identically in every table, diagram, and card, so the eye learns it once.
- **Never colour alone.** Icons carry the grade too, so it survives greyscale and colour vision
  deficiency.
- **Instant filtering.** Search, plus filters for domain, divergence, and exam. No page reloads,
  no accounts, no build step to read it.
- **Scope diagrams and false-friend cards** as described in
  [design-decisions.md](design-decisions.md).
- **Typography** as decided there: Roboto for headings, Inter for body and tables, Roboto Mono
  for identifiers.

## Repository Shape for an Open-Source Project

```
README.md              One screen that earns the star: pitch, poster, sample of the good part
LICENSE                MIT for code
data/
  schema/              JSON Schema for both content types
  mappings/*.yml       One file per domain, so pull requests do not collide
  terms/*.yml          The decoder
docs/                  Long-form chapters, the reading path
scripts/
  validate.py          Schema check, breaks_when enforcement, staleness report
  build.py             Emits the site and the JSON others can consume
site/                  Generated, published
.github/
  workflows/           Validation and link checking on every pull request
  ISSUE_TEMPLATE/      "This mapping is wrong" and "This service was renamed"
CONTRIBUTING.md        How to add a row, with a copyable example
```

One file per domain matters more than it looks. CloudComparer keeps everything in a single
177 KB YAML file, which means every concurrent contribution conflicts. Splitting by domain is
the difference between a project that accepts pull requests and one that accumulates 39 open
issues.

## Why This Earns Stars

People star from the README, usually without clicking through. So the README must, in one
screen, show the poster, state the one-line pitch, and show a real ⚠️ row with its
`breaks_when` note visible. That row is the proof, and it is something no competitor's README
can show, because none of them holds that information.

The rest is table stakes that the incumbents mostly skip: a licence, a contributing guide with
a copyable example, issue templates aimed at the two things readers actually notice, and a
green build badge that says the data was checked today.

## Getting Started, Honestly Scoped

The dataset does not need to be complete to be useful, and attempting completeness first is how
these projects die. Order of work:

1. The schema, the validator, and the domains where divergence is worst: identity, networking,
   and the resource hierarchy.
2. The decoder, seeded with the terms already documented in
   [09-confusing-terms.md](09-confusing-terms.md).
3. The site and the generated poster.
4. Storage, compute, and databases.
5. Everything else, contributor-driven.

A hundred rows that each say something true and non-obvious beat six hundred that say Compute
Engine is EC2.

<!-- This document follows common-doc-guidelines.md. -->
