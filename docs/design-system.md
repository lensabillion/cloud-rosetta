# Design System

Written before rebuilding, and grounded in measurements of the guides that already work rather
than in taste. Supersedes the visual half of [design-decisions.md](design-decisions.md); the
typography evidence there still stands.

Measurements taken 10 September 2026 at a 1280px viewport, using computed styles from the live
sites.

## The Diagnosis

The current page is a single screen holding 38 mapping rows, three filter groups, a statistics
block and a terminology view, with no navigation and nothing hidden. It is dense, and density is
the whole problem. Measured against the guides people actually learn from:

| | Tech Interview Handbook | javascript.info | Cloud Rosetta, current |
| --- | --- | --- | --- |
| Reading column | 607px | 736px | ~1140px, split into 3 columns |
| Characters per line | 67 | 92 | Far past both, in narrow columns |
| Body size | 16px | 16px | 15px |
| Line height | 1.65 | 1.5 | 1.62 |
| Gap between sections | 54px | 24px | 38px, but 9px between rows |
| Distinct font sizes | About 4 | About 5 | **12** |
| Smallest text | 14px | 13px | **9.5px** |
| Items on one page | 1 topic, ~3,000 words | 1 topic | **38 rows plus 16 terms** |
| Navigation | 300px always-visible sidebar | Persistent sidebar | **None** |

Three numbers explain the complaint. **Twelve font sizes** means nothing has a rank, so
everything competes. **9.5px** is below comfortable reading for anyone, and it is used for the
provider labels that carry the page's whole structure. **Thirty-eight rows with no navigation**
means there is no way in and no sense of progress.

The typography pass fixed the type. It did not fix the layout, and layout is what was wrong.

## What the Best Guides Actually Do

