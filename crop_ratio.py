
import os
import shutil
from PIL import Image, ImageOps

SOURCE_FOLDER = "images"
BACKUP_FOLDER = "backup_before_crop"

VALID_EXTS = (
    ".jpg", ".jpeg", ".png", ".webp",
    ".bmp", ".avif"
)

os.makedirs(BACKUP_FOLDER, exist_ok=True)

files = sorted(
    f for f in os.listdir(SOURCE_FOLDER)
    if os.path.isfile(os.path.join(SOURCE_FOLDER, f))
    and f.lower().endswith(VALID_EXTS)
)

passed = 0
cropped_count = 0
errors = 0

for filename in files:
    path = os.path.join(SOURCE_FOLDER, filename)

    try:
        with Image.open(path) as img:
            img = ImageOps.exif_transpose(img)
            w, h = img.size

            # Đã đúng 3:4 thì giữ nguyên
            if w * 4 == h * 3:
                print(f"[ĐẠT] {filename}: {w}x{h}")
                passed += 1
                continue

            # Tìm kích thước 3:4 lớn nhất có thể nằm trong ảnh
            # Chỉ giảm chiều rộng hoặc chiều cao, không phóng to
            if w * 4 > h * 3:
                # Ảnh quá rộng: giữ chiều cao, giảm chiều rộng
                new_h = h
                new_w = (3 * h) // 4
            else:
                # Ảnh quá cao: giữ chiều rộng, giảm chiều cao
                new_w = w
                new_h = (4 * w) // 3

            # Crop chính giữa
            left = (w - new_w) // 2
            top = (h - new_h) // 2
            cropped = img.crop((
                left, top,
                left + new_w, top + new_h
            ))

            # Sao lưu bản gốc, giữ nguyên cấu trúc thư mục
            backup_path = os.path.join(BACKUP_FOLDER, filename)
            if not os.path.exists(backup_path):
                shutil.copy2(path, backup_path)

            # Lưu file tạm rồi thay file cũ
            temp_path = path + ".tmp"
            save_format = Image.registered_extensions().get(
                os.path.splitext(filename)[1].lower()
            )

            cropped.save(temp_path, format=save_format)
            os.replace(temp_path, path)

            print(
                f"[CROP] {filename}: {w}x{h} -> "
                f"{new_w}x{new_h}"
            )
            cropped_count += 1

    except Exception as e:
        errors += 1
        print(f"[LỖI] {filename}: {e}")

print("-" * 60)
print(f"Đã đúng tỷ lệ: {passed}")
print(f"Đã crop: {cropped_count}")
print(f"Lỗi: {errors}")
print(f"Bản gốc sao lưu tại: {BACKUP_FOLDER}")
