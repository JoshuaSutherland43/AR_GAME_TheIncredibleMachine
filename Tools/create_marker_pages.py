from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "Assets" / "Editor" / "Vuforia" / "ImageTargetTextures" / "ClassExampleTargets"
OUTPUT_DIR = PROJECT_ROOT / "Docs" / "MarkerPages"

# A4 at 300 DPI
PAGE_W = 2480
PAGE_H = 3508
MARGIN = 180
MARKER_MAX_W = 1500
MARKER_MAX_H = 1900

ROLE_BY_TARGET = {
    "img_target_01": "Frame Anchor (Main Machine)",
    "img_target_02": "Plank Spawner",
    "img_target_03": "Cube Spawner",
    "img_target_04": "Rope Spawner",
    "img_target_05": "Start / Reset Button",
    "img_target_06": "Spare Marker",
}


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates = ["arialbd.ttf", "segoeuib.ttf"]
    else:
        candidates = ["arial.ttf", "segoeui.ttf"]

    for name in candidates:
        try:
            return ImageFont.truetype(name, size=size)
        except OSError:
            pass

    return ImageFont.load_default()


def parse_target_name(image_path: Path) -> str:
    # e.g. img_target_01_scaled.jpg -> img_target_01
    stem = image_path.stem
    if stem.endswith("_scaled"):
        return stem[:-7]
    return stem


def fit_inside(width: int, height: int, max_w: int, max_h: int) -> tuple[int, int]:
    scale = min(max_w / width, max_h / height, 1.0)
    return int(width * scale), int(height * scale)


def create_page(image_path: Path, page_index: int, page_count: int) -> Image.Image:
    target_name = parse_target_name(image_path)
    role = ROLE_BY_TARGET.get(target_name, "Custom Marker")

    page = Image.new("RGB", (PAGE_W, PAGE_H), "white")
    draw = ImageDraw.Draw(page)

    font_title = load_font(84, bold=True)
    font_subtitle = load_font(46, bold=True)
    font_body = load_font(34)
    font_small = load_font(28)

    title = f"AR Marker Page {page_index}/{page_count}"
    subtitle = f"{role}"
    line_1 = f"Target Name: {target_name}"
    line_2 = "Print at 100% scale (no fit-to-page), keep flat, matte paper preferred."

    draw.text((MARGIN, 120), title, fill="black", font=font_title)
    draw.text((MARGIN, 250), subtitle, fill=(25, 25, 25), font=font_subtitle)
    draw.text((MARGIN, 320), line_1, fill=(40, 40, 40), font=font_body)
    draw.text((MARGIN, 370), line_2, fill=(55, 55, 55), font=font_small)

    marker = Image.open(image_path).convert("RGB")
    fitted_w, fitted_h = fit_inside(marker.width, marker.height, MARKER_MAX_W, MARKER_MAX_H)
    marker = marker.resize((fitted_w, fitted_h), Image.Resampling.LANCZOS)

    x = (PAGE_W - fitted_w) // 2
    y = 620 + (MARKER_MAX_H - fitted_h) // 2

    border = 10
    draw.rectangle((x - border, y - border, x + fitted_w + border, y + fitted_h + border), outline="black", width=3)
    page.paste(marker, (x, y))

    footer = "Keep this marker visible while scanning. Avoid glare and strong shadows."
    draw.text((MARGIN, PAGE_H - 160), footer, fill=(55, 55, 55), font=font_small)

    return page


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    source_images = sorted(SOURCE_DIR.glob("img_target_*_scaled.jpg"))
    if not source_images:
        raise FileNotFoundError(f"No marker images found in {SOURCE_DIR}")

    generated_pages: list[Image.Image] = []
    role_lines: list[str] = []

    for i, image_path in enumerate(source_images, start=1):
        target_name = parse_target_name(image_path)
        role = ROLE_BY_TARGET.get(target_name, "Custom Marker")
        page = create_page(image_path, i, len(source_images))
        out_png = OUTPUT_DIR / f"{i:02d}_{target_name}_{role.replace('/', '_').replace(' ', '_')}.png"
        page.save(out_png, "PNG", dpi=(300, 300))
        generated_pages.append(page.convert("RGB"))
        role_lines.append(f"{target_name}: {role}")

    pdf_path = OUTPUT_DIR / "MarkerPages_A4_Printable.pdf"
    generated_pages[0].save(
        pdf_path,
        "PDF",
        resolution=300.0,
        save_all=True,
        append_images=generated_pages[1:],
    )

    mapping_path = OUTPUT_DIR / "MarkerRoleMapping.txt"
    mapping_text = [
        "Marker Role Mapping",
        "===================",
        "",
        *role_lines,
        "",
        "Recommended assignment for this project:",
        "- Frame image target: img_target_01",
        "- Plank spawner target: img_target_02",
        "- Cube spawner target: img_target_03",
        "- Rope spawner target: img_target_04",
        "- Start/reset button target: img_target_05",
        "- Spare: img_target_06",
    ]
    mapping_path.write_text("\n".join(mapping_text), encoding="utf-8")

    print(f"Generated {len(source_images)} PNG pages")
    print(f"PDF: {pdf_path}")
    print(f"Mapping: {mapping_path}")


if __name__ == "__main__":
    main()
