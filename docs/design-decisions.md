# Design Decisions

Why this guide looks and reads the way it does. Written before the content, so the content has
something to conform to. Revisit this document rather than inventing a new pattern mid-chapter.

## The Problem the Design Has to Solve

The research in [research-pain-points.md](research-pain-points.md) points at one thing. The
difficulty is not finding the equivalent of a service. Plenty of comparison tables already do
that, including
[Microsoft's own Google Cloud to Azure comparison](https://learn.microsoft.com/en-us/azure/architecture/gcp-professional/services).
The difficulty is that near-equivalents behave differently in ways that decide exam questions,
and a flat three-column table actively hides that.

So the design rule for the whole project:

> Equivalence is the cheap part. Every representation must foreground **divergence**.

A table that says "EC2 / Virtual Machines / Compute Engine" and stops has taught a reader
something they already suspected and hidden the thing that will cost them a mark.

## Decision 1: Grade Every Mapping

Every row in every mapping table carries a divergence grade in its own column.

| Grade | Meaning | Reader action |
| --- | --- | --- |
| ✅ | Close equivalent. Mental model transfers. | Learn one, use the name elsewhere |
| ⚠️ | Maps, but behaves differently in a way that changes answers | Read the note. This is where marks are lost |
| ❌ | No honest equivalent. The clouds solve this differently | Learn each separately; do not translate |

The ⚠️ rows are the product. Everything else is scaffolding around them.

## Decision 2: Scope Diagrams Carry the Mental Model

Prose is bad at containment. A reader can read "a Google VPC is global while an AWS VPC is
regional" three times and still place a subnet in a zone on exam day.

The fix is a set of nested-box diagrams, drawn once and reused, showing the containment chain
for each cloud side by side at the same scale:

- AWS: organization, organizational unit, account, region, VPC, availability zone, subnet
- Azure: tenant, management group, subscription, resource group, region, VNet, subnet
- Google Cloud: organization, folder, project, VPC as a global object, region, subnet

Drawn side by side, the differences are visible in about two seconds. Described in prose they
take three paragraphs and still do not stick.

## Decision 3: A Scope Ruler for Regional, Zonal, and Global

A second recurring visual: a horizontal band per cloud with three lanes for global, regional,
and zonal, with resources placed in their lane. This makes a specific, high-frequency trap
visible rather than memorized, for example that a Google VPC sits in the global lane while an
AWS subnet sits in the zonal lane.

## Decision 4: False-Friend Cards for Colliding Terms

Terms that mean different things per cloud get a card, not a table row. The word is the
heading, and three short panels underneath say what it denotes in each cloud, with an explicit
statement of what category of thing it is. "Role" is the model case: an identity in AWS, a
permission set in the other two.

Cards work here because the unit of confusion is the word, and the reader arrives looking up a
word rather than browsing a domain.

## Decision 5: Decision Trees Only Where Choice Is Genuinely Branching

Reserved for the handful of selections that generate exam questions repeatedly, such as which
storage tier, which load balancer, and which database. Not applied everywhere. A decision tree
for something with one sensible answer is decoration.

## Decision 6: Split Markdown Source and a Published Web Guide

The Markdown in `docs/` is the source of truth: greppable, diffable, and editable without
tooling. The published web guide is a rendering of the same material with search and filters
that Markdown cannot provide. When the two disagree, the Markdown wins and the web guide gets
rebuilt.

## Typography

Requirement: pick the two typefaces people most like, on evidence rather than taste, and use
those two.

### Evidence

Google Fonts is the only source publishing usage at a scale that supports a claim about what
people actually choose. As of the twelve months ending May 2025, across a library of 1,826
families serving more than 50 million websites:

| Typeface | Evidence | Reading |
| --- | --- | --- |
| Roboto | Roughly 28 trillion cumulative views, the highest of any family | The most-used typeface on the web by a wide margin |
| Inter | 414 billion views in the year to May 2025, growing 57% year on year; described as the most-installed sans-serif on the web in 2026 | The current preference, and the one still gaining |

Sources: [Kinsta's Google Fonts analysis](https://kinsta.com/blog/best-google-fonts/),
[FontFYI on variable fonts](https://fontfyi.com/blog/best-variable-fonts/).

Roboto wins on accumulated use, Inter on current momentum. Rather than arbitrate between a
lifetime total and a growth rate, the guide uses both.

### Assignment

Four cuts drawn from those two families. Every one is a real variable font served by Google
Fonts, confirmed by requesting weight ranges and checking that ranges came back.

| Role | Face | Why this one |
| --- | --- | --- |
| Display | **Roboto Serif**, 800 | Headline, the hero figure, decoder headwords, row titles. See below |
| Micro-labels | **Roboto**, 700, uppercase | Column labels, badges, tabs. A grotesque stays legible at 10px where a serif silts up |
| Text | **Inter**, 400 to 600 | Body, tables, panels, controls. Drawn for screen reading at small sizes, ships tabular figures, and this guide is mostly digits in columns |
| Identifiers | **Roboto Mono**, 400 to 500 | Exam codes, dates, row ids. Things that must not be mistaken for prose |

**Why a serif carries the display.** The first build set Roboto against Inter, which was the
honest reading of the usage evidence and a weak piece of design: two neutral grotesques at text
size are effectively one typeface, so the pairing bought nothing but an extra request. Roboto
Serif fixes that without leaving the two families the evidence supported, since it belongs to the
Roboto superfamily.

It also fits the content. The decoder is a dictionary, and a dictionary sets its headwords with
authority. "Role", "Resource group" and "Availability set" standing at 27px in a serif read as
entries to be looked up, which is exactly what they are. Every cloud vendor's documentation is
set in a grotesque, so a serif also puts visible distance between this and the material it
corrects.

### The Scale

One scale, roughly a major third through the middle and opening up at display. Every size on the
page comes from it, replacing the eleven ad hoc values the first build accumulated.

| Token | Size | Used for |
| --- | --- | --- |
| `--t-micro` | 10px | Uppercase labels, badges, tags |
| `--t-mini` | 11.5px | Metadata, verification stamps |
| `--t-small` | 13px | Panel prose, notes |
| `--t-base` | 15px | Body |
| `--t-lede` | 17.5px | Opening paragraphs |
| `--t-h3` | 21px | Row concept titles |
| `--t-h2` | 27px | Decoder headwords |
| `--t-h1` | 42px | Page title |
| `--t-hero` | 84px | The finding |

Leading tightens as size grows, from 1.62 at body to 0.82 at the hero figure. Tracking is
negative at display, zero in text, and positive only for uppercase, which is the one place
letter-spacing genuinely belongs. `font-optical-sizing: auto` is set and the optical size axis is
requested for Roboto Serif; browsers apply it where the served font carries the axis.

### Caveats

The usage evidence pointed at two grotesques, and the honest thing to say is that following it
literally produced a worse page than following it in spirit. Roboto Serif keeps the project
inside the researched families while giving the display real separation from the text. Anyone who
wants the strict reading can swap `--serif` for `--sans` in one line.

## Colour and Accessibility

- Each cloud gets one consistent hue, used identically everywhere: AWS, Azure, and Google Cloud
  keep the same colour in every table, diagram, and card.
- Divergence grades are never colour alone. The ✅, ⚠️, and ❌ marks carry the meaning so the
  grading survives greyscale printing and colour vision deficiency.
- Light and dark themes are both defined, since readers study at night.

<!-- This document follows common-doc-guidelines.md. -->
