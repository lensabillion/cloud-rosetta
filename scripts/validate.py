#!/usr/bin/env python3
"""Validate the Cloud Rosetta dataset.

Beyond schema conformance this enforces the rule the whole project rests on: a row
that does not claim an exact match must say what breaks. Without that check the
dataset degrades into another name table, which is what every predecessor became.

Usage: python scripts/validate.py [--max-age-days N]
Exit code 0 if the data is publishable, 1 otherwise.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import re
import sys

import yaml
from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CLOUDS = ("aws", "azure", "gcp")

# Rows older than this are reported but do not fail the build. Rows older than
# STALE_FAIL_DAYS do fail, because silently stale data was the main weakness
# found in every competing project.
STALE_WARN_DAYS = 180
STALE_FAIL_DAYS = 540


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"{where}: {msg}")


def load(path: pathlib.Path):
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def check_schema(doc, schema, where: str, rep: Report) -> None:
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(doc), key=lambda e: list(e.path)):
        loc = "/".join(str(p) for p in err.path) or "(root)"
        rep.error(where, f"{loc}: {err.message}")


def check_age(value: str, where: str, rep: Report, today: dt.date) -> None:
    try:
        seen = dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        rep.error(where, f"verified is not an ISO date: {value!r}")
        return
    if seen > today:
        rep.error(where, f"verified date is in the future: {value}")
        return
    age = (today - seen).days
    if age > STALE_FAIL_DAYS:
        rep.error(where, f"last verified {age} days ago, over the {STALE_FAIL_DAYS} day limit")
    elif age > STALE_WARN_DAYS:
        rep.warn(where, f"last verified {age} days ago, due for a recheck")


def exam_registry() -> tuple[set[str], set[str]]:
    path = DATA / "exams.yml"
    if not path.exists():
        return set(), set()
    exams = (load(path) or {}).get("exams") or []
    return ({e["code"] for e in exams},
            {e["code"] for e in exams if e.get("status") == "current"})


def validate_mappings(rep: Report, today: dt.date) -> int:
    schema = json.loads((DATA / "schema" / "mapping.schema.json").read_text())
    known, current = exam_registry()
    seen_ids: dict[str, str] = {}
    count = 0

    for path in sorted((DATA / "mappings").glob("*.yml")):
        rel = path.relative_to(ROOT)
        doc = load(path)
        check_schema(doc, schema, str(rel), rep)
        if not isinstance(doc, dict):
            continue

        if doc.get("domain") != path.stem:
            rep.error(str(rel), f"domain {doc.get('domain')!r} does not match filename stem {path.stem!r}")

        for row in doc.get("rows") or []:
            if not isinstance(row, dict):
                continue
            count += 1
            rid = row.get("id", "<missing id>")
            where = f"{rel}#{rid}"

            if rid in seen_ids:
                rep.error(where, f"duplicate id, already used in {seen_ids[rid]}")
            else:
                seen_ids[rid] = str(rel)

            divergence = row.get("divergence")
            breaks = (row.get("breaks_when") or "").strip()

            # The rule that makes this dataset different from its predecessors.
            if divergence in ("partial", "none") and not breaks:
                rep.error(
                    where,
                    f"divergence is {divergence!r} but breaks_when is empty. "
                    "A row that does not claim an exact match must say what breaks.",
                )
            if divergence == "exact" and breaks:
                rep.warn(where, "divergence is exact but breaks_when is populated; is it really exact?")

            named = [c for c in CLOUDS if (row.get(c) or {}).get("name")]
            if not named:
                rep.error(where, "no cloud has a name; the row describes nothing")
            if len(named) == 1 and divergence != "none":
                rep.error(
                    where,
                    f"only {named[0]} has an equivalent, so divergence should be 'none', not {divergence!r}",
                )

            for cloud in CLOUDS:
                block = row.get(cloud) or {}
                if block.get("name") is None and not block.get("note"):
                    rep.warn(f"{where}.{cloud}", "no equivalent and no note explaining what to do instead")

            # A tag is a promise that studying this helps for that exam. Offering a
            # retired exam as a live filter breaks that promise silently.
            for tag in row.get("exam_tags") or []:
                if known and tag not in known:
                    rep.error(f"{where}.exam_tags", f"{tag!r} is not in data/exams.yml")
                elif current and tag in known and tag not in current:
                    rep.error(f"{where}.exam_tags", f"{tag!r} names a retired exam; remove it or move it to a historical view")

            check_age(row.get("verified", ""), where, rep, today)

    return count


def validate_terms(rep: Report, today: dt.date) -> int:
    schema = json.loads((DATA / "schema" / "term.schema.json").read_text())
    count = 0
    seen: set[str] = set()

    for path in sorted((DATA / "terms").glob("*.yml")):
        rel = path.relative_to(ROOT)
        doc = load(path)
        check_schema(doc, schema, str(rel), rep)
        if not isinstance(doc, dict):
            continue

        for term in doc.get("terms") or []:
            if not isinstance(term, dict):
                continue
            count += 1
            name = term.get("term", "<missing>")
            where = f"{rel}#{name}"

            key = name.strip().lower()
            if key in seen:
                rep.error(where, "duplicate term")
            seen.add(key)

            senses = [c for c in CLOUDS if term.get(c)]
            if len(senses) < 2:
                rep.error(where, "a false friend needs at least two clouds to collide")

            if term.get("severity") == "high":
                cats = {(term[c] or {}).get("category") for c in senses}
                if len(cats) < 2:
                    rep.error(
                        where,
                        "severity is 'high' but every cloud has the same category; "
                        "high means the word denotes different kinds of thing",
                    )

            check_age(term.get("verified", ""), where, rep, today)

    return count


def validate_exams(rep: Report, today: dt.date) -> int:
    path = DATA / "exams.yml"
    if not path.exists():
        return 0
    schema = json.loads((DATA / "schema" / "exam.schema.json").read_text())
    doc = load(path)
    rel = path.relative_to(ROOT)
    check_schema(doc, schema, str(rel), rep)

    seen = set()
    for exam in (doc or {}).get("exams") or []:
        code = exam.get("code", "<missing>")
        where = f"{rel}#{code}"
        if code in seen:
            rep.error(where, "duplicate exam code")
        seen.add(code)
        # A shared index page is not evidence about one exam. F03 asked for
        # per-exam official links and this is what enforces it.
        if exam.get("url", "").rstrip("/").endswith("aws-certification-exam-guides.html"):
            rep.error(where, "cites the shared exam-guides index rather than this exam's own page")
        check_age(exam.get("verified", ""), where, rep, today)
    return len(seen)


def check_doc_links(rep: Report) -> int:
    """Markdown chapters that link to files which do not exist."""
    docs = ROOT / "docs"
    total = 0
    for path in sorted(docs.rglob("*.md")):
        for target in re.findall(r"\]\(([^)#:]+\.md)(?:#[^)]*)?\)", path.read_text(encoding="utf-8")):
            total += 1
            if not (path.parent / target).resolve().exists():
                rep.error(str(path.relative_to(ROOT)), f"links to a file that does not exist: {target}")
    return total


def check_house_style(rep: Report) -> None:
    """The dataset must be in the shape scripts/fmt.py emits, so that a diff
    shows what changed rather than how it was serialised."""
    import fmt as formatter
    for path, render in formatter.targets():
        original = path.read_text(encoding="utf-8")
        if render(yaml.safe_load(original)) != original:
            rep.error(str(path.relative_to(ROOT)), "not in house style. Run: python scripts/fmt.py")


def check_links_wellformed(rep: Report) -> int:
    """Shape check only. Reaching the network is the job of the link-check workflow."""
    pattern = re.compile(r"https?://[^\s\"'<>)\]]+")
    total = 0
    for path in sorted(DATA.rglob("*.yml")):
        text = path.read_text(encoding="utf-8")
        for url in pattern.findall(text):
            total += 1
            if url.startswith("http://"):
                rep.warn(str(path.relative_to(ROOT)), f"insecure http link: {url}")
            if "docs.microsoft.com" in url:
                rep.error(
                    str(path.relative_to(ROOT)),
                    f"docs.microsoft.com is retired and redirects; use learn.microsoft.com: {url}",
                )
    return total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--today", default=None, help="Override today's date, ISO format, for testing.")
    args = parser.parse_args()
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()

    rep = Report()
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    rows = validate_mappings(rep, today)
    terms = validate_terms(rep, today)
    exams = validate_exams(rep, today)
    links = check_links_wellformed(rep)
    doclinks = check_doc_links(rep)
    check_house_style(rep)

    print(f"Cloud Rosetta data check   {rows} mapping rows, {terms} terms, "
          f"{exams} exams, {links} links, {doclinks} chapter links")
    print("-" * 68)

    for w in rep.warnings:
        print(f"  warn   {w}")
    for e in rep.errors:
        print(f"  ERROR  {e}")

    print("-" * 68)
    if rep.errors:
        print(f"FAILED   {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
        return 1
    print(f"PASSED   0 errors, {len(rep.warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
