# Quy trình xử lý ảnh cây

Các script trong repo giúp kiểm tra ảnh cây theo tỷ lệ dọc **3:4** và tạo ảnh đầu ra kích thước **768 × 1024 pixel**.

## 1. Lấy mã nguồn và cài đặt

Cài Python 3, sau đó mở PowerShell và chạy:

```powershell
git clone https://github.com/phanmanhcuongdev/image_process.git
cd image_process
py -m pip install Pillow
New-Item -ItemType Directory -Force images
```

Các lệnh dùng `py` trên Windows. Nếu máy bạn không có lệnh này, thay `py` bằng `python`.

Chạy các lệnh xử lý từ thư mục `image_process` để các script tìm đúng thư mục ảnh.

## 2. Chuẩn bị ảnh

1. Tìm và tải các ảnh cây cần xử lý.
2. **Bắt buộc:** dùng phần mềm chỉnh sửa ảnh để crop từng ảnh theo tỷ lệ **3:4** và đặt cây ở trung tâm khung hình. Không bỏ qua bước này: `crop_ratio.py` tự crop chính giữa ảnh, nên có thể cắt mất cây nếu cây không nằm giữa khung hình.
3. Đặt ảnh trực tiếp trong thư mục `images` vừa tạo, cùng cấp với các file `.py`. Không đặt ảnh trong thư mục con.

Các script nhận ảnh có phần mở rộng `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp` và `.avif`. Khả năng đọc/ghi còn tùy định dạng Pillow hỗ trợ trong môi trường của bạn.

Ví dụ:

```text
image_process/
├── images/
│   ├── cay_1.jpg
│   └── cay_2.png
├── check_ratio.py
├── crop_ratio.py
├── resize_images.py
└── scan_sizes.py
```

## 3. Kiểm tra tỷ lệ ảnh

```powershell
py check_ratio.py
```

Script kiểm tra ảnh trong `images`. `[ĐẠT]` nghĩa là ảnh có tỷ lệ chính xác 3:4; `[SAI]` nghĩa là chưa đúng tỷ lệ; `[LỖI]` nghĩa là không đọc được ảnh. Nếu ảnh lỗi, kiểm tra định dạng và file ảnh trước khi tiếp tục.

## 4. Sửa ảnh chưa đúng tỷ lệ (nếu có)

Nếu `check_ratio.py` báo `[SAI]` dù đã crop ảnh bằng phần mềm, có thể chạy:

```powershell
py crop_ratio.py
```

Script sẽ crop chính giữa ảnh sai tỷ lệ về 3:4, không phóng to ảnh, rồi thay ảnh đó trong `images`. Bản gốc được sao lưu vào `backup_before_crop` (không ghi đè bản sao lưu đã tồn tại). Vì thao tác crop tự động lấy chính giữa ảnh, hãy đảm bảo cây được căn giữa bằng phần mềm trước khi chạy.

Sau đó kiểm tra lại:

```powershell
py check_ratio.py
```

Chỉ tiếp tục khi mọi ảnh cần xử lý đều báo `[ĐẠT]`. Nếu còn `[SAI]`, hãy chỉnh lại ảnh bằng phần mềm rồi kiểm tra lại. Không resize ảnh sai tỷ lệ vì sẽ làm biến dạng ảnh.

## 5. Resize ảnh

```powershell
py resize_images.py
```

Script đọc ảnh trong `images`, áp dụng hướng ảnh EXIF, chuyển sang RGB và resize thành đúng **768 × 1024 pixel**. Kết quả được lưu dưới dạng JPEG chất lượng 95 trong thư mục `processed` (tự tạo khi chạy). Tên file được giữ nguyên nhưng phần mở rộng đầu ra luôn là `.jpg`; file cùng tên trong `processed` sẽ bị ghi đè.

## 6. Kiểm tra kích thước đầu ra

`scan_sizes.py` kiểm tra kích thước ảnh trong `images`, **không phải** `processed`:

```powershell
py scan_sizes.py
```

Để kiểm tra trực tiếp ảnh đầu ra trong `processed`, chạy:

```powershell
py -c "from pathlib import Path; from PIL import Image; files=sorted(Path('processed').glob('*.jpg')); print('So anh:', len(files)); [print(p.name, Image.open(p).size, 'DAT' if Image.open(p).size == (768, 1024) else 'SAI') for p in files]"
```

Mỗi ảnh cần hiện kích thước `(768, 1024)` và trạng thái `DAT`. Nếu số ảnh bằng 0, kiểm tra xem ảnh đầu vào có nằm trực tiếp trong `images` hay không.

## Tóm tắt quy trình

1. Crop **bắt buộc** từng ảnh bằng phần mềm, đặt cây ở trung tâm.
2. Chép ảnh vào `images`.
3. Chạy `py check_ratio.py`.
4. Nếu còn ảnh sai tỷ lệ, chạy `py crop_ratio.py`, rồi chạy lại `py check_ratio.py`.
5. Khi tất cả ảnh đạt tỷ lệ 3:4, chạy `py resize_images.py`.
6. Kiểm tra ảnh trong `processed` có kích thước `(768, 1024)`.

Ảnh đầu vào nằm trong `images`, bản gốc trước khi crop tự động được lưu trong `backup_before_crop`, và ảnh JPEG sau resize nằm trong `processed`.