[Tech Interview Handbook](https://github.com/yangshun/tech-interview-handbook) has 142,545 stars
and is the example to follow. Four things it does that this project does not.

### 1. The Structure Is a Journey, and It Is Always Visible

Its sidebar, taken from
[the repository's own configuration](https://github.com/yangshun/tech-interview-handbook/blob/main/apps/website/sidebars.js):

```
Introduction
Getting an interview
Coding interview preparation
System design interview preparation
Behavioral interview preparation
Salary and offer negotiation preparation
Algorithms study cheatsheets        <- reference, deliberately last
```

Every category is named for **a thing the reader is trying to do**, and they run in the order a
real job search happens. Most are set `collapsible: false`, so the entire shape of the handbook
is visible from any page. You always know where you are and how much is left.

Reference material sits at the end, separated from the journey. The two are not mixed.

Cloud Rosetta has no journey at all. It is one catalogue with filters, which serves someone who
already knows what to look up and abandons everyone else.

### 2. The Reading Column Is Narrow

At a 1280px viewport its content column is **607 pixels**, under half the screen, at 67
characters per line. javascript.info is similar at 736px. Neither fills the window, because
long lines are hard to read and the eye loses its place returning to the left margin.

This project uses 1140px and then subdivides it into three columns, which produces cramped
columns *and* a wide page. The worst of both.

### 3. One Page Does One Job

Each handbook page covers a single topic at roughly 3,000 words, with an H2/H3 outline that
reads as a table of contents. The page can be finished.

Cloud Rosetta's single page covers six domains, a decoder and a hierarchy diagram. It cannot be
finished, only scrolled.

### 4. The Entry Point Asks One Thing

Its landing page is an illustration, a one-line description, and a single button reading "Start
reading now." Nothing else competes.

Cloud Rosetta's first screen shows a headline, a thesis, a large statistic, a three-row legend, a
four-item severity strip, three tabs, a search box, two filter buttons, a domain filter row and
an exam filter row, before a single mapping is visible. That is eleven things asking for
attention at once.

## Principles

1. **Separate the journey from the reference.** A path for people learning, a catalogue for
   people looking things up, and never both in the same view. This mirrors the split the
   [Diátaxis framework](https://diataxis.fr/) makes between tutorial and reference; they serve
   different readers and mixing them serves neither.
2. **One page, one job.** If a page cannot be finished, it is a catalogue and belongs in the
   reference half.
3. **Prose gets 640 pixels, never more.** About 68 characters per line. Tables and diagrams may
   break out wider; sentences may not.
4. **Four type sizes, and 16px is the floor for anything a reader must read.** Labels may go to
   13px. Nothing goes below that.
5. **Whitespace is the structure.** 56px between major sections, 24px between paragraphs. If
   two things are related, the gap says so; if they are not, a bigger gap says that.
6. **Show less by default.** A row's supporting note opens on demand rather than shouting from
   the page. Filters live behind a control rather than occupying the masthead.
7. **One primary action per screen.** The entry point offers a single obvious way in.

## The Information Architecture

Journey first, reference second, in the sidebar order below. Every label names what the reader
wants, not what the content is.

```
Start here
  What these three clouds are            00-landscape
  How they are shaped differently        01-mental-models

Learn the parts that differ
  Who can do what                        02-identity
  How the network is put together        03-networking
  Where data lives                       05-databases

Look it up
  The word means something else here     09-confusing-terms
  Service equivalents, graded            reference/<domain>
  Which exam, and what it costs          10-exam-map

Practise
  Drills and self-check                  practice
```

Four groups, ten pages, all visible at once. "Look it up" is where the current single page goes,
split by domain so each page can be finished.

## The Visual System

### Layout

| Element | Value |
| --- | --- |
| Sidebar | 280px, fixed, always visible above 1024px |
| Reading column | 640px maximum for prose |
| Full-bleed elements | Tables and diagrams may reach 880px |
| Page gutter | 32px desktop, 20px mobile |
| Section gap | 56px |
| Paragraph gap | 24px |

### Type

Four sizes. The current nine-step scale was itself too many, and twelve rendered sizes proved it.

| Role | Size | Line height | Weight |
| --- | --- | --- | --- |
| Page title | 34px | 1.2 | 800, Roboto Serif |
| Section | 23px | 1.3 | 700, Roboto Serif |
| Body | 16px | 1.65 | 400, Inter |
| Label and caption | 13px | 1.45 | 600, Roboto, uppercase where it is a label |

Identifiers, exam codes and dates stay in Roboto Mono at body size. The typeface choices carry
over unchanged; only the scale changes.

### Colour

The stone palette and the three provider hues carry over. Two changes:

- **Tinted row backgrounds go.** Filling every cell with a severity tint is what makes the page
  feel crowded. Severity moves to a single small marker plus the left rule.
- **The dark masthead shrinks** to a single band. It currently occupies most of the first screen
  and says little.

### Density

The rule that would have prevented this: **on any screen, at most one thing should be
competing for attention.** A page showing rows shows rows. Filters open from a control. The
statistic belongs on the entry page, once, not above every view.

## What Changes

| Now | After |
| --- | --- |
| One page, 38 rows, no navigation | Ten pages in four groups, sidebar always visible |
| 1140px, three columns | 640px prose, sidebar at 280px |
| Twelve font sizes, smallest 9.5px | Four sizes, floor 13px, body 16px |
| Every note always open, every cell tinted | Notes open on demand, severity as one marker |
| Eleven elements before the first mapping | One heading, one sentence, one way in |
| Reference only | Journey, then reference, then practice |

## What Is Not Changing

The dataset, the divergence and bite grading, the required "what breaks" note, the freshness
dates, the validator and formatter, and the generated surfaces. None of that was the problem.
The data model is the part of this project that works; the rebuild is a new set of renderings
over the same source.

## Acceptance

The rebuild is done when, measured the same way as the table at the top:

- The reading column is 640px or less and lines run 60 to 75 characters
- Fewer than six distinct font sizes render, and none below 13px
- Every page has a sidebar showing the whole structure
- The entry page presents one primary action
- No page mixes journey and reference

<!-- This document follows common-doc-guidelines.md. -->
