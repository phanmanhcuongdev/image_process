
import os
from PIL import Image, ImageOps

SOURCE_FOLDER = "images"

VALID_EXTS = (
    ".jpg", ".jpeg", ".png", ".webp",
    ".bmp", ".avif"
)

files = sorted(
    f for f in os.listdir(SOURCE_FOLDER)
    if os.path.isfile(os.path.join(SOURCE_FOLDER, f))
    and f.lower().endswith(VALID_EXTS)
)

passed = 0
failed = 0
errors = 0

print(f"Thư mục kiểm tra: {os.path.abspath(SOURCE_FOLDER)}")
print(f"Tổng số ảnh: {len(files)}")
print("-" * 70)

for filename in files:
    file_path = os.path.join(SOURCE_FOLDER, filename)

    try:
        with Image.open(file_path) as img:
            img = ImageOps.exif_transpose(img)
            w, h = img.size

            if w * 4 == h * 3:
                print(f"[ĐẠT] {filename}: {w}x{h} (3:4)")
                passed += 1
            else:
                print(
                    f"[SAI] {filename}: {w}x{h} "
                    f"(tỷ lệ {w / h:.6f})"
                )
                failed += 1

    except Exception as e:
        print(f"[LỖI] {filename}: {e}")
        errors += 1

print("-" * 70)
print(f"Đạt tỷ lệ 3:4: {passed}")
print(f"Sai tỷ lệ: {failed}")
print(f"Lỗi đọc ảnh: {errors}")
print(f"Tổng cộng: {len(files)}")
