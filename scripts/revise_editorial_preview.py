"""Create the editorially corrected 112-page preview used by the Markdown build.

The current checkout does not contain the LaTeX source that generated the
authoritative PDF.  This script therefore applies true redactions and inserts
only the approved editorial replacements.  Its output is an intermediate PDF
under tmp/pdfs; the user-facing deliverable is the page-image Markdown preview.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


FONT_DIR = Path(
    r"C:\Users\ferna\AppData\Local\Programs\MiKTeX\fonts\opentype\public\lm"
)


def paragraph_css(
    *,
    font_size: float = 12.0,
    line_height: float = 1.5,
    indent: float = 35.0,
) -> str:
    return f"""
@font-face {{
  font-family: LMRoman;
  src: url(lmroman12-regular.otf);
  font-weight: normal;
}}
@font-face {{
  font-family: LMRoman;
  src: url(lmroman12-bold.otf);
  font-weight: bold;
}}
* {{
  font-family: LMRoman;
  color: #000000;
}}
body {{
  margin: 0;
  padding: 0;
  font-size: {font_size}pt;
  line-height: {line_height};
  text-align: justify;
}}
p {{
  margin: 0 0 4pt 0;
  text-indent: {indent}pt;
}}
ul {{
  margin: 1pt 0 4pt 14pt;
  padding-left: 12pt;
}}
li {{
  margin: 0;
  padding-left: 2pt;
}}
"""


COMPACT_BODY_CSS = paragraph_css(font_size=10.5, line_height=1.34, indent=22)

CAPTION_CSS = """
@font-face {
  font-family: LMRoman;
  src: url(lmroman10-regular.otf);
  font-weight: normal;
}
* {
  font-family: LMRoman;
  color: #000000;
}
body {
  margin: 0;
  padding: 0;
  font-size: 9pt;
  line-height: 1.18;
  text-align: left;
}
"""

CENTER_CSS = """
@font-face {
  font-family: LMRoman;
  src: url(lmroman12-regular.otf);
  font-weight: normal;
}
* {
  font-family: LMRoman;
  color: #000000;
}
body {
  margin: 0;
  padding: 0;
  font-size: 12pt;
  line-height: 1.5;
  text-align: center;
}
"""

BIBLIOGRAPHY_CSS = """
@font-face {
  font-family: LMRoman;
  src: url(lmroman12-regular.otf);
  font-weight: normal;
}
@font-face {
  font-family: LMRoman;
  src: url(lmroman12-italic.otf);
  font-style: italic;
}
* {
  font-family: LMRoman;
  color: #000000;
}
body {
  margin: 0;
  padding: 0;
  font-size: 12pt;
  line-height: 1.25;
  text-align: left;
}
p {
  margin: 0 0 8pt 0;
}
.link {
  color: #2905c3;
}
"""


def redact_and_insert(
    page: pymupdf.Page,
    redact_rect: pymupdf.Rect,
    insert_rect: pymupdf.Rect,
    html: str,
    css: str,
    archive: pymupdf.Archive,
    *,
    scale_low: float = 0.99,
) -> tuple[float, float]:
    page.add_redact_annot(redact_rect, fill=(1, 1, 1), cross_out=False)
    page.apply_redactions(images=0, graphics=0)
    spare, scale = page.insert_htmlbox(
        insert_rect,
        html,
        css=css,
        archive=archive,
        scale_low=scale_low,
        overlay=True,
    )
    if spare < 0 or scale < scale_low:
        raise RuntimeError(
            f"Replacement did not fit physical page {page.number + 1}: "
            f"spare={spare}, scale={scale}"
        )
    return spare, scale


def replace_years(
    page: pymupdf.Page,
    replacements: tuple[tuple[str, str], ...],
    *,
    color: tuple[float, float, float],
) -> int:
    """Atomically replace same-width year labels and preserve their baselines."""

    found: list[tuple[pymupdf.Rect, str]] = []
    for old, new in replacements:
        found.extend((rect, new) for rect in page.search_for(old))
    if not found:
        return 0
    for rect, _new in found:
        page.add_redact_annot(
            pymupdf.Rect(rect.x0 - 0.35, rect.y0 - 0.5, rect.x1 + 0.35, rect.y1 + 0.5),
            fill=(1, 1, 1),
            cross_out=False,
        )
    page.apply_redactions(images=0, graphics=0)
    font_name = "year_fix_lmroman12"
    page.insert_font(
        fontname=font_name,
        fontfile=str(FONT_DIR / "lmroman12-regular.otf"),
    )
    for rect, new in found:
        page.insert_text(
            pymupdf.Point(rect.x0, rect.y1 - 2.6118),
            new,
            fontname=font_name,
            fontsize=11.9552,
            color=color,
            overlay=True,
        )
    return len(found)


def revise(input_pdf: Path, output_pdf: Path) -> None:
    if not input_pdf.is_file():
        raise FileNotFoundError(input_pdf)
    if not FONT_DIR.is_dir():
        raise FileNotFoundError(FONT_DIR)

    document = pymupdf.open(input_pdf)
    if document.page_count != 112:
        raise ValueError(f"Expected 112 pages, found {document.page_count}")
    archive = pymupdf.Archive(str(FONT_DIR))

    # Item 5 - physical page 3.  Remove the abnTeX example record and leave a
    # neutral marker until the BCE issues the definitive cataloguing record.
    catalog_html = """
