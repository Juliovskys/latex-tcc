"""Confere a transposição, seus vínculos e a identidade do PDF compilado."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / 'tmp/pdfs/build'
PDF = ROOT / 'output/pdf/TCC_Avaliacao_Contextual_Medio_Prazo.pdf'
CONTENT = ['introducao', 'referencialteorico', 'metodologia', 'desenvolvimento',
           'consideracoes', 'apendices', 'resumo', 'abstract', 'abreviaturas', 'listaapendices']


def main():
    md = (ROOT / 'docs/tcc.md').read_text(encoding='utf-8')
    tex_files = [ROOT / f'latex/editaveis/{name}.tex' for name in CONTENT]
    tex = '\n'.join(p.read_text(encoding='utf-8') for p in tex_files)
    aux = (BUILD / 'tcc.aux').read_text(encoding='utf-8')
    bbl = (BUILD / 'tcc.bbl').read_text(encoding='utf-8')
    log = (BUILD / 'tcc.log').read_text(encoding='utf-8')
    assert not re.search(r'Overfull|undefined|Missing character|multiply defined', log), 'Aviso crítico no log.'
    assert 'TCCLATEXTOKEN' not in tex, 'Token de conversão não resolvido.'
    keys = set(re.findall(r'\]\(#ref-([^)]+)\)', md))
    cited = {key for group in re.findall(r'\\cite(?:online)?(?:\[[^\]]+\])?\{([^}]+)\}', tex) for key in group.split(',')}
    listed = set(re.findall(r'\\bibitem\[[^\]]+\]\{([^}]+)\}', bbl))
    assert keys == cited == listed, 'Chaves de citação divergem entre Markdown, LaTeX e BBL.'
    labels = re.findall(r'\\label\{([^}]+)\}', tex)
    assert len(labels) == len(set(labels)), 'Rótulo LaTeX repetido.'
    assert set(re.findall(r'\\ref\{([^}]+)\}', tex)) <= set(labels), 'Remissão sem destino.'
    for ident, kind, number in re.findall(r'<a id="((?:tab|qua):[^"]+)"></a>\s*\n\*\*(Tabela|Quadro) (\d+) —', md):
        match = re.search(r'\\newlabel\{' + re.escape(ident) + r'\}\{\{(?:\\M@TitleReference\s*\{)?([^}]+)\}', aux)
        assert match and match[1] == number, f'Numeração divergente: {kind} {ident}.'
    counts = {'references': len(keys),
              'quadros': (BUILD / 'tcc.loq').read_text(encoding='utf-8').count('\\contentsline'),
              'tables': (BUILD / 'tcc.lot').read_text(encoding='utf-8').count('\\contentsline'),
              'figures': (BUILD / 'tcc.lof').read_text(encoding='utf-8').count('\\contentsline'),
              'appendices': len(re.findall(r'^# Apêndice', md, re.M))}
    assert counts == {'references': 57, 'quadros': 19, 'tables': 2, 'figures': 7, 'appendices': 12}, counts
    for letter in 'abcdefghijkl':
        assert f'\\newlabel{{sec:apendice-{letter}}}' in aux
    assert (ROOT / 'docs/referencias-tcc.bib').read_bytes() == (ROOT / 'latex/bibliografia.bib').read_bytes()
    for entry in re.split(r'(?=\\bibitem\[)', bbl)[1:]:
        year = re.search(r'\\abntrefinfo\{[^\n]*\}\{(\d{4}[a-z])\}', entry)
        if year:
            assert entry.count(year[1]) >= 2, 'Sufixo ausente no corpo da referência.'
    assert PDF.read_bytes() == (BUILD / 'tcc.pdf').read_bytes(), 'PDF publicado difere da compilação.'
    reader = PdfReader(PDF)
    assert all(len(page.extract_text() or '') > 15 or (page.extract_text() or '').strip() == 'Apêndices'
               for page in reader.pages), 'Página sem conteúdo textual.'
    frozen = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True,
                            text=True, check=True).stdout.strip()
    sources = [ROOT / 'docs/tcc.md', ROOT / 'docs/referencias-tcc.bib',
               ROOT / 'scripts/sincronizar_tcc.py', ROOT / 'scripts/compilar-tcc.ps1',
               ROOT / 'scripts/verificar_latex.py',
               ROOT / 'latex/tcc.tex', ROOT / 'latex/abntex2-alf-tcc.bst',
               ROOT / 'latex/bibliografia.bib', ROOT / 'latex/editaveis/informacoes.tex',
               ROOT / 'latex/figuras/capa.png', *tex_files,
               *sorted((ROOT / 'latex/fixos').glob('*')),
               *sorted((ROOT / 'docs/figuras').glob('*.png')),
               *sorted((ROOT / 'latex/figuras/apendices').glob('lean*.png'))]
    hashes = {str(p.relative_to(ROOT)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sources if p.is_file()}
    matches_commit = True
    for filename, digest in hashes.items():
        tracked = subprocess.run(['git', 'show', f'{frozen}:{filename}'], cwd=ROOT, capture_output=True)
        disk = (ROOT / filename).read_bytes()
        actual = tracked.stdout
        if Path(filename).suffix in {'.md', '.bib', '.py', '.ps1', '.tex', '.sty', '.bst'}:
            actual = actual.replace(b'\r\n', b'\n')
            disk = disk.replace(b'\r\n', b'\n')
        if tracked.returncode or actual != disk:
            matches_commit = False
            break
    record = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'source_commit': frozen,
              'source_files_match_commit': matches_commit,
              'commit_comparison': 'Textos comparados ignorando apenas LF/CRLF; binários byte a byte. Hashes registram os bytes locais efetivamente utilizados.',
              'pdf': str(PDF.relative_to(ROOT)), 'pdf_sha256': hashlib.sha256(PDF.read_bytes()).hexdigest(),
              'pages': len(reader.pages), **counts,
              'source_sha256': hashes,
              'checks': 'Compilação; vínculos; numeração; correspondência bibliográfica; sufixos; listas; identidade do PDF. Revisão visual registrada no relatório de transposição.',
              'limitations': 'Não executa CopySpider, revisão institucional ou avaliação com participantes.'}
    destination = ROOT / 'docs/evidencias/compilacao-medio-prazo.json'
    destination.write_text(json.dumps(record, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'OK LaTeX/PDF: {len(reader.pages)} páginas; {counts}; log sem avisos críticos.')


if __name__ == '__main__':
    main()
