#!/usr/bin/env python3
"""Generate the Cloud Rosetta web guide from the YAML dataset.

The site is a rendering, never a source. Every row on the page comes from
data/, so the published guide cannot drift from the data the validator checks.

Usage: python scripts/build.py [--out site/index.html]
"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import pathlib
import sys

import yaml

import surfaces

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CLOUDS = (("aws", "AWS"), ("azure", "Azure"), ("gcp", "Google Cloud"))

GRADE = {
    "exact":   ("✅", "Close equivalent",   "The mental model transfers. Learn it once."),
    "partial": ("⚠️", "Behaves differently", "Maps, but differs in a way that changes answers."),
    "none":    ("❌", "No honest equivalent", "The clouds solve this differently. Do not translate."),
}
BITE = {
    "serious": ("❗", "Serious", "Significant risk or cost: a security exposure, real money, or an architectural choice that is hard to correct."),
    "regular": ("🔸", "Regular", "Consequences are things not working, breaking, or not scaling gracefully."),
    "tip":     ("🔹", "Tip",     "Important or often overlooked, but nothing breaks if you miss it."),
}
SEVERITY = {
    "high":   ("Different kind of thing", "Same word, different category of object."),
    "medium": ("Materially different",    "Same category, behaviour differs enough to matter."),
    "low":    ("Naming difference",       "Mostly cosmetic, still worth knowing."),
}


def esc(value) -> str:
    return html.escape(str(value if value is not None else ""), quote=True)


def para(text) -> str:
    """YAML folded blocks arrive as one line; keep them that way but tidy."""
    return esc(" ".join(str(text or "").split()))


def load_mappings() -> list[dict]:
    domains = []
    for path in sorted((DATA / "mappings").glob("*.yml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        domains.append(doc)
    return domains


def load_terms() -> list[dict]:
    terms: list[dict] = []
    for path in sorted((DATA / "terms").glob("*.yml")):
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        terms.extend(doc.get("terms") or [])
    return terms


def cloud_cell(row: dict, key: str, label: str) -> str:
    block = row.get(key) or {}
    name = block.get("name")
    url = block.get("url")
    formerly = block.get("formerly") or []
    note = block.get("note")

    if name:
        inner = f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(name)}</a>' if url else esc(name)
        body = f'<span class="svc">{inner}</span>'
    else:
        body = '<span class="svc none">No equivalent</span>'

    extra = ""
    if block.get("maturity") == "superseded":
        extra += '<span class="mat">&#9873; superseded by the vendor</span>'
    if formerly:
        extra += f'<span class="formerly">was {esc(", ".join(formerly))}</span>'
    if note:
        extra += f'<span class="cnote">{para(note)}</span>'

    return (
        f'<div class="cell {key}">'
        f'<span class="clabel">{esc(label)}</span>{body}{extra}'
        f"</div>"
    )


def render_row(row: dict, domain: str) -> str:
    grade = row.get("divergence", "exact")
    icon, headline, _ = GRADE[grade]
    bite = row.get("bite", "tip")
    b_icon, b_label, b_help = BITE[bite]
    tags = row.get("exam_tags") or []

    cells = "".join(cloud_cell(row, k, lbl) for k, lbl in CLOUDS)

    detail = ""
    if row.get("breaks_when"):
        detail += (
            '<div class="well breaks"><span class="wlabel">Where it breaks</span>'
            f"<p>{para(row['breaks_when'])}</p></div>"
        )
    if row.get("shared_trap"):
        detail += (
            '<div class="well trap"><span class="wlabel">Same everywhere, still caught out</span>'
            f"<p>{para(row['shared_trap'])}</p></div>"
        )

    sources = ""
    if row.get("sources"):
        links = " ".join(
            f'<a href="{esc(u)}" target="_blank" rel="noopener">{esc(u.split("/")[2])}</a>'
            for u in row["sources"]
        )
        sources = f'<span class="srcs">Checked against {links}</span>'

    tagged = "".join(f'<span class="tag">{esc(t)}</span>' for t in tags)

    haystack = " ".join(
        [row.get("concept", ""), domain, grade, bite, " ".join(tags)]
        + [str((row.get(k) or {}).get("name") or "") for k, _ in CLOUDS]
        + [" ".join((row.get(k) or {}).get("formerly") or []) for k, _ in CLOUDS]
        + [row.get("breaks_when", ""), row.get("shared_trap", "")]
    ).lower()

    return f"""<article class="row g-{grade}" data-domain="{esc(domain)}" data-grade="{esc(grade)}" data-bite="{esc(bite)}" data-exams="{esc(' '.join(tags))}" data-find="{esc(haystack)}">
  <header class="rhead">
    <h3>{esc(row.get('concept'))}</h3>
    <span class="marks"><span class="bite b-{esc(bite)}" title="{esc(b_help)}"><span aria-hidden="true">{b_icon}</span>{esc(b_label)}</span><span class="grade" title="{esc(GRADE[grade][2])}"><span aria-hidden="true">{icon}</span>{esc(headline)}</span></span>
  </header>
  <div class="grid">{cells}</div>
  {detail}
  <footer class="rfoot"><span class="tags">{tagged}</span>{sources}<span class="stamp" title="Last checked against vendor documentation">Verified {esc(row.get('verified'))}</span></footer>