<p>Ficha catalográfica a ser emitida pela Biblioteca Central (BCE) da
Universidade de Brasília.</p>
"""
    redact_and_insert(
        document[2],
        pymupdf.Rect(82, 524, 542, 789),
        pymupdf.Rect(135, 642, 460, 704),
        catalog_html,
        CENTER_CSS,
        archive,
    )

    # Items 1 and 3 - printed page 36 / physical page 37.  Use the normal
    # 12-point, one-and-a-half-spaced body style and the approved contribution
    # wording.  Concision keeps the following subsection on the same page.
    contribution_html = """
<p>As atividades de concepção parcialmente compartilhadas abrangeram o
alinhamento do problema, a visão do produto, a dinâmica É / Não É / Faz / Não
Faz e o levantamento e a priorização iniciais das funcionalidades e do MVP.
Wesley participou apenas de parte dessas atividades, não de toda a Lean
Inception nem da discussão das quatro perspectivas apresentada a seguir.</p>

<p>As figuras históricas tiveram elaboração visual de Fernando; seu conteúdo
resultou dessas atividades parcialmente compartilhadas, com contribuições de
Julio e Fernando e participação parcial de Wesley.</p>

<p>As quatro perspectivas foram associadas às contribuições dos participantes,
sem lhes atribuir vínculo institucional ou condição de especialista
independente:</p>
<ul>
  <li><strong>Felipe</strong>: atendimento público; dúvidas e dificuldades dos cidadãos;</li>
  <li><strong>Lucas</strong>: gestão digital; indicadores para priorizar melhorias;</li>
  <li><strong>Diassis</strong>: estudante da UnB; viabilidade técnica, escopo, segurança e LGPD;</li>
  <li><strong>Bruno</strong>: estudante da UnB; experiência, jornada, interface e validação.</li>
</ul>

<p>Lucas, participante da discussão, e Lucas Almeida, persona fictícia da seção
4.3, são referências distintas. A participação parcial de Wesley nas atividades
compartilhadas não lhe atribui autoria do Trabalho 1 nem constitui avaliação
independente. A dinâmica foi alinhamento interno, não validação externa, e não
substitui requisitos, teste de usabilidade ou avaliação por especialistas.</p>
"""
    redact_and_insert(
        document[36],
        pymupdf.Rect(81, 80, 542, 456),
        pymupdf.Rect(85, 84, 538, 458),
        contribution_html,
        paragraph_css(),
        archive,
        scale_low=0.985,
    )

    # Item 1 - inserted planning paragraphs now use the same 12-point,
    # one-and-a-half-spaced body style as the surrounding text.
    hypothesis_html = """
<p>A comparação entre <em>feedback</em> contextual e formulário final constitui
hipótese para o TCC 2. H1: o convite contextual produz maior taxa de resposta
que o formulário apresentado somente ao final. H2: o convite contextual produz
comentários mais específicos sobre a etapa vivenciada. Antes da coleta, serão
definidas as variáveis dependentes: taxas de resposta e de conclusão, esforço
percebido, qualidade/especificidade do comentário, interrupção provocada e
adequação do momento da pergunta. A avaliação atual não testou essas hipóteses;
denominadores, codificação e critérios de análise serão fixados no protocolo do
TCC 2.</p>
"""
    redact_and_insert(
        document[39],
        pymupdf.Rect(81, 109, 542, 258),
        pymupdf.Rect(85, 112, 538, 262),
        hypothesis_html,
        paragraph_css(),
        archive,
        scale_low=0.985,
    )

    heuristic_html = """
