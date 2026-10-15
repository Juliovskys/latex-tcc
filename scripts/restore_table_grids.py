"""Restore the bordered table style in the latest TCC PDF.

The medium-term PDF is the authoritative content version, but its LaTeX source
is not present in this checkout.  This script therefore adds vector rules to
the existing PDF without reflowing or replacing any text.  Coordinates are in
PDF points and were measured from the 21 tables/quadros in that version.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

import pdfplumber
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas


@dataclass(frozen=True)
class GridFragment:
    label: str
    page: int
    top: float
    header_bottom: float
    bottom: float | None
    columns: tuple[float, ...]
    rows: tuple[float, ...]


FRAGMENTS = (
    GridFragment("Quadro 1", 26, 468.1, 486.3, 659.8, (85.0, 215.4, 275.8), (490.2, 514.2, 538.1, 562.0, 597.8, 633.7)),
    GridFragment("Quadro 2", 31, 103.0, 131.7, 377.0, (85.0, 170.2, 276.9, 392.3), (135.7, 171.6, 219.4, 255.3, 291.1)),
    GridFragment("Quadro 3", 43, 103.0, 131.6, 628.0, (85.0, 165.9, 281.2, 388.0), (135.6, 243.2, 303.0, 386.7, 470.4, 554.1)),
    GridFragment("Quadro 4", 50, 202.3, 220.4, 453.7, (85.0, 280.0), (224.7, 236.6, 248.6, 272.5, 308.4, 320.3, 344.2, 356.2, 380.1, 404.0, 416.0, 427.9)),
    GridFragment("Quadro 5", 51, 512.0, 540.7, 727.0, (85.0, 174.5, 302.7, 435.2), (544.7, 580.6, 629.2, 677.0)),
    GridFragment("Quadro 6", 52, 488.4, 506.6, 632.3, (85.0, 160.4, 240.0, 353.3, 432.9), (510.5, 546.4, 594.2)),
    GridFragment("Tabela 1", 53, 344.7, 362.9, 404.9, (85.0, 164.6, 231.5, 311.1, 390.8), (366.9, 378.8, 390.8)),
    GridFragment("Quadro 7", 53, 628.0, 646.1, 759.9, (85.0, 178.8, 315.6, 418.0), (650.1, 686.0, 721.9)),
    GridFragment("Quadro 8", 55, 103.0, 131.7, 425.7, (85.0, 157.3, 289.8, 426.6), (135.7, 183.5, 231.4, 291.9, 327.8, 375.6)),
    GridFragment("Quadro 9", 56, 103.0, 131.7, 377.0, (85.0, 160.4, 248.4, 344.9, 437.1), (135.7, 195.5, 243.3, 291.1)),
    GridFragment("Quadro 10 - parte 1", 59, 500.4, 529.1, None, (85.0, 170.2, 272.6, 392.3), (533.1, 592.9, 628.8, 712.4, 760.3)),
    GridFragment("Quadro 10 - parte 2", 60, 103.6, 132.3, 270.0, (85.0, 170.2, 272.6, 392.3), (136.3, 231.9)),
    GridFragment("Quadro 11", 60, 416.2, 444.9, 785.9, (85.0, 174.5, 294.1, 388.0), (448.9, 496.7, 544.6, 592.4, 628.2, 664.1, 688.0, 735.8)),
    GridFragment("Tabela 2", 62, 372.9, 401.5, 527.3, (85.0, 320.4, 433.3), (405.5, 417.5, 429.4, 453.4, 465.3, 477.3, 489.2, 501.2, 513.1)),
    GridFragment("Quadro 12", 64, 103.0, 131.7, 460.7, (85.0, 174.5, 302.7, 426.6), (135.7, 183.5, 219.4, 255.3, 303.1, 362.9, 410.7)),
    GridFragment("Quadro 13 - parte 1", 90, 352.5, 370.7, None, (85.0, 136.7, 271.5), (374.7, 410.5, 434.4, 470.3, 506.2, 542.0, 589.9, 625.7, 661.6, 709.4, 745.3)),
    GridFragment("Quadro 13 - parte 2", 91, 103.6, 121.7, 163.8, (85.0, 136.7, 271.5), (125.7,)),
    GridFragment("Quadro 14", 91, 284.6, 302.7, 775.1, (85.0, 136.7, 267.1), (306.7, 342.5, 378.4, 414.3, 462.1, 498.0, 533.8, 569.7, 605.6, 653.4, 701.2, 737.1)),
    GridFragment("Quadro 15 - parte 1", 93, 382.7, 411.3, None, (85.0, 156.1, 223.1, 344.9, 399.2), (415.3, 499.0, 558.8, 642.5, 714.2)),
    GridFragment("Quadro 15 - parte 2", 94, 103.6, 132.2, 568.8, (85.0, 156.1, 223.1, 344.9, 399.2), (136.2, 196.0, 279.6, 339.4, 411.1, 459.0, 482.9, 518.7)),
    GridFragment("Quadro 16", 95, 103.0, 121.2, 581.7, (85.0, 128.5), (125.2, 149.1, 173.0, 196.9, 220.8, 244.7, 268.6, 292.5, 316.5, 340.4, 364.3, 388.2, 412.1, 436.0, 459.9, 483.8, 507.7, 531.7, 555.6)),
    GridFragment("Quadro 17 - parte 1", 96, 488.2, 528.8, None, (85.0, 178.8, 294.1, 370.8), (532.8, 592.5, 652.3, 700.1)),
    GridFragment("Quadro 17 - parte 2", 97, 103.6, 144.1, 413.3, (85.0, 178.8, 294.1, 370.8), (148.1, 207.9, 279.6, 327.5)),
    GridFragment("Quadro 18 - parte 1", 97, 687.8, 706.0, None, (85.0, 127.3, 229.7, 426.6), (710.0,)),
    GridFragment("Quadro 18 - parte 2", 98, 103.6, 121.7, 522.5, (85.0, 127.3, 229.7, 426.6), (125.7, 173.5, 221.4, 257.2, 305.1, 340.9, 376.8, 412.7, 448.5)),
    GridFragment("Quadro 19 - parte 1", 100, 642.4, 671.0, None, (85.0, 202.3, 297.7), (675.0, 698.9, 722.8, 746.7, 770.6)),
    GridFragment("Quadro 19 - parte 2", 101, 103.6, 132.2, 210.1, (85.0, 202.3, 297.7), (136.2, 160.1, 184.0)),
)


def nearest_rule(page, expected_top: float):
    candidates = [
        line
        for line in page.lines
        if line["width"] > 350 and abs(line["top"] - expected_top) <= 1.0
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

    # The earlier bordered LaTeX tables used the default 6 pt tabular padding.
    # The current booktabs layout removed the outer padding, so the restored
    # rules sit 6 pt before each column start and 6 pt after the last rule.
    padding = 6.0
    left = fragment.columns[0] - padding
    right = top_rule["x1"] + padding
    verticals = (left,) + tuple(x - padding for x in fragment.columns[1:]) + (right,)

    horizontal_rows = []
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
        horizontal_rows.append((last_bottom + next_start) / 2.0)

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
    for y in horizontal_rows:
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
        "row_rules": tuple(horizontal_rows),
    }


def make_overlay(width: float, height: float, geometries):
    stream = BytesIO()
    drawing = canvas.Canvas(stream, pagesize=(width, height))
    drawing.setStrokeColorRGB(0, 0, 0)
    drawing.setLineWidth(0.45)

    for geometry in geometries:
        left = geometry["left"]
        right = geometry["right"]
        top = geometry["top"]
        bottom = geometry["bottom"]

        for top_y in (top, geometry["header_bottom"], *geometry["row_rules"], bottom):
            drawing.line(left, height - top_y, right, height - top_y)
        for x in geometry["verticals"]:
            drawing.line(x, height - top, x, height - bottom)

    drawing.save()
    stream.seek(0)
    return PdfReader(stream).pages[0]


def restore_grids(input_pdf: Path, output_pdf: Path):
    if not input_pdf.is_file():
        raise FileNotFoundError(input_pdf)

    by_page = defaultdict(list)
    with pdfplumber.open(input_pdf) as source_layout:
        if len(source_layout.pages) != 112:
            raise ValueError(
                f"Expected the 112-page medium-term version, got {len(source_layout.pages)} pages"
            )
        for fragment in FRAGMENTS:
            page = source_layout.pages[fragment.page - 1]
            by_page[fragment.page].append(resolve_geometry(page, fragment))

    reader = PdfReader(str(input_pdf))
    writer = PdfWriter()
    writer.clone_document_from_reader(reader)

    for page_number, geometries in by_page.items():
        target_page = writer.pages[page_number - 1]
        width = float(target_page.mediabox.width)
        height = float(target_page.mediabox.height)
        target_page.merge_page(make_overlay(width, height, geometries), over=True)

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with output_pdf.open("wb") as destination:
        writer.write(destination)

    check = PdfReader(str(output_pdf))
    if len(check.pages) != len(reader.pages):
        raise ValueError("Output page count changed unexpectedly")

    unique_labels = {
        fragment.label.split(" - parte", 1)[0] for fragment in FRAGMENTS
    }
    print(
        f"Restored grids for {len(unique_labels)} tables/quadros "
        f"across {len(FRAGMENTS)} page fragments; output has {len(check.pages)} pages."
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_pdf", type=Path)
    parser.add_argument("output_pdf", type=Path)
    args = parser.parse_args()
    restore_grids(args.input_pdf.resolve(), args.output_pdf.resolve())


if __name__ == "__main__":
    main()
