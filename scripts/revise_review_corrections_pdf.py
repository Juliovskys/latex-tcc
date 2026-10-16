"""Apply the review corrections to the current 112-page TCC PDF.

Corrections:
* H1 concerns response rate only; task completion remains a secondary outcome.
* The six inserted planning paragraphs use the normal body font size and margin.
* Corrupted ordinal and legal symbols are replaced throughout the PDF.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pymupdf


FONT_DIR = Path(
    r"C:\Users\ferna\AppData\Local\Programs\MiKTeX\fonts\opentype\public\lm"
)


def paragraph_css(line_height: float) -> str:
    """CSS close to the 12-point LaTeX body used in the source PDF."""

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
  font-size: 12pt;
  line-height: {line_height};
  text-align: justify;
}}
p {{
  margin: 0;
  text-indent: 35pt;
}}
"""


def redact_and_insert(
    page: pymupdf.Page,
    redact_rect: pymupdf.Rect,
    insert_rect: pymupdf.Rect,
    html: str,
    css: str,
    archive: pymupdf.Archive,
) -> tuple[float, float]:
    page.add_redact_annot(redact_rect, fill=(1, 1, 1), cross_out=False)
    page.apply_redactions(images=0, graphics=0)
    spare, scale = page.insert_htmlbox(
        insert_rect,
        html,
        css=css,
        archive=archive,
        scale_low=0.99,
        overlay=True,
    )
    if spare < 0 or scale < 0.99:
        raise RuntimeError(
            f"Replacement did not fit physical page {page.number + 1}: "
            f"spare={spare}, scale={scale}"
        )
    return spare, scale


def replace_words(
    page: pymupdf.Page,
    replacements: list[tuple[pymupdf.Rect, pymupdf.Point, str, float, str]],
) -> None:
    """Replace small corrupted words while preserving their original baselines."""

    for rect, _origin, _text, _size, _font in replacements:
        padded = pymupdf.Rect(rect.x0 - 0.35, rect.y0 - 0.5, rect.x1 + 0.35, rect.y1 + 0.5)
        page.add_redact_annot(padded, fill=(1, 1, 1), cross_out=False)
    page.apply_redactions(images=0, graphics=0)

    registered: set[str] = set()
    for _rect, origin, text, size, font_file in replacements:
        font_name = f"fix_{Path(font_file).stem.replace('-', '_')}"
        if font_name not in registered:
            page.insert_font(fontname=font_name, fontfile=str(FONT_DIR / font_file))
            registered.add(font_name)
        page.insert_text(
            origin,
            text,
            fontname=font_name,
            fontsize=size,
            color=(0, 0, 0),
            overlay=True,
        )


