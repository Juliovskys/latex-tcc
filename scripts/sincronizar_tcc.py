"""Sincroniza o manuscrito aprovado em docs/tcc.md com o modelo LaTeX.

Uso: python scripts/sincronizar_tcc.py --pandoc CAMINHO_DO_PANDOC
O Markdown e seu BibTeX são as fontes editoriais; não recria dados empíricos.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = 'https://github.com/Juliovskys/latex-tcc'
ARCHIVE_COMMIT = 'd24af5d8ccfa088c7857983fe4d24b08af5337b0'
HEADER = '% Gerado a partir de docs/tcc.md por scripts/sincronizar_tcc.py.\n'
WIDTHS = {
    1: [.28, .12, .60], 2: [.18, .23, .25, .34], 3: [.42, .58],
    4: [.19, .28, .29, .24], 5: [.16, .17, .25, .17, .25],
    6: [.17, .14, .17, .17, .35], 7: [.20, .30, .22, .28],
    8: [.15, .29, .30, .26], 9: [.16, .19, .21, .20, .24],
    10: [.18, .22, .26, .34], 11: [.19, .26, .20, .35],
    12: [.52, .24, .24], 13: [.19, .28, .27, .26],
}
TABLE_LABELS = [
    'marcos-legais-avaliacao', 'posicionamento-solucoes', 'endpoints-prototipo',
    'formas-coleta-situada', 'sensibilidade-limiares', 'simulacao-sintetica-limiares',
    'regras-dificuldade', 'atributos-feedback', 'decisoes-design',
    'criterios-avaliacao-preliminar', 'avaliacao-heuristica-preliminar',
    'resultados-preliminares-fluxos', 'alternativas-design',
]
TABLE_WIDTHS = {'tab:' + label: WIDTHS[i] for i, label in enumerate(TABLE_LABELS, 1)}
TABLE_WIDTHS['tab:construtos-indicadores-dados'] = [.17, .25, .23, .35]
TABLE_WIDTHS.update({
    'qua:requisitos-funcionais': [.10, .29, .61],
    'qua:requisitos-nao-funcionais': [.10, .28, .62],
    'qua:rastreabilidade-software': [.15, .14, .27, .11, .33],
    'qua:catalogo-testes': [.08, .92],
    'qua:qualidade-produto': [.20, .25, .16, .39],
    'qua:plano-vv': [.08, .22, .44, .26],
    'qua:acessibilidade': [.25, .20, .55],
})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pandoc', default='pandoc')
    parser.add_argument('--sufixos-bbl', type=Path,
                        help='Harmoniza os anos exibidos no Markdown com os sufixos gerados pelo BibTeX.')
    args = parser.parse_args()
    if args.sufixos_bbl:
        bbl = args.sufixos_bbl.read_text(encoding='utf-8')
        years = dict(re.findall(r'\\bibitem\[[^\]]+\]\{([^}]+)\}\s*\\abntrefinfo\{[^\n]*\}\{(\d{4}[a-z]?)\}', bbl))
        assert years, 'Nenhum ano bibliográfico encontrado no BBL.'
        source = ROOT / 'docs/tcc.md'
        text = source.read_text(encoding='utf-8')
        def label(match):
            year = years.get(match[2])
            content = re.sub(r'\b' + year[:4] + r'[a-z]?\b', year, match[1]) if year else match[1]
            return '[' + content + '](#ref-' + match[2] + ')'
        text = re.sub(r'\[([^\]]+)\]\(#ref-([^)]+)\)', label, text)
        for key, year in years.items():
            pattern = r'(<a id="ref-' + re.escape(key) + r'"></a>\s*\n)(.*?)(?=\n<a id=|\n# Apêndice|\Z)'
            text = re.sub(pattern, lambda m: m[1] + re.sub(r'\b' + year[:4] + r'[a-z]\b', year, m[2]), text, flags=re.S)
        source.write_text(text, encoding='utf-8')
    tokens = {}

    def token(latex):
        key = f'TCCLATEXTOKEN{len(tokens):05d}END'
        tokens[key] = latex
        return key

    def prepare(text):
        # Os identificadores do sumário portátil são substituídos por rótulos
        # semânticos do LaTeX; podem estar no fim do capítulo anterior no MD.
        text = re.sub(r'<a id="secao-[^"]+"></a>\s*', '', text)
        text = re.sub(r'<sup>([^<]+)</sup>',
                      lambda m: token('\\textsuperscript{' + m[1] + '}'), text)
        # Resolver grupos antes dos vínculos individuais para permitir sufixos a/b
        # pelo BibTeX, em vez de transportar anos renderizados manualmente.
        links = r'\[[^\]]+\]\(#ref-[^)]+\)'

        def citegroup(match):
            keys = re.findall(r'\(#ref-([^)]+)\)', match.group())
            return token('\\cite{' + ','.join(keys) + '}')

        text = re.sub(r'\((' + links + r')(?:;\s*' + links + r')*\)', citegroup, text)
        def narrative_citation(match):
            locator = re.search(r',\s*((?:slide|p\.)\s*\d+(?:[–-]\d+)?)', match[1])
            option = '[' + locator[1] + ']' if locator else ''
            return token('\\citeonline' + option + '{' + match[2] + '}')
        text = re.sub(r'\[([^\]]+)\]\(#ref-([^)]+)\)', narrative_citation, text)
        text = re.sub(r'\[[^\]]+\]\(#((?:tab|qua|fig|sec):[^)]+)\)',
                      lambda m: token('\\ref{' + m[1] + '}'), text)
        # Remissões encadeadas e intervalos usam os mesmos rótulos dos títulos.
        def section_chain(match):
            return match[1] + ' ' + re.sub(
                r'\d+(?:\.\d+)*',
                lambda n: token('\\ref{sec:' + n[0].replace('.', '-') + '}'), match[2])
        text = re.sub(r'\b(seções|Seções)\s+(\d+(?:\.\d+)*(?:\s*(?:,|e|a|–|-)\s*\d+(?:\.\d+)*)+)',
                      section_chain, text)
        text = re.sub(r'\b(Apêndices|apêndices)\s+([A-L](?:\s*[–-]\s*[A-L]))',
                      lambda m: m[1] + ' ' + re.sub(r'[A-L]', lambda n: token(
                          '\\ref{sec:apendice-' + n[0].lower() + '}'), m[2]), text)
        # Remissões ainda escritas em texto puro também usam contadores.
        for (kind, number), label in CROSSREFS.items():
            text = re.sub(r'\b' + re.escape(kind) + r'\s+' + re.escape(number) + r'(?!\d|\.\d)',
                          lambda m, ident=label, word=kind: m[0] if re.match(r'\s+[—–]', text[m.end():])
                          else word + ' ' + token('\\ref{' + ident + '}'), text)
        def numbered_heading(match):
            level, number, title = match.groups()
            ident = 'sec:' + number.lower().replace('.', '-')
            return '<a id="' + ident + '"></a>\n\n' + level + ' ' + title
        text = re.sub(r'^(#+)\s+(\d+(?:\.\d+)*|[A-L](?:\.\d+)+)\s+(.+)$',
                      numbered_heading, text, flags=re.M)
        text = re.sub(r'^# Apêndice ([A-L]) — (.+)$',
                      lambda m: '<a id="sec:apendice-' + m[1].lower() + '"></a>\n\n# ' + m[2], text, flags=re.M)
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
        latex = latex.replace(r'\raggedright\arraybackslash', r'\RaggedRight\arraybackslash')
        for char, value in {'→': r'\ensuremath{\rightarrow}',
                            '≥': r'\ensuremath{\geq}',
                            '≤': r'\ensuremath{\leq}',
                            '×': r'\ensuremath{\times}'}.items():
            latex = latex.replace(char, value)
        return latex

    def inline_code(node):
        if isinstance(node, list):
            return [inline_code(item) for item in node]
        if not isinstance(node, dict):
            return node
        if node.get('t') == 'Str' and re.fullmatch(r'(?:RF|RNF|RN)\d+(?:/\d+)+[;,]?', node['c']):
            return {'t': 'RawInline', 'c': ['latex', node['c'].replace('/', r'/\allowbreak ')]}
        if node.get('t') == 'Code':
            escapes = {'\\': r'\textbackslash{}', '{': r'\{', '}': r'\}',
                       '_': r'\_', '#': r'\#', '$': r'\$', '%': r'\%',
                       '&': r'\&', '^': r'\textasciicircum{}', '~': r'\textasciitilde{}'}
            value = ''.join(escapes.get(char, char) for char in node['c'][1])
            if any(char in value for char in '≥≤→×'):
                return {'t': 'RawInline', 'c': ['latex', r'\texttt{' + value + '}']}
            return {'t': 'RawInline', 'c': ['latex', r'\texttt{\seqsplit{' + value + '}}']}
        if node.get('t') == 'Link':
            target = node['c'][2][0]
            if not re.match(r'^(?:https?://|#)', target):
                target = REPOSITORY + '/blob/' + ARCHIVE_COMMIT + '/docs/' + target
                node['c'][2][0] = target
        return {key: inline_code(value) for key, value in node.items()}

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
        aliases = []
        caption = None
        kind = None
        historical = False
        compact_feedback_list = False
        table_source = None
        for block in blocks:
            header_aliases = []
            if block['t'] == 'RawBlock' and block['c'][0] == 'html':
                match = re.fullmatch(r'<a id="([^"]+)"></a>', block['c'][1].strip())
                if match:
                    if pending:
                        aliases.append(pending)
                    pending = match[1]
                continue
            if block['t'] == 'Header' and pending:
                block['c'][1][0] = pending
                pending = None
                header_aliases, aliases = aliases, []
            if block['t'] == 'Header':
                compact_feedback_list = plain(block['c'][2]) == 'Feedback e painel'
                if plain(block['c'][2]) == 'Requisitos não funcionais':
                    # O quadro cabe inteiro quando a seção começa em página
                    # própria; evita uma última linha isolada após o rodapé.
                    output.append(raw('\\clearpage'))
                if block['c'][0] == 1:
                    historical = plain(block['c'][2]) == 'Registros históricos da concepção compartilhada'
                elif historical and block['c'][0] == 2:
                    output.append(raw('\\clearpage'))
            if compact_feedback_list and block['t'] == 'BulletList':
                # Os quatro campos já terminam em ponto e vírgula. Apresentá-los
                # em linha evita uma página com apenas o fim do apêndice B.
                fields = []
                for item in block['c']:
                    assert len(item) == 1 and item[0]['t'] in ('Plain', 'Para')
                    if fields:
                        fields.append({'t': 'Space'})
                    fields.extend(item[0]['c'])
                block = {'t': 'Para', 'c': fields}
            if block['t'] == 'Para':
                html = ''.join(n['c'][1] for n in block['c']
                               if n['t'] == 'RawInline' and n['c'][0] == 'html')
                match = re.fullmatch(r'<a id="([^"]+)"></a>', html)
                if match:
                    if pending:
                        aliases.append(pending)
                    pending = match[1]
                    continue
                content = plain(block['c'])
                if re.match(r'^(?:Tabela|Quadro) \d+ — ', content):
                    kind = content.split()[0]
                    caption = re.sub(r'^(?:Tabela|Quadro) \d+ — ', '', content)
                    continue
                if re.match(r'^Figura \d+ — ', content) and block['c'][0]['t'] == 'Strong':
                    continue  # legenda já incorporada na figura
                image = next((n for n in block['c'] if n['t'] == 'Image'), None)
                if image:
                    attr, alt, destination = image['c']
                    title = re.sub(r'^Figura \d+ — ', '', plain(alt)).rstrip('.')
                    title_tex = writer([{'t': 'Plain', 'c': [{'t': 'Str', 'c': title}]}], doc).strip()
                    absolute = (ROOT / 'docs' / destination[0]).resolve()
                    path = os.path.relpath(absolute, ROOT / 'latex').replace('\\', '/')
                    placement = '!ht' if historical else 'htbp'
                    output.append(raw('\\begin{figure}[' + placement + ']\n\\centering\n'
                                      '\\caption{' + title_tex + '}\\label{' + pending + '}\n'
                                      '\\includegraphics[width=\\textwidth,height=.70\\textheight,keepaspectratio]{' + path + '}\n'))
                    pending = None
                    caption = 'figure-source'
                    continue
                if caption == 'figure-source' and content.startswith('Fonte:'):
                    source = writer([block], doc).strip().removeprefix('Fonte:').strip()
                    output.append(raw('\\fonte{' + source + '}\n\\end{figure}'))
                    caption = None
                    continue
                if content.startswith('Fonte:'):
                    source = writer([block], doc).strip().removeprefix('Fonte:').strip()
                    if table_source is not None:
                        index, columns = table_source
                        # O último rodapé pertence à tabela: a fonte não pode
                        # migrar sozinha para a página seguinte.
                        footer = ('\\multicolumn{' + str(columns) + '}{@{}p{\\textwidth}@{}}{'
                                  '\\fonte{' + source + '}}\\tabularnewline\n\\endlastfoot')
                        output[index]['c'][1] = output[index]['c'][1].replace('\\endlastfoot', footer, 1)
                        table_source = None
                    else:
                        output.append(raw('\\fonte{' + source + '}'))
                    continue
            if block['t'] == 'Table':
                if pending == 'tab:regras-dificuldade':
                    # O quadro de três regras é lido como unidade. Evitar que
                    # sua última linha seja expulsa pelo rodapé da longtable.
                    output.append(raw('\\clearpage'))
                if caption:
                    weights = TABLE_WIDTHS.get(pending, [1 / len(block['c'][2])] * len(block['c'][2]))
                    block['c'][0][0] = pending
                    block['c'][1] = [None, [{'t': 'Plain', 'c': [{'t': 'Str', 'c': caption}]}]]
                    pending = None
                    caption = None
                else:
                    weights = [1 / len(block['c'][2])] * len(block['c'][2])
                assert len(weights) == len(block['c'][2])
                for spec, width in zip(block['c'][2], weights):
                    spec[0] = {'t': 'AlignLeft'}
                    spec[1] = {'t': 'ColWidth', 'c': width}
                table_tex = writer([inline_code(block)], doc)
                caption_text = writer([{'t':'Plain','c':block['c'][1][1][0]['c']}], doc).strip()
                if kind == 'Quadro':
                    # A legenda sem entrada automática não polui a lista de tabelas.
                    # A lista própria recebe a entrada dentro da legenda, já com o contador avançado.
                    table_tex = table_tex.replace('\\caption{', '\\caption[]{\\TCCquadroentry{' +
                                                  caption_text + '}', 1)
                    table_tex = '\\begin{TCCquadro}\n' + table_tex + '\\end{TCCquadro}\n'
                table_tex = table_tex.replace('\\endfirsthead\n', '\\endfirsthead\n\\caption[]{' +
                                              caption_text + ' (continuação)}\\tabularnewline\n', 1)
                table_source = (len(output) + 1, len(block['c'][2]))
                output.extend([raw('\\begingroup\\footnotesize\\SingleSpacing\n'
                                   '\\setlength{\\tabcolsep}{4pt}\n'
                                   '\\setlength{\\LTpre}{.6\\baselineskip}\n'
                                   '\\setlength{\\LTpost}{.4\\baselineskip}\n'
                                   '\\setlength{\\LTcapwidth}{\\textwidth}'), raw(table_tex), raw('\\endgroup')])
                kind = None
                continue
            output.append(inline_code(block))
            for alias in header_aliases:
                output.append(raw('\\label{' + alias + '}'))
        assert pending is None and caption is None, (pending, caption)
        return HEADER + writer(output, doc)

    manuscript = (ROOT / 'docs/tcc.md').read_text(encoding='utf-8')
    CROSSREFS = {(kind, number): ident for ident, kind, number in re.findall(
        r'<a id="((?:tab|qua|fig):[^"]+)"></a>\s*\n(?:\*\*)?(Tabela|Quadro|Figura) (\d+) —', manuscript)}
    for ident, number in re.findall(r'<a id="(fig:[^"]+)"></a>\s*\n!\[Figura (\d+)', manuscript):
        CROSSREFS['Figura', number] = ident
    for level, number in re.findall(r'^(#+) (\d+(?:\.\d+)*|[A-L](?:\.\d+)+) ', manuscript, re.M):
        if len(level) > 1:
            for word in ('seção', 'Seção', 'seções', 'Seções'):
                CROSSREFS[word, number] = 'sec:' + number.lower().replace('.', '-')
    for letter in re.findall(r'^# Apêndice ([A-L]) —', manuscript, re.M):
        CROSSREFS['Apêndice', letter] = 'sec:apendice-' + letter.lower()
    pieces = re.split(r'(?m)^(# [^\n]+)\n', manuscript)
    sections = {pieces[i][2:]: pieces[i + 1] for i in range(1, len(pieces), 2)}
    editable = ROOT / 'latex/editaveis'
    for title, name in [('1 Introdução', 'introducao'), ('2 Referencial Teórico', 'referencialteorico'),
                        ('3 Metodologia', 'metodologia'), ('4 Desenvolvimento da Solução', 'desenvolvimento'),
                        ('5 Considerações Finais', 'consideracoes')]:
        (editable / (name + '.tex')).write_text(convert('# ' + title + '\n' + sections[title]), encoding='utf-8')
    for title, name in [('Resumo', 'resumo'), ('Abstract', 'abstract')]:
        content = sections[title]
        body, keywords = re.split(r'\*\*(?:Palavras-chave|Keywords|Key-words)\*\*:', content)
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
    (editable / 'apendices.tex').write_text(HEADER + '\\begin{apendicesenv}\n\\setlength{\\parskip}{0pt}\n\\partapendices\n' + convert(combined) + '\\end{apendicesenv}\n', encoding='utf-8')
    listing = '\n'.join('\\item[' + title.split(' — ')[0] + '] ' + title.split(' — ')[1] +
                        '\\dotfill\\pageref{sec:apendice-' + title.split(' — ')[0][-1].lower() + '}'
                        for title, _ in appendices)
    (editable / 'listaapendices.tex').write_text(HEADER + '\\pdfbookmark[0]{Lista de apêndices}{listaapendices}\n\\chapter*{Lista de apêndices}\n\\begin{description}\n' + listing + '\n\\end{description}\n\\cleardoublepage\n', encoding='utf-8')
    shutil.copyfile(ROOT / 'docs/referencias-tcc.bib', ROOT / 'latex/bibliografia.bib')
    print('Sincronizados: 11 arquivos de conteúdo e bibliografia. Figuras e dados preservados.')


if __name__ == '__main__':
    main()
