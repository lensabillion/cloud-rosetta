"""Exercise real builds in isolated folders; never rewrite the developer's outputs."""
from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile
from textwrap import dedent
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUTPUTS = ('site/index.html', 'README.md', 'docs/09-confusing-terms.md',
           'docs/10-exam-map.md', 'docs/hierarchy-diagram.md',
           'dist/poster.svg', 'dist/drills.tsv', 'dist/rosetta.json')


class BuildTests(unittest.TestCase):
    def workspace(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = pathlib.Path(temp.name)
        for name in ('scripts', 'data', 'docs'):
            shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy2(ROOT / 'README.md', root / 'README.md')
        return root

    def run_build(self, root, date='2026-09-14'):
        code = dedent("""
            import datetime, runpy, sys
            frozen_date = sys.argv[-1]
            class Clock(datetime.date):
                @classmethod
                def today(cls):
                    return cls.fromisoformat(frozen_date)
            datetime.date = Clock
            sys.path.insert(0, 'scripts')
            sys.argv = ['scripts/build.py']
            runpy.run_path('scripts/build.py', run_name='__main__')
        """)
        result = subprocess.run([sys.executable, '-c', code, date], cwd=root,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return {name: (root / name).read_bytes() for name in OUTPUTS}

    def test_one_build_propagates_changed_terms_and_is_clock_independent(self):
        root = self.workspace()
        terms = root / 'data/terms/false-friends.yml'
        # Alter a real field rendered by both the decoder and its Markdown chapter.
        terms.write_text(terms.read_text().replace('term: Role', 'term: Role probe', 1))
        first = self.run_build(root)
        self.assertIn(b'Role probe', first['site/index.html'])
        second = self.run_build(root, '2026-10-15')
        self.assertEqual(first, second)

    def test_check_rejects_each_stale_or_missing_surface_without_rewriting(self):
        root = self.workspace()
        self.run_build(root)
        result = subprocess.run([sys.executable, 'scripts/check_generated.py'], cwd=root,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        (root / 'site/obsolete.html').write_text('obsolete page')
        for name in OUTPUTS:
            path = root / name
            if name == 'dist/drills.tsv':
                path.unlink()
            elif name in ('README.md', 'docs/10-exam-map.md'):
                text = path.read_text()
                start = text.index('<!-- BEGIN')
                end = text.index('-->', start) + 3
                path.write_text(text[:end] + '\nSTALE PROBE\n' + text[end:])
            else:
                path.write_bytes(path.read_bytes() + b'\nSTALE PROBE\n')
        result = subprocess.run([sys.executable, 'scripts/check_generated.py'], cwd=root,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        for name in OUTPUTS:
            self.assertIn(name, result.stdout + result.stderr)
        self.assertIn('site/obsolete.html', result.stdout)
        self.assertFalse((root / 'dist/drills.tsv').exists())
        self.assertTrue((root / 'site/index.html').read_bytes().endswith(b'STALE PROBE\n'))

    def test_check_reports_build_failure(self):
        root = self.workspace()
        (root / 'data/mappings/identity.yml').write_text('rows: [invalid')
        result = subprocess.run([sys.executable, 'scripts/check_generated.py'], cwd=root,
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('ParserError', result.stderr)

    def test_document_has_explicit_encoding_viewport_and_language(self):
        output = self.run_build(self.workspace())['site/index.html'].decode('utf-8')
        self.assertTrue(output.startswith('<!doctype html>'))
        self.assertIn('<html lang="en">', output)
        self.assertIn('<meta charset="utf-8">', output[:1024])
        self.assertIn('width=device-width, initial-scale=1', output)
        self.assertTrue(output.rstrip().endswith('</body>\n</html>'))