def revise(input_pdf: Path, output_pdf: Path) -> None:
    if not input_pdf.is_file():
        raise FileNotFoundError(input_pdf)
    if not FONT_DIR.is_dir():
        raise FileNotFoundError(FONT_DIR)

    document = pymupdf.open(input_pdf)
    if document.page_count != 112:
        raise ValueError(f"Expected 112 pages, found {document.page_count}")
    archive = pymupdf.Archive(str(FONT_DIR))

    # Item 22 - printed page 39 / physical page 40.
    # H1 has only response rate as its primary outcome.  Completion remains in
    # the retained list of dependent variables and in the secondary outcomes.
    hypothesis_html = """
<p>A comparação entre <em>feedback</em> contextual e formulário final é
reformulada como hipótese a ser testada no TCC 2. H1: o convite contextual
produz maior taxa de resposta do que o formulário apresentado apenas ao final.
H2: o convite contextual produz comentários mais específicos sobre a etapa
vivenciada. Antes da coleta, serão definidas as variáveis dependentes: taxa de
resposta, taxa de conclusão, esforço percebido, qualidade/especificidade do
comentário, interrupção provocada e percepção de adequação do momento da
pergunta. A avaliação atual não testou essas hipóteses; denominadores, regras de
codificação e critérios de análise deverão ser fixados no protocolo do TCC 2.</p>
"""
    redact_and_insert(
        document[39],
        pymupdf.Rect(81, 109, 542, 258),
        pymupdf.Rect(85, 112, 538, 259),
        hypothesis_html,
        paragraph_css(1.31),
        archive,
    )

    # Item 23 - printed page 40 / physical page 41.
    heuristic_html = """
<p>O relato distingue três procedimentos. O primeiro é uma verificação
funcional interna da implementação. O segundo é denominado claramente
<strong>avaliação heurística interna/preliminar</strong>, pois foi conduzido
pelos próprios autores. O terceiro, realizado no Figma com oito cidadãos,
constitui teste exploratório de usabilidade, não verificação de API. Para o TCC
2, planeja-se uma avaliação heurística externa por especialistas, separada do
teste de usabilidade com cidadãos. Não se afirma que essa avaliação externa já
tenha sido executada.</p>
"""
    redact_and_insert(
        document[40],
        pymupdf.Rect(81, 662, 542, 791),
        pymupdf.Rect(85, 665, 538, 792),
        heuristic_html,
        paragraph_css(1.24),
        archive,
    )

    # Item 13 - printed page 96 / physical page 97.
    validation_html = """
<p>Este plano prepara o TCC 2 e não relata a execução das atividades previstas.
A <strong>verificação do software</strong> pergunta se o sistema foi construído
corretamente conforme requisitos e contratos; a <strong>validação da
solução</strong> investiga se ele resolve adequadamente o problema em uso. O
Quadro 18 prevê testes funcionais, integração/API, usabilidade, acessibilidade,
desempenho e segurança. As evidências atuais são parciais e não substituem essas
atividades.</p>
"""
    redact_and_insert(
        document[96],
        pymupdf.Rect(81, 581, 542, 665),
        pymupdf.Rect(85, 584, 538, 666),
        validation_html,
        paragraph_css(1.12),
        archive,
    )

    # Item 18 - printed page 99 / physical page 100.
    accessibility_html = """
<p>A acessibilidade é incorporada como <strong>requisito de qualidade</strong>
e será avaliada no TCC 2. Isso é essencial em serviços públicos, pois barreiras
podem impedir o exercício de direitos ou o cumprimento de obrigações, e o
referencial reconhece desigualdades de acesso, dispositivos e letramento
digital. O Quadro 19 seleciona critérios da WCAG 2.2 e define evidências
futuras; não representa auditoria completa nem declaração de conformidade AA.</p>
"""
    redact_and_insert(
        document[99],
        pymupdf.Rect(81, 534, 542, 616),
        pymupdf.Rect(85, 537, 538, 617),
        accessibility_html,
        paragraph_css(1.12),
        archive,
    )

    # Item 19 - printed page 101 / physical page 102.
    perspectives_html = """
<p>Este apêndice planeja três perspectivas de avaliação para o TCC 2, sem
afirmar que tenham sido executadas: usuários/cidadãos, para experiência e
esforço; gestores públicos, para utilidade e acionabilidade dos indicadores; e
especialistas/engenheiros, para qualidade técnica, arquitetura, segurança e
usabilidade. A ausência de avaliação externa permanece como limitação atual.
Os protocolos são prospectivos e devem ser detalhados antes da coleta. A
amostra histórica de oito participantes auxilia o refinamento dos instrumentos,
mas não oferece poder inferencial para H1 e H2.</p>
"""
    redact_and_insert(
        document[101],
        pymupdf.Rect(81, 193, 542, 296),
        pymupdf.Rect(85, 197, 538, 298),
        perspectives_html,
        paragraph_css(1.18),
        archive,
    )

    # Item 15 - printed page 102 / physical page 103.
    calibration_html = """
<p>Esta seção planeja a calibração dos sinais comportamentais; sua execução
depende de nova coleta no TCC 2. Será verificado se muitos cliques, tempo
elevado, retornos e abandono correspondem à dificuldade percebida. A análise
confrontará os gatilhos com rótulos independentes para identificar verdadeiros
positivos, falsos positivos, verdadeiros negativos e falsos negativos. Os oito
participantes históricos não foram rotulados para essa finalidade. As regras e
métricas seguintes constituem protocolo prospectivo, não calibração já
realizada.</p>
"""
    redact_and_insert(
        document[102],
        pymupdf.Rect(81, 523, 542, 638),
        pymupdf.Rect(85, 527, 538, 640),
        calibration_html,
        paragraph_css(1.18),
        archive,
    )

    # Encoding repairs found by searching the complete extracted text.
    replace_words(
        document[51],
        [
            (pymupdf.Rect(493.4596, 218.8112, 510.3761, 230.7664), pymupdf.Point(493.4596, 228.1546), "13º", 11.9552, "lmroman12-regular.otf"),
            (pymupdf.Rect(84.9514, 236.7385, 101.8680, 248.6936), pymupdf.Point(84.9514, 246.0818), "11º", 11.9552, "lmroman12-regular.otf"),
            (pymupdf.Rect(348.2926, 254.6657, 365.2091, 266.6208), pymupdf.Point(348.2926, 264.0090), "14º", 11.9552, "lmroman12-regular.otf"),
            (pymupdf.Rect(502.1674, 254.6657, 519.0839, 266.6208), pymupdf.Point(502.1674, 264.0090), "12º", 11.9552, "lmroman12-regular.otf"),
            (pymupdf.Rect(323.7844, 385.8255, 340.7010, 397.7807), pymupdf.Point(323.7844, 395.1689), "13º", 11.9552, "lmroman12-regular.otf"),
        ],
    )
    replace_words(
        document[52],
        [
            (pymupdf.Rect(209.7920, 662.3241, 226.9476, 672.2867), pymupdf.Point(209.7920, 670.1102), "13º;", 9.9626, "lmroman10-regular.otf"),
            (pymupdf.Rect(278.4246, 662.3241, 292.8107, 672.2867), pymupdf.Point(278.4246, 670.1102), "14º", 9.9626, "lmroman10-regular.otf"),
            (pymupdf.Rect(209.7920, 698.1897, 226.9477, 708.1523), pymupdf.Point(209.7920, 705.9758), "11º;", 9.9626, "lmroman10-regular.otf"),
            (pymupdf.Rect(278.4246, 698.1897, 292.8107, 708.1523), pymupdf.Point(278.4246, 705.9758), "12º", 9.9626, "lmroman10-regular.otf"),
            (pymupdf.Rect(212.2827, 734.0553, 226.6687, 744.0179), pymupdf.Point(212.2827, 741.8414), "13º", 9.9626, "lmroman10-regular.otf"),
        ],
    )
    replace_words(
        document[98],
        [
            (pymupdf.Rect(213.3307, 349.7976, 224.3892, 361.7528), pymupdf.Point(213.3307, 359.1410), "6º", 11.9552, "lmroman12-regular.otf"),
            (pymupdf.Rect(410.1799, 367.7249, 416.0379, 379.6801), pymupdf.Point(410.1799, 377.0682), "§", 11.9552, "lmroman12-regular.otf"),
            (pymupdf.Rect(420.9635, 367.7249, 435.2738, 379.6801), pymupdf.Point(420.9635, 377.0682), "2º,", 11.9552, "lmroman12-regular.otf"),
        ],
    )

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    if output_pdf.exists():
        output_pdf.unlink()
    document.set_metadata(
        {
            **document.metadata,
            "title": (
                "Avaliação Contextual de Serviços Públicos Digitais - "
                "planejamento do TCC 2 revisado"
            ),
            "modDate": pymupdf.get_pdf_now(),
        }
    )
    document.save(output_pdf, garbage=4, deflate=True, clean=True)
    document.close()

    # Stable post-save checks.  Poppler performs the complete accented-text
    # check in the verification workflow.
    check = pymupdf.open(output_pdf)
    if check.page_count != 112:
        raise RuntimeError("Page count changed during revision")
    item22 = " ".join(check[39].get_text().split())
    if "maior taxa de resposta do que" not in item22:
        raise RuntimeError("Corrected H1 was not found")
    if "resposta e de conclusão" in item22:
        raise RuntimeError("Old compound H1 remains on page 40")
    check.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    revise(args.input_pdf.resolve(), args.output_pdf.resolve())


if __name__ == "__main__":
    main()