</article>"""


def render_term(term: dict) -> str:
    sev = term.get("severity", "low")
    sev_label, sev_help = SEVERITY[sev]

    panels = ""
    for key, label in CLOUDS:
        sense = term.get(key)
        if not sense:
            continue
        url = sense.get("url")
        cat = esc(sense.get("category"))
        cat_html = f'<a href="{esc(url)}" target="_blank" rel="noopener">{cat}</a>' if url else cat
        panels += (
            f'<div class="panel {key}"><span class="clabel">{esc(label)}</span>'
            f'<span class="cat">{cat_html}</span>'
            f"<p>{para(sense.get('meaning'))}</p></div>"
        )

    also = ""
    if term.get("see_also"):
        also = '<span class="also">See also ' + ", ".join(esc(s) for s in term["see_also"]) + "</span>"

    haystack = (
        term.get("term", "")
        + " "
        + term.get("why_it_hurts", "")
        + " "
        + " ".join(str((term.get(k) or {}).get("meaning") or "") for k, _ in CLOUDS)
    ).lower()

    return f"""<article class="term s-{sev}" data-sev="{esc(sev)}" data-find="{esc(haystack)}">
  <header class="thead">
    <h3>{esc(term.get('term'))}</h3>
    <span class="sev" title="{esc(sev_help)}">{esc(sev_label)}</span>
  </header>
  <div class="panels">{panels}</div>
  <div class="well hurts"><span class="wlabel">Why it costs marks</span><p>{para(term.get('why_it_hurts'))}</p></div>
  <footer class="rfoot">{also}<span class="stamp">Verified {esc(term.get('verified'))}</span></footer>
