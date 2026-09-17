#!/usr/bin/env python3
"""Assemble the multi-page guide from the dataset and the Markdown chapters.

The frame follows react.dev, read from its source and recorded in
docs/design-system.md: a sticky top bar with one tab per section, a sidebar
holding only the current section's tree, breadcrumbs above every title, an
outline of the page beside it on wide screens, and previous/next links at the
foot. Pages are routed on the hash so the guide stays a single publishable
document.
"""

from __future__ import annotations

import dataclasses
import html
import pathlib
import re

import design
import diagrams
import mdlite

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
DOCS = ROOT / "docs"
CLOUDS = (("aws", "AWS"), ("azure", "Azure"), ("gcp", "Google Cloud"))
DIVERGENCE = {"exact": "Similar purpose", "partial": "Behaves differently", "none": "Different object or architecture"}
BITE = {"serious": "Serious", "regular": "Regular", "tip": "Tip"}
BITE_HELP = {
    "serious": "Significant risk or cost: a security exposure, real money, or an architectural choice that is hard to correct.",
    "regular": "Consequences are things not working, breaking, or not scaling gracefully.",
    "tip": "Important or often overlooked, but nothing breaks if you miss it.",
}
REPO = "https://github.com/lensabillion/cloud-rosetta"
DOCS_URL = REPO + "/blob/main/docs"


def esc(v) -> str:
    return html.escape(str(v if v is not None else ""), quote=True)


def flat(v) -> str:
    return esc(" ".join(str(v or "").split()))


def plain(text: str) -> str:
    """Heading text with its Markdown removed, for outline and tab labels."""
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return esc(re.sub(r"[`*]", "", text))


# ---------------------------------------------------------------------- icons
# Drawn here rather than copied, so nothing depends on another site's assets.
# Everything is currentColor; colour comes from the stylesheet.

def _icon(paths: str, size: int = 24, box: int = 24, cls: str = "") -> str:
    name = f' class="{cls}"' if cls else ""
    return (f'<svg{name} viewBox="0 0 {box} {box}" width="{size}" height="{size}" '
            f'aria-hidden="true" focusable="false">{paths}</svg>')


_STROKE = 'fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"'
ICON_MENU = _icon(f'<path d="M4 7h16M4 12h16M4 17h16" {_STROKE} stroke-width="2"/>', cls="icon-open")
ICON_CLOSE = _icon(f'<path d="M6 6l12 12M18 6L6 18" {_STROKE} stroke-width="2"/>', cls="icon-close")
ICON_SEARCH = _icon(f'<circle cx="11" cy="11" r="6.5" {_STROKE} stroke-width="2"/>'
                    f'<path d="M16 16l4.5 4.5" {_STROKE} stroke-width="2"/>', size=20)
ICON_MOON = _icon(f'<path d="M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5z" {_STROKE} stroke-width="1.8"/>',
                  size=22, cls="icon-moon")
ICON_SUN = _icon(f'<circle cx="12" cy="12" r="4" {_STROKE} stroke-width="1.8"/>'
                 f'<path d="M12 2.6v2.2M12 19.2v2.2M2.6 12h2.2M19.2 12h2.2M5.4 5.4l1.6 1.6'
                 f'M17 17l1.6 1.6M5.4 18.6l1.6-1.6M17 7l1.6-1.6" {_STROKE} stroke-width="1.8"/>',
                 size=22, cls="icon-sun")
# GitHub's mark, from Octicons (MIT), used only to link to the repository.
ICON_GITHUB = _icon(
    '<path fill="currentColor" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82'
    '-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 '
    '1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08'
    '-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 '
    '2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46'
    '.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z"/>', size=20, box=16)
