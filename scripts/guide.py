#!/usr/bin/env python3
"""Assemble the multi-page guide from the dataset and the Markdown chapters.

Built to docs/design-system.md. The structure is a journey first and a
reference second, never mixed in one view, with the whole shape visible in a
sidebar from every page. Pages are routed on the hash so the guide stays a
single publishable document.
"""

from __future__ import annotations

import datetime as dt
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


def esc(v) -> str:
    return html.escape(str(v if v is not None else ""), quote=True)


def flat(v) -> str:
    return esc(" ".join(str(v or "").split()))


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


# --------------------------------------------------------------------- pages

def page_home(counts: dict, terms: int, exams: int) -> str:
    return f"""<section class="page hero" id="p-home">
<p class="eyebrow">AWS &middot; Azure &middot; Google Cloud</p>
<h1>The same idea, three different shapes.</h1>
<p class="lede">Most cross-cloud comparisons tell you what a service is called somewhere else.
This one tells you <b>what breaks when you assume it works the same way</b>, and it says so on
every row.</p>
<a class="cta" href="#00-landscape">Start reading &rarr;</a>
<p class="after">{counts['total']} graded mappings, {terms} colliding terms and {exams} exams.
Free and open source, with primary sources and explicit caveats.</p>
</section>"""


DIAGRAM_MARK = re.compile(r"!\[[^\]]*\]\(assets/architecture/([a-z-]+)\.svg\)")


def page_from_markdown(slug: str, path: pathlib.Path) -> str:
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

    # A chapter with several sections gets a contents block, placed after the
    # opening paragraph so the reader sees what the page covers before scrolling.
    tops = [(i, txt) for lvl, i, txt in outline if lvl == 2]
    if len(tops) >= 4:
        items = "".join(f'<a href="#{esc(i)}">{esc(txt)}</a>' for i, txt in tops)
        toc = f'<nav class="toc" aria-label="On this page"><b>On this page</b>{items}</nav>'
        cut = body.find("</p>")
        body = body[:cut + 4] + toc + body[cut + 4:] if cut != -1 else toc + body
    return f'<section class="page hide" id="p-{slug}">{body}</section>'


def page_reference(domain: str, title: str, rows: list[dict]) -> str:
    serious = sum(1 for r in rows if r.get("bite") == "serious")
    body = "".join(row_html(r, domain) for r in rows)
    extra = '<button data-filter="serious" aria-pressed="false">Only what hurts</button>'
    return f"""<section class="page hide" id="p-ref-{domain}">
<p class="eyebrow">Service equivalents</p>
<h1>{esc(title)}</h1>
<p>{len(rows)} mappings, {serious} of them graded serious. Each row states how far the
equivalence can be trusted; open a note to see what actually differs.</p>
{toolbar('ref-' + domain, extra)}
<div class="list">{body}</div>
<p class="empty hide">Nothing on this page matches. <button type="button" data-clear>Show all entries</button></p>
</section>"""


def page_decoder(terms: list[dict]) -> str:
    order = {"high": 0, "medium": 1, "low": 2}
    terms = sorted(terms, key=lambda t: (order[t["severity"]], t["term"].lower()))
    high = sum(1 for t in terms if t["severity"] == "high")
    body = "".join(term_html(t, {term["term"] for term in terms}) for t in terms)
    return f"""<section class="page hide" id="p-decoder">
<p class="eyebrow">Look it up</p>
<h1>The word means something else here</h1>
<p>{len(terms)} terms the three clouds use differently. {high} of them name a different
<em>kind of thing</em> rather than the same thing behaving differently, which is why a service
comparison table cannot hold them.</p>
{toolbar('decoder')}
<div class="list">{body}</div>
<p class="empty hide">No term matches. <button type="button" data-clear>Show all terms</button></p>
</section>"""


def page_exams(exams: list[dict]) -> str:
    levels = ["foundational", "associate", "professional", "expert", "specialty"]
    names = {"aws": "AWS", "azure": "Azure", "gcp": "Google Cloud"}
    current = [e for e in exams if e["status"] == "current"]
    retired = [e for e in exams if e["status"] != "current"]

    out = []
    for prov in ("aws", "azure", "gcp"):
        rows = sorted([e for e in current if e["provider"] == prov],
                      key=lambda e: (levels.index(e["level"]), e["code"]))
        if not rows:
            continue
        trs = "".join(
            f'<tr><td><code>{esc(e["code"])}</code></td>'
            f'<td><a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["name"])}</a></td>'
            f'<td>{esc(e["level"])}</td><td>{esc(e["verified"])}</td></tr>' for e in rows)
        out.append(f'<h2>{names[prov]}</h2><div class="tw"><table><thead><tr>'
                   f'<th>Code</th><th>Certification</th><th>Level</th><th>Verified</th>'
                   f'</tr></thead><tbody>{trs}</tbody></table></div>')

    trs = "".join(
        f'<tr><td><code>{esc(e["code"])}</code></td>'
        f'<td><a href="{esc(e["url"])}" target="_blank" rel="noopener">{esc(e["name"])}</a></td>'
        f'<td>{names[e["provider"]]}</td><td>{flat(e.get("note", "Retired."))}</td></tr>'
        for e in sorted(retired, key=lambda e: e["code"]))
    out.append(f'<h2>Retired</h2><p>Listed rather than deleted, because course material for them '
               f'is still on sale.</p><div class="tw"><table><thead><tr><th>Code</th>'
               f'<th>Certification</th><th>Cloud</th><th>Note</th></tr></thead>'
               f'<tbody>{trs}</tbody></table></div>')

    return f"""<section class="page wide hide" id="p-exams">
<p class="eyebrow">Look it up</p>
<h1>Which exam, and what it costs</h1>
<p>{len(current)} current exams and {len(retired)} retired ones, each linked to the vendor's own
page. An exam retiring and a product retiring are separate events; only the exam is tracked here.</p>
{"".join(out)}
</section>"""


