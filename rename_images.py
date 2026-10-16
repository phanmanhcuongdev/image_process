from pathlib import Path

FOLDER = Path("images")
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".avif"}

files = sorted(
    (p for p in FOLDER.iterdir()
     if p.is_file() and p.suffix.lower() in EXTS),
    key=lambda p: p.name.lower()
)

# Lượt 1: đổi sang tên tạm để tránh đè file
temp_files = []

for i, path in enumerate(files, start=1):
    temp = path.with_name(f"__tmp_rename_{i}{path.suffix.lower()}")
    path.rename(temp)
    temp_files.append((temp, i))

# Lượt 2: đánh số từ 1
for temp, i in temp_files:
    new_path = FOLDER / f"{i}{temp.suffix.lower()}"
    temp.rename(new_path)

print(f"Đã đánh số lại {len(files)} ảnh.")