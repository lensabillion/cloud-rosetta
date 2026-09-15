# Interaction Review — 15 September 2026

## Fixed Behaviors

- Chapter navigation closes the mobile menu before positioning the document, moves keyboard
  focus into the destination, and positions the target after the page layout updates. The
  Azure contents link was observed landing below its intended section; the revised link was
  browser-tested with its heading visible near the top of the viewport.
- Comparison and term titles have stable direct links. Related terms link to existing entries.
- Search and severity filters are represented in the URL and restored on route navigation.
  Search includes provider notes. The decoder has search without an irrelevant severity button.
- Clear controls reset both query and severity. Empty results have a one-click recovery button.
- Menu expansion is announced through `aria-expanded`; Escape closes the menu.
- Modified link clicks retain native browser behavior for opening another tab.
- Markdown links preserve nested paths and section fragments. Source links are not rewritten
  simply because they end in `.md`, and query separators are escaped once rather than twice.
  Repository source-file links point to GitHub instead of missing files on the published site.

## Verification

Seven Python tests cover generated surfaces and link compilation. A table of five real link
failure classes failed before the resolver repair and passes afterward. JavaScript syntax,
YAML style, data validation and generated-output checks run separately. Browser exercises
cover section navigation, comparison filtering, empty-result recovery, menu navigation and
term search. No cloud resources are involved.

Tracked as `cloud-upqf`. Source: `scripts/router.js`, `scripts/guide.py` and `scripts/mdlite.py`.

## Official Architecture Icons

All three providers publish service icon libraries. Current diagrams use project-drawn labeled
boxes. Using provider artwork is tracked separately as `cloud-f7an`.

| Provider | Official library | Application to this guide |
| --- | --- | --- |
| AWS | [Architecture icons](https://aws.amazon.com/architecture/icons/) | Use the current service/resource icons alongside service labels |
| Azure | [Architecture icons and usage guidance](https://learn.microsoft.com/en-us/azure/architecture/icons/) | Keep names beside icons; preserve shape and orientation |
| Google Cloud | [Official product icon library](https://cloud.google.com/icons) | Follow the product-icon overview for the selected library |

Icons identify products; the diagram must still explain data flow, ownership, location,
security controls and failure behavior. They do not replace readable labels or source citations.

<!-- This document follows common-doc-guidelines.md. -->
