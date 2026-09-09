# Cloud Rosetta Learning Experience Review

**Review started 9 September 2026; completed 10 September, at baseline `2fc0c8e`.**
Review task: `cloud-0apf`.
Scope: the repository, generated HTML, GitHub reading surfaces, dataset, learning design,
and representative claims checked against primary documentation. This is a review and proposed
roadmap; the findings below have not been implemented.

## Assessment

Cloud Rosetta has a useful differentiator: it explains where service-name translations fail.
It is currently a compact reference for people who already know some cloud, with an exam bias.
It does not yet provide a coherent education for someone starting from zero. The strongest
next investment is a learning structure and a correctness pass, followed by interface polish.

Keep the shared YAML dataset, stable concept identifiers, explicit divergence notes, provider
links, terminology decoder, and generated reading surfaces. Keep the restrained visual identity
and consistent provider colors. The core should grow into a **GitHub-first field guide**, with
an optional website for searching, comparing, and practicing.

| Goal | Current assessment | Evidence |
| --- | --- | --- |
| Learn from zero | Not yet met | The landing page opens with mappings, IaaS, and exam codes; no link to the introductory chapter |
| Discover something as an experienced reader | Promising, not proven | Useful identity and archive-storage distinctions exist, but several advanced claims are inaccurate |
| Find an answer easily | Partly met | Search and domain filtering work; no stable row links, clear-all action, or chapter navigation |
| Professional presentation | Partly met | Consistent typography and columns; oversized preamble, tiny labels, corrupted symbols, constrained diagrams |
| Trust the explanation | Needs correction before expansion | “Verified” dates coexist with demonstrably incorrect IAM, database, and exam explanations |
| Learn without a website | Partly met | Markdown chapters exist; important mappings and notes are not fully exposed through the GitHub reading path |

These are reviewer judgments, not scores from a user study. No claim that every expert will
learn something can be guaranteed; test useful novelty with representative readers instead.

## What Has Been Built

- 38 mappings in six domains: compute 7, databases 6, hierarchy 6, identity 6, networking 8,
  storage 5. Six are graded exact, 20 partial, and 12 none.
- 16 terminology entries; a validator covering schemas, dates, uniqueness, and required
  divergence explanations; a generated site, decoder chapter, README section, hierarchy
  diagram, SVG poster, TSV flashcards, and JSON export.
- Prose chapters for landscape, mental models, identity, networking, terminology, and exams.
  Compute/storage/database learning chapters, a complete beginner sequence, and exercises with
  worked solutions remain missing. Existing breadth beads must not be mistaken for completed
  learning coverage just because their first mapping rows exist.
- Research and design records, contribution instructions, and automated data/link checks.

## Evidence and Limitations

The existing virtual environment's validator passed: **38 mappings, 16 terms, 150 links,
zero errors or warnings**. This validates structure, not factual truth or link reachability.
A build in an isolated copy reproduced all seven generated outputs without changes on the same
date. Advancing the build date one day changed the site, poster, and JSON with identical input.

Browser checks used the generated page served over ordinary local HTTP, the default desktop
viewport, and a 390 × 844 CSS-pixel viewport. Observed: Windows-1252 decoding, quirks mode,
no document language, functional search, inert decoder filters, a 384-pixel sticky mobile
control area, and a hierarchy canvas 904 pixels wide inside a 324-pixel container. The viewport
override was reset. This was responsive-width testing, not physical-device testing.

The desktop screenshot showed a cohesive dark palette but most of the initial screen was
branding, legends, and controls. Generated severity icons visibly appeared as corrupted text.
Search for `role` returned four mappings and three terms in their respective views. Changing
views and filters left the URL unchanged. ArrowRight on the first tab did not implement tab
navigation; the source has no keyboard handler or associated tab panels.

Not performed: a full factual audit of all 54 entries, physical-device or screen-reader tests,
light-theme/contrast certification, public deployment validation, all-link verification, or
sessions with real beginner/expert participants. The README's external artifact link was not
proven broken; its independence from repository publishing is the concern.

## Findings and Acceptance Criteria

Priority: **P1** materially blocks learning, accuracy, or normal use; **P2** improves discovery,
maintenance, or depth. These are product priorities, not a claim of a production incident.

### F01 · P1 · Teach Permission Evaluation Without False Universal Rules

**Evidence:** `data/mappings/identity.yml` (`iam.evaluation`, `iam.two-role-systems`) and
`docs/02-identity.md`. AWS is presented as a six-stage pipeline every grant must survive.
Google is described as having no separation between directory and resource administration.

