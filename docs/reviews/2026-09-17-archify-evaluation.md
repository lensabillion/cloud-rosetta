# Archify Evaluation

**Question:** can the [Archify](https://github.com/tt-a1i/archify) skill draw this guide's
architecture diagrams? **Answer:** not the embedded ones. It suits sequence and lifecycle
diagrams, and interactive companions linked from a chapter.

Evaluated 17 September 2026 against Archify 2.17, installed globally with the `archify` skill
only. The maintainer skill `archify-review` was left out because its triggers would fire during
ordinary code review in every project.

## Method

The guide's AWS resilient web application, from
[reference-architectures.md](../reference-architectures.md), was authored as an Archify
architecture specification, validated, delivered, rendered twice, checked in a browser with
Archify's `visual-check`, and inspected in its 1440 by 900 light screenshot. No project file was
changed during the trial.

## What Works

| Check | Result |
| --- | --- |
| Validation at `showcase` quality | All 9 artifact checks pass, 0 warnings, after one label repair |
| Determinism | Two deliveries of the same specification are byte-identical |
| External references | None; the output is self-contained |
| Layout | Orthogonal routes, every arrow labelled, no crossings |

Determinism matters most: the output would pass `scripts/check_generated.py`.

## What Conflicts With This Project

| This project requires | Archify produces |
| --- | --- |
| Diagrams embedded inline in the guide page | An 804,580 byte standalone viewer; the drawing is 15,625 bytes, 1.9% of the file |
| Drawings styled by `data/design.yml` | Colour carried by 68 CSS classes and no literal fills, so an extracted drawing loses its styling |
| Lato | JetBrains Mono throughout |
| The palette in `data/design.yml` | 139 colours, 2 of which are project tokens |
| One hue per cloud | Hue per component type: backend green, database purple |
| Official AWS, Azure and Google service icons | A 107-entry logo catalogue with no AWS, no Azure and no individual cloud services |
| Nothing below 14px | `visual-check` reported node text projecting to 6px |
| Named availability zones, VPCs and subnets | Boundary kinds limited to `region` and `security-group` |

## The Accuracy Risk

The last row is the one that affects correctness rather than appearance. With no zone container,
the trial drew the private application subnets as a single box spanning both zones. That is
wrong: an AWS subnet resides in exactly one Availability Zone, which this guide states in
`hier.virtual-network-scope`.

Archify did not force that choice; two boxes could have been drawn. Each would still render, and
appear in the legend, as a security group. A subnet is not a security group, so the drawing would
teach the confusion the guide exists to prevent.

## Recommendation

- **Keep `scripts/diagrams.py` for every diagram embedded in the guide.**
- **Use Archify for sequence and lifecycle diagrams**, which the guide does not yet have, such as
  an RDS failover sequence or a request's path through a load balancer. The boundary limitation
  does not apply there.
- **Use Archify for interactive companions**, linked from a chapter as an optional exploration
  alongside the embedded drawing, never in place of it.
- The update check makes one outbound request; it is disabled on this machine through
  `ARCHIFY_UPDATE_CHECK_DISABLED=1` in `~/.zshenv`.

<!-- This document follows common-doc-guidelines.md. -->
