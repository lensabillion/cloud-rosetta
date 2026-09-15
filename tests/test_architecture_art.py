"""Check portable artwork and the content/layout contract for service diagrams."""
import base64
import json
import pathlib
import sys
import unittest
import xml.etree.ElementTree as ET

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import architecture_art
import design


class ArchitectureArtTests(unittest.TestCase):
    def test_official_artwork_is_embedded_unchanged_in_every_export(self):
        manifest = json.loads((ROOT / 'data/vendor-icons/manifest.json').read_text())
        assets = {(ROOT / 'data/vendor-icons' / name).read_bytes() for name in manifest}
        used = set()
        for name in design.load()['diagram']['scenes']:
            drawing = ET.fromstring(architecture_art.render(name).svg())
            images = drawing.findall('{http://www.w3.org/2000/svg}image')
            self.assertTrue(images, name)
            for image in images:
                href = image.attrib['href']
                self.assertTrue(href.startswith('data:image/svg+xml;base64,'))
                payload = base64.b64decode(href.split(',', 1)[1], validate=True)
                self.assertIn(payload, assets)
                ET.fromstring(payload)
                used.add(payload)
        self.assertEqual(used, assets, 'An unused vendor asset should not be shipped')

    def test_named_scopes_and_flows_have_matching_in_bounds_geometry(self):
        tokens = design.load()['diagram']
        scenes = yaml.safe_load((ROOT / 'data/architecture-scenes.yml').read_text())
        self.assertEqual(set(scenes), set(tokens['scenes']))
        for name, scene in scenes.items():
            geometry = tokens['scenes'][name]
            self.assertEqual(set(scene['elements']), set(geometry['elements']), name)
            for key, element in scene['elements'].items():
                self.assertTrue(element['title'].strip(), f'{name}/{key}')
                shape = geometry['elements'][key]
                if element['kind'] == 'edge':
                    points = shape['points'] + [shape['label_at']]
                    self.assertGreaterEqual(len(shape['points']), 2)
                else:
                    x, y, w, h = shape['rect']
                    self.assertGreater(w, 0)
                    self.assertGreater(h, 0)
                    points = [(x, y), (x+w, y+h)]
                for x, y in points:
                    self.assertTrue(0 <= x <= tokens['width'] and 0 <= y <= geometry['height'], f'{name}/{key}')
