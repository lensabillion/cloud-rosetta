#!/usr/bin/env python3
"""Emit every reading surface from the one dataset.

HTML is not the primary surface. On GitHub the README is where people arrive,
read, and decide to star, so it has to carry real content rather than links to
content. This module generates that, plus the surfaces HTML cannot be:
a poster that travels in chat, a flashcard deck for revision, and JSON for
anyone who wants to build on the data.

Called by build.py. Not usually run directly.
"""

from __future__ import annotations

import csv
import datetime as dt
import io
import json
import pathlib

import design

CLOUDS = (("aws", "AWS"), ("azure", "Azure"), ("gcp", "Google Cloud"))
BITE_MARK = {"serious": "❗", "regular": "🔸", "tip": "🔹"}
GRADE_MARK = {"exact": "✅", "partial": "⚠️", "none": "❌"}


def latest_verification(domains: list[dict], terms: list[dict]) -> str:
    """Newest recorded source check, not a claim that every entry was rechecked."""
    dates = [str(row["verified"]) for doc in domains for row in doc["rows"]]
    dates.extend(str(term["verified"]) for term in terms)
    return max(dates)


def _name(row: dict, key: str) -> str:
    block = row.get(key) or {}
    name = block.get("name")
    if not name:
        return "*none*"
    url = block.get("url")
    label = f"**{name}**" if block.get("maturity") == "superseded" else name
    out = f"[{label}]({url})" if url else label
    if block.get("maturity") == "superseded":
        out += " ⚑"
    return out


# --------------------------------------------------------------------------- README

def readme_block(domains: list[dict], terms: list[dict]) -> str:
    """The generated middle of the README: real content, not a link to content."""
    rows = [r for d in domains for r in d["rows"]]
    serious = [r for r in rows if r.get("bite") == "serious"]

    out = [
        "<!-- BEGIN GENERATED. Edit data/, then run: python scripts/build.py -->",
        "",
        "## The Legend",
        "",
        "Two independent axes, because they answer different questions. Severity wording follows",
        "[og-aws](https://github.com/open-guides/og-aws), which defines it by consequence.",
        "",
        "| | How far the mapping transfers | | How badly it bites |",
        "| --- | --- | --- | --- |",
        "| ✅ | Similar purpose; verify configuration. | ❗ | Serious. Security risk, real money, or hard to undo. |",
        "| ⚠️ | Behaves differently in a way that changes answers. | 🔸 | Regular. It breaks, or it fails to scale. |",
        "| ❌ | Different object or architecture; read the caveat. | 🔹 | Tip. Often overlooked, nothing breaks. |",
        "",
        "Service lifecycle and exam coverage are separate; check official documentation.",
        "",
        f"## The {len(serious)} Differences That Will Actually Hurt You",
        "",
        "Filtered to ❗ only. This is the table to read if you read nothing else.",
        "",
        "| | Concept | AWS | Azure | Google Cloud |",
        "| --- | --- | --- | --- | --- |",
    ]

    for row in serious:
        out.append(
            f"| {GRADE_MARK[row['divergence']]} | **{row['concept']}** | "
            + " | ".join(_name(row, k) for k, _ in CLOUDS)
            + " |"
        )

    out += [
        "",
        "<details>",
        "<summary><b>Open for the conditions and caveats</b></summary>",
        "",
    ]
    for row in serious:
        note = " ".join(str(row.get("breaks_when") or row.get("shared_trap") or "").split())
        out.append(f"- **{row['concept']}.** {note}")
    out += ["", "</details>", ""]

    high = [t for t in terms if t["severity"] == "high"]
    out += [
        f"## {len(high)} Words That Mean Different Things",
        "",
        "Severity `high` means the clouds use the word for **different categories of object**,",
        "not merely for things that behave differently.",
        "",
        "| Word | AWS | Azure | Google Cloud |",
        "| --- | --- | --- | --- |",
    ]
    for term in high:
        cells = []
        for key, _ in CLOUDS:
            sense = term.get(key)
            cells.append(f"*{sense['category']}*" if sense else "—")
        out.append(f"| **{term['term']}** | " + " | ".join(cells) + " |")

    out += [
        "",
        "The full decoder, with what each one actually means and why it costs marks, is in",
        "[docs/09-confusing-terms.md](docs/09-confusing-terms.md).",
        "",
        "<!-- END GENERATED -->",
    ]
    return "\n".join(out)