ICON_NEXT = _icon(f'<path d="M6 4l4 4-4 4" {_STROKE} stroke-width="1.8"/>', size=16, box=16)
ICON_PREV = _icon(f'<path d="M10 4L6 8l4 4" {_STROKE} stroke-width="1.8"/>', size=16, box=16)
ICON_ARROW = _icon(f'<path d="M6 4l4 4-4 4" {_STROKE} stroke-width="1.8"/>', size=16, box=16, cls="tree-arrow")
ICON_ANCHOR = _icon(f'<path d="M6.6 9.4l2.8-2.8M6.9 4.6l1-1a2.7 2.7 0 0 1 3.8 3.8l-1 1M9.1 11.4l-1 1a2.7 2.7 0 0 '
                    f'1-3.8-3.8l1-1" {_STROKE} stroke-width="1.5"/>', size=16, box=16)


# --------------------------------------------------------------------- pieces

def service_line(row: dict, key: str, label: str) -> str:
    block = row.get(key) or {}
    name, url = block.get("name"), block.get("url")
    if name:
        inner = f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(name)}</a>' if url else esc(name)
    else:
        inner = "<em>no equivalent</em>"
    extra = ""
    if block.get("maturity") == "superseded":
        extra += '<span class="meta">&#9873; superseded by the vendor</span>'
    if block.get("formerly"):
        extra += f'<span class="meta was">was {esc(", ".join(block["formerly"]))}</span>'
    if block.get("note"):
        extra += f'<span class="meta">{flat(block["note"])}</span>'
    return (f'<div class="svc {key}"><span class="who">{esc(label)}</span>'
            f'<span class="what">{inner}{extra}</span></div>')


def row_html(row: dict, domain: str) -> str:
    div, bite = row.get("divergence", "exact"), row.get("bite", "tip")
    services = "".join(service_line(row, k, lbl) for k, lbl in CLOUDS)

    note = ""
    if row.get("breaks_when"):
        note = ('<details class="note"><summary>Where it breaks</summary>'
                f'<p>{flat(row["breaks_when"])}</p></details>')
    elif row.get("shared_trap"):
        note = ('<details class="note"><summary>Same everywhere, still caught out</summary>'
                f'<p>{flat(row["shared_trap"])}</p></details>')

    evidence = " ".join(f'<a href="{esc(url)}" target="_blank" rel="noopener">Source {i+1}</a>'
                        for i, url in enumerate(row.get("sources") or []))
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in row.get("exam_tags") or [])
    hay = " ".join([row.get("concept", ""), domain, div, bite, " ".join(row.get("exam_tags") or [])]
                   + [str((row.get(k) or {}).get("name") or "") for k, _ in CLOUDS]
                   + [row.get("breaks_when", ""), row.get("shared_trap", "")]
                   + [str((row.get(k) or {}).get("note") or "") for k, _ in CLOUDS]).lower()

    return f"""<article id="mapping-{esc(row['id'])}" class="row" data-bite="{esc(bite)}" data-div="{esc(div)}" data-find="{esc(hay)}">
<div class="rhead"><h3><a href="#mapping-{esc(row['id'])}">{esc(row.get('concept'))}</a></h3><span class="marks">
<span class="mk b-{esc(bite)}" title="{esc(BITE_HELP[bite])}">{esc(BITE[bite])}</span>
<span class="mk d-{esc(div)}">{esc(DIVERGENCE[div])}</span></span></div>
<div class="svcs">{services}</div>
{note}
<div class="rfoot">{tags}{evidence}<span class="stamp">Recorded check {esc(row.get('verified'))}</span></div>
</article>"""


