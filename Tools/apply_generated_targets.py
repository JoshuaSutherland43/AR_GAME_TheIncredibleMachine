from __future__ import annotations

from pathlib import Path
from PIL import Image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
GEN_DIR = PROJECT_ROOT / "Docs" / "GeneratedTargets"
VUFORIA_IMG_DIR = PROJECT_ROOT / "Assets" / "Editor" / "Vuforia" / "ImageTargetTextures" / "ClassExampleTargets"

MAPPING = [
    ("img_target_gen_01.png", "frame_generator_img_target_01.png", "img_target_01_scaled.jpg"),
    ("img_target_gen_02.png", "object_spawner_plank_img_target_02.png", "img_target_02_scaled.jpg"),
    ("img_target_gen_03.png", "object_spawner_cube_img_target_03.png", "img_target_03_scaled.jpg"),
    ("img_target_gen_04.png", "object_spawner_rope_img_target_04.png", "img_target_04_scaled.jpg"),
    ("img_target_gen_05.png", "run_reset_button_img_target_05.png", "img_target_05_scaled.jpg"),
    ("img_target_gen_06.png", "spare_marker_img_target_06.png", "img_target_06_scaled.jpg"),
]


def main() -> None:
    missing = [src for src, _, _ in MAPPING if not (GEN_DIR / src).exists()]
    if missing:
        raise FileNotFoundError(f"Missing generated source files: {missing}")

    for source_name, renamed_name, vuforia_target_name in MAPPING:
        source_path = GEN_DIR / source_name
        renamed_path = GEN_DIR / renamed_name
        vuforia_path = VUFORIA_IMG_DIR / vuforia_target_name

        # Rename source file to role-specific name.
        if source_path.exists() and source_path != renamed_path:
            if renamed_path.exists():
                renamed_path.unlink()
            source_path.rename(renamed_path)

        # Apply same image to Vuforia image target preview slot.
        with Image.open(renamed_path) as img:
            rgb = img.convert("RGB")
            rgb.save(vuforia_path, "JPEG", quality=95, optimize=True)

        print(f"{renamed_name} -> {vuforia_target_name}")


if __name__ == "__main__":
    main()
