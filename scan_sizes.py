
from pathlib import Path
from collections import Counter
from PIL import Image, ImageOps

FOLDER = Path("images")
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".avif"}

files = sorted(
    (
        p for p in FOLDER.iterdir()
        if p.is_file() and p.suffix.lower() in EXTS
    ),
    key=lambda p: p.name.lower()
)

size_counts = Counter()
errors = []

print(f"Tổng số file ảnh: {len(files)}\n")

for path in files:
    try:
        with Image.open(path) as img:
            img = ImageOps.exif_transpose(img)
            w, h = img.size
            size_counts[(w, h)] += 1
            print(f"{path.name:20} {w:5} x {h:<5}")
    except Exception as e:
        errors.append((path.name, str(e)))

print("\n===== TỔNG HỢP KÍCH THƯỚC =====")
for (w, h), count in size_counts.most_common():
    print(f"{w} x {h}: {count} ảnh")

print(f"\nSố ảnh đọc được: {sum(size_counts.values())}")
print(f"Số ảnh lỗi: {len(errors)}")

if errors:
    print("\n===== FILE LỖI =====")
    for name, err in errors:
        print(f"{name}: {err}")
