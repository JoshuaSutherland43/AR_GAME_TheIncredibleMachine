from __future__ import annotations

import argparse
import random
from pathlib import Path

from PIL import Image, ImageDraw


DEFAULT_PALETTE = [
    "#A6C534",
    "#B3D255",
    "#C0E078",
    "#D2EE92",
    "#E4FBAD",
    "#CAD246",
    "#D2DC5C",
    "#D8E673",
    "#E2F084",
    "#ECFA97",
    "#9AB8B9",
    "#556F90",
    "#1E4D6C",
    "#2B394B",
    "#2B394B",
]


def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    value = hex_color.strip().lstrip("#")
    return int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16)


def draw_triangle(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], color: tuple[int, int, int]) -> None:
    draw.polygon(points, fill=color)


def generate_pattern_image(
    width: int,
    ratio: float,
    columns: int,
    rows: int,
    palette: list[tuple[int, int, int]],
    seed: int | None = None,
) -> Image.Image:
    rng = random.Random(seed)
    height = int(width / ratio)

    image = Image.new("RGBA", (width, height), (0, 0, 0, 255))
    draw = ImageDraw.Draw(image, "RGBA")

    x_incr = width / columns
    y_incr = height / rows

    x_pos = 0.0
    while x_pos < width:
        y_pos = 0.0
        while y_pos < height:
            c = lambda: palette[rng.randrange(0, len(palette))]

            # 1
            draw_triangle(draw, [(x_pos, y_pos), (x_pos + x_incr, y_pos), (x_pos + x_incr, y_pos + y_incr)], c())
            draw_triangle(draw, [(x_pos, y_pos), (x_pos, y_pos + y_incr), (x_pos + x_incr, y_pos + y_incr)], c())

            # 2
            draw_triangle(
                draw,
                [(x_pos + x_incr, y_pos), (x_pos + 2 * x_incr, y_pos), (x_pos + x_incr, y_pos + y_incr)],
                c(),
            )
            draw_triangle(
                draw,
                [(x_pos + 2 * x_incr, y_pos), (x_pos + x_incr, y_pos + y_incr), (x_pos + 2 * x_incr, y_pos + y_incr)],
                c(),
            )

            # 3
            draw_triangle(
                draw,
                [(x_pos, y_pos + y_incr), (x_pos, y_pos + 2 * y_incr), (x_pos + x_incr, y_pos + y_incr)],
                c(),
            )
            draw_triangle(
                draw,
                [(x_pos, y_pos + 2 * y_incr), (x_pos + x_incr, y_pos + 2 * y_incr), (x_pos + x_incr, y_pos + y_incr)],
                c(),
            )

            # 4
            draw_triangle(
                draw,
                [
                    (x_pos + x_incr, y_pos + y_incr),
                    (x_pos + 2 * x_incr, y_pos + y_incr),
                    (x_pos + 2 * x_incr, y_pos + 2 * y_incr),
                ],
                c(),
            )
            draw_triangle(
                draw,
                [
                    (x_pos + x_incr, y_pos + y_incr),
                    (x_pos + x_incr, y_pos + 2 * y_incr),
                    (x_pos + 2 * x_incr, y_pos + 2 * y_incr),
                ],
                c(),
            )

            y_pos += y_incr * 2
        x_pos += x_incr * 2

    circle_count = int(1.5 * columns * rows)
    for _ in range(circle_count):
        size = rng.uniform(x_incr / 10.0, x_incr)
        col = palette[rng.randrange(0, len(palette))]
        color_rgba = (col[0], col[1], col[2], 210)

        cx = rng.uniform(0, width)
        cy = rng.uniform(0, height)
        bounds = (cx - size / 2, cy - size / 2, cx + size / 2, cy + size / 2)
        draw.ellipse(bounds, fill=color_rgba)

    return image.convert("RGB")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Vuforia-friendly marker images.")
    parser.add_argument("--count", type=int, default=6, help="How many marker images to generate.")
    parser.add_argument("--width", type=int, default=1280, help="Image width in pixels.")
    parser.add_argument("--ratio", type=float, default=4.0 / 3.0, help="Width/height ratio.")
    parser.add_argument("--columns", type=int, default=20, help="Grid columns.")
    parser.add_argument("--rows", type=int, default=15, help="Grid rows.")
    parser.add_argument("--seed", type=int, default=None, help="Optional seed for deterministic output.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("Docs/GeneratedTargets"),
        help="Output directory for generated images.",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="generated_target_",
        help="Output filename prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    args.output.mkdir(parents=True, exist_ok=True)

    palette = [hex_to_rgb(c) for c in DEFAULT_PALETTE]

    for i in range(1, args.count + 1):
        seed = None if args.seed is None else args.seed + i
        image = generate_pattern_image(
            width=args.width,
            ratio=args.ratio,
            columns=args.columns,
            rows=args.rows,
            palette=palette,
            seed=seed,
        )

        output_path = args.output / f"{args.prefix}{i:02d}.png"
        image.save(output_path, "PNG")
        print(output_path)


if __name__ == "__main__":
    main()
