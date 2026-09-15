"""Keep authored link destinations intact when compiling the single-page guide."""
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
import guide
import mdlite


class LinkTests(unittest.TestCase):
    def test_links_resolve_without_losing_paths_fragments_or_query_parameters(self):
        previous = mdlite.RESOLVE
        self.addCleanup(setattr, mdlite, 'RESOLVE', previous)
        mdlite.RESOLVE = guide.resolve
        cases = {
            '02-identity.md#check-your-understanding': '#02-identity--check-your-understanding',
            '../scripts/diagrams.py': 'https://github.com/lensabillion/cloud-rosetta/blob/main/scripts/diagrams.py',
            'reviews/example.md': 'https://github.com/lensabillion/cloud-rosetta/blob/main/docs/reviews/example.md',
            'https://example.com/original.md': 'https://example.com/original.md',
            'https://example.com/?a=1&b=2': 'https://example.com/?a=1&amp;b=2',
        }
        for original, expected in cases.items():
            with self.subTest(original=original):
                self.assertIn('href="' + expected + '"', mdlite.inline('[Destination](' + original + ')'))