def term_html(term: dict, known_terms: set[str]) -> str:
    sev = term.get("severity", "low")
    senses = ""
    for key, label in CLOUDS:
        s = term.get(key)
        if not s:
            continue
        cat = esc(s.get("category"))
        cat = f'<a href="{esc(s["url"])}" target="_blank" rel="noopener">{cat}</a>' if s.get("url") else cat
        senses += (f'<div class="sense {key}"><span class="who">{esc(label)}</span>'
                   f'<span><span class="cat">{cat}</span><p>{flat(s.get("meaning"))}</p></span></div>')
    hay = (term.get("term", "") + " " + term.get("why_it_hurts", "") + " " +
           " ".join(str((term.get(k) or {}).get("meaning") or "") for k, _ in CLOUDS)).lower()
    related = " · ".join(f'<a href="#term-{mdlite.slug(name)}">{esc(name)}</a>'
                         for name in term.get("see_also", []) if name in known_terms)
    related = f'<p>Related terms: {related}</p>' if related else ''
    label = {"high": "Different kind of thing", "medium": "Materially different", "low": "Naming difference"}[sev]
    return f"""<article id="term-{mdlite.slug(term['term'])}" class="term s-{esc(sev)}" data-find="{esc(hay)}">
<h3><a href="#term-{mdlite.slug(term['term'])}">{esc(term.get('term'))}</a></h3><span class="sev">{esc(label)}</span>
<div class="senses">{senses}</div>
<details class="note" open><summary>Why the distinction matters</summary><p>{flat(term.get('why_it_hurts'))}</p></details>{related}
</article>"""


def toolbar(scope: str, extra: str = "") -> str:
    return (f'<div class="toolbar"><input type="search" data-scope="{scope}" '
            f'placeholder="Search this page" aria-label="Search this page" aria-description="Search names and explanations on this page">{extra}'
            f'<button type="button" data-clear>Clear search and filters</button>'
            f'<span class="tcount" role="status" aria-live="polite" data-count="{scope}"></span></div>')


def anchored(body: str) -> str:
    """A heading anchor on every section, as react.dev puts one on each heading."""
    def add(match):
        tag, ident, inner = match.group(1), match.group(2), match.group(3)
        anchor = (f'<a class="anchor" href="#{ident}" aria-label="Link to this section">{ICON_ANCHOR}</a>')
        return f'<{tag} id="{ident}">{inner}{anchor}</{tag}>'

    return re.sub(r'<(h[23]) id="([^"]+)">(.*?)</\1>', add, body, flags=re.S)


# ---------------------------------------------------------------------- pages

@dataclasses.dataclass
class Page:
    """One routed page: its body, and the outline shown beside it."""
    slug: str
    body: str
    outline: list[tuple[int, str, str]] = dataclasses.field(default_factory=list)
    extra_class: str = ""


def page_home(counts: dict, terms: int, exams: int) -> Page:
    body = f"""<p class="eyebrow">AWS &middot; Azure &middot; Google Cloud</p>
<h1 id="home--title">The same idea, three different shapes.</h1>
<p class="lede">Most cross-cloud comparisons tell you what a service is called somewhere else.
This one tells you <b>what breaks when you assume it works the same way</b>, and it says so on
every row.</p>
<div class="hero-actions"><a class="cta" href="#00-landscape">Start reading &rarr;</a>
<a class="cta secondary" href="#ref">Look up a service</a></div>
<p class="after">{counts['total']} graded mappings, {terms} colliding terms and {exams} exams.
Free and open source, with primary sources and explicit caveats.</p>"""
    return Page("home", body, extra_class=" hero")


DIAGRAM_MARK = re.compile(r"!\[[^\]]*\]\(assets/architecture/([a-z-]+)\.svg\)")


