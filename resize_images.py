
from pathlib import Path
from PIL import Image, ImageOps

SOURCE = Path("images")
OUTPUT = Path("processed")
TARGET_SIZE = (768, 1024)

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".avif"}
OUTPUT.mkdir(parents=True, exist_ok=True)

files = sorted(
    (
        p for p in SOURCE.iterdir()
        if p.is_file() and p.suffix.lower() in EXTS
    ),
    key=lambda p: p.name.lower()
)

success = 0
errors = []

for path in files:
    try:
        with Image.open(path) as src:
            img = ImageOps.exif_transpose(src).convert("RGB")
            img = img.resize(TARGET_SIZE, Image.Resampling.LANCZOS)

            output_path = OUTPUT / f"{path.stem}.jpg"
            img.save(output_path, format="JPEG", quality=95, optimize=True)

        success += 1
        print(f"OK: {path.name} -> 768x1024")

    except Exception as e:
        errors.append((path.name, str(e)))
        print(f"ERROR: {path.name}: {e}")

print(f"\nTổng ảnh: {len(files)}")
print(f"Thành công: {success}")
print(f"Lỗi: {len(errors)}")
print(f"Đầu ra: {OUTPUT.resolve()}")
