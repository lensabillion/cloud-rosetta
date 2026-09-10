#!/usr/bin/env python3
"""A small Markdown renderer for the subset this guide actually uses.

Rendering happens at build time so the site needs no client-side Markdown
library, and so a chapter and its rendered page cannot drift.

Supported: ATX headings, paragraphs, fenced code, bullet and ordered lists,
tables, blockquotes, horizontal rules, inline code, bold, italic, links, and
HTML comments (dropped). Anything outside that is passed through escaped.
"""

from __future__ import annotations

import html
import re

_INLINE_CODE = re.compile(r"`([^`]+)`")
_LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
_BOLD = re.compile(r"\*\*([^*]+)\*\*")
_ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")


def inline(text: str) -> str:
    """Escape first, then re-introduce the few tags we allow."""
    out = html.escape(text, quote=False)
    slots: list[str] = []

    def stash(markup: str) -> str:
        slots.append(markup)
        return f"\x00{len(slots) - 1}\x00"

    out = _INLINE_CODE.sub(lambda m: stash(f"<code>{m.group(1)}</code>"), out)
    out = _LINK.sub(lambda m: stash(_link(m.group(1), m.group(2))), out)
    out = _BOLD.sub(lambda m: f"<strong>{m.group(1)}</strong>", out)
    out = _ITALIC.sub(lambda m: f"<em>{m.group(1)}</em>", out)
    return re.sub(r"\x00(\d+)\x00", lambda m: slots[int(m.group(1))], out)


# site.py installs a resolver so a chapter link can become an in-page route when
# that chapter is a page, and a link to the repository when it is not.
RESOLVE = None


def _link(label: str, href: str) -> str:
    external = href.startswith(("http://", "https://"))
    if href.endswith(".md"):
        stem = href.rsplit("/", 1)[-1][:-3]
        href = RESOLVE(stem) if RESOLVE else "#" + stem
        external = href.startswith(("http://", "https://"))
    rel = ' target="_blank" rel="noopener"' if external else ""
    return f'<a href="{html.escape(href, quote=True)}"{rel}>{label}</a>'


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def render(md: str) -> tuple[str, list[tuple[int, str, str]]]:
    """Return (html, outline) where outline is a list of (level, id, text)."""
    lines = md.replace("\r\n", "\n").split("\n")
    out: list[str] = []
    outline: list[tuple[int, str, str]] = []
    i, n = 0, len(lines)

    while i < n:
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        if line.startswith("<!--"):
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            continue

        if line.startswith("```"):
            lang = line[3:].strip()
            i += 1
            buf: list[str] = []
            while i < n and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            cls = f' class="lang-{html.escape(lang, quote=True)}"' if lang else ""
            out.append(f"<pre{cls}><code>{html.escape(chr(10).join(buf), quote=False)}</code></pre>")
            continue

        if re.match(r"^(-{3,}|\*{3,})\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            ident = slug(text)
            if level >= 2:
                outline.append((level, ident, text))
            out.append(f'<h{level} id="{ident}">{inline(text)}</h{level}>')
            i += 1
            continue

        if line.lstrip().startswith("|") and i + 1 < n and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            head = _cells(line)
            i += 2
            body = []
            while i < n and lines[i].lstrip().startswith("|"):
                body.append(_cells(lines[i]))
                i += 1
            out.append(_table(head, body))
            continue

        if re.match(r"^\s*[-*]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
            ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            items: list[str] = []
            while i < n and (re.match(r"^\s*[-*]\s+", lines[i]) or re.match(r"^\s*\d+\.\s+", lines[i])):
                items.append(re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", lines[i]))
                i += 1
                # continuation lines belong to the item above
                while i < n and lines[i].startswith("  ") and lines[i].strip() and not re.match(r"^\s*(?:[-*]|\d+\.)\s+", lines[i]):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(t)}</li>" for t in items) + f"</{tag}>")
            continue

        if line.lstrip().startswith(">"):
            buf = []
            while i < n and lines[i].lstrip().startswith(">"):
                buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            out.append(f"<blockquote>{inline(' '.join(b for b in buf if b.strip()))}</blockquote>")
            continue

        buf = []
        while i < n and lines[i].strip() and not _breaks_paragraph(lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append(f"<p>{inline(' '.join(buf))}</p>")

    return "\n".join(out), outline


def _breaks_paragraph(line: str) -> bool:
    return (
        line.startswith(("#", "```", ">", "<!--"))
        or line.lstrip().startswith("|")
        or bool(re.match(r"^\s*[-*]\s+", line))
        or bool(re.match(r"^\s*\d+\.\s+", line))
        or bool(re.match(r"^(-{3,}|\*{3,})\s*$", line))
    )


def _cells(row: str) -> list[str]:
    return [c.strip() for c in row.strip().strip("|").split("|")]


def _table(head: list[str], body: list[list[str]]) -> str:
    ths = "".join(f"<th>{inline(c)}</th>" for c in head)
    trs = ""
    for row in body:
        row = (row + [""] * len(head))[: len(head)]
        trs += "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>"
    return f'<div class="tw"><table><thead><tr>{ths}</tr></thead><tbody>{trs}</tbody></table></div>'