def page_from_markdown(slug: str, path: pathlib.Path) -> Page:
    source = path.read_text(encoding="utf-8")
    # The sidebar is the navigation, so a chapter's own "next" footer is noise
    # here. It stays in the Markdown, where GitHub readers still need it.
    source = re.split(r"\n## Next\b", source)[0]
    source = re.sub(r"\n\*\*Next:\*\*.*?(?:\n\n|\Z)", "\n", source, flags=re.S)
    # Verification is shown per row and in the footer; a dated preamble on every
    # chapter is meta-commentary that pushes the content down the page.
    source = re.sub(r"\nVerified against vendor documentation on [^\n]*\n(?:[^\n]*\n)?", "\n", source)
    source = re.sub(r"\nMeasurements taken [^\n]*\n(?:[^\n]*\n)?", "\n", source)
    source = re.sub(r"\nFacts marked \*\*verified\*\*[^\n]*\n(?:[^\n]*\n)*?\n", "\n", source)
    # Swap each marker for a sentinel that survives Markdown rendering, then put
    # the drawing back. Keeps the chapter readable as plain Markdown.
    wanted: list[str] = []

    def stash(m):
        wanted.append(m.group(1))
        return f"\n\nFIGURESLOT{len(wanted) - 1}FIGURESLOT\n\n"

    body, outline = mdlite.render(DIAGRAM_MARK.sub(stash, source))
    # Heading IDs must be unique across chapters mounted in the same document.
    for _, ident, _ in outline:
        body = body.replace(f'id="{ident}"', f'id="{slug}--{ident}"')
        body = body.replace(f'href="#{ident}"', f'href="#{slug}--{ident}"')
    outline = [(level, f"{slug}--{ident}", title) for level, ident, title in outline]
    for i, name in enumerate(wanted):
        body = body.replace(f"<p>FIGURESLOT{i}FIGURESLOT</p>", diagrams.render(name, slug + "-" + name))
    if "FIGURESLOT" in body:
        raise SystemExit(f"{path.name}: a diagram slot was not filled")

    # A chapter with several sections gets a contents card, placed after the
    # opening paragraph, because the outline column only appears on wide screens.
    tops = [(i, txt) for lvl, i, txt in outline if lvl == 2]
    if len(tops) >= 4:
        items = "".join(f'<li><a href="#{esc(i)}">{plain(txt)}</a></li>' for i, txt in tops)
        card = (f'<div class="inline-toc"><p class="inline-toc-title">On this page</p>'
                f'<ul>{items}</ul></div>')
        cut = body.find("</p>")
        body = body[:cut + 4] + card + body[cut + 4:] if cut != -1 else card + body
    return Page(slug, anchored(body), outline)


def page_reference_index(domains: list[dict]) -> Page:
    rows = [r for d in domains for r in d["rows"]]
    serious = sum(1 for r in rows if r.get("bite") == "serious")
    items = ""
    for doc in domains:
        count = len(doc["rows"])
        hurts = sum(1 for r in doc["rows"] if r.get("bite") == "serious")
        items += (f'<li><a href="#ref-{esc(doc["domain"])}">{esc(doc.get("title", doc["domain"].title()))}</a>'
                  f'<span>{count} mappings, {hurts} graded serious</span></li>')
    body = f"""<h1 id="ref--title">Service equivalents</h1>
<p>{len(rows)} mappings across {len(domains)} domains, {serious} of them graded serious. Each row
states how far the equivalence can be trusted, and what differs when it cannot.</p>
<ul class="index-list">{items}</ul>"""
    return Page("ref", body)


def page_reference(domain: str, title: str, rows: list[dict]) -> Page:
    serious = sum(1 for r in rows if r.get("bite") == "serious")
    body = "".join(row_html(r, domain) for r in rows)
    extra = '<button data-filter="serious" aria-pressed="false">Only what hurts</button>'
    outline = [(2, f"mapping-{r['id']}", r.get("concept", "")) for r in rows]
    markup = f"""<h1 id="ref-{esc(domain)}--title">{esc(title)}</h1>
<p>{len(rows)} mappings, {serious} of them graded serious. Each row states how far the
equivalence can be trusted; open a note to see what actually differs.</p>
{toolbar('ref-' + domain, extra)}
<div class="list">{body}</div>
<p class="empty hide">Nothing on this page matches. <button type="button" data-clear>Show all entries</button></p>"""
    return Page(f"ref-{domain}", markup, outline)


def page_decoder(terms: list[dict]) -> Page:
    order = {"high": 0, "medium": 1, "low": 2}
    terms = sorted(terms, key=lambda t: (order[t["severity"]], t["term"].lower()))
    high = sum(1 for t in terms if t["severity"] == "high")
    body = "".join(term_html(t, {term["term"] for term in terms}) for t in terms)
    outline = [(2, f"term-{mdlite.slug(t['term'])}", t["term"]) for t in terms]
    markup = f"""<h1 id="decoder--title">The word means something else here</h1>
<p>{len(terms)} terms the three clouds use differently. {high} of them name a different
<em>kind of thing</em> rather than the same thing behaving differently, which is why a service
comparison table cannot hold them.</p>
{toolbar('decoder')}
<div class="list">{body}</div>
<p class="empty hide">No term matches. <button type="button" data-clear>Show all terms</button></p>"""
    return Page("decoder", markup, outline)


