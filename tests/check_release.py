"""Check the exact public distribution surface; not a universal secret scanner."""
from pathlib import Path
import os
import re

ROOT = Path(__file__).resolve().parents[1]
ALLOWED = {
    '.gitignore', 'README.md', 'LICENSE', 'SECURITY.md', 'CONTRIBUTING.md',
    'CHANGELOG.md', 'requirements-dev.txt', 'docs/README.en.md',
    'docs/SECURITY_REVIEW.md', 'scripts/01_Preparar_importacion_AAF.lua',
    'scripts/02_Importar_AAF.lua', 'tests/test_scripts.py', 'tests/check_release.py',
}
PATTERNS = {
    'personal home path': '/' + 'Users' + r'/[^\s/]+/',
    'external volume path': '/' + 'Volumes' + r'/[^\s]+',
    'Windows home path': r'[A-Za-z]:\\Users\\[^\\\s]+',
    'GitHub token': r'gh[pousr]_[A-Za-z0-9]{30,}',
    'GitHub fine-grained token': r'github_pat_[A-Za-z0-9_]{30,}',
    'AWS access key': r'AKIA[0-9A-Z]{16}',
    'private key': r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',
}
files = set()
errors = []
for directory, folders, names in os.walk(ROOT, followlinks=False):
    folders[:] = [name for name in folders if name not in {'.git', '.venv', 'venv', '__pycache__'}]
    for folder in folders:
        path = Path(directory) / folder
        if path.is_symlink():
            errors.append(f'Symlink directory: {path.relative_to(ROOT)}')
    for name in names:
        path = Path(directory) / name
        relative = path.relative_to(ROOT).as_posix()
        if relative == '.DS_Store':
            continue
        files.add(relative)
        if path.is_symlink():
            errors.append(f'Symlink file: {relative}')
            continue
        if relative not in ALLOWED:
            errors.append(f'Unexpected file: {relative}')
            continue
        if path.stat().st_size > 128 * 1024:
            errors.append(f'Unexpected file size: {relative}')
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            errors.append(f'Non-UTF-8 file: {relative}')
            continue
        for label, pattern in PATTERNS.items():
            if re.search(pattern, text):
                errors.append(f'{label}: {relative}')
        if relative.startswith('scripts/'):
            forbidden = [r'\bos\.execute\s*\(', r'\bio\.popen\s*\(',
                         r'\bExecProcess\s*\(', r'\b(?:loadfile|dofile)\s*\(',
                         r'\b(?:tcp_connect|socket)\s*\(']
            if any(re.search(pattern, text) for pattern in forbidden):
                errors.append(f'Unexpected execution/network API: {relative}')

for missing in sorted(ALLOWED - files):
    errors.append(f'Missing file: {missing}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(ALLOWED)} allowed UTF-8 files; no unexpected files, common secret patterns, personal paths or forbidden script APIs found.')
print('This check does not audit the native dependencies or detect every possible secret.')