def splice_readme(path: pathlib.Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    start = "<!-- BEGIN GENERATED"
    end = "<!-- END GENERATED -->"
    if start in text and end in text:
        head = text[: text.index(start)]
        tail = text[text.index(end) + len(end):]
        path.write_text(head + block + tail, encoding="utf-8")
    else:
        marker = "\n## Contributing"
        if marker in text:
            head, tail = text.split(marker, 1)
            path.write_text(head + block + "\n" + marker + tail, encoding="utf-8")
        else:
            path.write_text(text + "\n\n" + block + "\n", encoding="utf-8")


# --------------------------------------------------------------------------- Mermaid

# --------------------------------------------------------------------------- poster

def poster_svg(domains: list[dict], terms: list[dict]) -> str:
    """The whole service landscape on one sheet, graded.

    Cloud Product Mapping proved a poster travels where a site does not, and its
    weakness is that a name-to-name list cannot say where the mapping fails. This
    one carries every row in the dataset with its divergence on the left edge, so
    the eye finds the dangerous rows before it reads a word. Generated from the
    same YAML as everything else, so it cannot drift.
    """
    c = design.load()["colour"]["light"]
    ink, ink2, ink3 = c["ink"], c["ink2"], c["ink3"]
    hue = {"aws": c["aws"], "azure": c["azure"], "gcp": c["gcp"]}
    grade = {"exact": c["ink3"], "partial": c["fault"], "none": c["void"]}
    mark = {"exact": "", "partial": "!", "none": "X"}

    COLW, GUT, PAD = 760, 60, 52
    W = PAD * 2 + COLW * 2 + GUT
    LINE, ENTRY, HEAD, TOP = 20, 50, 46, 176

    order = [("hierarchy", "Resource hierarchy"), ("identity", "Identity and access"),
             ("networking", "Networking"), ("compute", "Compute and containers"),
             ("storage", "Storage"), ("databases", "Databases and analytics")]
    by = {d["domain"]: d for d in domains}
    groups = [(slug, title, by[slug]["rows"]) for slug, title in order if slug in by]

    # Pack each domain into whichever column is currently shorter. The first
    # attempt split on a running total and left one column half empty.
    heights = [HEAD + len(rows) * ENTRY + 10 for _, _, rows in groups]
    left, right, hl, hr = [], [], 0, 0
    for g, h in zip(groups, heights):
        if hl <= hr:
            left.append(g); hl += h
        else:
            right.append(g); hr += h
    colh = max(hl, hr)
    H = TOP + colh + 96

    p = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
         f'font-family="Lato, Helvetica, Arial, sans-serif">',
         f'<rect width="{W}" height="{H}" fill="{c["sheet"]}"/>']

    p.append(f'<text x="{PAD}" y="74" font-size="44" font-weight="900" fill="{ink}">Cloud Rosetta</text>')
    p.append(f'<text x="{PAD}" y="108" font-size="19" fill="{ink2}">Every service mapping, graded by how far the equivalence can be trusted.</text>')

    lx = PAD
    for label, colour, text in (("", grade["exact"], "safe to translate"),
                                ("!", grade["partial"], "behaves differently"),
                                ("X", grade["void" if False else "none"], "no honest equivalent")):
        p.append(f'<rect x="{lx}" y="132" width="4" height="18" fill="{colour}"/>')
        if label:
            p.append(f'<text x="{lx + 14}" y="147" font-size="14" font-weight="700" fill="{colour}">{label}</text>')
        p.append(f'<text x="{lx + (30 if label else 14)}" y="147" font-size="14" fill="{ink3}">{_x(text)}</text>')
        lx += 34 + len(text) * 7.4 + (16 if label else 0)
    p.append(f'<line x1="{PAD}" y1="{TOP - 24}" x2="{W - PAD}" y2="{TOP - 24}" stroke="{c["rule2"]}"/>')

    def draw(col, x0):
        y = TOP
        for _slug, title, rows in col:
            p.append(f'<text x="{x0}" y="{y + 16}" font-size="15" font-weight="900" '
                     f'letter-spacing="1.6" fill="{ink3}">{_x(title.upper())}</text>')
            p.append(f'<line x1="{x0}" y1="{y + 26}" x2="{x0 + COLW}" y2="{y + 26}" stroke="{c["rule"]}"/>')
            y += HEAD
            for r in rows:
                d = r.get("divergence", "exact")
                p.append(f'<rect x="{x0}" y="{y - 2}" width="3" height="{ENTRY - 12}" fill="{grade[d]}"/>')
                concept = r["concept"]
                p.append(f'<text x="{x0 + 14}" y="{y + 12}" font-size="15" font-weight="700" fill="{ink}">'
                         f'{_x(concept[:58])}</text>')
                if mark[d]:
                    p.append(f'<text x="{x0 + COLW}" y="{y + 12}" font-size="14" font-weight="900" '
                             f'text-anchor="end" fill="{grade[d]}">{mark[d]}</text>')
                # Fixed slots rather than estimated advance widths. Estimating is
                # how the first version collided seven labels: Lato is wider at
                # 14px than the estimate allowed.
                slot = (COLW - 14) / 3
                for i, (key, short) in enumerate((("aws", "AWS"), ("azure", "AZ"), ("gcp", "GC"))):
                    sx = x0 + 14 + i * slot
                    name = (r.get(key) or {}).get("name") or "none"
                    budget = int((slot - 56) / 7.6)
                    if len(name) > budget:
                        name = name[: budget - 1].rstrip(" ,") + "\u2026"
                    p.append(f'<text x="{sx}" y="{y + 12 + LINE}" font-size="14" font-weight="700" '
                             f'fill="{hue[key]}">{short}</text>')
                    p.append(f'<text x="{sx + 42}" y="{y + 12 + LINE}" font-size="14" '
                             f'fill="{ink2}">{_x(name)}</text>')
                y += ENTRY
            y += 10

    draw(left, PAD)
    draw(right, PAD + COLW + GUT)

    p.append(f'<line x1="{PAD}" y1="{H - 58}" x2="{W - PAD}" y2="{H - 58}" stroke="{c["rule2"]}"/>')
    # The date states when the data was last verified, not when this file happened
    # to be written. That makes the build deterministic and says something truer.
    checked = max((r.get("verified", "") for _, _, rows in groups for r in rows), default="")
    p.append(f'<text x="{PAD}" y="{H - 30}" font-size="14" fill="{ink3}">'
             f'{sum(len(r) for _, _, r in groups)} mappings &#183; newest verification {checked} '
             f'&#183; every claim links to vendor documentation in the guide &#183; CC BY 4.0</text>')
    p.append("</svg>")
    return "\n".join(p)