def page_exams(exams: list[dict]) -> Page:
    levels = ["foundational", "associate", "professional", "expert", "specialty"]
    names = {"aws": "AWS", "azure": "Azure", "gcp": "Google Cloud"}
    current = [e for e in exams if e["status"] == "current"]
    retired = [e for e in exams if e["status"] != "current"]

    out, outline = [], []
    for prov in ("aws", "azure", "gcp"):
        rows = sorted([e for e in current if e["provider"] == prov],
                      key=lambda e: (levels.index(e["level"]), e["code"]))
        if not rows:
            continue
        trs = "".join(
            f'<tr><td><code>{esc(e["code"])}</code></td>'
            f'<td><a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["name"])}</a></td>'
            f'<td>{esc(e["level"])}</td><td>{esc(e["verified"])}</td></tr>' for e in rows)
        outline.append((2, f"exams--{prov}", names[prov]))
        out.append(f'<h2 id="exams--{prov}">{names[prov]}</h2><div class="tw"><table><thead><tr>'
                   f'<th>Code</th><th>Certification</th><th>Level</th><th>Verified</th>'
                   f'</tr></thead><tbody>{trs}</tbody></table></div>')

    trs = "".join(
        f'<tr><td><code>{esc(e["code"])}</code></td>'
        f'<td><a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["name"])}</a></td>'
        f'<td>{names[e["provider"]]}</td><td>{flat(e.get("note", "Retired."))}</td></tr>'
        for e in sorted(retired, key=lambda e: e["code"]))
    outline.append((2, "exams--retired", "Retired"))
    out.append(f'<h2 id="exams--retired">Retired</h2><p>Listed rather than deleted, because course '
               f'material for them is still on sale.</p><div class="tw"><table><thead><tr><th>Code</th>'
               f'<th>Certification</th><th>Cloud</th><th>Note</th></tr></thead>'
               f'<tbody>{trs}</tbody></table></div>')

    markup = f"""<h1 id="exams--title">Which exam, and what it costs</h1>
<p>{len(current)} current exams and {len(retired)} retired ones, each linked to the vendor's own
page. An exam retiring and a product retiring are separate events; only the exam is tracked here.</p>
{"".join(out)}"""
    return Page("exams", anchored(markup), outline)


# ------------------------------------------------------------------- the frame

def _first_slug(section: dict) -> str:
    first = section["groups"][0][1][0]
    return first[0]


def topnav(sections: list[dict]) -> str:
    tabs = "".join(f'<a class="tab" data-tab="{esc(s["id"])}" href="#{esc(_first_slug(s))}">{esc(s["label"])}</a>'
                   for s in sections)
    return f"""<a class="skip" href="#main" data-skip>Skip to content</a>
<header class="topnav">
  <div class="topnav-bar">
    <div class="topnav-start">
      <button class="control menu-button" type="button" aria-label="Menu" aria-controls="side" aria-expanded="false">{ICON_MENU}{ICON_CLOSE}</button>
      <a class="brand" href="#home">Cloud Rosetta</a>
    </div>
    <div class="topnav-middle">
      <button class="search-button" type="button" data-search-open aria-keyshortcuts="Meta+K Control+K">
        {ICON_SEARCH}<span>Search</span>
        <span class="keys"><kbd data-platform="mac">&#8984;</kbd><kbd data-platform="win">Ctrl</kbd><kbd>K</kbd></span>
      </button>
    </div>
    <div class="topnav-end">
      <nav class="tabs" aria-label="Sections">{tabs}</nav>
      <button class="control search-icon" type="button" data-search-open aria-label="Search">{ICON_SEARCH}</button>
      <button class="control themetog" type="button" aria-label="Switch between light and dark">{ICON_MOON}{ICON_SUN}</button>
      <a class="control" href="{REPO}" target="_blank" rel="noopener" aria-label="Cloud Rosetta on GitHub">{ICON_GITHUB}</a>
    </div>
  </div>
</header>"""


