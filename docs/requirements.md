# Requirements

Every instruction given for this project, broken into numbered items that can be checked off.
Kept current as instructions arrive. Bead IDs in the last column are the tracked work in `tbd`.

Status key: **done**, **in progress**, **open**.

## R1. The Core Deliverable

| # | Requirement | Status | Bead |
| --- | --- | --- | --- |
| R1.1 | A guide for people taking cloud certification exams on AWS, Azure and Google Cloud | in progress | cloud-vitw |
| R1.2 | Not only for certification. Also for people who want to know what is what | in progress | cloud-vitw |
| R1.3 | Cover the similarities between the three clouds | done | cloud-re1t |
| R1.4 | Cover the differences | done | cloud-re1t |
| R1.5 | Cover the confusing terms | done | cloud-csh9 |
| R1.6 | Deliver as Markdown in the repo **and** a published web guide | done | cloud-c4qp |
| R1.7 | Tune depth to foundational and associate certifications | done | cloud-ec1l |
| R1.8 | Emphasise all four of: service mapping tables, confusing terms decoder, mental model differences, exam traps and drills | in progress | cloud-50j2 |

## R2. Project Setup

| # | Requirement | Status | Bead |
| --- | --- | --- | --- |
| R2.1 | Run `tbd` and follow its setup instructions | done | — |
| R2.2 | Use the issue prefix `cloud` | done | — |
| R2.3 | Track all work as beads | in progress | — |

## R3. Research

| # | Requirement | Status | Bead |
| --- | --- | --- | --- |
| R3.1 | Research what has been done so far and document everything | done | cloud-e93a |
| R3.2 | Find what people who sat these exams found painful, across all three providers | done | cloud-449p |
| R3.3 | For existing resources, find the top 3 **strengths** | done | cloud-e93a |
| R3.4 | For existing resources, find the top 3 **weaknesses** | done | cloud-e93a |
| R3.5 | Research the two most-liked typefaces, on evidence, and use those two | done | cloud-3kgt |
| R3.6 | Set the background: what AWS, Azure and Google Cloud are, the current state of the market, current adoption coverage, and who uses each | in progress | cloud-xzhc |

Outputs: [research-pain-points.md](research-pain-points.md),
[research-existing-resources.md](research-existing-resources.md),
[design-decisions.md](design-decisions.md), [00-landscape.md](00-landscape.md).

## R4. The Platform

| # | Requirement | Status | Bead |
| --- | --- | --- | --- |
| R4.1 | Build a platform that **addresses** the weaknesses found in R3.4 | done | cloud-se24 |
| R4.2 | Build a platform that **keeps and enhances** the strengths found in R3.3 | done | cloud-se24 |
| R4.3 | Visually appealing | in progress | cloud-kml6 |
| R4.4 | Very usable | in progress | cloud-kml6 |
| R4.5 | Be creative about representation: illustration, graphs, or another form | in progress | cloud-zwpn |
| R4.6 | Structured to earn GitHub stars | in progress | cloud-57r1 |
| R4.7 | Open source | done | cloud-57r1 |

### R4.8 The Two-Audience Test

> A platform one comes to learn about cloud and gets what he wants in 5 minutes, but an expert
> on the subject needs to find what he doesn't know in it.

This governs every page and is the hardest requirement in the list, because the two readers pull
in opposite directions. It is treated as an acceptance test rather than a feature:

| Audience | Passes when | Fails when |
| --- | --- | --- |
| Newcomer, 5 minutes | Lands, orients, and leaves with a correct answer to a real question without reading linearly | The page demands prior vocabulary, or buries the answer below a wall of preamble |
| Expert | Finds at least one thing per page they did not know, and can verify it in one click | The page restates what any comparison table already says |

The mechanism that serves both at once is the divergence grade. A newcomer reads the row and
gets the equivalent. An expert filters to the ⚠️ and ❌ rows and reads only the notes, which is
where the non-obvious material lives. One dataset, two reading paths. Tracked as cloud-22js.

## R5. Sourcing and Documentation

| # | Requirement | Status | Bead |
| --- | --- | --- | --- |
| R5.1 | Document everything done, continuously rather than at the end | in progress | cloud-njl9 |
| R5.2 | Add work to beads so nothing is forgotten | in progress | cloud-njl9 |
| R5.3 | Link everything mentioned back to its original resource | in progress | cloud-wsfy |
| R5.4 | Break down and document the instructions themselves | done | cloud-a1sm |

R5.3 is a standing rule with three surfaces: prose in `docs/` cites inline, every entry in
`data/` carries a `url`, and the rendered site links every service name and every note's
supporting page.

## R6. Delivery

| # | Requirement | Status | Bead |
| --- | --- | --- | --- |
| R6.1 | Create a pull request | in progress | cloud-8pwg |

## Feedback Received and Acted On

| Date | Feedback | Response |
| --- | --- | --- |
| 2026-09-09 | "You just created the most boring, the most bare minimum HTML, no creativity whatsoever" | Accepted. The first build was a competent utilitarian layout, which under-read a request that had asked for visual appeal and creativity twice. Rebuilt around the Rosetta Stone idea: three vendor scripts held in a fixed column spine down the whole page, with a visible fracture drawn between columns wherever the translation fails. Tracked as cloud-kml6 |

<!-- This document follows common-doc-guidelines.md. -->

## R7. Learning Experience Review, September 2026

| # | Requirement | Status | Bead |
| --- | --- | --- | --- |
| R7.1 | Review existing UI, usability, and information presentation | done | cloud-0apf |
| R7.2 | Record evidence and suggested fixes in tbd | done | cloud-0apf |
| R7.3 | Suggest creative representations and GitHub-native delivery | done | cloud-0apf |
| R7.4 | Define and demonstrate a professional architecture diagram standard | done | cloud-0apf |
| R7.5 | Implement the reviewed architecture improvements throughout the guide | open | cloud-wkcf |
| R7.6 | Validate learning for people starting from zero and useful novelty for practitioners | open | cloud-22js |

Review evidence and the prioritized backlog are in
[the learning experience review](reviews/2026-09-09-learning-experience-review.md).
