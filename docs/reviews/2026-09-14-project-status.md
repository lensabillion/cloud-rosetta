# Project Status: 14 September 2026

The guide is a published first version with a redesigned reading experience. It is not yet
validated against the goal of teaching complete beginners and giving experienced readers
something new.

## GitHub and Local Baseline

Checked GitHub directly on September 14. Pull requests 2 through 5 are merged. The latest
`main` commit is `8cf6c1d`; the local `build/guide-rebuild` checkout at `a2d45ec` has the same
file tree and was clean before this session. The difference is merge history, not missing
local content. New fixes start from `origin/main` on `codex/verify-guide-outputs`.

The [published guide](https://lensabillion.github.io/cloud-rosetta/) has a successful Pages
run from September 10. The September 14 scheduled validation run passed. These checks cover
structure and generation, not a complete factual review or learning outcomes.

The build produces 15 routed pages, 38 mapping rows, 16 terminology entries, 21 registered
exams (18 current and 3 historical), and 160 flashcards. Chapters, a sidebar, previous/next
navigation, a chapter contents block, diagrams, practice material and GitHub Pages delivery
have landed since the original review.

## Fixes in This Branch

| Finding | Change | Evidence |
| --- | --- | --- |
| F13 / `cloud-jouq` | Compare every generated surface in an isolated build, including downloads and generated Markdown. Reject missing and unexpected output files. Run the same check before publishing. | Regression tests inject stale content into all eight outputs, remove the deck, add an obsolete page, and cause a build failure. The checker rejects them without rewriting the working copy. |
| F13 / `cloud-jouq` | Replace wall-clock build dates with the newest recorded source-verification date. Generate chapter inputs before assembling the website. | Builds under September 14 and October 15 clocks produce identical bytes. Source verification dates and elapsed-age validation remain separate. |
| F06 / `cloud-e6mb` | Add doctype, English language, UTF-8, responsive viewport, description, and explicit head/body boundaries. | Local HTTP browser reports UTF-8 and CSS1Compat. Home and first chapter fit a 390px viewport without page-wide overflow; desktop chapter navigation also works. |

The JSON export now exposes `latest_source_verification` instead of `generated`. Consumers
of the old field must update. The new field identifies the newest recorded check, not a
review of the entire dataset. Individual entries retain their verification dates.

## Work Still Required

| Area | Current gap | Tracked by |
| --- | --- | --- |
| Beginner route | Orientation still leads with provider comparisons and certifications. Build the application-based route covering compute, storage, network, identity, availability and cost. Correct oversimplified shared-responsibility wording. | `cloud-nwl1` |
| Navigation and accessibility | Inspect chapter-heading anchors, browser Back, stable row links, saved search/filter state, keyboard focus and menu announcements. A viewport smoke check is not a physical-device or screen-reader test. | `cloud-upqf`, `cloud-zp0k` |
| Reference and sourcing | Complete GitHub-readable service references, claim-level evidence and explicit review status. A passing schema and a vendor URL do not prove every statement. | `cloud-1pvk`, `cloud-wsfy` |
| Teaching depth | Replace unqualified translation cards with bounded decisions and explanations. Add provider-pair comparisons and expert challenges. | `cloud-50j2`, `cloud-d2yv` |
| Architecture | Audit ownership versus geography, identity decisions, database failover and private-service access in both browser and GitHub representations. Existing drawings do not close the entire architecture review. | `cloud-wkcf` |
| Learning outcomes | Conduct the recorded study with three newcomers and three practitioners. No participant results have been collected in this session. | `cloud-22js` |

The original [review and acceptance criteria](2026-09-09-learning-experience-review.md)
remain the work list. The tracker includes older tasks that appear partly implemented;
completion must be reconciled against their acceptance criteria rather than inferred from a
merged pull request.

## Review of This Change

Verdict: the bounded build and HTML changes pass local validation and four regression tests.
The isolated build keeps verification independent of the working copy and uses the existing
Python toolchain without another dependency. Both CI and Pages call the checker. Authored
portions of mixed Markdown documents remain inputs; only generated portions are replaced.

No blocking issue remained in the reviewed diff. The JSON metadata field change is deliberate
and documented in the contributor guide. Broader content, routing and device checks remain
open above. GitHub CI must also pass before these fixes are considered ready for merge.

<!-- This document follows common-doc-guidelines.md. -->