def sidebar(sections: list[dict]) -> str:
    """One tree per section, as react.dev shows only the tree you are inside.

    Below the sidebar breakpoint the same element becomes the menu overlay, with
    the section tabs on top, so there is one navigation tree in the document.
    """
    tabs = "".join(f'<a class="tab" data-tab="{esc(s["id"])}" href="#{esc(_first_slug(s))}">{esc(s["label"])}</a>'
                   for s in sections)
    trees = ""
    for section in sections:
        groups = ""
        for index, (title, items) in enumerate(section["groups"]):
            head_id = f'tree-{section["id"]}-{index}'
            head = f'<span class="tree-head" id="{head_id}">{esc(title)}</span>' if title else ""
            labelled = f' aria-labelledby="{head_id}"' if title else ""
            entries = ""
            for item in items:
                if len(item) == 3:
                    slug, text, children = item
                    subs = "".join(
                        f'<li><a class="tree-link" data-level="1" href="#{esc(child)}"><span>{esc(label)}</span>'
                        f'<span class="tree-count">{count}<span class="sr-only"> mappings</span></span></a></li>'
                        for child, label, count in children)
                    entries += (f'<li class="tree-parent" data-expanded="false">'
                                f'<a class="tree-link" data-level="0" href="#{esc(slug)}">'
                                f'<span>{esc(text)}</span>{ICON_ARROW}</a>'
                                f'<ul class="tree-children">{subs}</ul></li>')
                else:
                    slug, text = item
                    entries += (f'<li><a class="tree-link" data-level="0" href="#{esc(slug)}">'
                                f'<span>{esc(text)}</span></a></li>')
            groups += f'<li class="tree-group">{head}<ul{labelled}>{entries}</ul></li>'
        hidden = "" if section["id"] == "learn" else " hide"
        trees += (f'<nav class="tree{hidden}" data-tree="{esc(section["id"])}" '
                  f'aria-label="{esc(section["label"])}"><ul>{groups}</ul></nav>')
    return (f'<aside class="side" id="side">'
            f'<nav class="side-tabs" aria-label="Sections">{tabs}</nav>'
            f'<div class="side-rule" role="separator"></div>{trees}</aside>')


def breadcrumbs(trail: list[tuple[str, str]]) -> str:
    crumbs = "".join(f'<li><a href="#{esc(slug)}">{esc(label)}</a>{ICON_NEXT}</li>' for slug, label in trail)
    return f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{crumbs}</ol></nav>'


def pager(order: list[tuple[str, str]]) -> dict[str, str]:
    """Previous and next links for every page, taken from the sidebar order so
    the two can never disagree."""
    out = {}
    for i, (slug, label) in enumerate(order):
        prev_ = order[i - 1] if i else None
        next_ = order[i + 1] if i + 1 < len(order) else None
        links = ""
        if prev_:
            links += (f'<a class="pg prev" href="#{esc(prev_[0])}">{ICON_PREV}<span class="pg-text">'
                      f'<span class="pg-label">Previous</span>'
                      f'<span class="pg-title">{esc(prev_[1])}</span></span></a>')
        if next_:
            links += (f'<a class="pg next" href="#{esc(next_[0])}">{ICON_NEXT}<span class="pg-text">'
                      f'<span class="pg-label">Next</span>'
                      f'<span class="pg-title">{esc(next_[1])}</span></span></a>')
        out[slug] = f'<nav class="pager" aria-label="Nearby pages">{links}</nav>' if links else ""
    return out


