"""Create labeled contact sheets from sequential PDF page PNG files."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    images = sorted(args.image_dir.glob("page-*.png"))
    if not images:
        raise SystemExit("No page PNG files found")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    columns, rows = 4, 4
    thumb_width, thumb_height = 286, 404
    label_height, gap = 26, 12
    sheet_width = columns * thumb_width + (columns + 1) * gap
    sheet_height = rows * (thumb_height + label_height) + (rows + 1) * gap

    for offset in range(0, len(images), columns * rows):
        group = images[offset : offset + columns * rows]
        canvas = Image.new("RGB", (sheet_width, sheet_height), "#d8d8d8")
        draw = ImageDraw.Draw(canvas)
        for index, path in enumerate(group):
            row, column = divmod(index, columns)
            x = gap + column * thumb_width
            y = gap + row * (thumb_height + label_height)
            with Image.open(path) as source:
                page = source.convert("RGB")
                page.thumbnail((thumb_width, thumb_height))
                px = x + (thumb_width - page.width) // 2
                py = y + (thumb_height - page.height) // 2
                canvas.paste(page, (px, py))
            label = f"Página {offset + index + 1}"
            draw.text((x + 4, y + thumb_height + 5), label, fill="black")
        sheet_number = offset // (columns * rows) + 1
        canvas.save(args.output_dir / f"contact-sheet-{sheet_number:02d}.png")


if __name__ == "__main__":
    main()
