# Architecture redesign review

Scope: six service diagrams and their two chapters, based on upstream `074aaee`.
Tracked by `cloud-f7an`. Reviewed against the cloud architect and design skills.

## Findings and fixes

| ID | Severity | Finding | Fix |
| --- | --- | --- | --- |
| A1 | High | Service drawings lacked recognizable provider artwork and important distinctions were left in prose | Replace three deployment and three introductory diagrams with original provider icons, explicit scope labels and labelled request paths |
| A2 | High | The trade-off table asserted a shared two-zone topology, fixed footprint ratio and managed egress cost without establishing them | Qualify each topology, remove unsupported cost ratios, make egress a workload-dependent choice |
| A3 | Medium | Scaling the new wide SVG to the old minimum width would make the smallest labels less than 14px | Set a token-backed service-diagram minimum width and retain keyboard-scrollable figures and full-size links |
| A4 | Medium | The architecture chapter described obsolete hand-drawn artwork and included project maintenance details | Replace with a cloud-focused reading key; document asset origins under data/vendor-icons |
| A5 | Medium | Initial connectors crossed boundary labels in Azure and Google drawings | Reroute them through free space and repeat the browser review |

## Design assessment

Semantic scenes and token-owned geometry are separate, so a cloud-content edit does not require
hand-editing generated SVG. Embedded original SVG icons make exports portable; names remain
visible and accessible descriptions explain the flow without relying on icon recognition.
Google category icons are deliberate, following its current official product-icon guidance.

The alternatives are a manual diagram editor or an automatic graph layout library. Manual
editing would weaken reproducibility; automatic layout would need additional tooling and still
require review of provider boundaries. The small shared renderer supports the six compositions
without either dependency. Geometry remains manually curated and needs visual review after edits.

These are learning references, not deployed infrastructure. AWS and Google show VM operating
models; Azure shows a managed application runtime. No equivalence of availability guarantees,
fixed failover time, resource cost or untested security posture is asserted.

## Documentation

Chapter source links support the network and recovery behavior. Azure's fourth subnet is
explicitly a separation choice, not a vendor requirement. Reference trade-offs distinguish
illustrated compute pools from service-managed zone distribution. Icon archive sources and
original member paths are recorded in `data/vendor-icons/README.md` and `manifest.json`.

## Validation

- Browser inspection of all six standalone SVGs; revised Azure and Google routes inspected again.
- At 390px, page width remains 390px and the diagram retains its 1440px canvas in its scroll region.
- The Azure full-size link opens its standalone SVG from the mobile layout.
- House formatting, data validation, ten unit/build tests, design checks and generated-output checks.
- Tests cover embedded original asset bytes, named in-bounds scene geometry and rejection of an
  untokenized color in the new renderer, in addition to existing build/link regressions.

Verdict: ready for review after these fixes and passing checks. Browser testing here used the
in-app browser; this is not a claim of exhaustive cross-browser or assistive-technology testing.
The nine existing concept diagrams are retained; this change replaces the six service views.

<!-- This document follows common-doc-guidelines.md. -->
