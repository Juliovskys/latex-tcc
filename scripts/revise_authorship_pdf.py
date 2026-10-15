"""Revise authorship and scope statements in the authoritative medium-term PDF.

The LaTeX source that generated this 112-page version is not available in the
checkout.  This script therefore applies true PDF redactions to the affected
paragraphs and inserts the approved replacement text with Latin Modern fonts.
All other page content is preserved.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


FONT_DIR = Path(
    r"C:\Users\ferna\AppData\Local\Programs\MiKTeX\fonts\opentype\public\lm"
)

BODY_CSS = """
@font-face {
  font-family: LMRoman;
  src: url(lmroman10-regular.otf);
  font-weight: normal;
}
@font-face {
  font-family: LMRoman;
  src: url(lmroman10-bold.otf);
  font-weight: bold;
}
* {
  font-family: LMRoman;
  color: #000000;
}
body {
  margin: 0;
  padding: 0;
  font-size: 10pt;
  line-height: 1.34;
  text-align: justify;
}
p {
  margin: 0 0 6pt 0;
  text-indent: 22pt;
}
ul {
  margin: 1pt 0 6pt 12pt;
  padding-left: 12pt;
}
li {
  margin: 0 0 4pt 0;
  padding-left: 3pt;
}
"""

DENSE_BODY_CSS = BODY_CSS.replace("line-height: 1.34", "line-height: 1.22").replace(
    "margin: 0 0 6pt 0", "margin: 0 0 4pt 0"
).replace("margin: 1pt 0 6pt 12pt", "margin: 0 0 4pt 12pt").replace(
    "margin: 0 0 4pt 0", "margin: 0 0 2pt 0"
)

SECTION_BODY_CSS = BODY_CSS.replace("font-size: 10pt", "font-size: 10.5pt")
DENSE_SECTION_BODY_CSS = DENSE_BODY_CSS.replace(
    "font-size: 10pt", "font-size: 10.5pt"
)

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


def redact_and_insert(
    page: pymupdf.Page,
    redact_rect: pymupdf.Rect,
    insert_rect: pymupdf.Rect,
    html: str,
    css: str,
    archive: pymupdf.Archive,
    *,
    scale_low: float = 0.9,
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
            f"Replacement text did not fit page {page.number + 1}: "
            f"spare={spare}, scale={scale}"
        )
    return spare, scale


def revise(input_pdf: Path, output_pdf: Path) -> None:
    if not input_pdf.is_file():
        raise FileNotFoundError(input_pdf)
    if not FONT_DIR.is_dir():
        raise FileNotFoundError(FONT_DIR)

    document = pymupdf.open(input_pdf)
    if document.page_count != 112:
        raise ValueError(f"Expected 112 pages, found {document.page_count}")

    archive = pymupdf.Archive(str(FONT_DIR))

    # Printed page 35 / physical page 36: official titles and thematic split.
    split_html = """
<p>O tema inicial foi organizado pelo orientador em dois recortes. O
<strong>Trabalho 1</strong>, de Julio Cesar Gomes de Souza Crispim e Fernando
Gabriel dos Santos Carrijo, tem como título <em>“Avaliação Contextual de
Serviços Públicos Digitais: concepção e desenvolvimento de um sistema baseado
em indicadores de navegação e qualidade percebida”</em> e abrange avaliação
contextual, indicadores de navegação, CSAT, CES e modelos de qualidade
percebida. O <strong>Trabalho 2</strong>, de Wesley Pedrosa dos Santos,
intitula-se <em>“Avaliador de Serviços Públicos: proposta de sistema para
avaliação baseado em um indicador de advocacy do cidadão (Net promoter Score
adaptado)”</em>. O instrumento do segundo recorte não integra a especificação
vigente do Trabalho 1 e permanece neste documento somente nos registros
históricos identificados no Apêndice L.</p>
"""
    redact_and_insert(
        document[35],
        pymupdf.Rect(81, 660, 542, 820),
        pymupdf.Rect(85, 661, 538, 815),
        split_html,
        SECTION_BODY_CSS,
        archive,
        scale_low=0.95,
    )

    # Printed page 36 / physical page 37: shared activities and contribution.
    contribution_html = """
<p>As atividades de concepção parcialmente compartilhadas compreenderam o
alinhamento inicial do problema, a visão do produto, a delimitação por meio da
dinâmica É / Não É / Faz / Não Faz e o levantamento e a priorização iniciais de
funcionalidades e do MVP. Wesley participou somente de parte dessas atividades;
não participou de toda a Lean Inception nem da discussão das quatro
perspectivas apresentada a seguir.</p>

<p>A autoria intelectual do conteúdo discutido e registrado nesses artefatos
resulta de contribuições parciais de Julio e Fernando. Julio teve a maior
participação individual na formulação e na estrutura do TCC. Fernando realizou
a revisão e contribuiu parcialmente para essa formulação e estrutura, além de
produzir a elaboração visual das figuras históricas. A autoria da representação
gráfica, portanto, não deve ser confundida com autoria intelectual exclusiva do
conteúdo discutido.</p>

