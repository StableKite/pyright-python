"""Verify and unpack the source-built Pyright bundle before packaging."""

import hashlib
import json
import re
import tarfile
from pathlib import Path, PurePosixPath


def prepare_bundled_pyright() -> None:
    root = Path(__file__).resolve().parent
    manifest = json.loads((root / 'vendor' / 'PYRIGHT_NODE.json').read_text(encoding='utf-8'))
    archive_name = manifest['archive']
    if PurePosixPath(archive_name).name != archive_name or ':' in archive_name or '\\' in archive_name:
        raise RuntimeError('Invalid bundled Pyright archive name')
    archive_path = root / 'vendor' / archive_name
    payload = archive_path.read_bytes()
    if hashlib.sha256(payload).hexdigest() != manifest['sha256']:
        raise RuntimeError('Bundled Pyright archive SHA-256 mismatch')
    version_source = (root / 'src' / 'pyright' / '_version.py').read_text(encoding='utf-8')
    match = re.search(r"^__pyright_version__\s*=\s*['\"]([^'\"]+)['\"]", version_source, re.MULTILINE)
    if match is None or match.group(1) != manifest['version']:
        raise RuntimeError('Python wrapper and bundled Pyright versions differ')
    destination = root / 'src' / 'pyright' / 'dist'
    try:
        destination.resolve().relative_to(root)
    except ValueError:
        raise RuntimeError('Bundled Pyright destination escaped the source directory')
    if destination.is_symlink():
        raise RuntimeError('Bundled Pyright destination must not be a symlink')
    if destination.exists() and any(p.is_symlink() for p in destination.rglob('*')):
        raise RuntimeError('Bundled Pyright destination contains a symlink')
    destination.mkdir(parents=True, exist_ok=True)
    seen = set()
    with tarfile.open(archive_path, 'r:gz') as archive:
        for member in archive:
            name = PurePosixPath(member.name)
            if name.is_absolute() or '..' in name.parts or '\\' in member.name or ':' in member.name:
                raise RuntimeError('Invalid bundled Pyright member path')
            if not name.parts or name.parts[0] != 'package':
                raise RuntimeError('Expected npm package/ prefix')
            relative = PurePosixPath(*name.parts[1:])
            if member.isdir():
                continue
            if not member.isfile() or not name.parts[1:] or str(relative) in seen:
                raise RuntimeError('Unsupported or duplicate bundled Pyright member')
            data = archive.extractfile(member).read()
            record = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
            if manifest['files'].get(str(relative)) != record:
                raise RuntimeError('Bundled Pyright member does not match its manifest')
            target = destination.joinpath(*relative.parts)
            if target.is_symlink():
                raise RuntimeError('Bundled Pyright member must not overwrite a symlink')
            try:
                target.resolve().relative_to(destination.resolve())
            except ValueError:
                raise RuntimeError('Bundled Pyright target escaped the source directory')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            seen.add(str(relative))
    if seen != set(manifest['files']):
        raise RuntimeError('Bundled Pyright manifest member set differs from the archive')
    installed_files = {p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}
    if installed_files != seen:
        raise RuntimeError('Unexpected pre-existing files in bundled Pyright destination')
    package = json.loads((destination / 'package.json').read_text(encoding='utf-8'))
    if package['name'] != 'pyright' or package['version'] != manifest['version']:
        raise RuntimeError('Bundled Node package identity mismatch')
