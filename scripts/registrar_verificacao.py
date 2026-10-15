"""Executa os testes locais e registra evidência reproduzível, sem dados de participantes."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import sqlite3
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    'prototype-api/server.py', 'prototype-api/governance.py', 'prototype-api/admin.html',
    'prototype-api/test_feedback_ces.py', 'prototype-api/test_governance.py',
]


def git(*args):
    try:
        result = subprocess.run(['git', *args], cwd=ROOT, capture_output=True,
                                text=True, encoding='utf-8')
    except FileNotFoundError:
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def main():
    start = datetime.now(timezone.utc).isoformat()
    hashes = {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in FILES}
    command = [sys.executable, '-m', 'unittest', 'discover', '-s', 'prototype-api', '-p', 'test_*.py', '-v']
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
    output = run.stdout + run.stderr
    working_status = git('status', '--porcelain')
    result = {
        'started_at_utc': start, 'finished_at_utc': datetime.now(timezone.utc).isoformat(),
        'execution': 'Execução automatizada local assistida por agente; não é avaliação humana independente.',
        'python': platform.python_version(), 'sqlite': sqlite3.sqlite_version,
        'os': platform.system(), 'os_release': platform.release(),
        'branch': git('branch', '--show-current'), 'base_commit': git('rev-parse', 'HEAD'),
        'working_tree_has_changes': bool(working_status) if working_status is not None else None,
        'command': ['python', *command[1:]], 'return_code': run.returncode,
        'tests_reported': int(re.search(r'Ran (\d+) tests?', output)[1]) if re.search(r'Ran (\d+) tests?', output) else None,
        'source_sha256': hashes,
        'scope': 'Contratos e cenários selecionados, com bases temporárias e dados sintéticos. Sem validação com pessoas, carga ou auditoria global.',
    }
    destination = ROOT / 'docs/evidencias'
    destination.mkdir(exist_ok=True)
    (destination / 'verificacao-medio-prazo.txt').write_text(output, encoding='utf-8')
    (destination / 'verificacao-medio-prazo.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(output)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(run.returncode)


if __name__ == '__main__':
    main()