AWS evaluation combines unions and intersections and depends on request context and principal.
A universal sequential rule teaches the wrong outcome for resource policies and boundaries.
Google documents separate Workspace/Cloud Identity super administrator and organization IAM
administrator responsibilities. Organization Administrator is not an AWS-root equivalent.
Sources: [AWS evaluation logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html),
[Google organization administration](https://docs.cloud.google.com/resource-manager/docs/creating-managing-organization).

**Fix/acceptance:** rewrite both mappings and prose together, distinguish identity administration
from resource authorization across all three providers, and add two worked permission decisions
with explicit account/principal assumptions. Regenerate all outputs. A technical reviewer must
be able to reproduce the decisions from the cited documentation.

### F02 · P1 · Scope the Multi-AZ Lesson to the Actual Deployment Type

**Evidence:** `data/mappings/databases.yml:26` and `docs/10-exam-map.md` say Multi-AZ standbys
are unreadable and contrast them universally with read replicas.

AWS distinguishes Multi-AZ **DB instances**, whose standby does not serve reads, from Multi-AZ
**DB clusters**, whose standby instances can serve reads and provide failover. The current
simplification obscures the very kind of useful expert distinction this guide should teach.
Source: [RDS deployment types](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.html).

**Fix/acceptance:** separate instance, cluster, and read-replica cases; label engine/product
assumptions; explain availability versus read scaling using a failure diagram and a worked
scenario. Check Azure and Google behavior independently rather than copying the AWS mnemonic.

### F03 · P1 · Correct Certification Facts and Track Exam Lifecycle Centrally

**Evidence:** `docs/10-exam-map.md` gives 700 as the AWS associate passing score and reverses
Google associate/professional validity periods. The site offers AZ-204 as an ordinary filter
while that chapter calls it retired. Exam metadata is just free-text tags.

AWS specifies 720 for associate exams; Google specifies three years for foundational/associate
and two for professional credentials. Sources: [AWS scoring policy](https://aws.amazon.com/certification/policies/after-testing/),
[Google certification policy](https://support.google.com/cloud-certification/answer/9750149?hl=en).

**Fix/acceptance:** add a sourced exam registry with full names, level, current/retired status,
verification date, and official links. Generate filters and exam tables from it; put retired
exam tags in an explicit historical view. Recheck every listed exam, including Microsoft's
retirements, against [its registry](https://learn.microsoft.com/en-za/credentials/support/credential-retirement).
Do not infer product retirement from exam retirement.

### F04 · P1 · Replace Unsupported Exclusivity Claims With Current Comparisons

**Evidence:** `cmp.kubernetes` in `data/mappings/compute.yml` says GKE Autopilot has no direct
counterpart; `sto.redundancy` in `data/mappings/storage.yml` says One Zone-IA is S3's only
single-zone option. Both claims are too categorical.

Compare operational responsibilities with [EKS Auto Mode](https://docs.aws.amazon.com/eks/latest/userguide/automode.html)
and [AKS Automatic](https://learn.microsoft.com/en-us/azure/aks/intro-aks-automatic);
these need not be identical to be relevant alternatives. Include S3 Express One Zone in the
[storage comparison](https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-class-intro.html).

**Fix/acceptance:** revise these rows and the `exact/partial/none` rubric. Distinguish absent
capability from different implementation and partial parity. Audit “only,” “always,” “never,”
“no equivalent,” and product lifecycle claims, including the Fabric/Synapse wording. Capture
conditions, region/tier/version constraints, and direct evidence for each strong claim.

### F05 · P1 · Give Beginners a Route Before the Reference

**Evidence:** `scripts/template.html:239` opens with a defensive comparison pitch, 84%, two
classification systems, three tabs, and 16 exam-code filters. Its main content starts with
compute because filenames are sorted alphabetically in `scripts/build.py:58`. It never links
to `docs/00-landscape.md`. That chapter's SaaS responsibility row also oversimplifies the
customer's role to “data only”; identity, access, and configuration still need explanation.
Source: [shared responsibility](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility).

**Fix/acceptance:** give the first screen three routes: **Start from zero**, **Translate from
my cloud**, and **Challenge my knowledge**. The first route teaches compute, storage, networking,
identity, availability, and cost through one small application. Expand terms before abbreviating
them; provide a glossary and a visible next step. A newcomer should explain where code runs,
where data lives, who can access it, and why a bill appears after a five-minute introduction.
Longer lessons, not a five-minute promise, provide mastery.

### F06 · P1 · Emit a Complete HTML Document

**Evidence:** both `scripts/template.html:1` and `site/index.html:1` start with a title and omit
a doctype, UTF-8 declaration, viewport metadata, and `html lang`. Ordinary HTTP browsing
confirmed `document.characterSet = windows-1252` and `document.compatMode = BackCompat`.
The literal generated symbols are corrupted; numeric entities in the legend survive.

**Fix/acceptance:** generate a standalone standards-mode document with UTF-8, English language,
responsive viewport, head/body, and a useful description. Confirm correct symbols over ordinary
HTTP without special host headers. Verify phone rendering on an actual mobile browser as well
as desktop viewport resizing.

### F07 · P1 · Make Mobile Reading and Keyboard Use Practical

**Evidence:** at 390 pixels wide the sticky filter/navigation block measured 384 pixels tall,
nearly half the tested viewport. The 16 exam codes wrap into multiple rows; labels and dates
use 10–11.5 pixel type. The hierarchy requires horizontal panning. Tabs lack panel relationships
and keyboard behavior; the result count has no live-region semantics and there is no skip link.

**Fix/acceptance:** keep a compact search/filter summary sticky; disclose advanced and exam
filters on demand. Use readable text and generous targets, preserve visible focus, provide a
skip link, associate tabs with panels, and announce count updates. Follow the
[W3C tab pattern](https://www.w3.org/WAI/ARIA/apg/patterns/tabs/). Verify 390-pixel reading,
200% zoom, keyboard-only navigation, both themes, and a screen-reader smoke test. Aim for
controls to consume at most about one-fifth of the phone viewport during normal reading.

### F08 · P2 · Make Search, Filters, and Links Predictable

**Evidence:** the decoder leaves “Only what misleads” and “Only what hurts” visible. Clicking
changes their pressed state but leaves 16/16 terms; `apply()` filters decoder content by search
only. Search/filter/view state is absent from the URL, mapping articles lack stable IDs, related
term references are plain text, and there is no clear-all action.

**Fix/acceptance:** hide irrelevant filters or implement term-specific severity filters; show
active filters with a clear-all action. Add stable row/term anchors and URL state with reload
and Back support. Link related concepts. Make search coverage explicit and include provider
notes. A copied link must open the same explanation and filters; an empty result must offer a
one-step recovery.

### F09 · P1 · Finish the GitHub Reading and Distribution Experience

**Evidence:** README's primary guide link targets a Claude artifact; no repository-controlled
publication workflow is present. “Read the chapters” goes to a directory mixing educational and
internal project records. `dist/` is committed, but downloads are not prominently linked.
The generated README often reduces a useful caveat to an empty opening sentence such as
“The classic RDS trap, and it transfers” (`scripts/surfaces.py:78`). Full mapping explanations
are not generated as dedicated Markdown reference chapters.

**Fix/acceptance:** add a curated chapter index, a beginner entry link above the fold, complete
Markdown mappings, and direct diagram/flashcard/download links. Use authored one-line takeaways
rather than first-sentence truncation. Separate reader content from project records in navigation.
If retaining the site, publish through a stable repository-controlled URL and smoke-test it.
A reader must complete the core learning journey entirely on GitHub without opening HTML.

### F10 · P1 · Draw Separate Ownership, Location, and Traffic Models

**Evidence:** `HIERARCHY_SVG` in `scripts/build.py` and `mermaid_hierarchy()` in
`scripts/surfaces.py` imply one containment chain. AWS places an availability zone inside a VPC;
Google places a region inside a project. Administrative ownership, geographic scope, and network
membership are different relationships, not one tree. Google subnets' network membership is
also clearer in Mermaid than in the SVG, so the two diagrams teach different detail.

**Fix/acceptance:** use separate diagrams for resource ownership, network geography, and request
flow. Show AWS subnets belonging to a VPC and located in one AZ; never imply a VPC owns an AZ.
Show a Google global VPC with regional subnets. Sources:
[AWS subnets](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html),
[Google VPC scope](https://docs.cloud.google.com/vpc/docs/vpc),
[Azure network and zone scope](https://learn.microsoft.com/en-us/azure/virtual-network/virtual-networks-overview).
Apply the diagram standard below and make SVG and Markdown explain the same relationships.

### F11 · P1 · Stop Flashcards From Teaching Unqualified Equivalence

**Evidence:** `scripts/surfaces.py:drills_tsv` emits a name-equivalence card even for `none`
rows. The answer lists service names without the divergence warning; the caveat is a separate
card. Studying the first card alone teaches the assumption the project warns against.

**Fix/acceptance:** put the grade, critical distinction, and source on every relevant answer.
Use scenario questions for non-equivalents; keep factual recall for names. Add worked answers,
wrong-answer reasoning, prerequisite links, and a no-account practice path. Publish the TSV
with import instructions. Extend existing bead `cloud-50j2` rather than duplicating it.

### F12 · P1 · Make Verification Mean More Than a Date

**Evidence:** terminology sources are optional in `data/schema/term.schema.json` and the
Markdown decoder renderer drops sense URLs. Chapter facts are outside the dataset freshness
check. `verified` does not record which claim a source supports. The site cannot promise that
passing schema validation proves accuracy. The link-check job is advisory (`continue-on-error`).

**Fix/acceptance:** extend `cloud-wsfy` with required primary sources for substantive claims,
reviewer/date/conditions, a source-visible decoder, and a documented review cadence for chapters,
exam facts, and fast-changing product modes. Separate “schema passed,” “links reachable,” and
“claim reviewed.” Include a correction link from each concept. Require review of strong claims
before changing their verification date.

### F13 · P2 · Make Generated-Output Checks Reproducible

**Evidence:** `scripts/build.py` and `scripts/surfaces.py` insert today's date.
`.github/workflows/validate.yml` rebuilds and requires `site/` to be unchanged, including in a
weekly scheduled run. In an isolated copy, changing the date to September 10 changed the HTML
with unchanged data. The workflow also ignores drift in other committed generated outputs.

**Fix/acceptance:** separate content verification dates from build metadata; use deterministic
inputs for committed artifacts or exclude intentionally volatile metadata from comparisons.
Check all generated surfaces. The same source must pass drift checks on different days, while
an intentionally outdated output must fail. Freshness checks should still use real elapsed time.

### F14 · P2 · Make the Editorial Promise About Learning

**Evidence:** the headline asserts every other comparison lacks something, “84%” measures this
selected 38-row dataset, and repeated “costs marks” language narrows the audience. Useful novelty
is present but buried in long paragraphs. “No honest equivalent” can sound like no available
solution even when the row lists three services for a similar task.

**Fix/acceptance:** lead with a concrete learning outcome and show the denominator if keeping
the statistic. Use “same goal, different behavior” where appropriate. Add “what transfers,”
“what changes,” “when to choose it,” and “try this scenario.” Offer pairwise comparisons based
on the cloud the reader already knows. Verify novelty through `cloud-22js`, not an unsupported
promise that every expert will learn something on every page.

## Proposed Information Design

| Reader intent | First screen | Main representation | Check for learning |
| --- | --- | --- | --- |
| I know nothing about cloud | Start from zero: follow a photo-sharing app | Short narrative, labeled architecture, glossary | Explain four basic decisions in your own words |
| I know AWS, Azure, or Google Cloud | Choose known and target provider | Two-provider comparison, optional third column | Spot the assumption that would break a migration |
| I already work across clouds | Pick a challenge by domain | Constraint-driven scenario with answer disclosure | Predict behavior, explain the tradeoff, verify the source |
| I am studying for an exam | Choose a current exam by full name | Objective checklist and scenario exercises | Apply the concept without relying on keyword tricks |

Use one learning sequence: **what cloud is → first request → storing data → controlling access
→ surviving failure → understanding cost → comparing providers → operating real systems**.
Every chapter should have a goal, prerequisites, a concrete example, a useful diagram, a short
comparison, one deeper insight, a check question, sources, and next steps.

Recommended creative treatments, in order:

1. **One application, three implementations.** Teach a photo upload once, then show aligned
   AWS/Azure/Google implementations. Highlight only the decisions that change.
2. **Before and after a failure.** Draw the healthy system beside the failed-zone case; ask
   whether reads/writes still work before revealing the answer. GitHub can use two images and
   a details disclosure; an interactive version is optional.
3. **Change one constraint.** “Now the data must stay in one region,” or “Now traffic is idle
   most of the day.” Show the resulting architecture and explain the changed choice.
4. **False-friend cards.** Lead with the term, then its meaning and one wrong assumption.
   Link the card to a worked architecture example rather than stopping at definitions.
5. **Expert field notes.** Curate a few surprising, sourced behaviors per chapter, including
   counterexamples and conditions. This creates depth without overwhelming the beginner route.

Keep HTML optional. Markdown, SVGs, tables, disclosure blocks, and downloadable exercises can
carry the complete learning experience. A website adds search, progress, and richer interaction;
it must not become a second independently authored guide.

## Professional Architecture Standard

Use editable vector diagrams, with an SVG suitable for GitHub and a portable source. Mermaid
is appropriate for small structural or sequence diagrams; complex architectures need deliberate
layout. Raster illustrations may support an analogy, but technical labels and connections should
remain editable and reviewable.

Every architecture should:

- Answer one explicit question and label its assumptions and abstraction level.
- Use aligned columns, a consistent grid, readable labels, and a restrained palette.
- Distinguish administrative boundaries, region/zone placement, and public/private networks.
- Label arrows by meaning: request, replication, policy assignment, or membership. Use line style
  and text as well as color. Do not imply data traffic through an identity or monitoring service.
- Use provider names or official icons for provider-specific drawings; keep a common visual
  grammar so differences are comparable. Icons supplement labels.
- Include a legend, descriptive alternative text, source links, verification date, and a
  nearby explanation of the important tradeoff.
- Offer a readable phone treatment, such as one provider per panel, and an accessible text
  explanation. Verify exports at actual reading size and in grayscale.

First diagram set: ownership and billing; network geography; application request flow;
identity authorization; database failover versus read scaling; private service access.
These diagrams belong beside the explanations, not in a disconnected gallery.

The companion [network scope study](../assets/network-scope-review.svg) is a vector proposal
showing AWS, Azure, and Google scope separately from organizational ownership. It demonstrates the
recommended treatment; it is not a complete deployment design or a substitute for the full
architecture set.

## Delivery Order and Learning Validation

**First: establish trust and access.** F01–F04, F06, F09, F11–F12, then F13. Correct source
content before regenerating and distributing lessons or flashcards.

**Next: deliver one complete learning slice.** F05, F07–F08, F10, F14. Build the first-request
lesson with one architecture, an aligned comparison, and a challenge before expanding catalog
breadth. Continue compute/storage/databases work through the existing beads. Add operations,
cost, governance, and observability through the existing domain backlog.

**Then: test the learning outcome.** Extend `cloud-22js` with a formative study of at least
three newcomers and three practitioners. For newcomers, record time to first useful answer,
undefined vocabulary, four explanation questions, and one transfer scenario. For practitioners,
record a genuinely new insight, its source, and the ability to solve a changed scenario.
Target at least three correct basic explanations per newcomer within five minutes, and one
verified new insight per practitioner within ten minutes. These are pilot targets, not statistical
proof. Record failures, revise, and retest. A reviewer walkthrough cannot close this bead.

## Tracking

| Finding | Bead | Work |
| --- | --- | --- |
| F01 | `cloud-6oke` | Correct IAM evaluation and directory administration mental models |
| F02 | `cloud-rmtx` | Distinguish RDS Multi-AZ instances, clusters, and read replicas |
| F03 | `cloud-z3v7` | Correct exam facts and centralize certification lifecycle metadata |
| F04 | `cloud-aw7t` | Update Kubernetes and storage comparisons and audit exclusivity claims |
| F05 | `cloud-nwl1` | Create a first-principles learning route around one application |
| F06 | `cloud-e6mb` | Generate a complete UTF-8 standards-mode HTML document |
| F07 | `cloud-zp0k` | Make mobile reading and keyboard navigation accessible |
| F08 | `cloud-upqf` | Fix decoder filters and add stable links and recoverable search |
| F09 | `cloud-1pvk` | Complete GitHub reading paths and stable guide distribution |
| F10 | `cloud-wkcf` | Replace mixed hierarchy drawings with precise architecture diagrams |
| F13 | `cloud-jouq` | Make all generated-output drift checks deterministic |
| F14 | `cloud-d2yv` | Add reader-oriented comparisons and sourced expert challenges |
| F11 | `cloud-50j2` | Existing flashcard task extended with correctness and scenario requirements |
| F12 | `cloud-wsfy` | Existing sourcing task extended with claim-level review and source-visible outputs |
| Audience validation | `cloud-22js` | Existing acceptance test extended with a participant study protocol |

The accompanying tbd beads link to this report and carry finding-specific acceptance criteria.
Existing beads `cloud-22js`, `cloud-wsfy`, and `cloud-50j2` are extended rather than duplicated.
The review bead may close once this evidence and backlog are recorded; the implementation and
participant-validation beads remain open.

<!-- This document follows common-doc-guidelines.md. -->
