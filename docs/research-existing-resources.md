# What Already Exists, and Where It Falls Short

Surveyed 9 September 2026. Star and activity figures come from the GitHub API on that date.
The point of this document is not to rank other people's work but to find the gap worth
building into, and to name the things predecessors got right that would be foolish to discard.

## The Field

| Project | Stars | Forks | Last push | Open issues | Shape |
| --- | --- | --- | --- | --- | --- |
| [ilyas-it83/CloudComparer](https://github.com/ilyas-it83/CloudComparer) | 1,505 | 1,022 | 2024-08-01 | 39 | Jekyll site over one 177 KB YAML file, 7 clouds |
| [milanm/Cloud-Product-Mapping](https://github.com/milanm/Cloud-Product-Mapping) | 928 | 172 | 2025-08-29 | 4 | Infographic PDF and PNG plus a 36 KB README, 4 clouds |
| [in28minutes/learning-paths-cloud-and-devops](https://github.com/in28minutes/learning-paths-cloud-and-devops) | 137 | 74 | 2023-11-21 | 0 | Markdown learning paths |
| [navveenb/cloud-comparison-tool](https://github.com/navveenb/cloud-comparison-tool) | 9 | 2 | 2024-10-23 | 0 | Comparison tool, 100+ services |
| [roommen/cloud-service-map](https://github.com/roommen/cloud-service-map) | 1 | 1 | 2019-12-26 | 1 | Chrome extension, abandoned |

Alongside the community projects sit the two vendor comparisons, which are the strongest
competition because they are accurate and staffed:

- [Google Cloud's AWS and Azure comparison](https://docs.cloud.google.com/docs/get-started/aws-azure-gcp-service-comparison),
  a filterable table of several hundred services.
- [Microsoft's Google Cloud to Azure comparison](https://learn.microsoft.com/en-us/azure/architecture/gcp-professional/services).

## Top Three Strengths, Worth Keeping and Enhancing

### 1. Data Separated From Presentation

CloudComparer keeps every mapping in `_data/cloudservices.yml` and renders it with Jekyll. A
contributor edits YAML and never touches layout. The schema is simple:

```yaml
- category: Compute
  subcategory: Virtual Server
  service:
    - aws:
        - name: Amazon EC2
          ref: https://aws.amazon.com/ec2/
          icon: Arch_Amazon-EC2_64.png
```

That decision is almost certainly why the project has **1,022 forks against 1,505 stars**, a
fork-to-star ratio near 0.7 where a typical documentation repository sits far lower. People fork
it because it is genuinely editable.

**Enhance it by:** keeping YAML as the source of truth, adding a published JSON Schema so a bad
contribution fails in continuous integration rather than in review, and emitting JSON so other
people can build on the dataset instead of scraping it.

### 2. Every Entry Links to the Vendor's Own Page

Cloud Product Mapping links each of several hundred service names straight to its product page.
That single discipline turns a list into something you can act on, and it makes errors
checkable by a reader rather than a matter of trust.

**Enhance it by:** adding automated link checking so rot is caught by the build, and citing the
specific documentation page that supports a behavioural claim, not just the marketing page.

### 3. One Shareable Visual

Cloud Product Mapping's real product is a poster. It is a PDF and a PNG people put on a wall and
post in team chats, and much of its 928 stars follow from the image rather than the text. A
single glanceable artifact travels in a way a website does not.

**Enhance it by:** generating the poster from the data rather than drawing it by hand, so the
image can never drift from the table, and producing SVG so it stays sharp and stays diffable.

## Top Three Weaknesses, Worth Fixing

### 1. They Map Names, Not Behaviour

This is the central failure, and it is shared by every project surveyed including both vendor
pages. Google's own comparison presents service name equivalences without discussing where those
equivalences break down. A reader migrating a workload finds a mapping and no indication of
whether the mapped service actually behaves the same way.

Cloud Product Mapping is a step further back. Its README is not a mapping at all. It lists AWS
services under a category, then Azure services under the same category, then Google services,
as three parallel lists. There is no row-level claim that any particular service corresponds to
any other. A reader who wants the Azure equivalent of a specific AWS service cannot get it from
the table; they have to already know the answer.

None of them will tell you that an AWS security group cannot express a deny rule while an Azure
network security group can, or that an Azure availability set is not an availability zone.
Those are the facts that decide exam questions and outage post-mortems, and they are exactly
what a name-to-name table cannot hold.

**The fix:** every row carries a divergence grade, and a ⚠️ grade requires a populated
"breaks when" field before the build will pass. The note is not optional metadata; it is the
product.

### 2. They Rot Silently

CloudComparer was last pushed in August 2024 and carries 39 open issues. Cloud Product Mapping
was last pushed in August 2025 and still lists Azure Cognitive Search and Form Recognizer, both
since renamed, and links through `docs.microsoft.com`, a domain that now redirects.

The deeper problem is not that they are behind. Everything in this subject goes behind. The
problem is that **nothing on the page tells the reader it is behind.** A stale row looks
exactly like a fresh one, so a candidate revises a service name that no longer exists and has no
signal that anything is wrong. Given how aggressively all three vendors rename, this quietly
undoes the value of the whole resource.

**The fix:** a `verified` date on every row, rendered in the interface, with rows visibly
degrading as they age. A rename ledger recording what a thing used to be called, because the
old name is what stale courses taught and what readers will search for. Link checking in
continuous integration.

### 3. There Is No Terminology Layer

Not one project in the survey handles the words. The hardest thing about the second cloud is
not that Compute Engine is called EC2. It is that "role" means an assumable identity in one
cloud and a permission set in the other two, that "resource group" is compulsory in Azure and a
tag view in AWS, and that ASG expands to two unrelated things.

No comparison table can express this, because these are not services and therefore have no row.
They fall outside the data model every existing project chose.

**The fix:** treat terminology as a first-class content type with its own schema and its own
view, not as footnotes on a service table.

### Also Worth Naming: The Vendor Pages Are Not Neutral

Google's comparison exists to bring people to Google Cloud; Microsoft's exists to bring people
to Azure. Both are accurate, and neither will ever tell you that their own service is the weaker
choice for a given constraint. Neither maps AWS to Azure at all, because that route does not
serve either publisher. A neutral project can say things no vendor page will.

## The Gap in One Sentence

Everything that exists answers "what is this called over there". Nothing answers "what will
break when I assume it works the same way", and nothing at all handles the vocabulary.

<!-- This document follows common-doc-guidelines.md. -->