def _x(text: str) -> str:
    return (
        str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    )


# --------------------------------------------------------------------------- drills

def drills_tsv(domains: list[dict], terms: list[dict]) -> str:
    """Tab separated, front/back/tags. Imports straight into Anki.
    system-design-primer ships flashcards and names them in its description;
    for a certification guide the drill layer is the point, not a bonus."""
    buf = io.StringIO()
    writer = csv.writer(buf, delimiter="\t", quoting=csv.QUOTE_MINIMAL, lineterminator="\n")

    for domain in domains:
        for row in domain["rows"]:
            for key, label in CLOUDS:
                block = row.get(key) or {}
                if not block.get("name"):
                    continue
                others = [
                    f"{lbl}: {(row.get(k) or {}).get('name') or 'no equivalent'}"
                    for k, lbl in CLOUDS
                    if k != key
                ]
                writer.writerow([
                    f"{label} {block['name']} — compare the purpose and limits elsewhere.",
                    "; ".join(others) + " | Grade: " + row["divergence"]
                    + " | Caveat: " + " ".join(str(row.get("breaks_when") or row.get("shared_trap") or "Similar purpose does not imply identical limits or configuration.").split())
                    + " | Sources: " + ", ".join(row.get("sources") or [row[k]["url"] for k, _ in CLOUDS if row.get(k, {}).get("url")]),
                    f"{domain['domain']} mapping {row['divergence']}",
                ])
            if row.get("breaks_when"):
                writer.writerow([
                    f"{row['concept']} — where does the mapping break?",
                    " ".join(str(row["breaks_when"]).split()) + " | Sources: " + ", ".join(row.get("sources") or [row[k]["url"] for k, _ in CLOUDS if row.get(k, {}).get("url")]),
                    f"{domain['domain']} gotcha {row.get('bite','')}",
                ])

    for term in terms:
        senses = [f"{lbl}: {term[k]['category']}" for k, lbl in CLOUDS if term.get(k)]
        writer.writerow([
            f'"{term["term"]}" — what does it mean in each cloud?',
            "; ".join(senses) + " || " + " ".join(str(term["why_it_hurts"]).split())
            + " | Sources: " + ", ".join(term[k]["url"] for k, _ in CLOUDS if term.get(k, {}).get("url")),
            f"decoder {term['severity']}",
        ])

    return buf.getvalue()


