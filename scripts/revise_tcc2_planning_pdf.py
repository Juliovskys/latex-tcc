"""Make the long-term recommendations explicit as planning for TCC 2.

The authoritative 112-page PDF has no matching LaTeX source in the checkout.
This script therefore performs true redactions only in the six affected
methodological passages and inserts the approved replacement text with Latin
Modern fonts.  Existing tables, figures, appendices, pagination and the prior
authorship revision are preserved.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


FONT_DIR = Path(
    r"C:\Users\ferna\AppData\Local\Programs\MiKTeX\fonts\opentype\public\lm"
)


def body_css(font_size: float = 10.0, line_height: float = 1.28) -> str:
    return f"""
@font-face {{
  font-family: LMRoman;
  src: url(lmroman10-regular.otf);
  font-weight: normal;
}}
@font-face {{
  font-family: LMRoman;
  src: url(lmroman10-bold.otf);
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
  margin: 0;
  text-indent: 22pt;
}}
"""


def redact_and_insert(
    page: pymupdf.Page,
    redact_rect: pymupdf.Rect,
    insert_rect: pymupdf.Rect,
    html: str,
    css: str,
    archive: pymupdf.Archive,
    *,
    scale_low: float = 0.90,
) -> tuple[float, float]:
    """Remove the old paragraph and insert the replacement in its place."""

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
            f"Replacement text did not fit physical page {page.number + 1}: "
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

    # Item 22 — printed page 39 / physical page 40.  The existing list of
    # dependent variables immediately below this paragraph is retained.
    hypothesis_html = """
<p>A comparação entre <em>feedback</em> contextual e formulário final é
reformulada como hipótese a ser testada no TCC 2. H1: o convite contextual
produz maior taxa de resposta e de conclusão do que o formulário apresentado
apenas ao final. H2: o convite contextual produz comentários mais específicos
sobre a etapa vivenciada. Antes da coleta, serão definidas as variáveis
dependentes: taxa de resposta, taxa de conclusão, esforço percebido,
qualidade/especificidade do comentário, interrupção provocada e percepção de
adequação do momento da pergunta. A avaliação atual não testou essas hipóteses;
os denominadores, as regras de codificação e os critérios de análise deverão
ser fixados no protocolo do TCC 2.</p>
"""
    redact_and_insert(
        document[39],
        pymupdf.Rect(81, 110, 542, 254),
        pymupdf.Rect(85, 113, 538, 255),
        hypothesis_html,
        body_css(10.0, 1.27),
        archive,
        scale_low=0.96,
    )

    # Item 23 — printed page 40 / physical page 41.
    heuristic_html = """
<p>O relato distingue três procedimentos. O primeiro é uma verificação
funcional interna da implementação. O segundo é denominado claramente
<strong>avaliação heurística interna/preliminar</strong>, pois foi conduzido
pelos próprios autores. O terceiro, realizado no Figma com oito cidadãos,
constitui teste exploratório de usabilidade e não verificação de API. Para o
TCC 2, planeja-se incluir avaliação heurística externa por especialistas e
mantê-la separada do teste de usabilidade com cidadãos. Não se afirma que essa
avaliação externa já tenha sido executada.</p>
"""
    redact_and_insert(
        document[40],
        pymupdf.Rect(81, 663, 542, 788),
        pymupdf.Rect(85, 666, 538, 790),
        heuristic_html,
        body_css(10.0, 1.27),
        archive,
        scale_low=0.96,
    )

    # Item 13 — printed page 96 / physical page 97.  Quadro 18 already lists
    # the planned test families and remains unchanged.
    validation_html = """
<p>Este plano prepara o TCC 2 e não relata a execução das atividades previstas.
A <strong>verificação do software</strong> responde se o sistema foi
construído corretamente diante dos requisitos e contratos; a
<strong>validação da solução</strong> investiga se o sistema resolve
adequadamente o problema em condições de uso. Conforme o escopo, o Quadro 18
prevê testes funcionais, de integração/API, usabilidade, acessibilidade,
desempenho e segurança. Os testes automatizados locais e o estudo histórico no
Figma são evidências parciais já disponíveis, mas não substituem as atividades
planejadas para o TCC 2.</p>
"""
    redact_and_insert(
        document[96],
        pymupdf.Rect(81, 582, 542, 655),
        pymupdf.Rect(85, 585, 538, 661),
        validation_html,
        body_css(9.4, 1.18),
        archive,
        scale_low=0.93,
    )

    # Item 18 — printed page 99 / physical page 100.
    accessibility_html = """
