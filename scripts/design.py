#!/usr/bin/env python3
"""The one place the design is turned into CSS and into a page.

`data/design.yml` holds every colour, size and spacing value. This module emits
the :root custom properties the built page uses, and renders the Design page
that shows those same tokens in use. Both read the same file, so the page cannot
describe a design the site is not running.
"""

from __future__ import annotations

import html
import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SOURCE = ROOT / "data" / "design.yml"


def load() -> dict:
    return yaml.safe_load(SOURCE.read_text(encoding="utf-8"))


def esc(v) -> str:
    return html.escape(str(v if v is not None else ""), quote=True)


def _vars(pairs: dict, indent: str = "  ") -> str:
    return "\n".join(f"{indent}--{k}:{v};" for k, v in pairs.items())


def css(d: dict) -> str:
    """The :root block, plus both theme overrides, from the token file."""
    light, dark = d["colour"]["light"], d["colour"]["dark"]
    base = {**d["type"]["scale"], **d["type"]["leading"], **d["layout"],
            **{k: v for k, v in d["fonts"]["stacks"].items()}}
    return (
        "/* Generated from data/design.yml by scripts/design.py. Do not edit here. */\n"
        ":root{\n" + _vars(light) + "\n" + _vars(base) + "\n}\n"
        "@media (prefers-color-scheme:dark){\n  :root:not([data-theme=\"light\"]){\n"
        + _vars(dark, "    ") + "\n  }\n}\n"
        ':root[data-theme="dark"]{\n' + _vars(dark) + "\n}"
    )


def font_link(d: dict) -> str:
    return ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{d["fonts"]["google"]}&display=swap">')


# ------------------------------------------------------------------ the page

def _swatches(title: str, pairs: dict, note: str = "") -> str:
    cells = "".join(
        f'<div class="sw"><span class="chip" style="background:{esc(v)}"></span>'
        f'<b>--{esc(k)}</b><code>{esc(v)}</code></div>' for k, v in pairs.items())
    n = f"<p>{esc(note)}</p>" if note else ""
    return f"<h3>{esc(title)}</h3>{n}<div class=\"swatches\">{cells}</div>"


def page(d: dict) -> str:
    scale, leading, layout = d["type"]["scale"], d["type"]["leading"], d["layout"]
    light = d["colour"]["light"]

    roles = {
        "Headings": "ink", "Running text": "ink2", "Secondary text": "ink3",
        "Links": "link", "Primary action": "accent", "Hairlines": "rule",
    }
    role_rows = "".join(
        f"<tr><td>{esc(r)}</td><td><code>--{esc(t)}</code></td>"
        f'<td><span class="chip sm" style="background:{esc(light[t])}"></span> '
        f"<code>{esc(light[t])}</code></td></tr>" for r, t in roles.items())

    specimen = "".join(
        f'<div class="spec"><span class="lbl"><code>--{esc(k)}</code> {esc(v)}</span>'
        f'<span style="font-size:{esc(v)};line-height:{esc(leading["lh-head"] if i < 3 else leading["lh-body"])}">'
        f"The same idea, three different shapes</span></div>"
        for i, (k, v) in enumerate(scale.items()))

    providers = _swatches("Provider identity", {k: light[k] for k in ("aws", "azure", "gcp")},
                          "One hue per cloud, used identically in every table, diagram and card. "
                          "Never used for anything else.")
    severity = _swatches("Severity", {k: light[k] for k in ("fault", "void", "calm")},
                         "Always paired with a word or a mark, so the grading survives greyscale "
                         "and colour vision deficiency.")
    extra = _swatches("Accents", d["palette_extra"],
                      "From the source palette. Accent use only, never body text or large areas.")

    layout_rows = "".join(f"<tr><td><code>--{esc(k)}</code></td><td>{esc(v)}</td></tr>"
                          for k, v in layout.items())

    dev = "".join(
        f'<div class="dev"><b>{esc(x["what"])}</b><p>{esc(" ".join(str(x["why"]).split()))}</p></div>'
        for x in d["deviations"])

    return f"""<section class="page hide" id="p-design">
<p class="eyebrow">Design</p>
<h1>The design system</h1>
<p>Every colour, size and spacing value in this guide comes from one file,
<code>data/design.yml</code>. This page is generated from that same file, so it cannot describe a
design the site is not running. Change a token there and both follow.</p>

<nav class="toc" aria-label="On this page"><b>On this page</b>
<a href="#design--where-it-comes-from">Where it comes from</a>
<a href="#design--typography">Typography</a>
<a href="#design--colour">Colour</a>
<a href="#design--layout">Layout and spacing</a>
<a href="#design--components">Components</a>
<a href="#design--deviations">Deviations from the source</a></nav>

<h2 id="design--where-it-comes-from">Where it comes from</h2>
<p>The palette, type scale and spacing are taken from
<a href="{esc(d['meta']['source'])}" target="_blank" rel="noopener">the Elegant Themes blog</a>,
measured from computed styles at a 1280px viewport on {esc(d['meta']['measured'])}. That site runs
Divi and sets everything in Lato, with blue-tinted neutrals rather than grey, unusually loose
leading and a single hot pink reserved for actions. Those are the decisions adopted here.</p>

<h2 id="design--typography">Typography</h2>
<p>Six sizes, matching the source's six. The source computes fractional values such as 36.8px from
multipliers; these are rounded to whole pixels, because a scale should read as a decision.
Running text is {esc(scale['t-body'])} at a line height of {esc(leading['lh-body'])}, which is
looser than most long-form sites and is what gives the page its air.</p>
<div class="specimens">{specimen}</div>

<h2 id="design--colour">Colour</h2>
<p>Nothing here is black and nothing is neutral grey. Every neutral carries a blue cast, taken
from the source.</p>
<div class="tw"><table><thead><tr><th>Role</th><th>Token</th><th>Light theme</th></tr></thead>
<tbody>{role_rows}</tbody></table></div>
{providers}{severity}{extra}

<h2 id="design--layout">Layout and spacing</h2>
<p>Prose is capped at {esc(layout['prose'])}, matching the source. Sections are separated by
{esc(layout['gap-section'])}, which is nearly double what most documentation sites use.</p>
<div class="tw"><table><thead><tr><th>Token</th><th>Value</th></tr></thead>
<tbody>{layout_rows}</tbody></table></div>

<h2 id="design--components">Components</h2>
<p>Buttons are fully pill-shaped at {esc(layout['radius-pill'])}, and the primary action is the one
place the accent appears.</p>
<div class="demo">
  <a class="cta" href="#home">Primary action</a>
  <span class="tag">exam code</span>
  <span class="mk b-serious">Serious</span>
  <span class="mk b-regular">Regular</span>
</div>

<h2 id="design--deviations">Deviations from the source</h2>
<p>Recorded rather than made silently. Each one is a place this guide does something the source
does not, and why.</p>
<div class="devs">{dev}</div>
</section>"""
