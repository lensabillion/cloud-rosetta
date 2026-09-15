#!/usr/bin/env python3
"""Fail the build when the design is bypassed.

data/design.yml is the single source for every colour, size and spacing value.
Nothing enforced that until this check existed, and the drawings had already
drifted to a previous palette without anyone noticing.

Usage: python scripts/check_design.py
Exit 0 if every visual value comes from the token file, 1 otherwise.
"""

from __future__ import annotations

import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "design.yml"

COLOUR = re.compile(r"#[0-9A-Fa-f]{3,8}\b|\b(?:rgb|hsl)a?\(")
CSS_SIZE = re.compile(r"font-size:\s*([0-9.]+)(px|rem|em)")
SVG_SIZE = re.compile(r'font-size="([0-9.]+)"')


def known_colours(doc: dict) -> set[str]:
    out = set()
    for group in ("light", "dark"):
        out |= {v.upper() for v in doc["colour"][group].values()}
    out |= {v.upper() for v in doc.get("palette_extra", {}).values()}
    return out


def main() -> int:
    doc = yaml.safe_load(SOURCE.read_text(encoding="utf-8"))
    allowed = known_colours(doc)
    scale = {v for v in doc["type"]["scale"].values()}
    errors: list[str] = []

    # 1. The page stylesheet may not contain a literal colour or size at all.
    shell = ROOT / "scripts" / "shell.html"
    text = shell.read_text(encoding="utf-8")
    body = text.split("{{TOKENS}}", 1)[-1]
    for hit in COLOUR.findall(body) or []:
        errors.append(f"{shell.relative_to(ROOT)}: literal colour. Use var(--token) and define it in data/design.yml")
        break
    for value, unit in CSS_SIZE.findall(body):
        errors.append(
            f"{shell.relative_to(ROOT)}: font-size:{value}{unit} is a literal. "
            f"Use one of {', '.join(sorted(scale))} through var(--t-*)"
        )

    # 2. Generated drawings may inline colours, because a standalone SVG cannot
    #    read CSS custom properties, but every value must still be a token.
    for path in [ROOT / "scripts" / "diagrams.py", ROOT / "scripts" / "surfaces.py", ROOT / "scripts" / "architecture_art.py"]:
        src = path.read_text(encoding="utf-8")
        for hit in re.findall(r"#[0-9A-Fa-f]{6}", src):
            if hit.upper() not in allowed:
                errors.append(f"{path.relative_to(ROOT)}: {hit} is not a value in data/design.yml")

    # 3. Drawn text respects the interface floor. Checked against the generated
    #    drawings, not the source, because a size can reach the output through a
    #    helper's default without appearing as a literal anywhere.
    floor = float(str(doc["type"]["scale"]["t-label"]).rstrip("px"))
    drawings = sorted((ROOT / "site" / "assets" / "architecture").glob("*.svg"))
    poster = ROOT / "dist" / "poster.svg"
    if poster.exists():
        drawings.append(poster)
    for svg in drawings:
        for s in sorted({s for s in SVG_SIZE.findall(svg.read_text(encoding="utf-8"))}):
            if float(s) < floor:
                errors.append(f"{svg.relative_to(ROOT)}: drawn text at {s}px is below the {floor:.0f}px floor")

    # 4. Labels inside a drawing must not sit on top of one another. Widths are
    #    estimated from an average advance of 0.55em, so this catches gross
    #    collisions rather than hairline touches; the exact test needs a browser.
    figures = overlaps = 0
    for svg in sorted((ROOT / "site" / "assets" / "architecture").glob("*.svg")):
        figures += 1
        body = svg.read_text(encoding="utf-8")
        boxes = []
        for m in re.finditer(r"<text\b([^>]*)>([^<]*)<", body):
            attrs, label = m.group(1), m.group(2).strip()
            if not label:
                continue
            def num(name, default=None):
                hit = re.search(rf'{name}="([-0-9.]+)"', attrs)
                return float(hit.group(1)) if hit else default
            x, y = num("x"), num("y")
            size = num("font-size", 14.0)
            if x is None or y is None:
                continue
            w, h = len(label) * size * 0.52, size
            anchor = re.search(r'text-anchor="(\w+)"', attrs)
            anchor = anchor.group(1) if anchor else "start"
            if anchor == "middle":
                x -= w / 2
            elif anchor == "end":
                x -= w
            # a baseline sits near the bottom of the glyph box
            boxes.append((x, y - size * 0.78, w, h, label[:20]))
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                ax, ay, aw, ah, al = boxes[i]
                bx, by, bw, bh, bl = boxes[j]
                if ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah:
                    overlaps += 1
                    if overlaps <= 5:
                        errors.append(f"{svg.relative_to(ROOT)}: labels overlap, {al!r} and {bl!r}")

    print(f"Design check   {len(allowed)} known colours, {len(scale)} sizes, "
          f"{figures} drawings checked for label collisions")
    print("-" * 68)
    for e in errors:
        print(f"  ERROR  {e}")
    print("-" * 68)
    if errors:
        print(f"FAILED   {len(errors)} value(s) bypass data/design.yml")
        return 1
    print("PASSED   every visual value comes from data/design.yml")
    return 0


if __name__ == "__main__":
    sys.exit(main())