<p>As quatro perspectivas foram associadas às contribuições dos participantes,
sem lhes atribuir vínculo institucional ou condição de especialista
independente:</p>
<ul>
  <li><strong>Felipe</strong>, atendimento público, representando dúvidas recorrentes e dificuldades relatadas por cidadãos;</li>
  <li><strong>Lucas</strong>, gestão digital, representando indicadores acionáveis para priorização de melhorias;</li>
  <li><strong>Diassis</strong>, estudante da UnB, representando viabilidade técnica, escopo acadêmico, segurança e LGPD;</li>
  <li><strong>Bruno</strong>, estudante da UnB, representando experiência do usuário, jornada, clareza de interface e validação.</li>
</ul>

<p>Lucas, participante da discussão, e Lucas Almeida, persona fictícia da seção
4.3, são referências distintas. A colaboração parcial de Wesley nas atividades
compartilhadas de concepção é distinta dessa discussão e não lhe atribui autoria
do Trabalho 1 nem constitui avaliação independente. A dinâmica foi uma
atividade interna de alinhamento e delimitação, não uma validação externa, e não
substitui especificação de requisitos, teste de usabilidade ou avaliação por
especialistas independentes.</p>
"""
    redact_and_insert(
        document[36],
        pymupdf.Rect(81, 80, 542, 455),
        pymupdf.Rect(85, 84, 538, 455),
        contribution_html,
        DENSE_SECTION_BODY_CSS,
        archive,
        scale_low=0.95,
    )

    # Appendix A inventory: distinguish visual production from intellectual content.
    inventory_html = """
<p>Os quatro registros de visão, delimitação e funcionalidades tiveram
elaboração visual de Fernando Gabriel dos Santos Carrijo. Seu conteúdo
intelectual resulta das contribuições parciais de Julio e Fernando descritas na
seção 3.3.1. Reproduzidos no Apêndice L com seus arquivos originais, permitem
confrontar a síntese textual com os artefatos disponíveis, sem substituí-los por
imagens reconstruídas. A contextualização distingue esses registros das
decisões e capacidades da versão atual.</p>
"""
    redact_and_insert(
        document[78],
        pymupdf.Rect(81, 238, 542, 334),
        pymupdf.Rect(85, 241, 538, 334),
        inventory_html,
        BODY_CSS,
        archive,
        scale_low=0.98,
    )

    # Appendix L opening note: repeat the attribution where the records appear.
    historical_html = """
<p>Os quatro registros a seguir tiveram elaboração visual de Fernando Gabriel
dos Santos Carrijo. Seu conteúdo intelectual resulta das contribuições parciais
de Julio e Fernando descritas na seção 3.3.1. As imagens são reproduzidas sem
alteração; as datas individuais de produção não estão identificadas.</p>
"""
    redact_and_insert(
        document[107],
        pymupdf.Rect(81, 191, 542, 269),
        pymupdf.Rect(85, 195, 538, 269),
        historical_html,
        BODY_CSS,
        archive,
        scale_low=0.98,
    )

    caption_html = (
        "Fonte: elaboração visual de Fernando Gabriel dos Santos Carrijo; "
        "conteúdo intelectual de concepção atribuído parcialmente a Julio e "
        "Fernando, conforme a seção 3.3.1; data individual não identificada."
    )
    caption_regions = (
        (108, pymupdf.Rect(81, 434, 542, 467), pymupdf.Rect(85, 437, 538, 477)),
        (109, pymupdf.Rect(81, 573, 542, 606), pymupdf.Rect(85, 576, 538, 616)),
        (110, pymupdf.Rect(81, 428, 542, 460), pymupdf.Rect(85, 431, 538, 471)),
        (111, pymupdf.Rect(81, 638, 542, 670), pymupdf.Rect(85, 641, 538, 681)),
    )
    for page_index, redact_rect, insert_rect in caption_regions:
        redact_and_insert(
            document[page_index],
            redact_rect,
            insert_rect,
            caption_html,
            CAPTION_CSS,
            archive,
            scale_low=0.95,
        )

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    document.set_metadata(
        {
            **document.metadata,
            "modDate": pymupdf.get_pdf_now(),
        }
    )
    document.save(output_pdf, garbage=4, deflate=True, clean=True)
    document.close()

    check = pymupdf.open(output_pdf)
    if check.page_count != 112:
        raise RuntimeError("Page count changed during revision")
    combined = "\n".join(check[index].get_text() for index in (35, 36, 78, 107))
    # PyMuPDF may expose replacement-font diacritics differently from Poppler,
    # so these checks deliberately use stable ASCII fragments. Final textual
    # verification is also performed with pdftotext in the build workflow.
    required = (
        "O Trabalho 1",
        "O Trabalho 2",
        "Julio teve a maior",
        "Fernando Gabriel dos Santos Carrijo",
    )
    missing = [phrase for phrase in required if phrase not in combined]
    check.close()
    if missing:
        raise RuntimeError(f"Missing expected replacement text: {missing}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    revise(args.input_pdf.resolve(), args.output_pdf.resolve())


if __name__ == "__main__":
    main()
