#!/usr/bin/env python3
"""Rebuild in isolation and reject stale, missing, or unexpected generated outputs."""
from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
GENERATED_FILES = (
    'README.md', 'docs/09-confusing-terms.md', 'docs/10-exam-map.md',
    'docs/hierarchy-diagram.md',
)
GENERATED_DIRS = ('site', 'dist')


def inventory(root: pathlib.Path) -> set[str]:
    paths = set(GENERATED_FILES)
    for directory in GENERATED_DIRS:
        paths.update(p.relative_to(root).as_posix()
                     for p in (root / directory).rglob('*') if p.is_file())
    return paths


def main() -> int:
    with tempfile.TemporaryDirectory(prefix='cloud-generated-') as temporary:
        expected = pathlib.Path(temporary)
        for name in ('scripts', 'data', 'docs'):
            shutil.copytree(ROOT / name, expected / name,
                            ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copy2(ROOT / 'README.md', expected / 'README.md')
        # Only authored portions of mixed documents are build inputs. Fully
        # generated chapters must be recreated rather than inherited from disk.
        for name in ('docs/09-confusing-terms.md', 'docs/hierarchy-diagram.md'):
            (expected / name).unlink(missing_ok=True)
        result = subprocess.run([sys.executable, 'scripts/build.py'], cwd=expected,
                                capture_output=True, text=True)
        if result.returncode:
            print(result.stdout, end='')
            print(result.stderr, end='', file=sys.stderr)
            return result.returncode
        paths = inventory(ROOT) | inventory(expected)
        stale = [name for name in sorted(paths)
                 if not (ROOT / name).is_file() or not (expected / name).is_file()
                 or (ROOT / name).read_bytes() != (expected / name).read_bytes()]
        if stale:
            print('Generated outputs differ; run python scripts/build.py:')
            for name in stale:
                print(f'  {name}')
            return 1
        print(f'All {len(paths)} generated outputs match their sources.')
        return 0


if __name__ == '__main__':
    sys.exit(main())
