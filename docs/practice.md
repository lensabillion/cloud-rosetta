# Practice

Reading a comparison table produces recognition, not recall. These drills exist to tell the
difference. Nothing here predicts an exam score; it tells you which of your beliefs are wrong.

## The Flashcard Deck

The build generates a deck from the same dataset as everything else, so a card can never
disagree with a chapter.

```bash
python scripts/build.py    # writes dist/drills.tsv
```

`dist/drills.tsv` is tab separated as front, back, tags. It imports directly into
[Anki](https://apps.ankiweb.net/) through File, then Import, with the field separator set to
tab. Three kinds of card are generated:

| Card type | Front | Tagged |
| --- | --- | --- |
| Translation | A service name in one cloud | `<domain> mapping <divergence>` |
| Gotcha | A concept, asking where the mapping breaks | `<domain> gotcha <bite>` |
| Decoder | A colliding term, asking what it means in each cloud | `decoder <severity>` |

Filter the deck by tag to study one way. `tag:gotcha` alone is the highest-value session,
because the translations are the part you can look up and the gotchas are the part you cannot.

## Drill the Decision, Not the Keyword

Most wrong answers come from matching a keyword to a service instead of reading the constraint.
Practise the constraint. For each scenario, name the deciding word before naming a service.

| The constraint says | What is being tested |
| --- | --- |
| Least operational overhead | Managed or serverless over self-managed, even at higher unit cost |
| Must survive a data centre failure | Zones, not an Azure availability set, and not a read replica |
| Must be reachable from on-premises with a private address | An Azure private endpoint, not a service endpoint |
| Reporting queries must not slow the application | A read replica, not a failover standby |
| Block one specific address while broad allow rules stay | A deny-capable control, so not an AWS security group alone |
| Cheapest, and retrieval can wait hours | Offline archive tiers, where retrieval time is the trade |
| Cheapest, but must read instantly | Google Archive is online; on AWS this is Glacier Instant Retrieval |

## Self-Check

Cover the right column. If you cannot answer in about five seconds, the underlying chapter has
not landed yet.

| Question | Answer | Chapter |
| --- | --- | --- |
| Which cloud's "role" is an identity with its own credentials? | AWS | [Identity](02-identity.md) |
| An SCP allows an action and no IAM policy grants it. Allowed? | No. An SCP limits, it never grants | [Identity](02-identity.md) |
| Which cloud's virtual network is global? | Google Cloud | [Mental Models](01-mental-models.md) |
| Which cloud puts a subnet inside a single zone? | AWS | [Mental Models](01-mental-models.md) |
| Deleting which container destroys everything inside it? | An Azure resource group | [Mental Models](01-mental-models.md) |
| ASG: expand it, twice | AWS Auto Scaling group; Azure application security group | [Decoder](09-confusing-terms.md) |
| Is an RDS Multi-AZ standby readable? | It depends on the deployment type, so the question is underspecified | [Databases](05-databases.md) |
| AWS associate passing score | 720, and it is a scaled score, not a percentage | [Exam Map](10-exam-map.md) |
| How long is a Google professional certification valid? | Two years. Foundational and associate last three | [Exam Map](10-exam-map.md) |

## Where This Stops

These drills cover the cross-cloud material in this guide. They are not a syllabus for any
certification, and no question here is taken from an exam. Build your checklist from the
official objectives linked in [the exam map](10-exam-map.md).

**Next:** [chapter index](README.md) · [the decoder](09-confusing-terms.md)

<!-- This document follows common-doc-guidelines.md. -->
