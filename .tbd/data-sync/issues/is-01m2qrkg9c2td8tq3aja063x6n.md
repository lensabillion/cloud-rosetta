---
type: is
id: is-01m2qrkg9c2td8tq3aja063x6n
title: Audit repository parity and reconcile unfinished backlog
kind: task
status: closed
priority: 1
version: 3
labels: []
dependencies: []
created_at: 2026-09-17T13:23:55.819Z
updated_at: 2026-09-17T13:25:56.632Z
closed_at: 2026-09-17T13:25:56.632Z
close_reason: Compared main with freshly fetched GitHub, reviewed all 21 unfinished entries against current files, passed local checks, recorded review and prioritized remaining work. Follow-up record reconciliation tracked as cloud-k4o5.
resolution: null
duplicate_of: null
---

## Notes

# Repository and Backlog Review — 17 September 2026

## Repository Parity

After fetching GitHub, local main and origin/main both point to 1bae5a248159e4a60aeaf9819d0080dc87f7d19e: zero commits ahead or behind. There are no open pull requests. Latest validation and GitHub Pages publication succeeded on that commit. PR16's official-icon architecture redesign and PR17's sidebar/table changes are merged; PR20 records Archify's removal.

The only working-copy difference was .tbd/state.yml's last_doc_sync_at timestamp. Preserve it outside the repository before restoring the tracked baseline after tracker synchronization. Old development branches were retained. Patch comparison finds their substantive work already represented in main; the remaining distinct reference-architecture commit changes tracker metadata only.

## Review

The project now has a reproducible, published guide with 38 mappings, 16 terminology entries, 21 exam records, 160 flashcards and 15 diagrams. Formatting, validation, design checks, ten tests and all 38 generated-output comparisons pass locally. These checks establish structural consistency, not complete factual accuracy or teaching effectiveness.

There were 21 unfinished tracker entries before this audit: 14 open and seven in progress, including the umbrella epic. Several are stale implementation records, so this is not 21 untouched features. No participant-study results, physical-device acceptance record or screen-reader completion evidence was found in the tracked review records. This audit reviewed files, tracker criteria and CI; it did not conduct a fresh full vendor-fact audit or live usability study.

## Prioritized Remaining Work

| Priority | Work | Remaining acceptance gap | Tracking |
| --- | --- | --- | --- |
| P0 | Prove learning outcomes | Run the defined pilot with three beginners and three practitioners; record timing, misunderstandings, transfer answers and source-verifiable new insights | cloud-22js |
| P1 | Finish beginner entry routes | The photo application, vocabulary and next steps exist. The home page still has one Start reading action, rather than clear beginner, translation and challenge routes. Validate five-minute comprehension through the pilot | cloud-nwl1 |
| P1 | Complete device/accessibility validation | Physical mobile browser, keyboard-only journey, 200% zoom, both themes and screen-reader smoke test remain unproven. Previous 390px checks do not replace these | cloud-zp0k, cloud-e6mb |
| P1 | Complete GitHub-native references | Publishing, chapter index and downloads exist. Full graded mapping explanations still require the web guide or YAML; generate complete readable Markdown references. Correct misleading chapter labels and self-links | cloud-1pvk |
| P1 | Expand compute and storage teaching | Existing mappings cover common services, but batch is missing and dedicated compute/storage teaching chapters are absent. VM-family selection and storage decisions need fuller treatment | cloud-yzde, cloud-3nrb |
| P1 | Finish claim review and freshness process | Decoder sources are now required and visible. Claim/reviewer/conditions records, chapter review cadence, concept correction links and a complete strong-claim audit are not established | cloud-wsfy, cloud-aw7t |
| P1 | Finish scenario-based drills | Caveats and sources now accompany flashcards; five worked practice scenarios and import guidance exist. Non-equivalent mappings still generate generic comparison prompts rather than systematic bounded decision scenarios | cloud-50j2 |
| P2 | Expand missing domains | Add queues, pub/sub, ETL, orchestration and observability; KMS, threat/posture management and IaC; commitments, free tiers, support and SLA calculations. Some foundations already exist: warehouse, streaming, secrets, guardrails and spot | cloud-fn3p, cloud-e70t, cloud-4bqj |
| P2 | Make expert comparison routes useful | Add provider-pair views and consistent what-transfers/what-changes/when-to-choose prompts. Novelty needs the participant study, not an editorial promise | cloud-d2yv |
| P2 | Reconcile project records | Requirements still report seven tests and delivery history through PR9; the progress log calls delivered work open. The index advertises market coverage removed from Foundations. Design docs contain contradictory Design-page statements | cloud-k4o5 |

## Delivered Work With Stale Completion Records

These should be closed or narrowed after reconciling the old criteria, rather than implemented again:

- cloud-f09b: measured design document exists in docs/design-system.md.
- cloud-e473: multi-page rebuild, reading column and navigation are delivered. Old 16px/four-size wording is superseded by the current approved design system.
- cloud-6oke: directory/resource distinction and two bounded AWS permission decisions are present; generated outputs and CI pass.
- cloud-rmtx: separate RDS deployment modes, failover diagram and worked scenario are present.
- cloud-z3v7: central exam registry and current/historical views are integrated. Its pending-integration note is stale; ongoing lifecycle re-verification belongs in the sourcing process.
- cloud-wkcf: ownership, network scope and traffic diagrams are separated; Markdown and site share SVGs. Any further visual concerns should become specific findings rather than repeating the original defect.

Keep cloud-e6mb's physical-device acceptance gap visible even though the HTML defect is fixed. Keep cloud-22js open until actual participant evidence exists. The umbrella cloud-vitw remains open while these learning and coverage gaps remain.

## Recommended Order

Reconcile stale task records, finish the entry routes and accessibility acceptance pass, then run a small learner pilot before adding more content. Use the pilot to prioritize missing chapters. Complete Markdown reference parity and scenario drills next, then broaden coverage. Continue source verification throughout.
