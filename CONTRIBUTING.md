# Contributing

The most valuable contribution to this project is a correction. Vendors rename services
constantly and a stale row is worse than a missing one, because a reader trusts it.

## Ground Rules

1. **Never edit `site/`.** It is generated. Change the data and rebuild.
2. **Every claim needs a vendor link.** Documentation pages, not marketing pages, for anything
   behavioural.
3. **A row that is not an exact match must say what breaks.** The build enforces this. It is the
   whole point of the project.
4. **Set `verified` to the date you actually checked**, not the date you copied the row from
   somewhere else.

## Adding or Fixing a Mapping

Files live in `data/mappings/`, one per domain, so parallel pull requests do not collide.

```yaml
- id: sto.archive-tier               # stable dotted id, never renumbered or reused
  concept: Cheapest archival storage tier
  divergence: none                   # exact | partial | none
  aws:
    name: S3 Glacier Deep Archive
    url: https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html
  azure:
    name: Archive access tier
    url: https://learn.microsoft.com/en-us/azure/storage/blobs/access-tiers-overview
  gcp:
    name: Archive storage class
    url: https://docs.cloud.google.com/storage/docs/storage-classes
  breaks_when: >
    Retrieval behaviour differs fundamentally. Google's Archive class is online with the
    same millisecond latency as Standard. AWS Glacier and the Azure Archive tier are
    offline and need a restore or rehydration taking minutes to hours.
  exam_tags: [SAA-C03, AZ-104, ACE]
  sources:
    - https://docs.cloud.google.com/storage/docs/storage-classes
  verified: '2026-09-09'
```

### Choosing a Divergence Grade

| Grade | Use when |
| --- | --- |
| `exact` | The mental model transfers. Someone who knows one can use the other name and be right. |
| `partial` | It maps, but a real behavioural difference would change a design decision or an exam answer. |
| `none` | There is no honest equivalent, or the clouds solve the problem in structurally different ways. |

When in doubt, choose `partial` and write the note. A note nobody needed costs a reader ten
seconds. A missing note costs them a mark.

If the mapping is genuinely exact but there is still a shared trap people fall into, use
`shared_trap` rather than `breaks_when`, so `breaks_when` keeps its strict meaning of
"where the mapping lies".

### A Cloud With No Equivalent

Set `name: null` and explain what to do instead:

```yaml
  gcp:
    name: null
    note: No equivalent. Labels and separate projects do this job.
```

## Adding a Terminology Entry

Files live in `data/terms/`. A term needs at least two clouds to collide, and `severity: high`
means the word denotes **different kinds of thing**, not merely different behaviour. The
validator checks both.

## Before You Open a Pull Request

```bash
python -m venv .venv && ./.venv/bin/pip install pyyaml jsonschema
./.venv/bin/python scripts/validate.py
./.venv/bin/python scripts/build.py
```

`validate.py` checks schema conformance, id uniqueness, the `breaks_when` rule, staleness, and
that no link points at retired domains such as `docs.microsoft.com`. It runs on every pull
request. Warnings are fine to ship; errors are not.

## Reporting Something Wrong

Open an issue. The two most useful kinds:

- **This mapping is wrong.** Say which id, what is wrong, and link the vendor page that shows it.
- **This was renamed.** Say the old name and the new one. Old names go in the `formerly` field
  rather than being deleted, because that is what stale courses taught and what readers search
  for.

## Scope

In scope: AWS, Azure, and Google Cloud, at foundational and associate certification depth.

Out of scope for now: other cloud providers, pricing figures that go stale within a quarter, and
practice-exam questions reproduced from anywhere. Contributions of the last kind will be closed.