<p>O relato distingue três procedimentos: verificação funcional interna da
implementação; <strong>avaliação heurística interna/preliminar</strong>,
conduzida pelos autores; e teste exploratório de usabilidade no Figma com oito
cidadãos, que não corresponde à verificação de API. Para o TCC 2, planeja-se
avaliação heurística externa por especialistas, separada do teste de usabilidade
com cidadãos. Essa avaliação externa ainda não foi executada.</p>
"""
    redact_and_insert(
        document[40],
        pymupdf.Rect(81, 662, 542, 793),
        pymupdf.Rect(85, 665, 538, 798),
        heuristic_html,
        paragraph_css(),
        archive,
        scale_low=0.985,
    )

    perspectives_html = """
<p>Este apêndice planeja, para o TCC 2, três perspectivas de avaliação ainda não
executadas: cidadãos, para experiência e esforço; gestores públicos, para
utilidade dos indicadores; e especialistas/engenheiros, para qualidade técnica,
arquitetura, segurança e usabilidade. A falta de avaliação externa permanece
uma limitação. Os protocolos serão detalhados antes da coleta. Os oito
participantes históricos auxiliam os instrumentos, mas não dão poder
inferencial a H1 e H2.</p>
"""
    redact_and_insert(
        document[101],
        pymupdf.Rect(81, 193, 542, 297),
        pymupdf.Rect(85, 197, 538, 306),
        perspectives_html,
        paragraph_css(),
        archive,
        scale_low=0.985,
    )

    # Items 1 and 4 - correct spacing and add the direct Fawcett citation.
    calibration_html = """
<p>Esta seção planeja a calibração dos sinais comportamentais para nova coleta
no TCC 2. Será verificado se cliques, tempo, retornos e abandono correspondem à
dificuldade percebida. Os gatilhos serão comparados a rótulos independentes para
identificar verdadeiros positivos, falsos positivos, verdadeiros negativos e
falsos negativos (FAWCETT, 2006). Os oito participantes históricos não foram
rotulados para esse fim; portanto, trata-se de protocolo prospectivo, não
calibração realizada.</p>
"""
    redact_and_insert(
        document[102],
        pymupdf.Rect(81, 523, 542, 639),
        pymupdf.Rect(85, 527, 538, 648),
        calibration_html,
        paragraph_css(),
        archive,
        scale_low=0.985,
    )

    # Item 2 - consistent attribution in A.4, the Appendix L opening, and the
    # four historical figure captions.
    attribution_sentence = (
        "conteúdo resultante das atividades de concepção parcialmente "
        "compartilhadas (seção 3.3.1), com contribuições de Julio e Fernando e "
        "participação parcial de Wesley Pedrosa dos Santos"
    )
    inventory_html = f"""
<p>Os quatro registros de visão, delimitação e funcionalidades tiveram
elaboração visual de Fernando Gabriel dos Santos Carrijo e {attribution_sentence}.
Reproduzidos no Apêndice L em seus arquivos originais, permitem confrontar a
síntese textual com os artefatos disponíveis, sem substituí-los por imagens
reconstruídas. A contextualização distingue esses registros das decisões e
capacidades da versão atual.</p>
"""
    redact_and_insert(
        document[78],
        pymupdf.Rect(81, 238, 542, 334),
        pymupdf.Rect(85, 241, 538, 336),
        inventory_html,
        COMPACT_BODY_CSS,
        archive,
        scale_low=0.98,
    )

    historical_html = """
