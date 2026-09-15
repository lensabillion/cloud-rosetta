"""Render service architectures from cloud content and centralized design geometry."""
from __future__ import annotations

import base64
from dataclasses import dataclass
import html
import pathlib
import textwrap

import yaml
import design

ROOT = pathlib.Path(__file__).resolve().parent.parent
# Conservative average glyph advance for wrapping and label backplates.
GLYPH_ADVANCE = 0.56


def esc(value):
    return html.escape(str(value), quote=True)


@dataclass
class ArchitectureDrawing:
    name: str
    title: str
    description: str
    height: int
    markup: str

    def svg(self):
        return self.markup


def render(name: str) -> ArchitectureDrawing:
    tokens = design.load()
    scene = yaml.safe_load((ROOT / 'data/architecture-scenes.yml').read_text(encoding='utf-8'))[name]
    style = tokens['diagram']
    geometry = style['scenes'][name]
    colours = tokens['colour']['light']
    sizes = {k: float(v.removesuffix('px')) for k, v in tokens['type']['scale'].items()}
    height, width = geometry['height'], style['width']
    parts = []

    def text(x, y, value, max_width, size='t-label', bold=False, colour='ink2'):
        font_size = sizes[size]
        # These are conservative text metrics, not a second type scale.
        limit = max(1, int(max_width / (font_size * GLYPH_ADVANCE)))
        lines = textwrap.wrap(value, limit, break_long_words=False, break_on_hyphens=False)
        for index, line in enumerate(lines):
            baseline = y + index * style['line_height']
            parts.append(f'<text x="{x}" y="{baseline}" font-size="{font_size:g}" '
                         f'font-weight="{700 if bold else 400}" fill="{colours[colour]}">{esc(line)}</text>')
        return len(lines)

    text(*style['title_position'], scene['title'], width - style['padding'] * 2,
         't-section', True, 'ink')
    text(*style['subtitle_position'], scene['subtitle'], width - style['padding'] * 2)
    elements = scene['elements']
    for key, element in elements.items():
        if element['kind'] != 'boundary':
            continue
        shape = geometry['elements'][key]
        x, y, w, h = shape['rect']
        network = key in ('vpc', 'vnet')
        stroke = colours[scene['provider']] if network else colours['rule2']
        dash = '' if network else f' stroke-dasharray="{",".join(map(str, style["boundary_dash"]))}"'
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{style["radius"]}" '
                     f'fill="none" stroke="{stroke}" stroke-width="{style["stroke"]}"{dash}/>')
        lx, ly = shape.get('label_at', [x + style['boundary_label_inset'][0], y + style['boundary_label_inset'][1]])
        text(lx, ly, element['title'], w - style['padding'] * 2, bold=True)

    for key, element in elements.items():
        if element['kind'] not in ('card', 'note'):
            continue
        x, y, w, h = geometry['elements'][key]['rect']
        note = element['kind'] == 'note'
        if not note:
            parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{style["radius"]}" '
                         f'fill="{colours["sheet"]}" stroke="{colours["rule2"]}" stroke-width="{style["stroke"]}"/>')
        if icon := element.get('icon'):
            payload = base64.b64encode((ROOT / 'data/vendor-icons' / icon).read_bytes()).decode('ascii')
            parts.append(f'<image x="{x + style["icon_inset"]}" y="{y + style["icon_inset"]}" '
                         f'width="{style["icon"]}" height="{style["icon"]}" '
                         f'href="data:image/svg+xml;base64,{payload}" preserveAspectRatio="xMidYMid meet"/>')
        inset = style['text_inset'] if element.get('icon') else style['plain_inset']
        tx, ty = x + inset, y + style['title_baseline']
        available = w - inset - style['plain_inset']
        lines = text(tx, ty, element['title'], available, 't-nav', True, 'ink')
        if element.get('detail'):
            text(tx, ty + lines * style['detail_gap'], element['detail'], available)

    for key, element in elements.items():
        if element['kind'] != 'edge':
            continue
        geometry_edge = geometry['elements'][key]
        points = geometry_edge['points']
        path = 'M' + ' L'.join(f'{x},{y}' for x, y in points)
        dash = f' stroke-dasharray="{",".join(map(str, style["control_dash"]))}"' if element.get('control') else ''
        parts.append(f'<path d="{path}" fill="none" stroke="{colours["ink2"]}" '
                     f'stroke-width="{style["stroke"]}" marker-end="url(#{name}-arrow)"{dash}/>')
        x, y = geometry_edge['label_at']
        font_size = sizes['t-label']
        label_width = len(element['title']) * font_size * GLYPH_ADVANCE
        pad = style['label_pad']
        parts.append(f'<rect x="{x-label_width/2-pad}" y="{y-font_size-pad/2}" '
                     f'width="{label_width+pad*2}" height="{font_size+pad}" fill="{colours["sheet"]}"/>')
        text(x-label_width/2, y, element['title'], label_width+pad)

    text(style['padding'], height-style['footer_inset'],
         'Solid arrows: labelled traffic or replication. Dashed arrows: policy/control. Conceptual design; assumptions and sources in the chapter.',
         width-style['padding']*2)
    header = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
              f'role="img" aria-labelledby="{name}-title {name}-desc" '
              f'font-family="{esc(tokens["fonts"]["stacks"]["text"])}">'
              f'<title id="{name}-title">{esc(scene["title"])}</title>'
              f'<desc id="{name}-desc">{esc(scene["description"])}</desc>'
              f'<defs><marker id="{name}-arrow" viewBox="0 0 10 10" refX="9" refY="5" '
              f'markerWidth="{style["marker_size"]}" markerHeight="{style["marker_size"]}" orient="auto">'
              f'<path d="M0,0 L10,5 L0,10 z" fill="{colours["ink2"]}"/></marker></defs>'
              f'<rect width="{width}" height="{height}" fill="{colours["sheet"]}"/>')
    return ArchitectureDrawing(name, scene['title'], scene['description'], height, header + ''.join(parts) + '</svg>\n')