</article>"""


HIERARCHY_SVG = """
<svg viewBox="0 0 900 330" role="img" aria-labelledby="hier-t hier-d" class="diagram">
  <title id="hier-t">Resource hierarchy of AWS, Azure and Google Cloud side by side</title>
  <desc id="hier-d">Nested containers drawn at the same scale. AWS nests organization, organizational unit, account, then a regional VPC whose subnets sit inside one availability zone. Azure nests tenant, management group, subscription, resource group, then a regional virtual network with regional subnets. Google Cloud nests organization, folder, project, then a global VPC whose subnets are regional.</desc>
  <g class="dg">
    <!-- AWS -->
    <text x="20" y="26" class="dh dh-aws">AWS</text>
    <rect x="20" y="38" width="260" height="270" rx="6" class="d1"/>
    <text x="32" y="58" class="dl">Organization</text>
    <rect x="34" y="68" width="232" height="228" rx="5" class="d2"/>
    <text x="46" y="88" class="dl">Organizational unit</text>
    <rect x="48" y="98" width="204" height="186" rx="4" class="d3"/>
    <text x="60" y="118" class="dl dl-key">Account</text>
    <text x="60" y="134" class="dn">isolation + billing + identity</text>
    <rect x="62" y="144" width="176" height="128" rx="4" class="d4"/>
    <text x="74" y="164" class="dl">Region</text>
    <rect x="76" y="174" width="148" height="86" rx="4" class="d5"/>
    <text x="88" y="194" class="dl">VPC <tspan class="dn">regional</tspan></text>
    <rect x="90" y="204" width="120" height="44" rx="3" class="d6"/>
    <text x="102" y="222" class="dl">Availability Zone</text>
    <text x="102" y="238" class="dl dl-key">Subnet</text>

    <!-- Azure -->
    <text x="320" y="26" class="dh dh-azure">Azure</text>
    <rect x="320" y="38" width="260" height="270" rx="6" class="d1"/>
    <text x="332" y="58" class="dl">Entra ID tenant</text>
    <rect x="334" y="68" width="232" height="228" rx="5" class="d2"/>
    <text x="346" y="88" class="dl">Management group</text>
    <rect x="348" y="98" width="204" height="186" rx="4" class="d3"/>
    <text x="360" y="118" class="dl dl-key">Subscription</text>
    <text x="360" y="134" class="dn">billing boundary</text>
    <rect x="362" y="144" width="176" height="128" rx="4" class="d4"/>
    <text x="374" y="164" class="dl dl-key">Resource group</text>
    <text x="374" y="180" class="dn">mandatory, deletes contents</text>
    <rect x="376" y="190" width="148" height="70" rx="4" class="d5"/>
    <text x="388" y="210" class="dl">Virtual network <tspan class="dn">regional</tspan></text>
    <text x="388" y="234" class="dl dl-key">Subnet <tspan class="dn">regional, spans zones</tspan></text>

    <!-- Google Cloud -->
    <text x="620" y="26" class="dh dh-gcp">Google Cloud</text>
    <rect x="620" y="38" width="260" height="270" rx="6" class="d1"/>
    <text x="632" y="58" class="dl">Organization</text>
    <rect x="634" y="68" width="232" height="228" rx="5" class="d2"/>
    <text x="646" y="88" class="dl">Folder</text>
    <rect x="648" y="98" width="204" height="126" rx="4" class="d3"/>
    <text x="660" y="118" class="dl dl-key">Project</text>
    <text x="660" y="134" class="dn">isolation boundary</text>
    <rect x="662" y="144" width="176" height="66" rx="4" class="d4"/>
    <text x="674" y="164" class="dl">Region</text>
    <text x="674" y="188" class="dl dl-key">Subnet <tspan class="dn">regional</tspan></text>
    <rect x="648" y="234" width="204" height="52" rx="4" class="d5 dglobal"/>
    <text x="660" y="254" class="dl dl-key">VPC network</text>
    <text x="660" y="272" class="dn">global, sits outside any region</text>
  </g>