<p>Os quatro registros a seguir tiveram elaboração visual de Fernando. Seu
conteúdo resultou das atividades parcialmente compartilhadas da seção 3.3.1,
com contribuições de Julio e Fernando e participação parcial de Wesley. As
imagens são reproduzidas sem alteração; as datas individuais não estão
identificadas.</p>
"""
    redact_and_insert(
        document[107],
        pymupdf.Rect(81, 191, 542, 270),
        pymupdf.Rect(85, 195, 538, 273),
        historical_html,
        paragraph_css(),
        archive,
        scale_low=0.98,
    )

    caption_html = (
        "Fonte: elaboração visual de Fernando Gabriel dos Santos Carrijo; "
        f"{attribution_sentence}; data individual não identificada."
    )
    caption_regions = (
        (108, pymupdf.Rect(81, 434, 542, 469), pymupdf.Rect(85, 437, 538, 482)),
        (109, pymupdf.Rect(81, 573, 542, 608), pymupdf.Rect(85, 576, 538, 621)),
        (110, pymupdf.Rect(81, 428, 542, 462), pymupdf.Rect(85, 431, 538, 476)),
        (111, pymupdf.Rect(81, 638, 542, 672), pymupdf.Rect(85, 641, 538, 686)),
    )
    for page_index, redact_rect, insert_rect in caption_regions:
        redact_and_insert(
            document[page_index],
            redact_rect,
            insert_rect,
            caption_html,
            CAPTION_CSS,
            archive,
            scale_low=0.98,
        )

    # Item 6 - remap all Lima and Pereira modules, including in-text citations
    # and the source-classification list.
    link_blue = tuple(channel / 255 for channel in (41, 5, 195))
    mapping = {
        19: (("2020b", "2020d"),),
        23: (("2020c", "2020b"),),
        26: (("2020d", "2020c"),),
        29: (("2020b", "2020d"),),
        34: (
            ("2020c);", "2020b);"),
            ("2020d);", "2020c);"),
            ("2020b).", "2020d)."),
        ),
    }
    replaced = 0
    for page_index, changes in mapping.items():
        replaced += replace_years(document[page_index], changes, color=link_blue)
    if replaced != 8:
        raise RuntimeError(f"Expected 8 Lima/Pereira year replacements, found {replaced}")

    # Keep the bibliography itself in module order instead of preserving the
    # previous citation-order sequence (1, 4, 2, 3).
    bibliography_html = """
<p>LIMA, O. B. de; PEREIRA, W. C. <em>Avaliação da qualidade de serviços como
base para gestão e melhoria de serviços públicos:</em> Módulo 1: Visão geral
sobre serviços e avaliação de serviços públicos. Brasília, 2020a. Citado 4
vezes nas páginas <span class="link">19</span>, <span class="link">21</span>,
<span class="link">22</span> e <span class="link">34</span>.</p>

<p>LIMA, O. B. de; PEREIRA, W. C. <em>Avaliação da qualidade de serviços como
base para gestão e melhoria de serviços públicos:</em> Módulo 2: Histórico e
evolução dos modelos de avaliação de serviço. Brasília, 2020b. Citado 2 vezes
nas páginas <span class="link">23</span> e <span class="link">34</span>.</p>

<p>LIMA, O. B. de; PEREIRA, W. C. <em>Avaliação da qualidade de serviços como
base para gestão e melhoria de serviços públicos:</em> Módulo 3: Aplicação de
ferramentas de avaliação a um serviço específico. Brasília, 2020c. Citado 2
vezes nas páginas <span class="link">26</span> e <span class="link">34</span>.</p>

<p>LIMA, O. B. de; PEREIRA, W. C. <em>Avaliação da qualidade de serviços como
base para gestão e melhoria de serviços públicos:</em> Módulo 4: Melhoria dos
serviços públicos. Brasília, 2020d. Citado 3 vezes nas páginas
<span class="link">19</span>, <span class="link">29</span> e
<span class="link">34</span>.</p>
"""
    redact_and_insert(
        document[73],
        pymupdf.Rect(81, 244, 542, 451),
        pymupdf.Rect(85, 247, 538, 453),
        bibliography_html,
        BIBLIOGRAPHY_CSS,
        archive,
        scale_low=0.985,
    )

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    if output_pdf.exists():
        output_pdf.unlink()
    document.set_metadata({**document.metadata, "modDate": pymupdf.get_pdf_now()})
    document.save(output_pdf, garbage=4, deflate=True, clean=True)
    document.close()

    check = pymupdf.open(output_pdf)
    if check.page_count != 112:
        raise RuntimeError("Page count changed during editorial revision")
    combined = "\n".join(
        check[index].get_text()
        for index in (2, 34, 36, 39, 40, 78, 101, 102, 107, 108, 109, 110, 111)
    )
    required = (
        "a ser emitida pela Biblioteca Central",
        "elaboração visual de Fernando",
        "participação parcial de Wesley",
        "planeja, para o TCC 2, três perspectivas de avaliação",
        "FAWCETT, 2006",
        "2020a",
        "2020b",
        "2020c",
        "2020d",
    )
    missing = [phrase for phrase in required if phrase not in combined]
    check.close()
    if missing:
        raise RuntimeError(f"Missing corrected content: {missing}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    revise(args.input_pdf.resolve(), args.output_pdf.resolve())


if __name__ == "__main__":
    main()
