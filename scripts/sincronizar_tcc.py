"""Sincroniza o manuscrito aprovado em docs/tcc.md com o modelo LaTeX.

Uso: python scripts/sincronizar_tcc.py --pandoc CAMINHO_DO_PANDOC
O Markdown e seu BibTeX são as fontes editoriais; não recria dados empíricos.
"""
import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADER = '% Gerado a partir de docs/tcc.md por scripts/sincronizar_tcc.py.\n'
WIDTHS = {
    1: [.28, .12, .60], 2: [.18, .23, .25, .34], 3: [.42, .58],
    4: [.19, .28, .29, .24], 5: [.16, .17, .25, .17, .25],
    6: [.17, .14, .17, .17, .35], 7: [.20, .30, .22, .28],
    8: [.15, .29, .30, .26], 9: [.16, .19, .21, .20, .24],
    10: [.18, .22, .26, .34], 11: [.19, .26, .20, .35],
    12: [.52, .24, .24], 13: [.19, .28, .27, .26],
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pandoc', default='pandoc')
    args = parser.parse_args()
    tokens = {}

    def token(latex):
        key = f'TCCLATEXTOKEN{len(tokens):05d}END'
        tokens[key] = latex
        return key

    def prepare(text):
        text = re.sub(r'<sup>([^<]+)</sup>',
                      lambda m: token('\\textsuperscript{' + m[1] + '}'), text)
        # Resolver grupos antes dos vínculos individuais para permitir sufixos a/b
        # pelo BibTeX, em vez de transportar anos renderizados manualmente.
        links = r'\[[^\]]+\]\(#ref-[^)]+\)'

        def citegroup(match):
            keys = re.findall(r'\(#ref-([^)]+)\)', match.group())
            return token('\\cite{' + ','.join(keys) + '}')

        text = re.sub(r'\((' + links + r')(?:;\s*' + links + r')*\)', citegroup, text)
        text = re.sub(r'\[([^\]]+)\]\(#ref-([^)]+)\)',
                      lambda m: token('\\citeonline{' + m[2] + '}'), text)
        text = re.sub(r'\[[^\]]+\]\(#((?:tab|fig|sec):[^)]+)\)',
                      lambda m: token('\\ref{' + m[1] + '}'), text)
        text = re.sub(r'^(#+)\s+(?:\d+(?:\.\d+)*|[A-G]\.\d+)\s+', r'\1 ', text, flags=re.M)
        text = re.sub(r'^# Apêndice [A-G] — ', '# ', text, flags=re.M)
        return text

    def pandoc(data, from_format, to_format):
        return subprocess.run(
            [args.pandoc, '-f', from_format, '-t', to_format,
             '--top-level-division=chapter', '--wrap=none'],
            input=data, text=True, encoding='utf-8', capture_output=True, check=True,
        ).stdout

    def writer(blocks, template):
        document = {'pandoc-api-version': template['pandoc-api-version'],
                    'meta': {}, 'blocks': blocks}
        latex = pandoc(json.dumps(document, ensure_ascii=False), 'json', 'latex')
        for key, value in tokens.items():
            latex = latex.replace(key, value)
        latex = latex.replace('Figma/Useberry', r'Figma/\allowbreak Useberry')
        for char, value in {'→': r'\ensuremath{\rightarrow}',
                            '≥': r'\ensuremath{\geq}',
                            '≤': r'\ensuremath{\leq}',
                            '×': r'\ensuremath{\times}'}.items():
            latex = latex.replace(char, value)
        return latex

    def plain(node):
        if isinstance(node, list):
            return ''.join(plain(item) for item in node)
        if not isinstance(node, dict):
            return ''
        if node['t'] == 'Str':
            return node['c']
        if node['t'] in ('Space', 'SoftBreak', 'LineBreak'):
            return ' '
        if node['t'] == 'Code':
            return node['c'][1]
        return plain(node.get('c', []))

    def raw(text):
        return {'t': 'RawBlock', 'c': ['latex', text]}

    def convert(text):
        doc = json.loads(pandoc(prepare(text), 'gfm+tex_math_dollars', 'json'))
        blocks = doc['blocks']
        output = []
        pending = None
        caption = None
        for block in blocks:
            if block['t'] == 'RawBlock' and block['c'][0] == 'html':
                match = re.fullmatch(r'<a id="([^"]+)"></a>', block['c'][1].strip())
                if match:
                    pending = match[1]
                continue
            if block['t'] == 'Header' and pending:
                block['c'][1][0] = pending
                pending = None
            if block['t'] == 'Para':
                html = ''.join(n['c'][1] for n in block['c']
                               if n['t'] == 'RawInline' and n['c'][0] == 'html')
                match = re.fullmatch(r'<a id="([^"]+)"></a>', html)
                if match:
                    pending = match[1]
                    continue
                content = plain(block['c'])
                if re.match(r'^Tabela \d+ — ', content):
                    caption = re.sub(r'^Tabela \d+ — ', '', content)
                    continue
                if re.match(r'^Figura \d+ — ', content) and block['c'][0]['t'] == 'Strong':
                    continue  # legenda já incorporada na figura
                image = next((n for n in block['c'] if n['t'] == 'Image'), None)
                if image:
                    attr, alt, destination = image['c']
                    title = re.sub(r'^Figura \d+ — ', '', plain(alt)).rstrip('.')
                    title_tex = writer([{'t': 'Plain', 'c': [{'t': 'Str', 'c': title}]}], doc).strip()
                    path = destination[0].removeprefix('../latex/')
                    output.append(raw('\\begin{figure}[htbp]\n\\centering\n'
                                      '\\includegraphics[width=\\textwidth,height=.70\\textheight,keepaspectratio]{' + path + '}\n'
                                      '\\caption{' + title_tex + '}\\label{' + pending + '}\n'))
                    pending = None
                    caption = 'figure-source'
                    continue
                if caption == 'figure-source' and content.startswith('Fonte:'):
                    source = writer([block], doc).strip()
                    output.append(raw('\\par\\small\\raggedright ' + source + '\n\\end{figure}'))
                    caption = None
                    continue
            if block['t'] == 'Table':
                if caption:
                    # Ordem editorial estável dos treze rótulos, validada ao final.
                    labels = re.findall(r'<a id="(tab:[^"]+)"></a>\s+\*\*Tabela (\d+)', text)
                    number = int(dict(labels)[pending])
                    block['c'][0][0] = pending
                    block['c'][1] = [None, [{'t': 'Plain', 'c': [{'t': 'Str', 'c': caption}]}]]
                    weights = WIDTHS[number]
                    pending = None
                    caption = None
                else:
                    weights = [1 / len(block['c'][2])] * len(block['c'][2])
                assert len(weights) == len(block['c'][2])
                for spec, width in zip(block['c'][2], weights):
                    spec[0] = {'t': 'AlignLeft'}
                    spec[1] = {'t': 'ColWidth', 'c': width}
                output.extend([raw('\\begingroup\\footnotesize\\SingleSpacing\n'
                                   '\\setlength{\\tabcolsep}{4pt}\n'
                                   '\\setlength{\\LTcapwidth}{\\textwidth}'), block, raw('\\endgroup')])
                continue
            output.append(block)
        assert pending is None and caption is None, (pending, caption)
        return HEADER + writer(output, doc)

    manuscript = (ROOT / 'docs/tcc.md').read_text(encoding='utf-8')
    pieces = re.split(r'(?m)^(# [^\n]+)\n', manuscript)
    sections = {pieces[i][2:]: pieces[i + 1] for i in range(1, len(pieces), 2)}
    editable = ROOT / 'latex/editaveis'
    for title, name in [('1 Introdução', 'introducao'), ('2 Referencial Teórico', 'referencialteorico'),
                        ('3 Metodologia', 'metodologia'), ('4 Desenvolvimento da Solução', 'desenvolvimento'),
                        ('5 Considerações Finais', 'consideracoes')]:
        (editable / (name + '.tex')).write_text(convert('# ' + title + '\n' + sections[title]), encoding='utf-8')
    for title, name in [('Resumo', 'resumo'), ('Abstract', 'abstract')]:
        content = sections[title]
        body, keywords = re.split(r'\*\*(?:Palavras-chave|Key-words)\*\*:', content)
        tex = convert(body) + '\n\\vspace{\\onelineskip}\n\\noindent '
        label = 'Palavras-chave' if title == 'Resumo' else 'Keywords'
        tex += '\\textbf{' + label + ':} ' + convert(keywords).removeprefix(HEADER)
        opening = '\\begin{resumo}' + ('[Abstract]' if title == 'Abstract' else '')
        tex = opening + '\n' + tex + '\\end{resumo}\n'
        if title == 'Abstract':
            tex = '\\begin{otherlanguage*}{english}\n' + tex + '\\end{otherlanguage*}\n'
        (editable / (name + '.tex')).write_text(HEADER + tex, encoding='utf-8')
    siglas = []
    for line in sections['Abreviaturas e siglas'].splitlines():
        if line.startswith('|'):
            cells = [c.strip() for c in line.strip('|').split('|')]
            if cells[0] != 'Sigla' and not cells[0].startswith('-'):
                siglas.append('\\item[' + cells[0] + '] ' + cells[1])
    (editable / 'abreviaturas.tex').write_text(HEADER + '\\begin{siglas}\n' + '\n'.join(siglas) + '\n\\end{siglas}\n', encoding='utf-8')
    appendices = [(title, body) for title, body in sections.items() if title.startswith('Apêndice ')]
    combined = '\n'.join('# ' + title + '\n' + body for title, body in appendices)
    (editable / 'apendices.tex').write_text(HEADER + '\\begin{apendicesenv}\n\\partapendices\n' + convert(combined) + '\\end{apendicesenv}\n', encoding='utf-8')
    listing = '\n'.join('\\item[' + title.split(' — ')[0] + '] ' + title.split(' — ')[1] + '.' for title, _ in appendices)
    (editable / 'listaapendices.tex').write_text(HEADER + '\\pdfbookmark[0]{Lista de apêndices}{listaapendices}\n\\chapter*{Lista de apêndices}\n\\begin{description}\n' + listing + '\n\\end{description}\n\\cleardoublepage\n', encoding='utf-8')
    shutil.copyfile(ROOT / 'docs/referencias-tcc.bib', ROOT / 'latex/bibliografia.bib')
    print('Sincronizados: 11 arquivos de conteúdo e bibliografia. Figuras e dados preservados.')


if __name__ == '__main__':
    main()
