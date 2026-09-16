# Blog portfolio an toàn thông tin

Mã nguồn Jekyll cho website cá nhân của **Cao Trần Thành Trung**, sẵn sàng triển khai tại `https://peamatngu.github.io` bằng GitHub Pages.

## Chạy bằng Docker trong VS Code

Yêu cầu Docker Desktop đang chạy. Mở thư mục dự án bằng VS Code, mở Terminal tích hợp rồi chạy:

```powershell
docker compose up --build
```

Mở `http://127.0.0.1:4000`. Jekyll theo dõi thay đổi trong Markdown, layout, CSS và JavaScript; trang sẽ tự tải lại khi file được lưu.

Những lần sau, nếu `Gemfile` không thay đổi, chỉ cần:

```powershell
docker compose up
```

Nhấn `Ctrl+C` để dừng, sau đó có thể dọn container và network bằng:

```powershell
docker compose down
```

Các cổng chỉ được bind vào `127.0.0.1`, vì vậy bản preview không được mở ra mạng nội bộ.

## Chạy thử cục bộ

Yêu cầu Ruby và Bundler. Trên Windows, có thể cài Ruby bằng [RubyInstaller](https://rubyinstaller.org/).

```bash
bundle install
bundle exec jekyll serve --livereload
```

Mở `http://127.0.0.1:4000`. Để kiểm tra đúng chế độ GitHub Pages:

```bash
JEKYLL_ENV=production bundle exec jekyll build
```

PowerShell:

```powershell
$env:JEKYLL_ENV = "production"
bundle exec jekyll build
```

## Cập nhật thông tin cá nhân

Sửa phần `author` trong `_config.yml`. LinkedIn và CV đang để trống nên không xuất hiện trên trang chủ. Khi có CV, đặt file trong repository, ví dụ `assets/cv/cao-tran-thanh-trung.pdf`, rồi đặt:

```yml
linkedin: "https://www.linkedin.com/in/ten-cua-ban/"
cv: "/assets/cv/cao-tran-thanh-trung.pdf"
avatar: "/assets/images/avatar.jpg"
```

Ảnh `assets/images/profile-placeholder.svg` hiện là ảnh đại diện tạm thời và nên được thay bằng ảnh thật.

## Thêm bài viết Markdown

Đặt file vào đúng collection:

- `_ctf/` — CTF write-up.
- `_htb/` — Hack The Box machine write-up.
- `_binary/` — Binary Exploitation.

Tên file nên dùng chữ thường, không dấu và dấu gạch ngang, ví dụ `2026-09-16-ten-bai.md`. Front matter mẫu:

```yml
---
title: "Tên bài viết"
date: 2026-09-16
summary: "Mô tả ngắn cho thẻ bài viết."
difficulty: "Medium"
platform: "Hack The Box"
tags:
  - web
  - privilege-escalation
---
```

Không cần sửa trang danh sách: Jekyll tự lấy bài từ collection và sắp xếp bài mới nhất lên trước.

## Thêm ảnh

Dùng tên file rõ ràng, không dấu, không khoảng trắng:

```text
assets/images/ctf/<ten-bai>/01-burp-request.png
assets/images/htb/<ten-may>/01-nmap-scan.png
assets/images/binary/<ten-bai>/01-stack-layout.png
assets/images/achievements/<ten-chung-chi>.jpg
```

Trong Markdown, dùng đường dẫn bắt đầu từ `/`:

```markdown
![Kết quả quét Nmap](/assets/images/htb/nexus/01-nmap-scan.png)
```

Kiểm tra các đường dẫn ảnh đáng ngờ hoặc bị thiếu:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/check-content.ps1
```

Script sẽ báo file, dòng và URL; script không sửa nội dung và không ghi đè ảnh.

## Thêm achievement

1. Chép ảnh vào `assets/images/achievements/`.
2. Thêm một mục thật vào `_data/achievements.yml`:

```yml
- title: "Tên cuộc thi hoặc chứng chỉ"
  date: "Tháng 09/2026"
  result: "Kết quả hoặc thứ hạng"
  description: "Mô tả ngắn."
  image: "/assets/images/achievements/ten-chung-chi.jpg"
  alt: "Mô tả nội dung ảnh certificate"
  verification: "https://duong-dan-xac-minh.example"
```

Chỉ thêm dữ liệu đã được xác minh. Nếu không có link xác minh, để `verification: ""`.

## Bật GitHub Pages

1. Tạo repository công khai tên chính xác `PeaMatNgu.github.io`.
2. Đưa toàn bộ nội dung thư mục này lên nhánh `main` của repository đó.
3. Mở **Settings → Pages**.
4. Trong **Build and deployment**, chọn **Deploy from a branch**.
5. Chọn nhánh `main`, thư mục `/(root)`, rồi lưu.
6. Chờ GitHub Pages build và truy cập `https://peamatngu.github.io`.

Nếu dùng một repository dự án thay vì repository `PeaMatNgu.github.io`, phải đặt `baseurl: "/ten-repository"` trong `_config.yml` và dùng đúng URL dự án.

## Lỗi build thường gặp

- **YAML parse error:** kiểm tra dấu hai chấm trong title/summary; bọc giá trị bằng dấu nháy kép.
- **Trang không xuất hiện:** kiểm tra file nằm đúng `_ctf`, `_htb` hoặc `_binary` và có cặp dấu `---` ở đầu front matter.
- **Ảnh 404:** đường dẫn phân biệt chữ hoa/chữ thường trên GitHub Pages; chạy `scripts/check-content.ps1`.
- **Build local khác GitHub:** chạy `bundle update github-pages`, sau đó build lại; không thêm plugin ngoài danh sách GitHub Pages hỗ trợ.
- **Liên kết sai khi dùng project site:** cập nhật `baseurl` và ưu tiên Liquid `relative_url` trong layout/include.

## Cấu trúc chính

```text
_config.yml
_layouts/                 Layout chung và layout bài viết
_includes/                Header, footer, thẻ bài viết
_ctf/                     CTF write-up
_htb/                     HTB machine write-up
_binary/                  Binary Exploitation
_data/achievements.yml    Dữ liệu thành tích
assets/css/style.css      Giao diện responsive
assets/js/main.js         Menu, mục lục, nút copy code
scripts/check-content.ps1 Kiểm tra ảnh trong Markdown
```

Website không có backend, database, secret hoặc plugin Jekyll không tương thích với GitHub Pages.