<p>A acessibilidade é incorporada como <strong>requisito de qualidade</strong>
e sua avaliação é prevista para o TCC 2. Isso é especialmente relevante em
serviços públicos, nos quais barreiras de acesso podem impedir o exercício de
direitos ou o cumprimento de obrigações, e o referencial reconhece
desigualdades de acesso, dispositivos e letramento digital. O Quadro 19 usa a
WCAG 2.2 para selecionar critérios compatíveis com o protótipo atual e definir
evidências futuras; não representa auditoria completa nem declaração de
conformidade AA.</p>
"""
    redact_and_insert(
        document[99],
        pymupdf.Rect(81, 535, 542, 610),
        pymupdf.Rect(85, 538, 538, 614),
        accessibility_html,
        body_css(9.25, 1.17),
        archive,
        scale_low=0.92,
    )

    # Item 19 — printed page 101 / physical page 102.
    perspectives_html = """
<p>Este apêndice planeja três perspectivas de avaliação para o TCC 2, sem
afirmar que tenham sido executadas: usuários/cidadãos, para experiência e
esforço; gestores públicos, para utilidade e acionabilidade dos indicadores; e
especialistas/engenheiros, para qualidade técnica, arquitetura, segurança e
usabilidade. A ausência de avaliação externa permanece reconhecida como
limitação do trabalho atual. Os protocolos são prospectivos e devem ser
detalhados antes da coleta. A amostra histórica de oito participantes informa
o refinamento dos instrumentos, mas não oferece poder inferencial para as
hipóteses H1 e H2.</p>
"""
    redact_and_insert(
        document[101],
        pymupdf.Rect(81, 194, 542, 286),
        pymupdf.Rect(85, 198, 538, 294),
        perspectives_html,
        body_css(9.7, 1.22),
        archive,
        scale_low=0.95,
    )

    # Item 15 — printed page 102 / physical page 103.  The detailed decision
    # rule, confusion matrix and metrics that follow are preserved.
    calibration_html = """
<p>Esta seção planeja a calibração dos sinais comportamentais; sua execução
depende de nova coleta no TCC 2. Deverá ser verificado se “muitos cliques”,
tempo elevado, retornos e abandono correspondem de fato à dificuldade
percebida pelo usuário. A análise confrontará os gatilhos com rótulos de
dificuldade para identificar verdadeiros positivos, falsos positivos,
verdadeiros negativos e falsos negativos. Os oito participantes históricos não
foram rotulados para essa finalidade. Assim, as regras e métricas descritas a
seguir constituem protocolo prospectivo, e não calibração já realizada.</p>
"""
    redact_and_insert(
        document[102],
        pymupdf.Rect(81, 524, 542, 634),
        pymupdf.Rect(85, 528, 538, 636),
        calibration_html,
        body_css(9.8, 1.22),
        archive,
        scale_low=0.95,
    )

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    # This script owns its explicit output path; remove a prior failed build so
    # PyMuPDF can write the corrected PDF deterministically.
    if output_pdf.exists():
        output_pdf.unlink()
    document.set_metadata(
        {
            **document.metadata,
            "title": (
                "Avaliação Contextual de Serviços Públicos Digitais — "
                "planejamento do TCC 2"
            ),
            "modDate": pymupdf.get_pdf_now(),
        }
    )
    document.save(output_pdf, garbage=4, deflate=True, clean=True)
    document.close()

    # Machine-check the page count and stable fragments in every replacement.
    check = pymupdf.open(output_pdf)
    if check.page_count != 112:
        raise RuntimeError("Page count changed during revision")
    combined = "\n".join(
        check[index].get_text() for index in (39, 40, 96, 99, 101, 102)
    )
    # PyMuPDF may expose a few replacement-font diacritics differently from
    # Poppler, so these checks use stable fragments.  The build workflow also
    # performs a complete pdftotext inspection with the correct accents.
    required = (
        "testada no TCC 2",
        "interna/preliminar",
        "construído corretamente",
        "requisito de qualidade",
        "perspectivas de avaliação para o TCC 2",
        "calibração dos sinais comportamentais",
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