# --------------------------------------------------------------------- assembly

def pager(order: list[tuple[str, str]]) -> dict[str, str]:
    """Previous and next links for every page, taken from the sidebar order so
    the two can never disagree."""
    out = {}
    for i, (slug, label) in enumerate(order):
        prev_ = order[i - 1] if i else None
        next_ = order[i + 1] if i + 1 < len(order) else None
        links = ""
        if prev_:
            links += (f'<a class="pg prev" href="#{esc(prev_[0])}">'
                      f'<span>Previous</span>{esc(prev_[1])}</a>')
        if next_:
            links += (f'<a class="pg next" href="#{esc(next_[0])}">'
                      f'<span>Next</span>{esc(next_[1])}</a>')
        out[slug] = f'<nav class="pager">{links}</nav>' if links else ""
    return out


def nav(groups: list) -> str:
    out = []
    for title, items in groups:
        links = ""
        for item in items:
            if isinstance(item, tuple) and item[0] == "sub":
                kids = "".join(f'<a class="nl" href="#{esc(s)}">{esc(l)}</a>' for s, l in item[2])
                links += f'<div class="sub">{kids}</div>'
            else:
                slug, label = item
                links += f'<a class="nl" href="#{esc(slug)}">{esc(label)}</a>'
        out.append(f'<div class="grp"><h2>{esc(title)}</h2>{links}</div>')
    return "<nav id=\"nav\">" + "".join(out) + "</nav>"


ROUTER = "<script>\n" + pathlib.Path(__file__).with_name("router.js").read_text(encoding="utf-8") + "\n</script>"


REPO = "https://github.com/lensabillion/cloud-rosetta/blob/main/docs"

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


def _page_id(markup: str) -> str:
    m = re.search(r'id="p-([^"]+)"', markup)
    return m.group(1) if m else ""


def resolve(href: str) -> str:
    from urllib.parse import urljoin

    path, _, fragment = href.partition("#")
    stem = path[:-3] if path.endswith(".md") else path
    if stem in ROUTES and (not fragment or ROUTES[stem] == stem):
        return "#" + ROUTES[stem] + ("--" + fragment if fragment else "")
    return urljoin(REPO + "/", href)


def build(domains: list[dict], terms: list[dict], exams: list[dict], out: pathlib.Path) -> dict:
    mdlite.RESOLVE = resolve

    rows = [r for d in domains for r in d["rows"]]
    counts = {"total": len(rows),
              "serious": sum(1 for r in rows if r.get("bite") == "serious")}

    pages = [page_home(counts, len(terms), len(exams))]

    journey = [("00-landscape", "What these three clouds are"),
               ("01-mental-models", "How they are shaped differently")]
    learn = [("02-identity", "Who can do what"),
             ("03-networking", "How the network is put together"),
             ("architecture", "Architecture atlas"),
             ("reference-architectures", "Design a resilient application"),
             ("05-databases", "Where data lives")]

    for slug, _ in journey + learn:
        path = DOCS / f"{slug}.md"
        if path.exists():
            pages.append(page_from_markdown(slug, path))

    pages.append(page_decoder(terms))

    refs = []
    for doc in domains:
        slug, title = doc["domain"], doc.get("title", doc["domain"].title())
        pages.append(page_reference(slug, title, doc["rows"]))
        refs.append((f"ref-{slug}", title))

    if exams:
        pages.append(page_exams(exams))
    if (DOCS / "practice.md").exists():
        pages.append(page_from_markdown("practice", DOCS / "practice.md"))

    groups = [
        ("Start here", journey),
        ("Learn the parts that differ", learn),
        ("Look it up", [("decoder", "The word means something else here"),
                        ("sub", "Service equivalents", refs),
                        ("exams", "Which exam, and what it costs")]),
        ("Practise", [("practice", "Drills and self-check")]),
    ]

    order = [("home", "Start")]
    for _, items in groups:
        for item in items:
            if isinstance(item, tuple) and item[0] == "sub":
                order += [(s, l) for s, l in item[2]]
            else:
                order.append(item)
    pagers = pager(order)
    pages = [p.replace("</section>", pagers.get(_page_id(p), "") + "</section>", 1)
             if _page_id(p) in pagers else p for p in pages]

    tokens = design.load()
    shell = (ROOT / "scripts" / "shell.html").read_text(encoding="utf-8")
    shell = shell.replace("{{TOKENS}}", design.css(tokens)).replace("{{FONTS}}", design.font_link(tokens))
    if "{{" in shell:
        raise SystemExit("shell.html has an unfilled placeholder")
    # The guide carries cloud content only. The design system is developer
    # documentation and lives in data/design.yml, docs/design-system.md and the
    # cloud-rosetta-design skill, not in a reader-facing page.
    body = f"""
<button class="themetog" title="Switch light and dark" aria-label="Switch light and dark">&#9681;</button>
<div class="app">
  <aside class="side">
    <div class="brand"><a href="#home"><b>Cloud Rosetta</b></a>
      <span>AWS, Azure and Google Cloud, side by side</span></div>
    <button class="menutog" aria-controls="nav" aria-expanded="false">Contents</button>
    {nav(groups)}
  </aside>
  <main class="doc">
{"".join(pages)}
  </main>
</div>
{ROUTER}"""

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(shell + body + "\n</body>\n</html>\n", encoding="utf-8")
    return {"pages": len(pages), "rows": len(rows), "terms": len(terms), "exams": len(exams),
            "nav": sum(len(i) if t != "Look it up" else len(refs) + 2 for t, i in groups)}
