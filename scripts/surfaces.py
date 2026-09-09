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

CLOUDS = (("aws", "AWS"), ("azure", "Azure"), ("gcp", "Google Cloud"))
BITE_MARK = {"serious": "❗", "regular": "🔸", "tip": "🔹"}
GRADE_MARK = {"exact": "✅", "partial": "⚠️", "none": "❌"}


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
        "| ✅ | Close equivalent. Learn it once. | ❗ | Serious. Security risk, real money, or hard to undo. |",
        "| ⚠️ | Behaves differently in a way that changes answers. | 🔸 | Regular. It breaks, or it fails to scale. |",
        "| ❌ | No honest equivalent. Do not translate. | 🔹 | Tip. Often overlooked, nothing breaks. |",
        "",
        "⚑ marks a product its vendor has superseded. Do not learn it for a current exam.",
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
        "<summary><b>Open for what breaks in each of those, in one line</b></summary>",
        "",
    ]
    for row in serious:
        note = " ".join(str(row.get("breaks_when") or row.get("shared_trap") or "").split())
        first = note.split(". ")[0].rstrip(".") + "." if note else ""
        out.append(f"- **{row['concept']}.** {first}")
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

def mermaid_hierarchy() -> str:
    """GitHub renders Mermaid natively, so the diagram works inside Markdown."""
    return """```mermaid
flowchart TB
  subgraph AWS
    direction TB
    A1[Organization] --> A2[Organizational unit]
    A2 --> A3["Account<br/><i>isolation + billing + identity</i>"]
    A3 --> A4[Region]
    A4 --> A5["VPC<br/><i>regional</i>"]
    A5 --> A6[Availability Zone]
    A6 --> A7["Subnet<br/><i>lives in one zone</i>"]
  end
  subgraph Azure
    direction TB
    B1[Entra ID tenant] --> B2[Management group]
    B2 --> B3["Subscription<br/><i>billing boundary</i>"]
    B3 --> B4["Resource group<br/><i>mandatory, deletes contents</i>"]
    B4 --> B5["Virtual network<br/><i>regional</i>"]
    B5 --> B6["Subnet<br/><i>regional, spans zones</i>"]
  end
  subgraph GoogleCloud["Google Cloud"]
    direction TB
    C1[Organization] --> C2[Folder]
    C2 --> C3["Project<br/><i>isolation boundary</i>"]
    C3 --> C4[Region]
    C4 --> C5["Subnet<br/><i>regional</i>"]
    C3 -.-> C6["VPC network<br/><i>GLOBAL, outside any region</i>"]
    C6 -.-> C5
  end
```"""


# --------------------------------------------------------------------------- poster

def poster_svg(domains: list[dict], terms: list[dict]) -> str:
    """One shareable image. Cloud Product Mapping proved a poster travels where a
    site does not; generating it from the data means it can never drift."""
    rows = [r for d in domains for r in d["rows"] if r.get("bite") == "serious"]
    high = [t for t in terms if t["severity"] == "high"][:7]

    W, H = 1200, 1500
    y = 0
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="Roboto, Helvetica, Arial, sans-serif">',
        f'<rect width="{W}" height="{H}" fill="#16211F"/>',
        '<text x="56" y="86" fill="#FBFBF9" font-size="52" font-weight="900" letter-spacing="-1.6">Cloud Rosetta</text>',
        '<text x="56" y="122" fill="#93A6A1" font-size="19">What breaks when you assume AWS, Azure and Google Cloud work the same way.</text>',
        '<line x1="56" y1="148" x2="1144" y2="148" stroke="#334742"/>',
        '<text x="56" y="184" fill="#E5A057" font-size="14" font-weight="700" letter-spacing="2.6">THE DIFFERENCES THAT ACTUALLY HURT</text>',
    ]

    cols = (56, 420, 700, 950)
    parts += [
        f'<text x="{cols[1]}" y="216" fill="#E0A05B" font-size="12" font-weight="700" letter-spacing="2">AWS</text>',
        f'<text x="{cols[2]}" y="216" fill="#77B4E4" font-size="12" font-weight="700" letter-spacing="2">AZURE</text>',
        f'<text x="{cols[3]}" y="216" fill="#6DC195" font-size="12" font-weight="700" letter-spacing="2">GOOGLE CLOUD</text>',
    ]

    y = 240
    for row in rows[:14]:
        parts.append(f'<line x1="56" y1="{y - 14}" x2="1144" y2="{y - 14}" stroke="#243733"/>')
        concept = row["concept"][:44]
        parts.append(f'<text x="{cols[0]}" y="{y + 6}" fill="#EDF2EF" font-size="15" font-weight="500">{_x(concept)}</text>')
        for (key, _), cx in zip(CLOUDS, cols[1:]):
            nm = (row.get(key) or {}).get("name") or "no equivalent"
            parts.append(f'<text x="{cx}" y="{y + 6}" fill="#B9C8C4" font-size="13">{_x(nm[:30])}</text>')
        y += 40

    y += 26
    parts += [
        f'<line x1="56" y1="{y - 24}" x2="1144" y2="{y - 24}" stroke="#334742"/>',
        f'<text x="56" y="{y + 6}" fill="#E28C82" font-size="14" font-weight="700" letter-spacing="2.6">SAME WORD, DIFFERENT KIND OF THING</text>',
    ]
    y += 44
    for term in high:
        parts.append(f'<text x="{cols[0]}" y="{y}" fill="#EDF2EF" font-size="16" font-weight="700">{_x(term["term"])}</text>')
        for (key, _), cx in zip(CLOUDS, cols[1:]):
            sense = term.get(key)
            cat = sense["category"] if sense else "—"
            parts.append(f'<text x="{cx}" y="{y}" fill="#B9C8C4" font-size="13" font-style="italic">{_x(cat[:30])}</text>')
        y += 38

    parts += [
        f'<line x1="56" y1="{H - 66}" x2="1144" y2="{H - 66}" stroke="#334742"/>',
        f'<text x="56" y="{H - 36}" fill="#93A6A1" font-size="13">github.com — Cloud Rosetta &#183; generated from the dataset on {dt.date.today().isoformat()} &#183; CC BY 4.0</text>',
        "</svg>",
    ]
    return "\n".join(parts)


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
                    f"{label} {block['name']} — what is the equivalent elsewhere?",
                    "; ".join(others),
                    f"{domain['domain']} mapping {row['divergence']}",
                ])
            if row.get("breaks_when"):
                writer.writerow([
                    f"{row['concept']} — where does the mapping break?",
                    " ".join(str(row["breaks_when"]).split()),
                    f"{domain['domain']} gotcha {row.get('bite','')}",
                ])

    for term in terms:
        senses = [f"{lbl}: {term[k]['category']}" for k, lbl in CLOUDS if term.get(k)]
        writer.writerow([
            f'"{term["term"]}" — what does it mean in each cloud?',
            "; ".join(senses) + " || " + " ".join(str(term["why_it_hurts"]).split()),
            f"decoder {term['severity']}",
        ])

    return buf.getvalue()


# --------------------------------------------------------------------------- json

def dataset_json(domains: list[dict], terms: list[dict]) -> str:
    return json.dumps(
        {
            "generated": dt.date.today().isoformat(),
            "licence": "CC BY 4.0",
            "mappings": [dict(r, domain=d["domain"]) for d in domains for r in d["rows"]],
            "terms": terms,
        },
        indent=2,
        ensure_ascii=False,
    )
