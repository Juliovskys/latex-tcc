"""Confere vínculos, numeração e correspondência bibliográfica do Markdown, sem alterá-lo."""
from collections import Counter
import ast
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def main():
    source = ROOT / 'docs/tcc.md'
    text = source.read_text(encoding='utf-8')
    bib = (ROOT / 'docs/referencias-tcc.bib').read_text(encoding='utf-8')
    errors = []
    anchors = re.findall(r'<a id="([^"]+)"></a>', text)
    duplicates = [key for key, n in Counter(anchors).items() if n > 1]
    if duplicates:
        errors.append(f'Âncoras repetidas: {duplicates}')
    links = re.findall(r'\]\(#([^)]+)\)', text)
    missing = sorted(set(links) - set(anchors))
    if missing:
        errors.append(f'Destinos ausentes: {missing}')
    keys = re.findall(r'@\w+\s*\{([^,]+),', bib)
    if len(keys) != len(set(keys)):
        errors.append('Chaves bibliográficas repetidas')
    cited = {key[4:] for key in links if key.startswith('ref-')}
    listed = {key[4:] for key in anchors if key.startswith('ref-')}
    if cited != listed or cited != set(keys):
        errors.append(f'Citação/lista/BibTeX divergem: {cited ^ listed}; {cited ^ set(keys)}')
    captions = {}
    for match in re.finditer(r'<a id="((?:tab|qua):[^"]+)"></a>\s*\n\*\*(Tabela|Quadro) (\d+) — ', text):
        captions[match[1]] = (match[2], match[3])
    for kind in ('Tabela', 'Quadro'):
        numbers = [int(num) for actual, num in captions.values() if actual == kind]
        if numbers != list(range(1, len(numbers) + 1)):
            errors.append(f'Numeração de {kind}: {numbers}')
    for match in re.finditer(r'(Tabela|Quadro)\s*\[(\d+)\]\(#((?:tab|qua):[^)]+)\)', text):
        if captions.get(match[3]) != (match[1], match[2]):
            errors.append(f'Remissão incorreta: {match[0]}')
    for target in re.findall(r'!\[[^\]]*\]\(([^)]+)\)', text):
        if not (source.parent / target).is_file():
            errors.append(f'Figura ausente: {target}')
    main_body = text[:text.index('# Referências')]
    if re.search(r'\bNPS\b|Net Promoter', main_body, re.I):
        errors.append('Indicador retirado ainda presente no texto atual')
    # Rastreabilidade: os testes citados devem existir como métodos da classe indicada.
    cases = re.findall(r'`(prototype-api/test_[^`:]+\.py)::([A-Za-z_]+)\.(test_[A-Za-z_]+)`', text)
    for filename, class_name, method in cases:
        tree = ast.parse((ROOT / filename).read_text(encoding='utf-8'))
        members = {f'{node.name}.{item.name}' for node in tree.body if isinstance(node, ast.ClassDef)
                   for item in node.body if isinstance(item, ast.FunctionDef)}
        if class_name + '.' + method not in members:
            errors.append(f'Teste citado inexistente: {filename}::{class_name}.{method}')
    evidence_path = ROOT / 'docs/evidencias/verificacao-medio-prazo.json'
    if evidence_path.exists():
        evidence = json.loads(evidence_path.read_text(encoding='utf-8'))
        for filename, expected in evidence['source_sha256'].items():
            if hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() != expected:
                errors.append(f'Arquivo mudou desde a execução registrada: {filename}')
        if evidence['return_code'] != 0 or evidence['tests_reported'] != len(cases):
            errors.append('Resultado/contagem dos testes diverge do catálogo')
    sections = re.findall(r'^#{1,4} (\d+(?:\.\d+)*) ', text, re.M)
    for target in re.findall(r'(?:seção|seções|Seção)\s+(\d+(?:\.\d+)*)', text):
        if target not in sections:
            errors.append(f'Seção inexistente: {target}')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'OK: {len(keys)} referências; {len(captions)} tabelas/quadros; '
          f'{len(re.findall(r"^# Apêndice", text, re.M))} apêndices; vínculos e figuras presentes.')


if __name__ == '__main__':
    main()
