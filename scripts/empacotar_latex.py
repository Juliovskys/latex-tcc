"""Prepara as fontes LaTeX portáteis; não altera as fontes do repositório."""
import hashlib
import json
from pathlib import Path
import shutil
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
STAGE = ROOT / 'tmp/pdfs/fontes-latex-final'
OUTPUT = ROOT / 'output/latex/TCC_Avaliacao_Contextual_Fontes_LaTeX_Final.zip'
EDITABLE = ['abreviaturas', 'abstract', 'apendices', 'consideracoes', 'desenvolvimento',
            'informacoes', 'introducao', 'listaapendices', 'metodologia',
            'referencialteorico', 'resumo']


def main():
    STAGE.mkdir(parents=True, exist_ok=True)
    files = ['latex/tcc.tex', 'latex/bibliografia.bib', 'latex/abntex2-alf-tcc.bst',
             'latex/latexmkrc', 'latex/figuras/capa.png',
             'latex/pretextuais/ficha-catalografica.pdf']
    files += [f'latex/editaveis/{name}.tex' for name in EDITABLE]
    files += [str(p.relative_to(ROOT)).replace('\\', '/')
              for p in sorted((ROOT / 'latex/fixos').iterdir()) if p.is_file()]
    staged = []
    for filename in files:
        source = ROOT / filename
        destination = STAGE / source.relative_to(ROOT / 'latex')
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix == '.tex':
            content = source.read_text(encoding='utf-8')
            for name in ['prototipo-portal-final', 'prototipo-feedback-final', 'prototipo-painel-final']:
                content = content.replace('../docs/figuras/' + name + '.jpg', 'figuras/final/' + name + '.jpg')
            destination.write_text(content, encoding='utf-8', newline='\n')
        else:
            shutil.copyfile(source, destination)
        staged.append(destination)
    for source in sorted((ROOT / 'docs/figuras').glob('*-final.jpg')):
        destination = STAGE / 'figuras/final' / source.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        staged.append(destination)
    readme = STAGE / 'LEIA-ME.md'
    readme.write_text('''# Fontes LaTeX do TCC

Arquivo principal: `tcc.tex`. Selecione XeLaTeX no editor ou no Overleaf.
O pacote preserva os textos do projeto e adapta somente os caminhos das três
imagens para que a pasta possa ser compilada independentemente do repositório.

Com Tectonic, execute nesta pasta:

```text
tectonic --keep-logs --keep-intermediates tcc.tex
```

Com uma distribuição TeX convencional, execute XeLaTeX, BibTeX e XeLaTeX
duas vezes, ou use `latexmk` com o arquivo de configuração incluído.
São necessários os pacotes abnTeX2 e os pacotes declarados em `fixos/pacotes.tex`.

A bibliografia usa `abntex2-alf-tcc.bst`, derivação identificada e com os avisos
de licença preservados. As letras dos anos são geradas automaticamente.
Não edite manualmente essas letras no campo de ano da bibliografia.

Os originais históricos de concepção permanecem no acervo externo identificado
no trabalho. A ficha catalográfica fornecida pelos autores está incluída como PDF
em pretextuais/. Os campos da data e dos membros convidados da banca ficam em branco.
O relatório CopySpider recebido foi analisado antes desta substituição da ficha
e dos campos da banca; o conteúdo do restante do trabalho permanece preservado.
A confirmação sobre a seção 3.3.1
e o Apêndice L foi informada por Julio; não equivale à aprovação da defesa.
''', encoding='utf-8', newline='\n')
    staged.append(readme)
    manifest = STAGE / 'manifesto-fontes.json'
    manifest.write_text(json.dumps({
        'main': 'tcc.tex', 'engine': 'XeLaTeX/Tectonic',
        'files': {str(p.relative_to(STAGE)).replace('\\', '/'): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in staged}}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    staged.append(manifest)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(OUTPUT, 'w', ZIP_DEFLATED) as archive:
        for p in staged:
            archive.write(p, p.relative_to(STAGE))
    with ZipFile(OUTPUT) as archive:
        assert archive.testzip() is None
    print(f'Fontes portáteis: {OUTPUT}; {len(staged)} arquivos.')


if __name__ == '__main__':
    main()