</svg>
"""



def render_terms_markdown(terms: list[dict]) -> str:
    """Emit the decoder as a Markdown chapter so the prose cannot drift from the data."""
    order = {"high": 0, "medium": 1, "low": 2}
    terms = sorted(terms, key=lambda t: (order[t["severity"]], t["term"].lower()))

    out = [
        "# The Confusing Terms Decoder",
        "",
        "Generated from `data/terms/`. Edit the YAML, not this file.",
        "",
        "The hardest part of a second cloud is not that Compute Engine is called EC2. It is that",
        "the same word denotes different kinds of thing depending on whose console you are in.",
        "These have no row in a service comparison table, because they are not services.",
        "",
        "**Severity** says how badly the word collides. `high` means the clouds use it for",
        "different categories of object. `medium` means the same category behaving differently.",
        "`low` means a naming difference worth knowing.",
        "",
        "## Index",
        "",
        "| Term | Severity | The collision in one line |",
        "| --- | --- | --- |",
    ]

    for term in terms:
        cats = " vs ".join(
            f"{lbl} {(term[k] or {}).get('category')}" for k, lbl in CLOUDS if term.get(k)
        )
        out.append(f"| [{term['term']}](#{term['term'].lower().replace(' ', '-')}) | {term['severity']} | {cats} |")

    out.append("")
    for term in terms:
        out += [f"## {term['term']}", "", f"**Severity: {term['severity']}.** {SEVERITY[term['severity']][1]}", ""]
        out.append("| Cloud | What it is | Meaning |")
        out.append("| --- | --- | --- |")
        for key, label in CLOUDS:
            sense = term.get(key)
            if not sense:
                continue
            meaning = " ".join(str(sense.get("meaning", "")).split())
            out.append(f"| {label} | {sense.get('category')} | {meaning} |")
        out += ["", "**Why it costs marks.** " + " ".join(str(term.get("why_it_hurts", "")).split()), ""]
        if term.get("see_also"):
            out += ["See also: " + ", ".join(term["see_also"]) + ".", ""]
        out += [f"*Verified {term.get('verified')}.*", ""]

    out += ["<!-- Generated by scripts/build.py from data/terms/. Do not edit by hand. -->", ""]
    return "\n".join(out)


def build(out: pathlib.Path) -> None:
    domains = load_mappings()
    terms = load_terms()

    rows_html, domain_chips = [], []
    exams: set[str] = set()
    counts = {"exact": 0, "partial": 0, "none": 0}
    oldest = None

    for doc in domains:
        slug = doc["domain"]
        title = doc.get("title", slug.title())
        domain_chips.append((slug, title))
        rows_html.append(f'<h2 class="dsec" id="d-{esc(slug)}" data-domain="{esc(slug)}">{esc(title)}</h2>')
        for row in doc["rows"]:
            counts[row["divergence"]] += 1
            exams.update(row.get("exam_tags") or [])
            seen = dt.date.fromisoformat(row["verified"])
            oldest = seen if oldest is None or seen < oldest else oldest
            rows_html.append(render_row(row, slug))

    terms_html = "".join(render_term(t) for t in sorted(terms, key=lambda t: ({"high": 0, "medium": 1, "low": 2}[t["severity"]], t["term"])))

    total = sum(counts.values())
    risky = counts["partial"] + counts["none"]
    pct = round(100 * risky / total) if total else 0

    dchips = "".join(
        f'<button class="chip" data-filter="domain" data-value="{esc(s)}">{esc(t)}</button>'
        for s, t in domain_chips
    )
    echips = "".join(
        f'<button class="chip mono" data-filter="exam" data-value="{esc(e)}">{esc(e)}</button>'
        for e in sorted(exams)
    )

    subs = {
        "ROWS": "\n".join(rows_html),
        "TERMS": terms_html,
        "DCHIPS": dchips,
        "ECHIPS": echips,
        "TOTAL": str(total),
        "RISKY": str(risky),
        "PCT": str(pct),
        "NTERMS": str(len(terms)),
        "EXACT": str(counts["exact"]),
        "PARTIAL": str(counts["partial"]),
        "NONE": str(counts["none"]),
        "DIAGRAM": HIERARCHY_SVG,
        "OLDEST": oldest.isoformat() if oldest else "",
        "BUILT": dt.date.today().isoformat(),
    }
    page = PAGE
    for key, value in subs.items():
        page = page.replace("{{" + key + "}}", value)
    if "{{" in page:
        leftover = page[page.index("{{"): page.index("{{") + 40]
        raise SystemExit(f"unreplaced template token near: {leftover!r}")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")

    chapter = ROOT / "docs" / "09-confusing-terms.md"
    chapter.write_text(render_terms_markdown(terms), encoding="utf-8")

    # Every other reading surface, from the same data. The README is the one that
    # matters most: on GitHub it is where people arrive and decide to star.
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    surfaces.splice_readme(ROOT / "README.md", surfaces.readme_block(domains, terms))
    (dist / "poster.svg").write_text(surfaces.poster_svg(domains, terms), encoding="utf-8")
    (dist / "drills.tsv").write_text(surfaces.drills_tsv(domains, terms), encoding="utf-8")
    (dist / "rosetta.json").write_text(surfaces.dataset_json(domains, terms), encoding="utf-8")
    (ROOT / "docs" / "hierarchy-diagram.md").write_text(
        "# Hierarchy Diagram\n\nGenerated. GitHub renders this natively.\n\n"
        + surfaces.mermaid_hierarchy() + "\n",
        encoding="utf-8",
    )

    drill_lines = (dist / "drills.tsv").read_text().count(chr(10))
    print(f"wrote {out.relative_to(ROOT)}  {total} rows, {len(terms)} terms, {risky} flagged ({pct}%)")
    print(f"wrote {chapter.relative_to(ROOT)}")
    print(f"wrote README.md generated block, dist/poster.svg, dist/rosetta.json")
    print(f"wrote dist/drills.tsv  {drill_lines} flashcards")


PAGE = pathlib.Path(__file__).with_name("template.html").read_text(encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default=str(ROOT / "site" / "index.html"))
    args = ap.parse_args()
    build(pathlib.Path(args.out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
