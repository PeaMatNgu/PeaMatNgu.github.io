---
title: "Path Traversal"
date: 2026-08-26
platform: "PortSwigger Web Security Academy"
learning_topic: "Web Vulnerabilities"
tags:
  - path-traversal
  - file-system
  - web-security
---

## Bản chất lỗ hổng

- Là lỗ hổng lợi dụng tham số đường dẫn của ứng dụng để truy cập vào file nằm ngoài thư mục mà ứng dụng đáng lẽ cho phép.

- Sử dụng “../” để lùi về cấp trước của file, khi lùi về đường dẫn đúng thì có thể đọc được file nhạy cảm.

## Cách khai thác

- Sử dụng “../” như bình thường, nếu như không có cơ chế sanitize, còn nếu như có thì có thể kiểm tra bằng cách truyền vào luôn đường dẫn tuyệt đối.

- Cách khai thác bằng nested traversal, bản chất vẫn là path traversal nhưng ứng dụng có cơ chế sanitize “../”, tuy nhiên ý tưởng đặt mỗi chuỗi “….//” thì có thể bypass qua được.

- Truyền vào payload bằng giá trị encode URL của “../”, nếu như server có logic tự động loại bỏ traversal, sau đó mới đưa kết quả cho ứng dụng. Để tấn công dùng chức năng intruder simple list và add “Fuzzing – Path Traversal”.

- Server logic kiểm tra giá trị truyền vào phải bắt đầu bằng đường dẫn hợp lệ ví dụ “/var/www/images” thì nếu như truyền “../” bình thường thì sẽ bị loại bỏ vì tên file bắt đầu không hợp lệ, lúc này chỉ cần truyền payload có đoạn đầu là tên file hợp lệ và lùi file như bình thường “/var/www/images/../../../etc/passwd”.

- Nếu như ứng dụng chỉ cho upload/đọc file nếu filename kết thúc bằng “.png”, ý tưởng là sẽ thêm byte null “%00” tượng trưng cho “\0” trước png để tạo thành payload dạng như “../etc/passwd%00.png”.

## Cách phòng chống

- Không cho user input trực tiếp vào filesystem API.

- Ưu tiên whitelist các giá trị được phép.

- Nếu không thể, giới hạn ký tự hợp lệ.

- Chuẩn hóa path bằng filesystem API.

- Đảm bảo path cuối cùng vẫn nằm trong base directory được phép.
