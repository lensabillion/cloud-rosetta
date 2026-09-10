#!/usr/bin/env python3
"""Write the dataset back in the project's house YAML style.

This exists because a generic YAML round-trip reformatted every mapping file,
producing 1,196 lines of diff for about 20 real changes and turning readable
folded blocks into wrapped quoted strings. Contributors edit this YAML by hand,
so its shape is part of the product.

Running this makes formatting reproducible instead of hand-maintained: edit the
data however you like, run the formatter, and the diff shows only what changed.

Usage:
  python scripts/fmt.py            rewrite the files in place
  python scripts/fmt.py --check    exit 1 if any file is not in house style
"""

from __future__ import annotations

import argparse
import pathlib
import sys
import textwrap

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
WIDTH = 96

ROW_ORDER = ["id", "concept", "divergence", "bite", "aws", "azure", "gcp",
             "breaks_when", "shared_trap", "exam_tags", "sources", "verified"]
PROVIDER_ORDER = ["name", "url", "formerly", "maturity", "note"]
TERM_ORDER = ["term", "severity", "aws", "azure", "gcp", "why_it_hurts", "see_also", "verified"]
SENSE_ORDER = ["meaning", "category", "url"]
CLOUDS = ("aws", "azure", "gcp")


def scalar(value) -> str:
    """Quote only where YAML needs it, so the common case stays clean."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value)
    # dates and anything that would otherwise parse as a non-string
    if text[:1].isdigit() and any(c in text for c in "-:") and " " not in text:
        return f"'{text}'"
    if text.strip() != text or text == "" or text[0] in "&*!|>%@`{[\"'" or ": " in text or text.endswith(":"):
        return "'" + text.replace("'", "''") + "'"
    return text


def folded(key: str, value: str, indent: str) -> list[str]:
    """A folded block, which is what makes long prose readable in a diff."""
    body = " ".join(str(value).split())
    # Never break on hyphens: that turns us-east-1a into "us- east-1a", which is a
    # data change disguised as formatting. Long tokens such as URLs stay whole.
    lines = textwrap.wrap(
        body, WIDTH - len(indent) - 2,
        break_on_hyphens=False, break_long_words=False,
    ) or [""]
    return [f"{indent}{key}: >-"] + [f"{indent}  {line}" for line in lines]


def flow_list(key: str, items: list, indent: str) -> list[str]:
    inline = f"{indent}{key}: [" + ", ".join(scalar(i) for i in items) + "]"
    if len(inline) <= WIDTH:
        return [inline]
    return [f"{indent}{key}:"] + [f"{indent}  - {scalar(i)}" for i in items]


def block_list(key: str, items: list, indent: str) -> list[str]:
    return [f"{indent}{key}:"] + [f"{indent}  - {scalar(i)}" for i in items]


def provider(key: str, block: dict, indent: str) -> list[str]:
    out = [f"{indent}{key}:"]
    inner = indent + "  "
    for field in PROVIDER_ORDER:
        if field not in block:
            continue
        value = block[field]
        if field == "formerly":
            out += flow_list(field, value, inner)
        elif field == "note":
            out += folded(field, value, inner) if len(str(value)) > WIDTH - len(inner) - 8 \
                else [f"{inner}{field}: {scalar(value)}"]
        else:
            out.append(f"{inner}{field}: {scalar(value)}")
    return out


def render_mapping(doc: dict) -> str:
    out = [f"domain: {scalar(doc['domain'])}"]
    if doc.get("title"):
        out.append(f"title: {scalar(doc['title'])}")
    out.append("rows:")

    for i, row in enumerate(doc["rows"]):
        if i:
            out.append("")
        first = True
        for field in ROW_ORDER:
            if field not in row:
                continue
            value = row[field]
            lead = "  - " if first else "    "
            indent = "    "
            if field in CLOUDS:
                lines = provider(field, value or {}, indent)
            elif field in ("breaks_when", "shared_trap"):
                lines = folded(field, value, indent)
            elif field == "exam_tags":
                lines = flow_list(field, value, indent)
            elif field == "sources":
                lines = block_list(field, value, indent)
            else:
                lines = [f"{indent}{field}: {scalar(value)}"]
            if first:
                lines[0] = lead + lines[0][len(indent):]
                first = False
            out += lines
        unknown = set(row) - set(ROW_ORDER)
        if unknown:
            raise SystemExit(f"unknown field(s) on {row.get('id')}: {sorted(unknown)}")
    return "\n".join(out) + "\n"


def render_terms(doc: dict) -> str:
    out = ["terms:"]
    for i, term in enumerate(doc["terms"]):
        if i:
            out.append("")
        first = True
        for field in TERM_ORDER:
            if field not in term:
                continue
            value = term[field]
            indent = "    "
            if field in CLOUDS:
                lines = [f"{indent}{field}:"]
                inner = indent + "  "
                for sub in SENSE_ORDER:
                    if sub not in value:
                        continue
                    if sub == "meaning":
                        lines += folded(sub, value[sub], inner)
                    else:
                        lines.append(f"{inner}{sub}: {scalar(value[sub])}")
            elif field == "why_it_hurts":
                lines = folded(field, value, indent)
            elif field == "see_also":
                lines = flow_list(field, value, indent)
            else:
                lines = [f"{indent}{field}: {scalar(value)}"]
            if first:
                lines[0] = "  - " + lines[0][len(indent):]
                first = False
            out += lines
        unknown = set(term) - set(TERM_ORDER)
        if unknown:
            raise SystemExit(f"unknown field(s) on term {term.get('term')}: {sorted(unknown)}")
    return "\n".join(out) + "\n"


def _normalise(node):
    if isinstance(node, str):
        return node.rstrip()
    if isinstance(node, dict):
        return {k: _normalise(v) for k, v in node.items()}
    if isinstance(node, list):
        return [_normalise(v) for v in node]
    return node


def targets() -> list[tuple[pathlib.Path, object]]:
    out = [(p, render_mapping) for p in sorted((DATA / "mappings").glob("*.yml"))]
    out += [(p, render_terms) for p in sorted((DATA / "terms").glob("*.yml"))]
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true", help="report drift instead of rewriting")
    args = ap.parse_args()

    drifted = []
    for path, render in targets():
        original = path.read_text(encoding="utf-8")
        data = yaml.safe_load(original)
        formatted = render(data)

        # The formatter may normalise trailing whitespace on strings. Any other
        # change to the parsed data is a bug, and we refuse rather than write it.
        if _normalise(yaml.safe_load(formatted)) != _normalise(data):
            raise SystemExit(f"{path.relative_to(ROOT)}: formatting changed the data. Refusing.")

        if formatted != original:
            drifted.append(path.relative_to(ROOT))
            if not args.check:
                path.write_text(formatted, encoding="utf-8")

    if args.check:
        for path in drifted:
            print(f"  not in house style: {path}")
        print(f"{len(drifted)} file(s) drifted" if drifted else "all files in house style")
        return 1 if drifted else 0

    for path in drifted:
        print(f"  formatted {path}")
    print(f"{len(drifted)} file(s) rewritten" if drifted else "nothing to do")
    return 0


if __name__ == "__main__":
    sys.exit(main())
