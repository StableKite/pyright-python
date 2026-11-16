from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / 'version.py'


@pytest.mark.parametrize(
    ('current', 'candidate', 'newer'),
    [
        ('1.1.414-stablekite.7', '1.1.414', False),
        ('1.1.414-stablekite.0', '1.1.414', False),
        ('1.1.414-stablekite.123', '1.1.413', False),
        ('1.1.414-stablekite.7', '1.1.415', True),
        ('1.1.414-stablekite.7', '1.2.0', True),
        ('1.1.414-stablekite.7', '2.0.0', True),
        ('1.1.414-stablekite.7', '1.1.414-rc.1', False),
        ('1.1.414-stablekite.7', '1.1.415-rc.1', True),
        ('1.1.414-stablekite.7', '1.1.414+build.2', False),
        ('1.1.414-stablekite.7+build.2', '1.1.414', False),
        ('1.1.414', '1.1.414', False),
        ('1.1.414', '1.1.413', False),
        ('1.1.414', '1.1.415', True),
        ('1.1.414', '1.2.0', True),
        ('1.1.414', '2.0.0', True),
        ('1.1.414-rc.1', '1.1.414', True),
        ('1.1.414-rc.1', '1.1.414-rc.2', True),
        ('1.1.414-rc.2', '1.1.414-rc.1', False),
        ('1.1.414+build.1', '1.1.414+build.2', False),
    ],
)
def test_compare_real_cli_is_read_only(tmp_path: Path, current: str, candidate: str, newer: bool) -> None:
    source = tmp_path / 'src' / 'pyright' / '_version.py'
    source.parent.mkdir(parents=True)
    original = f'__pyright_version__ = {current!r}\n'.encode()
    source.write_bytes(original)
    readme = tmp_path / 'README.md'
    readme.write_bytes(b'rev: v1.1.414\n')

    result = subprocess.run(
        [sys.executable, '-I', '-B', str(SCRIPT), '--compare', candidate],
        cwd=tmp_path,
        capture_output=True,
    )

    assert result.returncode == 0, result.stderr.decode()
    assert result.stdout.strip() == (b'1' if newer else b'0')
    assert source.read_bytes() == original
    assert readme.read_bytes() == b'rev: v1.1.414\n'


@pytest.mark.parametrize(
    ('current', 'candidate'),
    [
        ('1.1.414-stablekite.invalid', '1.1.415'),
        ('1.1', '1.1.415'),
        ('1.1.414-stablekite.7', 'invalid'),
        ('1.1.414-stablekite.7', '1.1.415.1'),
    ],
)
def test_invalid_compare_real_cli_fails_closed(tmp_path: Path, current: str, candidate: str) -> None:
    source = tmp_path / 'src' / 'pyright' / '_version.py'
    source.parent.mkdir(parents=True)
    original = f'__pyright_version__ = {current!r}\n'.encode()
    source.write_bytes(original)

    result = subprocess.run(
        [sys.executable, '-I', '-B', str(SCRIPT), '--compare', candidate],
        cwd=tmp_path,
        capture_output=True,
    )

    assert result.returncode != 0
    assert result.stdout == b''
    assert b'ValueError' in result.stderr
    assert source.read_bytes() == original
