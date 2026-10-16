"""Finalize the table/quadro layout of the authoritative 107-page TCC PDF.

The authoritative PDF contains revisions that are newer than the LaTeX source in
this checkout.  This script therefore preserves its text and pagination while:

* restoring closed vector grids only to Quadros 1--19 (including the H.5 matrix);
* keeping Tabelas 1 and 2 in the open IBGE-style layout;
* correcting the Quadro 3 prose reference;
* marking the first and final fragments of split elements as ``continua`` and
  ``conclusão``;
* removing the standalone ``Apêndices`` divider and its generic TOC entry;
* decrementing the affected displayed page numbers, lists, TOC destinations and
  PDF bookmarks.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import pdfplumber
import pymupdf


FONT_DIR = Path(
    r"C:\Users\ferna\AppData\Local\Programs\MiKTeX\fonts\opentype\public\lm"
)
TEXT_LEFT = 85.0
TEXT_RIGHT = 538.3


@dataclass(frozen=True)
class GridFragment:
    label: str
    page: int
    top: float
    header_bottom: float
    bottom: float | None
    columns: tuple[float, ...]
    rows: tuple[float, ...]


# Coordinates are measured in PDF points from TCC_Avaliacao_Contextual.pdf.
# Tabelas 1 and 2 are deliberately absent: only textual quadros receive grids.
FRAGMENTS = (
    GridFragment("Quadro 1", 26, 405.1, 423.3, 608.8, (85.0, 215.4, 275.8), (427.3, 451.2, 475.1, 499.0, 534.9, 570.7)),
    GridFragment("Quadro 2", 31, 103.0, 131.7, 377.0, (85.0, 170.2, 276.9, 392.3), (135.7, 171.6, 219.4, 255.3, 291.1)),
    GridFragment("Quadro 3", 43, 155.0, 183.6, 680.0, (85.0, 165.9, 281.2, 388.0), (187.6, 295.2, 355.0, 438.7, 522.4, 606.1)),
    GridFragment("Quadro 4", 50, 202.3, 220.4, 453.7, (85.0, 280.0), (224.7, 236.6, 248.6, 272.5, 308.4, 320.3, 344.2, 356.2, 380.1, 404.0, 416.0, 427.9)),
    GridFragment("Quadro 5", 51, 494.1, 522.8, 709.1, (85.0, 174.5, 302.7, 435.2), (526.8, 562.6, 611.2, 659.1)),
    GridFragment("Quadro 6", 52, 488.4, 506.6, 632.3, (85.0, 160.4, 240.0, 353.3, 432.9), (510.5, 546.4, 594.2)),
    GridFragment("Quadro 7", 54, 103.0, 121.2, 235.0, (85.0, 178.8, 315.6, 418.0), (125.2, 161.0, 196.9)),
    GridFragment("Quadro 8", 55, 226.1, 254.8, 548.7, (85.0, 157.3, 289.8, 426.6), (258.8, 306.6, 354.4, 415.0, 450.9, 498.7)),
    GridFragment("Quadro 9", 56, 172.3, 201.0, 446.3, (85.0, 160.4, 248.4, 344.9, 437.1), (205.0, 264.8, 312.6, 360.4)),
    GridFragment("Quadro 10 - parte 1", 59, 617.2, 645.9, None, (85.0, 170.2, 272.6, 392.3), (649.9, 709.7)),
    GridFragment("Quadro 10 - parte 2", 60, 103.6, 132.3, 437.4, (85.0, 170.2, 272.6, 392.3), (136.3, 220.0, 267.8, 303.7, 399.3)),
    GridFragment("Quadro 11 - parte 1", 60, 603.1, 631.8, None, (85.0, 174.5, 294.1, 388.0), (635.8, 683.6, 731.4)),
    GridFragment("Quadro 11 - parte 2", 61, 103.6, 132.3, 329.8, (85.0, 174.5, 294.1, 388.0), (136.3, 172.1, 208.0, 231.9, 279.7)),
    GridFragment("Quadro 12 - parte 1", 64, 462.2, 490.9, None, (85.0, 174.5, 302.7, 426.6), (494.9, 554.7, 590.5, 626.4, 686.2, 746.0)),
    GridFragment("Quadro 12 - parte 2", 65, 103.6, 132.3, 186.3, (85.0, 174.5, 302.7, 426.6), (136.3,)),
    GridFragment("Quadro 13 - parte 1", 89, 352.5, 370.7, None, (85.0, 136.7, 271.5), (374.7, 410.5, 434.4, 470.3, 506.2, 542.0, 589.9, 625.7, 661.6, 709.4, 745.3)),
    GridFragment("Quadro 13 - parte 2", 90, 103.6, 121.7, 163.8, (85.0, 136.7, 271.5), (125.7,)),
    GridFragment("Quadro 14", 91, 149.5, 167.6, 640.1, (85.0, 136.7, 267.1), (171.6, 207.5, 243.4, 279.2, 327.1, 362.9, 398.8, 434.6, 470.5, 518.3, 566.2, 602.0)),
    GridFragment("Quadro 15 - parte 1", 93, 280.9, 309.4, None, (85.0, 156.1, 223.1, 344.9, 399.2), (313.4, 397.1, 456.9, 540.6, 612.3, 660.1)),
    GridFragment("Quadro 15 - parte 2", 94, 103.6, 132.2, 509.0, (85.0, 156.1, 223.1, 344.9, 399.2), (136.2, 219.9, 279.6, 351.4, 399.2, 423.1, 459.0)),
    GridFragment("Quadro 16 - parte 1", 94, 738.7, 756.9, None, (85.0, 128.5), (760.9,)),
    GridFragment("Quadro 16 - parte 2", 95, 103.6, 121.7, 558.3, (85.0, 128.5), (125.7, 149.6, 173.5, 197.5, 221.4, 245.3, 269.2, 293.1, 317.0, 340.9, 364.8, 388.7, 412.7, 436.6, 460.5, 484.4, 508.3, 532.2)),
    GridFragment("Quadro 17 - parte 1", 96, 476.9, 517.4, None, (85.0, 178.8, 294.1, 370.8), (521.4, 581.2, 641.0, 688.8)),
    GridFragment("Quadro 17 - parte 2", 97, 103.6, 144.1, 413.3, (85.0, 178.8, 294.1, 370.8), (148.1, 207.9, 279.6, 327.5)),
    GridFragment("Quadro 18", 98, 103.0, 121.2, 569.7, (85.0, 127.3, 229.7, 426.6), (125.2, 173.0, 220.8, 268.6, 304.5, 352.3, 388.2, 424.1, 459.9, 495.8)),
    GridFragment("Quadro 19 - parte 1", 100, 621.5, 650.1, None, (85.0, 202.3, 297.7), (654.0, 678.0, 701.9, 725.8, 749.7, 773.6)),
    GridFragment("Quadro 19 - parte 2", 101, 103.6, 132.2, 186.2, (85.0, 202.3, 297.7), (136.2, 160.1)),
)


CAPTION_REPLACEMENTS = (
    (59, "Quadro 10 – Critérios", "Quadro 10 – Critérios da avaliação preliminar do protótipo (continua)"),
    (60, "Quadro 10 – Critérios", "Quadro 10 – Critérios da avaliação preliminar do protótipo (conclusão)"),
    (60, "Quadro 11 – Avaliação", "Quadro 11 – Avaliação heurística interna/preliminar do protótipo (continua)"),
    (61, "Quadro 11 – Avaliação", "Quadro 11 – Avaliação heurística interna/preliminar do protótipo (conclusão)"),
    (62, "Tabela 2 – Resultados", "Tabela 2 – Resultados exploratórios por fluxo de avaliação (continua)"),
    (63, "Tabela 2 – Resultados", "Tabela 2 – Resultados exploratórios por fluxo de avaliação (conclusão)"),
    (64, "Quadro 12 – Alternativas", "Quadro 12 – Alternativas de design consideradas no MVP (continua)"),
    (65, "Quadro 12 – Alternativas", "Quadro 12 – Alternativas de design consideradas no MVP (conclusão)"),
    (89, "Quadro 13 – Requisitos", "Quadro 13 – Requisitos funcionais (continua)"),
    (90, "Quadro 13 – Requisitos", "Quadro 13 – Requisitos funcionais (conclusão)"),
    (93, "Quadro 15 – Necessidades", "Quadro 15 – Necessidades, requisitos, componentes e evidências (continua)"),
    (94, "Quadro 15 – Necessidades", "Quadro 15 – Necessidades, requisitos, componentes e evidências (conclusão)"),
    (94, "Quadro 16 – Casos", "Quadro 16 – Casos automatizados identificáveis (continua)"),
    (95, "Quadro 16 – Casos", "Quadro 16 – Casos automatizados identificáveis (conclusão)"),
    (96, "Quadro 17 – Características", "Quadro 17 – Características selecionadas e evidências (continua)"),
    (97, "Quadro 17 – Características", "Quadro 17 – Características selecionadas e evidências (conclusão)"),
    (100, "Quadro 19 – Critérios", "Quadro 19 – Critérios de acessibilidade e verificações previstas (continua)"),
    (101, "Quadro 19 – Critérios", "Quadro 19 – Critérios de acessibilidade e verificações previstas (conclusão)"),
)


def nearest_rule(page: pdfplumber.page.Page, expected_top: float):
    candidates = [
        line
        for line in page.lines
        if line["width"] > 300 and abs(line["top"] - expected_top) <= 1.1
    ]
    if len(candidates) != 1:
        raise ValueError(
            f"Expected one horizontal rule near y={expected_top}, found {len(candidates)}"
        )
    return candidates[0]


def words_in_fragment(page, fragment: GridFragment, end_top: float):
    left = fragment.columns[0] - 0.75
    right = nearest_rule(page, fragment.top)["x1"] + 0.75
    return [
        word
        for word in page.extract_words(x_tolerance=1, y_tolerance=1)
        if fragment.header_bottom < word["top"] < end_top
        and left < word["x0"] < right
    ]


def resolve_geometry(page, fragment: GridFragment):
    top_rule = nearest_rule(page, fragment.top)
    header_rule = nearest_rule(page, fragment.header_bottom)

    if fragment.bottom is None:
        body_words = words_in_fragment(page, fragment, 815.0)
        if not body_words:
            raise ValueError(f"No body words found for {fragment.label}")
        bottom_top = min(815.0, max(word["bottom"] for word in body_words) + 4.0)
    else:
        bottom_top = nearest_rule(page, fragment.bottom)["top"]

    body_words = words_in_fragment(page, fragment, bottom_top + 0.5)
    if not body_words:
        raise ValueError(f"No body words found for {fragment.label}")

    padding = 6.0
    left = fragment.columns[0] - padding
    right = top_rule["x1"] + padding
    verticals = (left,) + tuple(x - padding for x in fragment.columns[1:]) + (right,)

    row_rules = []
    for current_start, next_start in zip(fragment.rows, fragment.rows[1:]):
        current_words = [
            word
            for word in body_words
            if current_start - 1.5 <= word["top"] < next_start - 1.5
        ]
        if not current_words:
            raise ValueError(
                f"Unable to determine row boundary in {fragment.label}: "
                f"{current_start} -> {next_start}"
            )
        last_bottom = max(word["bottom"] for word in current_words)
        if last_bottom >= next_start:
            raise ValueError(
                f"Row overlap in {fragment.label}: {last_bottom} >= {next_start}"
            )
        row_rules.append((last_bottom + next_start) / 2.0)

    region_words = [
        word
        for word in page.extract_words(x_tolerance=1, y_tolerance=1)
        if top_rule["top"] < word["top"] < bottom_top
        and left < word["x0"] < right
    ]
    for x in verticals:
        collisions = [
            word
            for word in region_words
            if word["x0"] + 0.25 < x < word["x1"] - 0.25
        ]
        if collisions:
            raise ValueError(
                f"Vertical rule intersects text in {fragment.label} at x={x}: "
                f"{collisions[0]['text']}"
            )
    for y in row_rules:
        collisions = [
            word
            for word in region_words
            if word["top"] + 0.25 < y < word["bottom"] - 0.25
        ]
        if collisions:
            raise ValueError(
                f"Horizontal rule intersects text in {fragment.label} at y={y}: "
                f"{collisions[0]['text']}"
            )

    return {
        "left": left,
        "right": right,
        "top": top_rule["top"],
        "header_bottom": header_rule["top"],
        "bottom": bottom_top,
        "verticals": verticals,
        "row_rules": tuple(row_rules),
    }


def draw_grid(page: pymupdf.Page, geometry) -> None:
    shape = page.new_shape()
    left = geometry["left"]
    right = geometry["right"]
    top = geometry["top"]
    bottom = geometry["bottom"]
    for y in (top, geometry["header_bottom"], *geometry["row_rules"], bottom):
        shape.draw_line((left, y), (right, y))
    for x in geometry["verticals"]:
        shape.draw_line((x, top), (x, bottom))
    shape.finish(color=(0, 0, 0), width=0.45)
    shape.commit(overlay=True)


def find_block_rect(page: pymupdf.Page, marker: str) -> pymupdf.Rect:
    matches = []
    for block in page.get_text("blocks"):
        text = " ".join(block[4].split())
        if marker in text:
            matches.append(pymupdf.Rect(block[:4]))
    if len(matches) != 1:
        raise ValueError(
            f"Expected one block containing {marker!r} on physical page "
            f"{page.number + 1}, found {len(matches)}"
        )
    return matches[0]


def font_on_page(page: pymupdf.Page, key: str, filename: str) -> pymupdf.Font:
    font_path = FONT_DIR / filename
    if not font_path.is_file():
        raise FileNotFoundError(font_path)
    page.insert_font(fontname=key, fontfile=str(font_path))
    return pymupdf.Font(fontfile=str(font_path))


def replace_caption(page: pymupdf.Page, marker: str, new_text: str) -> None:
    rect = find_block_rect(page, marker)
    redaction = pymupdf.Rect(TEXT_LEFT, rect.y0 - 1.4, TEXT_RIGHT, rect.y1 + 1.4)
    page.add_redact_annot(redaction, fill=(1, 1, 1), cross_out=False)
    page.apply_redactions(images=0, graphics=0)
    font_key = "caption_lmroman10"
    font = font_on_page(page, font_key, "lmroman10-regular.otf")
    size = 9.9626
    width = font.text_length(new_text, fontsize=size)
    available = TEXT_RIGHT - TEXT_LEFT
    if width > available:
        raise ValueError(
            f"Caption does not fit page {page.number + 1}: {new_text!r}"
        )
    x = TEXT_LEFT + (available - width) / 2.0
    baseline = rect.y1 - size * 0.2185
    page.insert_text(
        (x, baseline),
        new_text,
        fontname=font_key,
        fontsize=size,
        color=(0, 0, 0),
        overlay=True,
    )


def replace_phrase(page: pymupdf.Page, old: str, new: str) -> None:
    matches = page.search_for(old)
    if len(matches) != 1:
        raise ValueError(
            f"Expected one occurrence of {old!r} on physical page "
            f"{page.number + 1}, found {len(matches)}"
        )
    rect = matches[0]
    page.add_redact_annot(
        pymupdf.Rect(rect.x0 - 0.4, rect.y0 - 0.5, rect.x1 + 0.4, rect.y1 + 0.5),
        fill=(1, 1, 1),
        cross_out=False,
    )
    page.apply_redactions(images=0, graphics=0)
    font_key = "body_lmroman12"
    font_on_page(page, font_key, "lmroman12-regular.otf")
    size = 11.9552
    page.insert_text(
        (rect.x0, rect.y1 - size * 0.2185),
        new,
        fontname=font_key,
        fontsize=size,
        color=(0, 0, 0),
        overlay=True,
    )


def replace_number(
    page: pymupdf.Page,
    word: dict,
    new_number: int,
    *,
    fontsize: float,
    font_filename: str,
    font_key: str,
) -> None:
    rect = pymupdf.Rect(word["x0"], word["top"], word["x1"], word["bottom"])
    page.add_redact_annot(
        pymupdf.Rect(rect.x0 - 0.5, rect.y0 - 0.45, rect.x1 + 0.5, rect.y1 + 0.45),
        fill=(1, 1, 1),
        cross_out=False,
    )
    page.apply_redactions(images=0, graphics=0)
    font = font_on_page(page, font_key, font_filename)
    text = str(new_number)
    x = rect.x1 - font.text_length(text, fontsize=fontsize)
    baseline = rect.y1 - fontsize * 0.2185
    page.insert_text(
        (x, baseline),
        text,
        fontname=font_key,
        fontsize=fontsize,
        color=(0, 0, 0),
        overlay=True,
    )


def collect_page_number_words(layout_document):
    selections: dict[int, list[dict]] = {}

    def select(page_number: int, predicate) -> None:
        words = layout_document.pages[page_number - 1].extract_words(
            x_tolerance=1, y_tolerance=1
        )
        chosen = [w for w in words if w["text"].isdigit() and predicate(w)]
        selections.setdefault(page_number, []).extend(chosen)

    # List of quadros: only appendix quadros move one page earlier.
    select(8, lambda w: w["x0"] > 515 and int(w["text"]) >= 88)
    # List of appendices.
    select(10, lambda w: w["x0"] > 515 and int(w["text"]) >= 78)
    # General contents, excluding the generic APÊNDICES line removed separately.
    select(14, lambda w: w["x0"] > 515 and w["top"] >= 711 and int(w["text"]) >= 78)
    select(15, lambda w: w["x0"] > 515 and int(w["text"]) >= 80)
    select(16, lambda w: w["x0"] > 515 and int(w["text"]) >= 96)
    # Printed page numbers of every appendix page.
    for page_number in range(79, 108):
        select(
            page_number,
            lambda w: w["x0"] > 515 and w["top"] < 70,
        )
    return selections


def remove_generic_appendices_entry(page: pymupdf.Page) -> None:
    rect = pymupdf.Rect(140, 675.5, 540, 698.5)
    page.add_redact_annot(rect, fill=(1, 1, 1), cross_out=False)
    page.apply_redactions(images=0, graphics=0)
    for link in page.get_links():
        source = link.get("from")
        if source is not None and pymupdf.Rect(source).intersects(rect):
            page.delete_link(link)


def adjust_bookmarks(document: pymupdf.Document) -> None:
    adjusted = []
    for level, title, page_number in document.get_toc(simple=True):
        normalized = title.strip().casefold()
        if normalized in {"apêndices", "apendices"}:
            continue
        adjusted.append([level, title, page_number])
    document.set_toc(adjusted)


def finalize(input_pdf: Path, output_pdf: Path) -> None:
    if not input_pdf.is_file():
        raise FileNotFoundError(input_pdf)
    if not FONT_DIR.is_dir():
        raise FileNotFoundError(FONT_DIR)

    with pdfplumber.open(input_pdf) as layout:
        if len(layout.pages) != 107:
            raise ValueError(f"Expected 107 pages, found {len(layout.pages)}")
        geometries = {
            fragment: resolve_geometry(layout.pages[fragment.page - 1], fragment)
            for fragment in FRAGMENTS
        }
        number_words = collect_page_number_words(layout)

    document = pymupdf.open(input_pdf)

    replace_phrase(document[42], "A tabela explicita", "O quadro explicita")
    for page_number, marker, replacement in CAPTION_REPLACEMENTS:
        replace_caption(document[page_number - 1], marker, replacement)

    remove_generic_appendices_entry(document[13])

    for page_number, words in number_words.items():
        page = document[page_number - 1]
        for word in words:
            old_value = int(word["text"])
            if page_number >= 79 and word["top"] < 70:
                replace_number(
                    page,
                    word,
                    old_value - 1,
                    fontsize=9.9626,
                    font_filename="lmroman10-regular.otf",
                    font_key="page_number_lmroman10",
                )
            else:
                replace_number(
                    page,
                    word,
                    old_value - 1,
                    fontsize=11.9552,
                    font_filename="lmroman12-regular.otf",
                    font_key="toc_number_lmroman12",
                )

    for fragment, geometry in geometries.items():
        draw_grid(document[fragment.page - 1], geometry)

    adjust_bookmarks(document)
    document.delete_page(77)  # physical page 78: standalone "Apêndices"

    metadata = document.metadata
    metadata["modDate"] = pymupdf.get_pdf_now()
    document.set_metadata(metadata)
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    if output_pdf.exists():
        output_pdf.unlink()
    document.save(output_pdf, garbage=4, deflate=True, clean=True)
    document.close()

    check = pymupdf.open(output_pdf)
    if check.page_count != 106:
        raise RuntimeError(f"Expected 106 output pages, found {check.page_count}")
    combined = "\n".join(page.get_text() for page in check)
    required = (
        "O quadro explicita",
        "Quadro 10 – Critérios da avaliação preliminar do protótipo (continua)",
        "Quadro 10 – Critérios da avaliação preliminar do protótipo (conclusão)",
        "Tabela 2 – Resultados exploratórios por fluxo de avaliação (continua)",
        "Tabela 2 – Resultados exploratórios por fluxo de avaliação (conclusão)",
        "APÊNDICE A – Síntese da Lean Inception",
    )
    missing = [text for text in required if text not in combined]
    if missing:
        raise RuntimeError(f"Missing required corrected text: {missing}")
    if "\nApêndices\n" in combined:
        raise RuntimeError("Standalone Appendices divider remains in output")
    check.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    finalize(args.input_pdf.resolve(), args.output_pdf.resolve())


if __name__ == "__main__":
    main()