def outline_column(pages: list[Page]) -> str:
    """react.dev's third column: the current page's headings, on wide screens."""
    navs = ""
    for page in pages:
        if len(page.outline) < 2:
            continue
        top = re.search(r'<h1 id="([^"]+)"', page.body)
        items = f'<li data-depth="2"><a href="#{esc(top.group(1))}">Overview</a></li>' if top else ""
        items += "".join(f'<li data-depth="{level}"><a href="#{esc(ident)}">{plain(text)}</a></li>'
                         for level, ident, text in page.outline)
        navs += (f'<nav class="page-toc hide" data-for="{esc(page.slug)}" aria-label="On this page">'
                 f'<p class="toc-title">On this page</p><ul>{items}</ul></nav>')
    return f'<div class="toc-col">{navs}</div>'


def site_footer(sections: list[dict]) -> str:
    columns = ""
    for section in sections:
        links = ""
        for _, items in section["groups"]:
            for item in items:
                links += f'<li><a href="#{esc(item[0])}">{esc(item[1])}</a></li>'
        columns += (f'<div class="foot-col"><p class="foot-head">{esc(section["label"])}</p>'
                    f'<ul>{links}</ul></div>')
    columns += (f'<div class="foot-col"><p class="foot-head">More</p><ul>'
                f'<li><a href="{REPO}" target="_blank" rel="noopener">Source on GitHub</a></li>'
                f'<li><a href="{REPO}/blob/main/CONTRIBUTING.md" target="_blank" rel="noopener">Send a correction</a></li>'
                f'<li><a href="{REPO}/tree/main/dist" target="_blank" rel="noopener">Flashcards and dataset</a></li>'
                f'</ul></div>')
    return f"""<footer class="site-foot">
<div class="foot-grid">
  <div class="foot-brand"><a class="brand" href="#home">Cloud Rosetta</a>
    <p>AWS, Azure and Google Cloud, and what breaks between them.</p>
    <p class="foot-legal">Code MIT. Content CC BY 4.0.</p></div>
  {columns}
</div>
</footer>"""


SEARCH_DIALOG = f"""<dialog class="search" aria-label="Search the guide">
  <div class="search-bar">{ICON_SEARCH}
    <input class="search-input" type="text" role="combobox" aria-expanded="true" aria-controls="search-results"
           aria-autocomplete="list" autocomplete="off" spellcheck="false" placeholder="Search the guide"
           aria-label="Search the guide">
    <button class="search-close" type="button" data-search-close>Esc</button>
  </div>
  <ul class="search-results" id="search-results" role="listbox" aria-label="Results"></ul>
  <p class="search-note" role="status" aria-live="polite"></p>
</dialog>"""


ROUTER_SOURCE = pathlib.Path(__file__).with_name("router.js").read_text(encoding="utf-8")


# Chapter stem -> in-page route. Anything not here links back to the repository,
# so a reference to a research document does not become a dead in-page link.
ROUTES = {
    "00-landscape": "00-landscape",
    "01-mental-models": "01-mental-models",
    "02-identity": "02-identity",
    "03-networking": "03-networking",
    "05-databases": "05-databases",
    "09-confusing-terms": "decoder",
    "10-exam-map": "exams",
    "practice": "practice",
    "architecture": "architecture",
    "reference-architectures": "reference-architectures",
    "README": "home",
}


def resolve(href: str) -> str:
    from urllib.parse import urljoin

    path, _, fragment = href.partition("#")
    stem = path[:-3] if path.endswith(".md") else path
    if stem in ROUTES and (not fragment or ROUTES[stem] == stem):
        return "#" + ROUTES[stem] + ("--" + fragment if fragment else "")
    return urljoin(DOCS_URL + "/", href)


# ------------------------------------------------------------------- assembly