# --------------------------------------------------------------------------- json

def dataset_json(domains: list[dict], terms: list[dict]) -> str:
    return json.dumps(
        {
            "latest_source_verification": latest_verification(domains, terms),
            "licence": "CC BY 4.0",
            "mappings": [dict(r, domain=d["domain"]) for d in domains for r in d["rows"]],
            "terms": terms,
        },
        indent=2,
        ensure_ascii=False,
    )


# --------------------------------------------------------------------------- exams

LEVELS = ["foundational", "associate", "professional", "expert", "specialty"]
PROVIDER_NAME = {"aws": "AWS", "azure": "Azure", "gcp": "Google Cloud"}


def exams_block(exams: list[dict]) -> str:
    """The exam table, generated from the registry so a retirement is recorded once.

    An exam retiring and a product retiring are separate events; the registry
    tracks only the exam, and retired entries stay listed rather than vanishing,
    because course material still sells them.
    """
    current = [e for e in exams if e["status"] == "current"]
    retired = [e for e in exams if e["status"] != "current"]

    out = ["<!-- BEGIN EXAMS. Generated from data/exams.yml by scripts/build.py -->", ""]
    out += [f"## Current Exams ({len(current)})", ""]

    for provider in ("aws", "azure", "gcp"):
        rows = [e for e in current if e["provider"] == provider]
        if not rows:
            continue
        rows.sort(key=lambda e: (LEVELS.index(e["level"]), e["code"]))
        out += [f"### {PROVIDER_NAME[provider]}", "",
                "| Code | Certification | Level | Verified |", "| --- | --- | --- | --- |"]
        for e in rows:
            out.append(f"| `{e['code']}` | [{e['name']}]({e['url']}) | {e['level']} | {e['verified']} |")
        out.append("")

    out += [f"## Retired ({len(retired)})", "",
            "Listed rather than deleted, because course material for them is still on sale.", "",
            "| Code | Certification | Cloud | Note |", "| --- | --- | --- | --- |"]
    for e in sorted(retired, key=lambda e: e["code"]):
        note = " ".join(str(e.get("note", "Retired.")).split())
        out.append(f"| `{e['code']}` | [{e['name']}]({e['url']}) | {PROVIDER_NAME[e['provider']]} | {note} |")

    out += ["", "<!-- END EXAMS -->"]
    return "\n".join(out)


def splice_exams(path: pathlib.Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    start, end = "<!-- BEGIN EXAMS", "<!-- END EXAMS -->"
    if start not in text or end not in text:
        raise SystemExit(f"{path}: missing BEGIN/END EXAMS markers")
    head = text[: text.index(start)]
    tail = text[text.index(end) + len(end):]
    path.write_text(head + block + tail, encoding="utf-8")