def build(domains: list[dict], terms: list[dict], exams: list[dict], out: pathlib.Path) -> dict:
    mdlite.RESOLVE = resolve

    rows = [r for d in domains for r in d["rows"]]
    counts = {"total": len(rows),
              "serious": sum(1 for r in rows if r.get("bite") == "serious")}

    journey = [("00-landscape", "What these three clouds are"),
               ("01-mental-models", "How they are shaped differently")]
    learn = [("02-identity", "Who can do what"),
             ("03-networking", "How the network is put together"),
             ("architecture", "Architecture atlas"),
             ("reference-architectures", "Design a resilient application"),
             ("05-databases", "Where data lives")]
    refs = [(f"ref-{d['domain']}", d.get("title", d["domain"].title()), len(d["rows"])) for d in domains]

    sections = [
        {"id": "learn", "label": "Learn", "groups": [
            ("Start here", journey),
            ("Learn the parts that differ", learn),
        ]},
        {"id": "reference", "label": "Reference", "groups": [
            ("Look it up", [("decoder", "The word means something else here"),
                            ("ref", "Service equivalents", refs),
                            ("exams", "Which exam, and what it costs")]),
        ]},
        {"id": "practise", "label": "Practise", "groups": [
            (None, [("practice", "Drills and self-check")]),
        ]},
    ]

    # Where each page sits: its section, its label, and the trail above its title.
    placement: dict[str, tuple[str, str, list[tuple[str, str]]]] = {}
    order: list[tuple[str, str]] = [("home", "Start")]
    for section in sections:
        root = [(_first_slug(section), section["label"])]
        for _, items in section["groups"]:
            for item in items:
                placement[item[0]] = (section["id"], item[1], root)
                order.append((item[0], item[1]))
                if len(item) == 3:
                    for child, label, _count in item[2]:
                        placement[child] = (section["id"], label, root + [(item[0], item[1])])
                        order.append((child, label))

    pages = [page_home(counts, len(terms), len(exams))]
    for slug, _ in journey + learn:
        path = DOCS / f"{slug}.md"
        if path.exists():
            pages.append(page_from_markdown(slug, path))
    pages.append(page_decoder(terms))
    pages.append(page_reference_index(domains))
    for doc in domains:
        pages.append(page_reference(doc["domain"], doc.get("title", doc["domain"].title()), doc["rows"]))
    if exams:
        pages.append(page_exams(exams))
    if (DOCS / "practice.md").exists():
        pages.append(page_from_markdown("practice", DOCS / "practice.md"))

    known = {page.slug for page in pages}
    missing = [slug for slug, _ in order if slug not in known and slug != "home"]
    if missing:
        raise SystemExit(f"navigation points at pages that were not built: {', '.join(missing)}")

    pagers = pager([entry for entry in order if entry[0] in known or entry[0] == "home"])
    markup = ""
    for page in pages:
        section, _label, trail = placement.get(page.slug, ("home", "", []))
        crumbs = breadcrumbs(trail) if trail else ""
        hidden = "" if page.slug == "home" else " hide"
        markup += (f'<section class="page{page.extra_class}{hidden}" id="p-{esc(page.slug)}" '
                   f'data-section="{esc(section)}">{crumbs}{page.body}{pagers.get(page.slug, "")}</section>')

    tokens = design.load()
    shell = (ROOT / "scripts" / "shell.html").read_text(encoding="utf-8")
    shell = shell.replace("{{TOKENS}}", design.css(tokens)).replace("{{FONTS}}", design.font_link(tokens))
    router = ROUTER_SOURCE
    for name, value in tokens["breakpoints"].items():
        shell = shell.replace("{{" + name + "}}", str(value))
        router = router.replace("{{" + name + "}}", str(value))
    if "{{" in shell or "{{" in router:
        raise SystemExit("shell.html or router.js has an unfilled placeholder")
    # The guide carries cloud content only. The design system is developer
    # documentation and lives in data/design.yml, docs/design-system.md and the
    # cloud-rosetta-design skill, not in a reader-facing page.
    body = f"""
{topnav(sections)}
<div class="frame">
{sidebar(sections)}
  <main class="doc" id="main">
{markup}
{site_footer(sections)}
  </main>
{outline_column(pages)}
</div>
{SEARCH_DIALOG}
<script>
{router}
</script>"""

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(shell + body + "\n</body>\n</html>\n", encoding="utf-8")
    return {"pages": len(pages), "rows": len(rows), "terms": len(terms), "exams": len(exams),
            "nav": len(order) - 1}
